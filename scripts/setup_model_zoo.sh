#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLASSMIND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

MODEL_ZOO_DIR="${CLASSMIND_MODEL_ZOO:-${CLASSMIND_DIR}/third_party/rdk_model_zoo}"

MODEL_ZOO_REPO="https://github.com/D-Robotics/rdk_model_zoo.git"
MODEL_ZOO_BRANCH="rdk_x5"
MODEL_ZOO_COMMIT="b60777a65e4ea315406b49cb5348d24ad85096f0"

MODEL_NAME="yolo11n_detect_bayese_640x640_nv12.bin"

MODEL_DIR="${MODEL_ZOO_DIR}/samples/vision/ultralytics_yolo/model"
MODEL_FILE="${MODEL_DIR}/${MODEL_NAME}"

MODEL_URL="https://archive.d-robotics.cc/downloads/rdk_model_zoo/rdk_x5/ultralytics_YOLO/${MODEL_NAME}"

echo "========================================"
echo " ClassMind RDK Model Zoo Setup"
echo "========================================"

if [ -d "${MODEL_ZOO_DIR}/.git" ]; then
    echo "Model Zoo repository already exists:"
    echo "${MODEL_ZOO_DIR}"
else
    echo "Cloning official D-Robotics RDK Model Zoo..."

    mkdir -p "$(dirname "${MODEL_ZOO_DIR}")"

    git clone \
        --branch "${MODEL_ZOO_BRANCH}" \
        --single-branch \
        "${MODEL_ZOO_REPO}" \
        "${MODEL_ZOO_DIR}"
fi

echo
echo "Checking out validated Model Zoo revision..."

cd "${MODEL_ZOO_DIR}"

git fetch origin "${MODEL_ZOO_BRANCH}"
git checkout "${MODEL_ZOO_COMMIT}"

CURRENT_COMMIT="$(git rev-parse HEAD)"

if [ "${CURRENT_COMMIT}" != "${MODEL_ZOO_COMMIT}" ]; then
    echo "ERROR: Model Zoo revision verification failed."
    echo "Expected: ${MODEL_ZOO_COMMIT}"
    echo "Current:  ${CURRENT_COMMIT}"
    exit 1
fi

echo
echo "Validated Model Zoo revision:"
echo "${CURRENT_COMMIT}"

mkdir -p "${MODEL_DIR}"

if [ -f "${MODEL_FILE}" ]; then
    echo
    echo "YOLO11n BPU model already exists:"
    echo "${MODEL_FILE}"
else
    echo
    echo "Downloading YOLO11n BPU model from D-Robotics..."
    echo "${MODEL_URL}"

    wget \
        --continue \
        --output-document="${MODEL_FILE}" \
        "${MODEL_URL}"
fi

if [ ! -s "${MODEL_FILE}" ]; then
    echo
    echo "ERROR: YOLO11n BPU model download failed."
    rm -f "${MODEL_FILE}"
    exit 1
fi

echo
echo "YOLO11n BPU model found:"
echo "${MODEL_FILE}"

echo
echo "Model size:"
du -h "${MODEL_FILE}"

echo
echo "========================================"
echo " ClassMind Model Zoo Setup Complete"
echo "========================================"

echo
echo "Model Zoo:"
echo "${MODEL_ZOO_DIR}"

echo
echo "Validated commit:"
echo "${MODEL_ZOO_COMMIT}"

echo
echo "Configure ClassMind with:"
echo
echo "export CLASSMIND_MODEL_ZOO=\"${MODEL_ZOO_DIR}\""