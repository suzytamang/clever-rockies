#!/usr/bin/bash

python_path="${PYTHON_EXE:=python}"
script_directory="$(realpath "$0" | sed 's|\(.*\)/.*|\1|')"
common_directory="$(dirname "${script_directory}")/common"
project_directory="$(dirname "${script_directory}")"
res_directory="$(dirname "${project_directory}")/res"

# echo "python_path: ${python_path}"
# echo "script_directory: ${script_directory}"
# echo "project_directory: ${project_directory}"
# echo "common_directory: ${common_directory}"
# echo "res_directory: ${res_directory}"

#LEXICON=$1
#CROSSCLASS=$2
if [[ ! -z "${CLEVER_OUTPUT}" ]]; then
    OUTPUT="${CLEVER_OUTPUT}"
else
    OUTPUT="$(realpath ../../output202210)"
fi
echo >&2 "OUTPUT: ${OUTPUT}"

if [[ ! -z "${CLEVER_ASSESSMENTTERMS}" ]]; then
    ASSESSMENTTERMS="${CLEVER_ASSESSMENTTERMS}"
else
    ASSESSMENTTERMS="$(realpath "${res_directory}/assessment_terms.txt")"
fi
echo >&2 "ASSESSMENTTERMS: ${ASSESSMENTTERMS}"

if [[ ! -z "${CLEVER_OTHERTERMS}" ]]; then
    OTHERTERMS="${CLEVER_OTHERTERMS}"
else
    OTHERTERMS="$(realpath "${res_directory}"/other_terms_to_drop.txt)"
fi
echo >&2 "OTHERTERMS: ${OTHERTERMS}"

main_targets_path="${common_directory}/main_targets"

oldIFS="$IFS"
IFS=$'\n' terms=($(<"$main_targets_path"))
IFS="$oldIFS"

pushd "$script_directory" > /dev/null

for TARGET in "${terms[@]}"
do
  #echo "Removing cross target subset tags for $TARGET$POLARITY"
  #python3 cross_tagging_removal.py -d $LEXICON -t $OUTPUT/$TARGET -c $CROSSCLASS

  echo "Filtering tagged templated text for $TARGET"
  "${python_path}" filterTemplated.py -p "${OUTPUT}"/ -t "${TARGET}" -a "${ASSESSMENTTERMS}" -o "${OTHERTERMS}" -sp 14 -tp 6
done

popd > /dev/null