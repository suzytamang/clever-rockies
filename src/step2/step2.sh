#!/usr/bin/bash

LEXICON=../../res/dicts/dict.txt
HEADERS=../../res/headers.txt
CORPUS=/tmp/workspacezone/tsv/lastmodifieddatetime_month=202210.txt
OUTPUT=../../output202210
SNIPPETS=250
LGCONTEXT=3
RGCONTEXT=2
WORKERS=8

# below weshow an example bash command for Step 2, tagging of text.  Each example corresponds with a different target clinical practice.

# injection drug use
python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets IDU --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/IDU --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# loneliness
python sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LONELINESS --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LONELINESS --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# lives alone
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LIVESALONE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LIVESALONE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# PDMP
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets PDMP --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/PDMP --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# jobinstable
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets JOBINSTABLE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/JOBINSTABLE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# sexual trauma
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets STRAUMA --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/STRAUMA --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# justice
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets JUSTICE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/JUSTICE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# social connectedness
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets SOCIALCONNECT --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/SOCIALCONNECT --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# housing
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets HOUSING --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/HOUSING --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# detoxification
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets DETOX --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/DETOX --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# access to lethal means
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets LETHALMEANS --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/LETHALMEANS --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# long covid and mental health
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets COVID --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/COVID --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# food security
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets FOODINSECURE --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/FOODINSECURE --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

# acitivites of daily living.  Specifically, bathing, dressing and eating.
python3 sequencer.py --lexicon $LEXICON --section-headers $HEADERS --main-targets ADL --snippet-length $SNIPPETS --snippets --notes $CORPUS --workers $WORKERS --output $OUTPUT/ADL --left-gram-context $LGCONTEXT --right-gram-context $RGCONTEXT

#python3 sequencer.py --lexicon ../../res/dicts/dict.txt --section-headers ../../res/headers.txt --main-targets IDU --snippet-length 200 --snippets --notes /tmp/workspacezone/tsv/lastmodifieddatetime_month=202204.txt --workers 8 --output ../../output/IDU --left-gram-context 3 --right-gram-context 2

