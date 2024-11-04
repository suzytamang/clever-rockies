# CLEVER (CL-inical EVE-nt R-ecognizer)

This repo includes the Python3 version of CLEVER code from the Program Evaluation Resource Center, Office of Mental Health and Suicide Prevention, Department of Veterans Affairs.

## Development Team

### Original Development Team
- Suzanne Tamang
- Manual 
- Tanya

### Continued Development Team
- Suzanne Tamang
- Asqar Shotqara
- Esther Meerwijk

## Setup and Installation
1. Create a new Conda environment with Python 3.12:
conda create -n clever_env python=3.12

2. Activate the environment:
conda activate clever_env

3. Create an output folder.

## Important Note on Working Directory
CLEVER relies on relative file paths. Always ensure you are in the correct directory before running any scripts. Incorrect working directories will likely result in file not found errors or unexpected behavior. When in doubt, use `pwd` (print working directory) to verify your current location in the file system.

## Running CLEVER
You can run CLEVER using either the shell scripts (.sh) on a Linux system or the Python scripts (.py) in any Conda environment like the one you just created.
You must change to the appropriate directory before running the scripts. 

### Generate Targets
Before running the main steps, you need to generate all the targets:

```bash
# Change to the src directory
cd src

# Using shell script
./grabtargets.sh

# Or using Python script
python grabtargets.py

# Return to the root directory
cd ..
```

### Testing Functionality
To test functionality and provide sample input/output text files for later modification:

```bash
# Change to the tests/resources directory
cd tests/resources

# Using shell script
./run_all_steps.sh

# Or using Python script
python run_all_steps.py

# Return to the root directory
cd ../..
```

### Main Steps

Run the scripts in each of the step folders under `./src`. The scripts are provided as examples. 
Change the target concept and output folder as needed. 

Important notes:
- Make sure that scripts retain their Unix file format. DOS line endings can cause issues.
- Ensure that the scripts do not end with an empty line.

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
