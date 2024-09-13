#!/usr/bin/bash

METADATA_PATH=
CLEVER_OUTPUT=
CORPUS=
USING_TEST_NOTES=0

show_help() {
    echo "Usage: all_steps.sh -n|--notes <path to notes> -m|--metadata <path to metadata> [-t|--test_files] [-h|--help] "
    exit 1
}

set_test_notes() {
    CORPUS="$(realpath ../tests/resources/test_notes/test_notes.txt)"
    METADATA_PATH="$(realpath ../tests/resources/test_notes/test_metadata.tsv)"
    CLEVER_OUTPUT="$(realpath ../tests/output)"
    USING_TEST_NOTES=1

    echo "Running CLEVER-Rockies using Test Notes"
    echo "CORPUS: ${CORPUS}"
    echo "METADATA_PATH: ${METADATA_PATH}"
    echo "CLEVER_OUTPUT: ${CLEVER_OUTPUT}"
}

set_metadata_path() {
    local metadata_path="$1"
    if [[ ! -f "$metadata_path" ]]; then
        echo >&2 "Invalid metadata: \"$metadata_path\""
        exit 1
    fi
    METADATA_PATH="$metadata_path"
}

set_notes_path() {
    local notes_path="$1"
    if [[ ! -f "$notes_path" ]]; then
        echo >&2 "Invalid notes path: \"$notes_path\""
        exit 1
    fi
    CORPUS="$notes_path"
}

set_output_path() {
    local output_path="$1"
    if [[ ! -d "$output_path" ]]; then
        echo >&2 "Invalid output path: \"$output_path\""
        exit 1
    fi
    CLEVER_OUTPUT="$output_path"
}

metadata_not_set() {
    echo >&2 "Metadata not set"
    echo >&2 
    show_help
    exit 1
}

clever_output_not_set() {
    echo >&2 "Output not set"
    exit 1
}

corpus_not_set() {
    echo >&2 "Corpus not set"
    exit 1
}

validate_settings() {

    [[ -z "${METADATA_PATH}" ]] && metadata_not_set
    [[ -z "${CLEVER_OUTPUT}" ]] && clever_output_not_set
    [[ -z "${CORPUS}" ]] && corpus_not_set

}

while [[ $# -gt 0 ]]
do
    case "$1" in
    -h | --help)
        show_help
        break
        ;;
    -t | --test_files)
        shift
        set_test_notes
        break
        ;;
    -m | --metadata)
        shift
        set_metadata_path "$1"
        shift
        ;;
    -n | --notes)
        shift
        set_notes_path "$1"
        shift
        ;;
    -o | --output)
        shift
        set_output_path "$1"
        shift
        ;;
    *)
        shift
        ;;
    esac
done

validate_settings

script_directory="$(realpath "$0" | sed 's|\(.*\)/.*|\1|')"
project_path="$(dirname "${script_directory}")"
res_path="${project_path}"/res
export LEXICON_PATH="$(realpath "${res_path}"/dicts/dict.txt)"
export HEADERS_PATH="$(realpath "${res_path}"/headers.txt)"


pushd "${script_directory}" > /dev/null
OLD_PYTHONPATH=
if [[ ! -z "${PYTHONPATH}" ]]; then
    OLD_PYTHONPATH="${PYTHONPATH}"
fi
export PYTHONPATH="$(pwd)"

export CLEVER_OUTPUT="${CLEVER_OUTPUT}"
export CORPUS="${CORPUS}"
export METADATA_PATH="${METADATA_PATH}"
export CLEVER_NUM_WORKERS=8

#######################################
# STEP 2
#######################################

if [[ "$USING_TEST_NOTES"=="1" ]]; then
    mkdir -p "${CLEVER_OUTPUT}"
    if [[ "$(find "${CLEVER_OUTPUT}"/ -type d -empty)" != "${CLEVER_OUTPUT}"/ ]]; then
        rm -rf "${CLEVER_OUTPUT}"/*
    fi
fi
pushd ./step2 > /dev/null
./step2.sh
popd > /dev/null

#######################################
# STEP 3
#######################################

pushd ./step3 > /dev/null
./step3.sh
popd > /dev/null


#######################################
# STEP 4
#######################################

pushd ./step4 > /dev/null
./step4.sh
popd > /dev/null

#######################################
# STEP 5
#######################################

pushd ./step5 > /dev/null
./step5.sh
popd > /dev/null

popd > /dev/null

if [[ ! -z "${OLD_PYTHONPATH}" ]]; then
    export PYTHONPATH="${OLD_PYTHONPATH}"
fi