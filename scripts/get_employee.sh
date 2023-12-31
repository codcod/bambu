#!/usr/bin/env bash

set -x

domain="$1"

http GET https://api.bamboohr.com/api/gateway.php/${domain}/v1/employees/1/