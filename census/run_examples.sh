#!/bin/zsh
# usage: run_examples.sh <task> '<json list of flag keys>'
# Prints example groups behind each structural signal for one task (see examples.py).
# Run from an environment where inspect_evals is installed.
SCRIPT_DIR=${0:A:h}
python "$SCRIPT_DIR/examples.py" "inspect_evals/$1" "$2" 2>&1 | grep -v "Warning\|Generating\|Map\|Saving\|Downloading\|examples/s\|it/s" | head -40
# Optional: datasets are cached under ~/.cache/huggingface; delete what you no longer need to save disk.
