# Function to run sequencer.py (Step 2)
from pathlib import Path

from common.parameters.sequencer_parameter import SequencerParameters
from common.consts import CORPUS, HEADERS, LEXICON, OUTPUT, get_environment_var
from step2.sequencer import sequencer_main


def run_sequencer(target: str, *, workers: int = 2, dry_run: bool = False) -> bool:

    sequencer_parameters = SequencerParameters(
        workers=get_environment_var("WORKERS", int) if workers is None else workers,
        right_gram=get_environment_var("RGCONTEXT", int),
        left_gram=get_environment_var("LGCONTEXT", int),
        snippet_length=get_environment_var("SNIPPETS", int),
        main_targets=target,
        lexicon=LEXICON,
        section_headers=HEADERS,
        output_folder=Path(OUTPUT) / target,
        notes_file=CORPUS,
    )

    from common.step_runner import DirectStepRunner

    runner = DirectStepRunner(
        "sequencer", sequencer_parameters, sequencer_main, dry_run=dry_run
    )

    return runner.run()


# logging.debug(f"Processing sequencer {target}...")
# result = subprocess.run(
#     [
#         "python",
#         os.path.join(SRC_DIR, "step2", "sequencer.py"),
#         "--lexicon",
#         LEXICON,
#         "--section-headers",
#         HEADERS,
#         "--main-targets",
#         target,
#         "--snippet-length",
#         str(SNIPPETS),
#         "--snippets",
#         "--notes",
#         CORPUS,
#         "--workers",
#         str(WORKERS),
#         "--output",
#         os.path.join(OUTPUT, target),
#         "--left-gram-context",
#         str(LGCONTEXT),
#         "--right-gram-context",
#         str(RGCONTEXT),
#     ],
#     capture_output=True,
#     text=True,
# )
# logging.debug(f"STDOUT for {target} sequencer: {result.stdout}")
# if result.stderr:
#     logging.warning(f"STDERR for {target} sequencer: {result.stderr}")
