1Inch Quotes: Modeling DEX Slippage
===================================

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![CI](https://github.com/xenophonlabs/oneinch-quotes/actions/workflows/CI.yml/badge.svg)](https://github.com/xenophonlabs/oneinch-quotes/actions/workflows/CI.yml/badge.svg)

*This repo is being used as part of the [crvUSD Risk Modeling effort](https://github.com/xenophonlabs/crvUSDrisk).*

TODO: 

- Complete README

- Add demo notebook with plots!


### Usage


- We provide a simple flask API for querying our database to create ``price impact curves''.


### Replicating this service

- This repo may be used to create a service that queries quotes from 1inch for all pairwise combinations of tokens in the `src/configs/tokens.py` file.

- These quotes are saved to a Postgres database

