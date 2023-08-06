from enum import Enum
from urllib.parse import urlparse, urlunparse
from requests import Request

import click
import urllib3
import threading
from typing import Optional, Union, List, AnyStr

from .base_client import BaseServiceClient
from dnastack.constants import *
from requests.exceptions import HTTPError
import re
from uuid import UUID
import pandas as pd
from search_python_client.search import DrsClient

from ..auth import OAuthTokenAuth
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import DRSDownloadException, DRSException


class DRSObject:
    """
    A class for a DRS resource

    :param url: The DRS url
    :raises ValueError if url is not a valid DRS url
    """

    def __init__(self, url: str):

        self.url = url

        if not DRSObject.is_drs_url(url):
            raise ValueError("The provided url is not a valid DRS url")

        self.object_id = DRSObject._get_object_id_from_url(url)
        self.drs_server = self._get_drs_server_from_url(url)

    @staticmethod
    def _get_drs_server_from_url(url: str) -> str:
        """
        Return the HTTPS server associated with the DRS url

        :param url: A drs url
        :return: The associated HTTPS server url
        """
        parsed_url = urlparse(url)
        path_prefix = "/".join(parsed_url.path.split("/")[:-1])
        return str(
            urlunparse(
                ("https", parsed_url.netloc, path_prefix + "/ga4gh/drs/v1/", "", "", "")
            )
        )

    @staticmethod
    def _get_object_id_from_url(url: str) -> str:
        """
        Return the object ID from a drs url

        :param url: A drs url
        :return: The object ID extracted from the URL
        :raises: ValueError if there isn't a valid DRS Object ID
        """
        parsed_url = urlparse(url)
        url_object_id = parsed_url.path.split("/")[-1]
        try:
            object_id = UUID(url_object_id, version=4)
        except ValueError:
            raise ValueError(f"{url_object_id} is not a valid UUID")

        return str(object_id)

    @staticmethod
    def is_drs_url(url: str) -> bool:
        """Returns true if url is a valid DRS url"""
        parsed_url = urlparse(url)
        return parsed_url.scheme == "drs"


