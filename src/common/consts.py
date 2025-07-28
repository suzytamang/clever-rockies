# Define base paths
# Get the directory of the current script
import os
from pathlib import Path
from typing import Callable, TypeVar


TEnvCastType = TypeVar("TEnvCastType", bound=int | str | Path)


def get_environment_var(
    key: str, cast_as: Callable[[str], TEnvCastType] = str
) -> TEnvCastType:
    assert key is not None
    env_value = os.getenv(key, None)
    if env_value is None:
        raise ValueError(f"Could not locate environment variable: {key}")

    try:
        return cast_as(env_value)
    except Exception as ex:
        raise ValueError(
            "Could not case environment variable {} to type {} ({})",
            key,
            repr(cast_as),
            ex,
        )


def find_project_root(marker_files=(".gitignore", ".gitattributes", ".flake8", ".env")):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    return None


PROJECT_ROOT = find_project_root()
assert PROJECT_ROOT is not None

# paths relative to project root

# RESOURCE directory
RES_DIR = os.path.join(PROJECT_ROOT, "res")
LEXICON = Path(RES_DIR) / "dicts" / "dict.txt"
HEADERS = Path(RES_DIR) / "headers.txt"
ASSESSMENTTERMS = os.path.join(RES_DIR, "assessment_terms.txt")
OTHERTERMS = os.path.join(RES_DIR, "other_terms_to_drop.txt")
NEG_TRIGS = os.path.join(RES_DIR, "neg_trigs.json")
NA_TRIGS = os.path.join(RES_DIR, "na_trigs.json")
CROSS_CLASS_FILE = os.path.join(RES_DIR, "ccf.json")

# TESTS
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
CORPUS = Path(TESTS_DIR) / "test_notes" / "tsv" / "test_notes_one_line.txt"
METADATA = os.path.join(
    TESTS_DIR, "test_notes", "metadata", "test_metadata_one_line.txt"
)

# SOURCE
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# RUNs
RUN_DIR: Path = get_environment_var("RUN_PATH", Path)
OUTPUT = os.path.join(RUN_DIR, "outputs_min")
TARGETS_FILE = os.path.join(RUN_DIR, "unique_targets.txt")

# Define constants
ANTS = "linkedAnts.txt"


__all__ = [
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
    "TARGETS_FILE",
    "get_environment_var",
]
