#!/bin/bash

cd "${0%/*}/" # Navigates to the directory that this script is currently stored in

FILES="AnsibleBatchGen.py GenNumbers.py"

echo "-- Flake8 Checks"
flake8 ${FILES}

echo

echo "-- PyRight Checks"
pyright ${FILES}
