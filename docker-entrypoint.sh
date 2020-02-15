#!/bin/bash

# Exit immediately if a  .
set -e

if [ "$1" = 'run-app' ]; then
    exec streamlit run kiwi.py
fi

exec "$@"