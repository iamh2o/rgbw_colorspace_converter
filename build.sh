#!/bin/bash

hash poetry
if [ $? -ne 0 ]; then
  echo "Installing poetry"
  curl -fsSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
fi

echo "Installing python dependencies with poetry"
poetry install

