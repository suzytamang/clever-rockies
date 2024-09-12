#!/usr/bin/bash


cd "$(dirname "$0")"

python_path="${PYTHON_EXE:=python}"
LEXICON="$(realpath ../../res/dicts/dict.txt)"
ANTS=linkedAnts.txt
if [[ ! -z "${METADATA_PATH}" ]]; then
    METADATA="${METADATA_PATH}"
else
    METADATA="$(realpath /tmp/workspacezone/METADATA/lastmodifieddatetime_month=202210.txt)"
fi
if [[ ! -z "${CLEVER_OUTPUT}" ]]; then
    OUTPUT="${CLEVER_OUTPUT}"
else
    OUTPUT="$(realpath ../../output202210)"
fi

"${python_path}" organize.py "${OUTPUT}/XYLA" "${LEXICON}" "${METADATA}" "${OUTPUT}/XYLA/$ANTS"
"${python_path}" organize.py "${OUTPUT}/A2AG" "${LEXICON}" "${METADATA}" "${OUTPUT}/A2AG/$ANTS"
"${python_path}" organize.py "${OUTPUT}/PDMP" "${LEXICON}" "${METADATA}" "${OUTPUT}/PDMP/$ANTS"
"${python_path}" organize.py "${OUTPUT}/CAFFINEDO" "${LEXICON}" "${METADATA}" "${OUTPUT}/CAFFINEDO/$ANTS"
"${python_path}" organize.py "${OUTPUT}/BTRAITS" "${LEXICON}" "${METADATA}" "${OUTPUT}/BTRAITS/$ANTS"
"${python_path}" organize.py "${OUTPUT}/BDD" "${LEXICON}" "${METADATA}" "${OUTPUT}/BDD/$ANTS"
"${python_path}" organize.py "${OUTPUT}/GAMINGDO" "${LEXICON}" "${METADATA}" "${OUTPUT}/GAMINGDO/$ANTS"
"${python_path}" organize.py "${OUTPUT}/GAMBLINGDO" "${LEXICON}" "${METADATA}" "${OUTPUT}/GAMBLINGDO/$ANTS"
"${python_path}" organize.py "${OUTPUT}/BEHAVIORAD" "${LEXICON}" "${METADATA}" "${OUTPUT}/BEHAVIORAD/$ANTS"
"${python_path}" organize.py "${OUTPUT}/MISOPHONIA" "${LEXICON}" "${METADATA}" "${OUTPUT}/MISOPHONIA/$ANTS"
"${python_path}" organize.py "${OUTPUT}/IDU" "${LEXICON}" "${METADATA}" "${OUTPUT}/IDU/$ANTS"
"${python_path}" organize.py "${OUTPUT}/JOBINSTABLE" "${LEXICON}" "${METADATA}" "${OUTPUT}/JOBINSTABLE/$ANTS"
"${python_path}" organize.py "${OUTPUT}/JUSTICE" "${LEXICON}" "${METADATA}" "${OUTPUT}/JUSTICE/$ANTS"
"${python_path}" organize.py "${OUTPUT}/LIVESALONE" "${LEXICON}" "${METADATA}" "${OUTPUT}/LIVESALONE/$ANTS"
"${python_path}" organize.py "${OUTPUT}/LONELINESS" "${LEXICON}" "${METADATA}" "${OUTPUT}/LONELINESS/$ANTS"
"${python_path}" organize.py "${OUTPUT}/SOCIALCONNECT" "${LEXICON}" "${METADATA}" "${OUTPUT}/SOCIALCONNECT/$ANTS"
"${python_path}" organize.py "${OUTPUT}/STRAUMA" "${LEXICON}" "${METADATA}" "${OUTPUT}/STRAUMA/$ANTS"
"${python_path}" organize.py "${OUTPUT}/HOUSING" "${LEXICON}" "${METADATA}" "${OUTPUT}/HOUSING/$ANTS"
"${python_path}" organize.py "${OUTPUT}/DETOX" "${LEXICON}" "${METADATA}" "${OUTPUT}/DETOX/$ANTS"
"${python_path}" organize.py "${OUTPUT}/FOODINSECURE" "${LEXICON}" "${METADATA}" "${OUTPUT}/FOODINSECURE/$ANTS"
"${python_path}" organize.py "${OUTPUT}/LETHALMEANS" "${LEXICON}" "${METADATA}" "${OUTPUT}/LETHALMEANS/$ANTS"
"${python_path}" organize.py "${OUTPUT}/ADL" "${LEXICON}" "${METADATA}" "${OUTPUT}/ADL/$ANTS"
"${python_path}" organize.py "${OUTPUT}/DODOUD" "${LEXICON}" "${METADATA}" "${OUTPUT}/DODOUD/$ANTS"
