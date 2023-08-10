# CLEVER (CL-inical EVE-nt R-ecognizer)

This repo includes the Python3 version of CLEVER code from the Program Evaluation Resource Center, Office of Mental Health and Suicide Prevention, Department of Veterans Affairs.

Original Development Team
Suzanne Tamang
Manual 
Tanya

Continued Developiment Team
Suzanne Tamang
Asqar Shotqara
Esther Meerwijk

Create an output folder.
Run the shell scripts in each of the step folders under ./src. The scripts are provided as examples. 
Change the target concept and output folder as needed. 
Make sure that scripts retain their Unix file format. DOS line endings cause trouble.
Make sure that the scripts do not end with an empty line.

Step 1 is not currently used.

Step 2 tags text from the corpus for terms from the dictionary. It returns the tagged terms and
some of its context, referred to as snippets, in extraction files, one for each worker.

Step 3 combines the extraction files with meta-data and returns one file: linkedAnts.txt.

Step 4 labels the snippets in the linkedAnts file as positive, negative if a negation term is
found, or not applicable if snippets do not apply to the experiencer (e.g. family members). It
returns three files: allPos_unfiltered.txt, allNeg_unfiltered.txt, and allNA_unfiltered.txt.
In older versions of CLEVER without step 5 the three files were named allPos.txt, allNeg.txt 
and allNA.txt.

Step 5 filters out snippets with assessments from the snippets that were labelled positive or
negative and returns two files: allPos.txt and allNeg.txt.
This step also contains a script to drop snippets that are cross-tagged. Meaning, they are 
tagged for multiple targets that are related but should only be tagged for one of those 
targets. This script is not required for step 5 to run successfully and may not apply to your
use of CLEVER.
# clever-py3
