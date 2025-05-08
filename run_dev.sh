#!/bin/bash
# run_dev.sh
export PYTHONPATH=.
fastmcp dev app/server/main.py:mcp
# Opcional: unset PYTHONPATH