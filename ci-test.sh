#!/usr/bin/env bash
apk add git openssl openssh curl openjdk17-jre

export TEST="TRUE"

export PORT=8000

set -e
pip3 install -r requirements.test.txt
pytest -v -s -x --cov-report html:coverage/html --junitxml coverage/junit.xml --cov-report=term --cov=.
# python -m coverage_output
