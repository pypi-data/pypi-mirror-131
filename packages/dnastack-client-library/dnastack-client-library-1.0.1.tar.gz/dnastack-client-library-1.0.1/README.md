# DNAstack Client Library
`dnastack` is the command line interface and Python library for DNAstack products. This project is written in Python and uses the [Click](https://click.palletsprojects.com/en/7.x/) CLI framework.

### Table of Contents
- [Getting Started](#getting-started)
  - [Command Line Interface](#command-line-interface)
    - [MacOS](#macos)
    - [Linux](#linux)
    - [Windows](#windows)
    - [Local Python](#running-the-cli-locally)
  - [Python Library](#python-library)
- [Distributing the CLI](#distributing-the-clipython-library)
- [API Reference](#api-references)
- [Authorization](#authorization)
- [Testing](#testing)

## Getting Started

### Command Line Interface

#### MacOS


##### With Homebrew
If you have from a command line, run the following:
```bash
brew tap install dnastack/dnastack
brew install dnastack
```

##### From a Command Line
From a command line,
```bash
mkdir ~/.dnastack; cd ~/.dnastack &&
  curl -L https://github.com/DNAstack/public-dnastack-cli/releases/latest/download/dnastack-mac.zip > ~/.dnastack/dnastack.zip &&
  unzip dnastack.zip && chmod u+x dnastack && rm dnastack.zip
```

Additionally, add the DNAStack CLI to your PATH by running `export PATH="$PATH:$HOME/.dnastack"`

#### Linux

From a command line, run:
```bash
mkdir ~/.dnastack; cd ~/.dnastack &&
  curl -L https://github.com/DNAstack/public-dnastack-cli/releases/latest/download/dnastack-mac.zip > ~/.dnastack/dnastack.zip &&
  unzip dnastack.zip && chmod u+x dnastack && rm dnastack.zip
```

Additionally, add the DNAStack CLI to your PATH by running `export PATH="$PATH:$HOME/.dnastack"`

#### Windows

From a Powershell command line, run:
```bash
Invoke-WebRequest `
https://github.com/DNAstack/public-dnastack-cli/releases/latest/download/dnastack-windows.exe `
-OutFile ( New-Item -Path "~/.dnastack/dnastack.exe" -Force )
```

Additionally, add the DNAStack CLI to your PATH by running `$env:Path += ";%USERPROFILE%\.dnastack"`


#### Locally using Python

After cloning into a local directory, navigate to the directory and do the following:
1. Run `pip3 install -r requirements.txt` to download all the dependencies
2. From the command line run `python3 -m dnastack ...`


### Usage
```
python3 -m dnastack config set data_connect.url https://collection-service.publisher.dnastack.com/collection/library/search/
python3 -m dnastack dataconnect tables list
python3 -m dnastack dataconnect tables get covid.cloud.variants
python3 -m dnastack dataconnect query "SELECT drs_url FROM covid.cloud.files LIMIT 10"
```

### Python Library
The CLI can also be imported as a Python library. It is hosted on PyPi here: https://pypi.org/project/dnastack-client-library/

You can simply install it as a dependency with `pip3 install dnastack-client-library` or through other traditional `pip` ways (e.g. `requirements.txt`)

To use the `dnastack-client-library` library in Jupyter Notebooks and other Python code, simply import the `PublisherClient` object

`from dnastack import PublisherClient`

#### Example

```python
from dnastack import PublisherClient
import pandas as pd

publisher_client = PublisherClient(dataconnect_url='[DATACONNECT_URL]')
# get tables
tables = publisher_client.dataconnect.list_tables()
# get table schema
schema = publisher_client.dataconnect.get_table('[TABLE_NAME]')
# query a table
results = publisher_client.dataconnect.query('SELECT * FROM ...')
# load a drs resource into a DataFrame
drs_df = pandas.DataFrame(publisher_client.load(['[DRS_URL]']))
# download a DRS resource into a file
publisher_client.download(['[DRS_URL]'])
```





## Distributing the CLI/Python library

### Versioning

The versioning for `dnastack-client-library` is done through the `bumpversion` utility.

For patch version updates (e.g. 1.0.0 to 1.0.1),
this process is done automatically by a git hook which updates the version in the project to the
next patch if it is not already a future version.

For minor (1.0.0 to 1.1.0) or major (1.0.0 to 2.0.0) version updates, the update has to be
done manually. This can be done by setting the value of `__version__` in [constants.py](dnastack/constants.py)
and [setup.cfg](setup.cfg) to the (future) version of choice.


### CI/CD Pipeline

In it's current state, the CI/CD pipeline for the dnastack-client-library:

1. Builds the *Linux* excutable of the CLI (Windows and Mac executables need to be built manually)
2. Publishes the available executables (i.e. the ones in the `dist` folder) to Github Releases
3. Builds and publishes the PyPI package.

These processes are all triggered after every push to the `main` branch of the repo.
You should not need to do any of the above manually.

The [cloudbuild.yaml](./cloudbuild.yaml) file in the root directory specifies the steps to be run by Google Cloud Build

The CI/CD pipeline also makes use of a bootstrap workspace to store secrets used in distribution.
More information of how this workspace is used and how to add/modify secrets can be found [here](docs/bootstrap-workspace.md)

## API References

**Note:** These references are not complete and very much a work in progress.

CLI: [CLI Reference](docs/reference/cli.md)


## Authorization

In the CLI, we use Wallet clients in order to authorize users to access Data Connect, Collections, DRS, and WES functionality.

### Passport
In order to log in to get an access token:

1. Make sure the client is correctly configured. You need to log in with the Wallet instance
associated with the service you are trying to gain access for. Information on creating a client and exisitng
configurations can be found [here](docs/clients.md). In order to set this configuration, run:
```bash
dnastack config set [SERVICE].auth.url [WALLET-URL]
dnastack config set [SERVICE].auth.client.id [CLIENT-ID]
dnastack config set [SERVICE].auth.client.secret [CLIENT-SECRET]
dnastack config set [SERVICE].auth.client.redirect_url [REDIRECT-URI]
```
2. Log in using `dnastack auth login [SERVICE]`. This will open a tab in your browser where you may login, then allow/deny access
to certain permissions. If allowed, a new token will be created and you will be able to access services.

### Refresh Token

Since the above requires user interaction to authenticate, it cannot be used in headless environments such as scripts.
The way that users should log in is through an OAuth refresh token.

In order to get an access token in a headless environment:

1. Manually generate a refresh token using the following script. This will require you to sign in using Passport.
The result of the final command will be a refresh_token for the service
```bash
# configure your service's oauth client
dnastack config set [SERVICE].auth.url [BASE AUTH URL]
dnastack config set [SERVICE].auth.client.id [CLIENT ID]
dnastack config set [SERVICE].auth.client.secret [CLIENT SECRET]
dnastack config set [SERVICE].auth.client.redirect_url [CLIENT SECRET]

# configure the service url
dnastack config set [SERVICE].url [SERVICE URL]

# log in with that service
dnastack auth login [SERVICE]

# get the token
dnastack config get [SERVICE].auth.refresh_token
```

2. In the headless environment, when log in is required, run
```bash
# configure your service's oauth client to the same as log in
dnastack config set [SERVICE].auth.url [BASE AUTH URL]
dnastack config set [SERVICE].auth.client.id [CLIENT ID]
dnastack config set [SERVICE].auth.client.secret [CLIENT SECRET]
dnastack config set [SERVICE].auth.client.redirect_url [CLIENT SECRET]

dnastack config set [SERVICE].auth.refresh_token [TOKEN]
```


## Testing

There are e2e-tests set up for the CLI. Instructions to run can be found [here](docs/e2e-tests.md)
