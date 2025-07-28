from pathlib import Path
from typing import List, TypedDict


class SequencerParameters(TypedDict):
    workers: int
    right_gram: int
    left_gram: int
    snippet_length: int
    snippets: str | None
    main_targets: List[str]
    lexicon: Path
    section_headers: Path
    output_folder: Path
    notes_file: Path
