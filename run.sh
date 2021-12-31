#!/bin/bash

export LANG=ko_KR.UTF-8
FLOW_NAME=$1
ARGUMENTS=$2
WORKING_DIR=$(dirname $0)
cd ${WORKING_DIR}
WORKING_DIR=`pwd`
echo "Working Directory: ${WORKING_DIR}"
source ${WORKING_DIR}/profile/nines_flow.profile
FILE_PATH="${WORKING_DIR}/main.py ${FLOW_NAME} ${ARGUMENTS}"
echo ${FILE_PATH}
python3 ${FILE_PATH}
