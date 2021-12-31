#!/bin/bash

export LANG=ko_KR.UTF-8
WORKING_DIR=$(dirname $0)
cd ${WORKING_DIR}
WORKING_DIR=`pwd`
echo "Working Directory: ${WORKING_DIR}"
source ${WORKING_DIR}/profile/nines_flow.profile
FILE_PATH="${WORKING_DIR}/cron.py"
echo ${FILE_PATH}
pyenv shell nines_flow
python3 ${FILE_PATH}