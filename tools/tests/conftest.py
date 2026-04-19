"""pytest configuration for the validator tests.

Puts the `tools/` directory on sys.path so `import validate` works.
"""
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
