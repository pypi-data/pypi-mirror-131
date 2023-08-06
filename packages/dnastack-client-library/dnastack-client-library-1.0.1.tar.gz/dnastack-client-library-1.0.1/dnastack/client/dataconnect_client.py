from typing import Iterator, Optional, Dict, AnyStr, Any
import requests
from requests import HTTPError, Request
from search_python_client.search import SearchClient

from .base_client import BaseServiceClient
from ..auth import OAuthTokenAuth
from ..constants import DEFAULT_SERVICE_REGISTRY
from ..exceptions import ServiceException


class DataConnectClient(BaseServiceClient):
    """
    A Client for the GA4GH Data Connect standard


    """

    def __init__(
        self,
        url: str,
        auth: Optional[OAuthTokenAuth] = None,
        registry_url: AnyStr = DEFAULT_SERVICE_REGISTRY,
    ):
        super().__init__(url=url, auth=auth, registry_url=registry_url)

    @property
    def _client(self) -> SearchClient:
        """
        Get a SearchClient instance, which is authorized if the service has an access token

        :return: a :class:`SearchClient` instance
        """
        if self.auth:
            req = Request(url=self.url)
            return SearchClient(self.url, wallet=self.auth.get_access_token(req))
        else:
            return SearchClient(self.url)

    def query(self, q: str) -> Iterator:
        """
        Run an SQL query against a Data Connect instance

        :param q: The SQL query to be executed
        :return: The formatted result of the SQL query
        """

        try:
            results = self._client.search_table(q)
            return results
        except HTTPError as h:
            self._raise_error(h.response, "The query was unsuccessful")

    def list_tables(self) -> Iterator:
        """
        Return the list of tables available at the Data Connect instance

        :return: A dict of available tables' metadata.
        """

        try:
            tables = self._client.get_table_list()
        except HTTPError as e:
            error_res = e.response
            self._raise_error(
                error_res,
                f"The server returned HTTP error code {error_res.status_code}",
            )

        return tables

    def get_table(self, table_name: AnyStr) -> Dict[AnyStr, Any]:
        """
        Get table metadata for a specific table

        :param table_name: The name of the table
        :return: A dict of table metadata.
        """

        try:
            table_info = self._client.get_table_info(table_name)
        except HTTPError as e:
            error_res = e.response
            self._raise_error(
                error_res,
                f"The server returned HTTP error code {error_res.status_code}",
            )

        results = table_info.to_dict()

        return results