def get_host(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc


def handle_file_response(download_file: str, data: Union[str, bytes]) -> str:
    # decode if fasta
    if re.search(r"\.fa", download_file):
        data = data.decode("utf-8")

    return data


# turn into dataframe for FASTA/FASTQ files, otherwise just return raw data
def file_to_dataframe(download_file: str, data: Union[str, bytes]):
    if re.search(r"\.fa", download_file):
        data = data.split("\n", maxsplit=1)

        meta = data[0]
        sequence = data[1].replace("\n", "")  # remove newlines

        return pd.DataFrame({"meta": [meta], "sequence": [sequence]})

    return data


def get_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.path.split("/")[-1]


class DownloadStatus(Enum):
    """An Enum to Describe the current status of a DRS download"""

    SUCCESS = 0
    FAIL = 1


class FilesClient(BaseServiceClient):
    def __init__(
        self,
        auth: Optional[OAuthTokenAuth] = None,
        registry_url: AnyStr = DEFAULT_SERVICE_REGISTRY,
    ):

        # A lock to prevent race conditions on exit_codes objects
        self.output_lock = threading.Lock()
        # lock to prevent race conditions for file output
        self.exit_code_lock = threading.Lock()

        super().__init__(auth=auth, registry_url=registry_url)

    def get_drs_client(self, drs_server: str) -> DrsClient:

        if self.auth:
            req = Request(url=drs_server)
            return DrsClient(drs_server, wallet=self.auth.get_access_token(req))
        else:
            return DrsClient(drs_server)

    def exit_download(
        self,
        url: str,
        status: DownloadStatus,
        message: str = "",
        exit_codes: dict = None,
    ) -> None:
        """
        Report a file download with a status and message

        :param url: The downloaded resource's url
        :param status: The reported status of the download
        :param message: A message describing the reason for setting the status
        :param exit_codes: A shared dict for all reports used by download_files
        """
        if exit_codes is not None:
            self.exit_code_lock.acquire()
            exit_codes[status][url] = message
            self.exit_code_lock.release()

    def download_file(
        self,
        url: str,
        output_dir: str,
        display_progress_bar: bool = False,
        out: Optional[list] = None,
        exit_codes: Optional[dict] = None,
    ) -> None:
        """
        Download a single DRS resource and output to a file or list

        :param url: The DRS resource url to download
        :param output_dir: The directory to download output to.
        :param display_progress_bar: Display a progress bar for the downloads to standard output
        :param out: If specified, output downloaded data to the list specified in the argument
        :param exit_codes: A shared dictionary of the exit statuses and messages
        :return:
        """

        http = urllib3.PoolManager()
        chunk_size = 1024
        download_url = None

        try:
            drs_object = DRSObject(url)
        except ValueError as v:
            self.exit_download(
                url,
                DownloadStatus.FAIL,
                f"There was an error while parsing the DRS url ({v})",
                exit_codes,
            )
            return

        drs_client = self.get_drs_client(drs_object.drs_server)

        try:
            object_info = drs_client.get_object_info(drs_object.object_id)
        except HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"DRS object at url [{url}] does not exist"
            elif e.response.status_code == 403:
                error_msg = "Access Denied"
            else:
                error_msg = "There was an error getting object info from the DRS Client"
            http.clear()
            self.exit_download(url, DownloadStatus.FAIL, error_msg, exit_codes)
            return

        if "access_methods" in object_info.keys():
            access_methods = object_info["access_methods"][0]
            for access_method in [am for am in access_methods if am["type"] == "https"]:
                # try to use the access_id to get the download url
                if "access_id" in access_method.keys():
                    object_access = drs_client.get_object_access(
                        drs_object.object_id, access_method["access_id"]
                    )
                    download_url = object_access["url"][0]
                    break
                # if we have a direct access_url for the access_method, use that
                elif "access_url" in access_method.keys():
                    download_url = access_method["access_url"]["url"]
                    break

            if not download_url:
                # we couldn't find a download url, exit unsuccessful
                http.clear()
                self.exit_download(
                    url,
                    DownloadStatus.FAIL,
                    f"Error determining access method",
                    exit_codes,
                )
        else:
            return  # next page token, just return

        try:
            download_stream = http.request("GET", download_url, preload_content=False)
        except HTTPError as e:
            http.clear()
            self.exit_download(
                url,
                DownloadStatus.FAIL,
                f"There was an error downloading [{download_url}] : {e}",
                exit_codes,
            )
            return

        download_filename = get_filename_from_url(download_url)

        if out is not None:
            data = handle_file_response(download_filename, download_stream.read())
            self.output_lock.acquire()
            out.append(file_to_dataframe(download_filename, data))
            self.output_lock.release()

        else:
            with open(f"{output_dir}/{download_filename}", "wb+") as dest:
                stream_size = int(download_stream.headers["Content-Length"])
                file_stream = download_stream.stream(chunk_size)
                if display_progress_bar:
                    click.echo(
                        f"Downloading {url} into {output_dir}/{download_filename}"
                    )
                    with click.progressbar(
                        length=stream_size, color=True
                    ) as download_progress:
                        for chunk in file_stream:
                            dest.write(chunk)
                            download_progress.update(chunk_size)
                else:
                    for chunk in file_stream:
                        dest.write(chunk)
        http.clear()
        self.exit_download(
            url, DownloadStatus.SUCCESS, "Download Successful", exit_codes
        )

    def download_files(
        self,
        urls: List[str],
        output_dir: str = os.getcwd(),
        display_progress_bar: bool = False,
        out: List = None,
    ) -> None:
        """
        Download a list of files and output either to files in the current directory or dump to a specified list

        :param urls: A list of DRS resource urls to download
        :param output_dir: The directory to download output to.
        :param display_progress_bar: Display a progress bar for the downloads to standard output
        :param out: If specified, output downloaded data to the list specified in the argument
        :raises: DRSDownloadException if one or more of the downloads fail
        """
        download_threads = []
        exit_codes = {status: {} for status in DownloadStatus}

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for url in urls:
            download = threading.Thread(
                target=self.download_file(
                    url,
                    output_dir,
                    display_progress_bar=display_progress_bar,
                    out=out,
                    exit_codes=exit_codes,
                ),
                name=url,
            )
            download.daemon = True
            download_threads.append(download)
            download.start()

        for thread in download_threads:
            thread.join()

        # at least one download failed, create exceptions
        failed_downloads = [
            DRSException(msg=msg, url=url)
            for url, msg in exit_codes.get(DownloadStatus.FAIL).items()
        ]
        if len(failed_downloads) > 0:
            raise DRSDownloadException(failed_downloads)
