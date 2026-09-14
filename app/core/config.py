"""Central application paths and constants."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
LOG_FILE = BASE_DIR / "app.log"
USERS_FILE = DATA_DIR / "users.json"
STUDENTS_FILE = DATA_DIR / "students.json"
COURSES_FILE = DATA_DIR / "courses.json"

def ensure_data_files() -> None:
    """Create the data directory and empty JSON files when needed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for file_path in (USERS_FILE, STUDENTS_FILE, COURSES_FILE):
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")
