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

```bash
TEST_NOTES_PATH="$(realpath tests/resources/test_notes/test_notes.txt)"
OUTPUT="$(realpath tests/output)"
LEXICON_PATH="$(realpath res/dicts/dict.txt)"
HEADERS_PATH="$(realpath res/headers.txt)"

./src/step2/step2.sh "$TEST_NOTES_PATH" "$OUTPUT"

```



