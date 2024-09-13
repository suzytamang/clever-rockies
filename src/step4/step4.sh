#!/usr/bin/bash

python_path="${PYTHON_EXE:=python}"
script_directory="$(realpath "$0" | sed 's|\(.*\)/.*|\1|')"

pushd "${script_directory}" > /dev/null

if [[ ! -z "${CLEVER_OUTPUT}" ]]; then
    OUTPUT="${CLEVER_OUTPUT}"
else
    OUTPUT="$(realpath ../../output202210)"
fi
echo >&2 "OUTPUT: ${OUTPUT}"

"${python_path}" cleverRules.py "${OUTPUT}/XYLA" XYLA
"${python_path}" cleverRules.py "${OUTPUT}/A2AG" A2AG
"${python_path}" cleverRules.py "${OUTPUT}/PDMP" PDMP
"${python_path}" cleverRules.py "${OUTPUT}/CAFFINEDO" CAFFINEDO
"${python_path}" cleverRules.py "${OUTPUT}/BTRAITS" BTRAITS
"${python_path}" cleverRules.py "${OUTPUT}/BDD" BDD
"${python_path}" cleverRules.py "${OUTPUT}/GAMINGDO" GAMINGDO
"${python_path}" cleverRules.py "${OUTPUT}/GAMBLINGDO" GAMBLINGDO
"${python_path}" cleverRules.py "${OUTPUT}/BEHAVIORAD" BEHAVIORAD
"${python_path}" cleverRules.py "${OUTPUT}/MISOPHONIA" MISOPHONIA
"${python_path}" cleverRules.py "${OUTPUT}/IDU" IDU
"${python_path}" cleverRules.py "${OUTPUT}/JOBINSTABLE" JOBINSTABLE
"${python_path}" cleverRules.py "${OUTPUT}/JUSTICE" JUSTICE
"${python_path}" cleverRules.py "${OUTPUT}/LIVESALONE" LIVESALONE
"${python_path}" cleverRules.py "${OUTPUT}/LONELINESS" LONELINESS
"${python_path}" cleverRules.py "${OUTPUT}/SOCIALCONNECT" SOCIALCONNECT
"${python_path}" cleverRules.py "${OUTPUT}/STRAUMA" STRAUMA
"${python_path}" cleverRules.py "${OUTPUT}/HOUSING" HOUSING
"${python_path}" cleverRules.py "${OUTPUT}/DETOX" DETOX
"${python_path}" cleverRules.py "${OUTPUT}/LETHALMEANS" LETHALMEANS
"${python_path}" cleverRules.py "${OUTPUT}/FOODINSECURE" FOODINSECURE
"${python_path}" cleverRules.py "${OUTPUT}/ADL" ADL
"${python_path}" cleverRules.py "${OUTPUT}/DODOUD" DODOUD

popd > /dev/null