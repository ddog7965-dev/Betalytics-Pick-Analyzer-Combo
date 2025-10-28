import os
from dotenv import load_dotenv

load_dotenv()

RATE_LIMIT_SECONDS: float = float(os.getenv("RATE_LIMIT_SECONDS", "1.5"))
OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
START_URL: str = os.getenv("START_URL", "https://www.betalytics.com/home")
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
MAX_JSON_BODY_BYTES: int = int(os.getenv("MAX_JSON_BODY_BYTES", "200000"))  # 200 KB cap
USER_AGENT: str = os.getenv("USER_AGENT", "AVN-ResearchBot/1.0 (+https://example.com/contact)")

STORAGE_STATE: str | None = os.getenv("STORAGE_STATE") or None
