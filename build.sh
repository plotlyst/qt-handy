#!/bin/bash

# exit when any command fails
set -e

rm -rf docs/build/*

sphinx-build -b html docs/source docs/build


