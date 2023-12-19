#!/usr/bin/bash

#LEXICON=$1
OUTPUT=../../output202210
#CROSSCLASS=$2
ASSESSMENTTERMS=../../res/assessment_terms.txt
OTHERTERMS=../../res/other_terms_to_drop.txt

terms=(
  XYLA
  A2AG
  PDMP 
  CAFFINEDO 
  BTRAITS 
  BDD 
  GAMINGDO 
  GAMBLINGDO 
  BEHAVIORAD 
  MISOPHONIA 
  IDU 
  JOBINSTABLE 
  JUSTICE 
  LIVESALONE 
  LONELINESS 
  SOCIALCONNECT 
  STRAUMA 
  HOUSING 
  DETOX 
  LETHALMEANS 
  FOODINSECURE 
  ADL
)

cd "$(dirname "$0")"

for TARGET in "${terms[@]}"
do
  #echo "Removing cross target subset tags for $TARGET$POLARITY"
  #python3 cross_tagging_removal.py -d $LEXICON -t $OUTPUT/$TARGET -c $CROSSCLASS

  echo "Filtering tagged templated text for $TARGET"
  python3 filterTemplated.py -p $OUTPUT/ -t $TARGET -a $ASSESSMENTTERMS -o $OTHERTERMS -sp 14 -tp 6
done
