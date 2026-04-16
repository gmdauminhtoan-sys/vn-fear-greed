"""
VN Fear & Greed - Auto Push Watcher
Theo doi file CSV trong thu muc, tu dong push len GitHub khi co thay doi.
"""

import os
import time
import subprocess
import sys
from datetime import datetime

# =================== CAU HINH ===================
WATCH_DIR = r"E:\APP\vn-fear-greed"
WATCH_FILE = "csv/update.csv"
CHECK_INTERVAL = 10  # Kiem tra moi 10 giay
# =================================================

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def get_mtime(filepath):
    try:
        return os.path.getmtime(filepath)
    except FileNotFoundError:
        return None

def git_push(repo_dir, csv_file):
    """Chay git add, commit, push."""
    try:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Stage file
        subprocess.run(
            ["git", "add", csv_file],
            cwd=repo_dir, check=True, capture_output=True
        )

        # Kiem tra co thay doi de commit khong
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=repo_dir, capture_output=True
        )
        if result.returncode == 0:
            log("Khong co thay doi moi trong CSV. Bo qua push.")
            return False

        # Commit
        subprocess.run(
            ["git", "commit", "-m", f"update: market data {date_str}"],
            cwd=repo_dir, check=True, capture_output=True
        )

        # Push
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=repo_dir, check=True, capture_output=True
        )

        log("Push thanh cong! GitHub Actions dang chay build...", "OK")
        return True

    except subprocess.CalledProcessError as e:
        log(f"Loi git: {e.stderr.decode('utf-8', errors='ignore').strip()}", "LOI")
        return False

def main():
    csv_path = os.path.join(WATCH_DIR, WATCH_FILE)

    print("=" * 50)
    print("  VN Fear & Greed - Auto Push Watcher")
    print(f"  Thu muc: {WATCH_DIR}")
    print(f"  File theo doi: {WATCH_FILE}")
    print(f"  Kiem tra moi: {CHECK_INTERVAL} giay")
    print("  Nhan Ctrl+C de dung")
    print("=" * 50)
    print()

    # Kiem tra thu muc ton tai
    if not os.path.isdir(WATCH_DIR):
        log(f"Thu muc khong ton tai: {WATCH_DIR}", "LOI")
        sys.exit(1)

    last_mtime = get_mtime(csv_path)
    if last_mtime:
        log(f"Dang theo doi {WATCH_FILE} (lan sua cuoi: {datetime.fromtimestamp(last_mtime).strftime('%H:%M:%S %d/%m/%Y')})")
    else:
        log(f"Chua tim thay {WATCH_FILE}, se theo doi khi file xuat hien...")

    try:
        while True:
            current_mtime = get_mtime(csv_path)

            if current_mtime is None:
                # File chua ton tai
                time.sleep(CHECK_INTERVAL)
                continue

            if last_mtime is None or current_mtime > last_mtime:
                if last_mtime is None:
                    log(f"Phat hien file CSV moi!")
                else:
                    log(f"Phat hien thay doi trong {WATCH_FILE}!")

                # Doi 3 giay de Amibroker ghi xong file
                time.sleep(3)

                git_push(WATCH_DIR, WATCH_FILE)
                last_mtime = get_mtime(csv_path)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print()
        log("Watcher da dung. Tam biet!")

if __name__ == "__main__":
    main()
