# Define base paths
# Get the directory of the current script
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the parent directory
BASE_DIR = os.path.dirname(SCRIPT_DIR)
RES_DIR = os.path.join(BASE_DIR, "res")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
SRC_DIR = os.path.join(BASE_DIR, "src")
RUN_DIR = os.path.join(BASE_DIR, "run")

# Define constants
LEXICON = os.path.join(RES_DIR, "dicts", "dict.txt")
HEADERS = os.path.join(RES_DIR, "headers.txt")
ANTS = "linkedAnts.txt"
ASSESSMENTTERMS = os.path.join(RES_DIR, "assessment_terms.txt")
OTHERTERMS = os.path.join(RES_DIR, "other_terms_to_drop.txt")
NEG_TRIGS = os.path.join(RES_DIR, "neg_trigs.json")
NA_TRIGS = os.path.join(RES_DIR, "na_trigs.json")
CROSS_CLASS_FILE = os.path.join(RES_DIR, "ccf.json")
CORPUS = os.path.join(TESTS_DIR, "test_notes", "tsv", "test_notes_one_line.txt")
METADATA = os.path.join(
    TESTS_DIR, "test_notes", "metadata", "test_metadata_one_line.txt"
)
OUTPUT = os.path.join(RUN_DIR, "outputs_min")


def get_environment_var(key: str) -> str:
    assert key is not None
    env_value = os.getenv(key, None)
    if env_value is None:
        raise ValueError(f"Could not locate environment variable: {key}")
    return env_value


__all__ = [
    "SCRIPT_DIR",
    "BASE_DIR",
    "RES_DIR",
    "TESTS_DIR",
    "SRC_DIR",
    "RUN_DIR",
    "LEXICON",
    "HEADERS",
    "ANTS",
    "ASSESSMENTTERMS",
    "OTHERTERMS",
    "NEG_TRIGS",
    "NA_TRIGS",
    "CROSS_CLASS_FILE",
    "CORPUS",
    "METADATA",
    "OUTPUT",
    "get_environment_var"
]
