# Testing

Placeholder for testing resources.

## Resources

File-level resources for using in testing.

### Test Notes

Test notes for use in testing CLEVER

### Command-Line

#### Windows

Notes using local python environment on Windows, using git-bash.  I am using a local Anaconda environment, so I located the python.exe in that folder.  I set it to a variable to permit easier use.

```shell
export PYTHON_EXE="/x/_/Project - PERC/clever-rockies/.venv/python"

echo $PYTHON_EXE
```

> /x/_/Project - PERC/clever-rockies/.venv/python

```shell
"${PYTHON_EXE}" --version
```

> Python 3.12.3

#### Executing test notes from command line

Need to set the PYTHON_PATH to point to the ```src``` directory.

```bash
export PYTHONPATH="$(realpath ./src)"
```

The following is used to setup testing

```bash
export NOTES_PATH="$(realpath tests/resources/test_notes/test_notes.txt)"
export METADATA_PATH="$(realpath tests/resources/test_notes/test_metadata.tsv)"
export CLEVER_OUTPUT="$(realpath tests/output)"
export LEXICON_PATH="$(realpath res/dicts/dict.txt)"
export HEADERS_PATH="$(realpath res/headers.txt)"

./src/step2/step2.sh "$NOTES_PATH" "$CLEVER_OUTPUT"
cd src
export PYTHONPATH="$(realpath "$(pwd)")"

```



