#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

if [ -z "${TEST_STUDENT_EMAIL:-}" ]; then
  echo "[ERROR] TEST_STUDENT_EMAIL is required"
  exit 1
fi

if [ -z "${TEST_STUDENT_PASSWORD:-}" ]; then
  echo "[ERROR] TEST_STUDENT_PASSWORD is required"
  exit 1
fi

curl -v http://127.0.0.1:8080/auth/login || true

pytest -q --alluredir=allure-results