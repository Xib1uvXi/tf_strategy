#/bin/bash

set -eux

flake8 .
mypy .
