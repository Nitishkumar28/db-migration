import logging
from logging.handlers import RotatingFileHandler
import uuid
import os
from datetime import datetime
import re


LOG_FILE = "migration.log"
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n")  

with open(LOG_FILE, "a", encoding="utf-8") as f:
     f.write(f"Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

RUN_ID = uuid.uuid4().hex[:8]

logger = logging.getLogger("db_migration")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "migration.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
)
fmt = "[%(asctime)s] [%(levelname)s] [%(runid)s] %(message)s"
handler.setFormatter(logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S"))

class RunIdFilter(logging.Filter):
    def filter(self, record):
        record.runid = RUN_ID
        return True

handler.addFilter(RunIdFilter())
logger.addHandler(handler)

def get_next_log_counter():
    if not os.path.exists(LOG_FILE):
        return 1
    count = 0
    pattern = re.compile(r"^Log\s+(\d+)\s+-")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if pattern.match(line):
                count += 1
    return count + 1
