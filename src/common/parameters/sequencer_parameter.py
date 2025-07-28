from pathlib import Path
from typing import Callable, List, TypeVar, TypedDict


TargetClass = List[str] | str


class StepParameters(TypedDict):
    pass


class SequencerParameters(StepParameters):
    workers: int
    right_gram: int
    left_gram: int
    snippet_length: int
    snippets: str | None
    lexicon: Path
    section_headers: Path
    output_folder: Path
    notes_file: Path


TStepParameters = TypeVar("TStepParameters")

StepMethod = Callable[[TargetClass, TStepParameters], None]
