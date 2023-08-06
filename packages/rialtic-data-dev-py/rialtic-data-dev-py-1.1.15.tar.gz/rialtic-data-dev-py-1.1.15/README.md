# Rialtic-Data DEV SDK (Python)

This repo contains an implementation of the `rialtic-data` interface as first implemented in
the `open-insight-marketplace/rialtic-data-python` repository.

As a development implementation, the content of this repository differs from the one mentioned above in two main ways:

1. The code in this repository is not capable of communicating with the production environment
2. This repository will contain implementations that allow for easy testing in development, with features such as
   loading data from a local file or database

Any other differences (such as the testing framework used) are in the effort of bringing this repository more in line
with our other Python repos under the `rialtic-community` org, and with our emerging practices and standards in this
org.

Most crucially, it is important that the interface maintains consistency with whichever implementation is currently used
by the platform team in production.

# Usage

In order to connect to the development data servers, an API key is needed. The tests currently expect environment
variable called `APIKEY` containing the key. See `test_rialtic_data.py` for an example of how to load and use this key.

