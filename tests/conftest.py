import sys
from pathlib import Path

# Ensure package under `src` is importable during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
