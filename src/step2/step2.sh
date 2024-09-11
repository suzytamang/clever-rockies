#!/usr/bin/bash

LEXICON=../../res/dicts/dict.txt
HEADERS=../../res/headers.txt
CORPUS=/tmp/workspacezone/tsv/lastmodifieddatetime_month=202210.txt
OUTPUT=../../output202210
SNIPPETS=250
LGCONTEXT=3
RGCONTEXT=2
WORKERS=8

main_targets=(XYLA A2AG PDMP CAFFINEDO BTRAITS BDD GAMINGDO GAMBLINGDO BEHAVIORAD MISOPHONIA IDU LONELINESS LIVESALONE JOBINSTABLE STRAUMA JUSTICE SOCIALCONNECT HOUSING DETOX LETHALMEANS FOODINSECURE ADL DODOUD IDU)

cd "$(dirname "$0")"

corpus_src="$1"
output="$2"
lexicon="$(realpath "$LEXICON")"
headers="$(realpath "$HEADERS")"

test_notes=0
if [[ "$corpus_src"=="test_notes" ]]; then
    echo >&2 "Using test notes"
    test_notes=1
    corpus_src="$(realpath "../../tests/resources/test_notes/test_notes_with_metadata_one_line.txt")"
fi

# below we show an example bash command for Step 2, tagging of text.  Each example corresponds with a different target clinical practice.

run_sequencer() {

    local main_target="$1"
    local corpus_src="$2"
    local output_path="$3"
    local lexicon="$4"
    local headers="$5"

    local full_output_path="$(realpath "${output_path}/${main_target}")"

    echo >&2 "output_path: $output_path"
    echo >&2 "corpus_src: $corpus_src"
    echo >&2 "lexicon: $lexicon"
    echo >&2 "headers: $headers"

    if [[ -z "$main_target" ]]; then
        echo >&2 "Main target empty"
        echo "1"
    else
        echo >&2 "Running Sequencer on Main Target: \"$main_target\""
        cmd="python sequencer.py --lexicon \""${lexicon}"\" --section-headers \""${headers}"\" --main-targets \""${main_target}"\" --snippet-length \""${SNIPPETS}"\" --snippets --notes \""${corpus_src}"\" --workers \""${WORKERS}"\" --output \""${full_output_path}"\" --left-gram-context \""${LGCONTEXT}"\" --right-gram-context \""${RGCONTEXT}"\""
        echo >&2 "$cmd"
        echo "0"
    fi
    
}

if [[ -z "$corpus_src" ]]; then
    corpus_src="$CORPUS"
fi

if [[ -z "$output" ]]; then
    output="$OUTPUT"
fi

echo "Processing corpus: $corpus_src"
echo "Output Root: $output"
echo "Lexicon: $lexicon"
echo "Headers: $headers"

for m in ${main_targets[@]}; do
    results="$(run_sequencer "$m" "$corpus_src" "$output" "$lexicon" "$headers")"
    if [[ "$results" == "1" ]]; then
        echo >&2 "Error encountered; exiting at step \"$m\""
        exit "1"
    fi
done

# # xylazine
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets XYLA --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/XYLA --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # alpha 2 agonists
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets A2AG --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/A2AG --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # prescription drug monitoring program
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets PDMP --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/PDMP --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # caffeine use disorder
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets CAFFINEDO --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/CAFFINEDO --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # cluster b traits
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets BTRAITS --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/BTRAITS --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # body dismorphic disorder
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets BDD --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/BDD --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # gaming disorder
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets GAMINGDO --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/GAMINGDO --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # gambling disorder
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets GAMBLINGDO --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/GAMBLINGDO --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # other behavioral addiction
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets BEHAVIORAD --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/BEHAVIORAD --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# #misophonia
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets MISOPHONIA --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/MISOPHONIA --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # injection drug use
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets IDU --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/IDU --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # loneliness
# python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LONELINESS --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LONELINESS --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # lives alone
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LIVESALONE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LIVESALONE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # job instable
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets JOBINSTABLE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/JOBINSTABLE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # sexual trauma
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets STRAUMA --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/STRAUMA --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # justice
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets JUSTICE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/JUSTICE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # social connectedness
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets SOCIALCONNECT --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/SOCIALCONNECT --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # housing
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets HOUSING --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/HOUSING --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # detoxification
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets DETOX --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/DETOX --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # access to lethal means
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LETHALMEANS --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LETHALMEANS --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # food security
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets FOODINSECURE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/FOODINSECURE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # acitivites of daily living.  Specifically, bathing, dressing and eating.
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets ADL --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/ADL --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# # department of defense opioid use disorder
# python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets DODOUD --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/DODOUD --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

#python3 sequencer.py --lexicon ../../res/dicts/dict.txt --section-headers ../../res/headers.txt --main-targets IDU --snippet-length 200 --snippets --notes /tmp/workspacezone/tsv/lastmodifieddatetime_month=202204.txt --workers 8 --output ../../output/IDU --left-gram-context 3 --right-gram-context 2
