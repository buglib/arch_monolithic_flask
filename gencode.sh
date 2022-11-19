#!/bin/bash

pip uninstall -y click && \
pip install click==6.7 && \
swagger_py_codegen -s swagger.yaml . -p api && \
pip uninstall -y click && \
pip install click