#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if a parameter is provided
if [ -z "$1" ]; then
  # Prompt the user for input if no parameter is provided
  echo "Please enter the template and data names [default]"
  read docxAndTemplateName
else
  # Use the provided parameter
  docxAndTemplateName="$1"
fi


cd "$SCRIPT_DIR"
pipenv install
pipenv run python fillInvoice.py $docxAndTemplateName
