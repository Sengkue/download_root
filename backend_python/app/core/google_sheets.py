import json
from pathlib import Path
from datetime import datetime, timezone
import gspread
from google.oauth2.service_account import Credentials

from app.core.config import GOOGLE_SHEET_ID, GOOGLE_CLIENT_EMAIL, GOOGLE_PRIVATE_KEY, ROOT_DIR, PROJECT_DIR

spreadsheet = None
is_connected = False

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def connect_google_sheets():
    global spreadsheet, is_connected
    try:
        sheet_id = GOOGLE_SHEET_ID
        client_email = GOOGLE_CLIENT_EMAIL
        private_key = GOOGLE_PRIVATE_KEY

        if not client_email or not private_key:
            creds_path = PROJECT_DIR / "google-credentials.json"
            if not creds_path.exists():
                creds_path = ROOT_DIR / "backend" / "google-credentials.json"
            if not creds_path.exists():
                print("Google credentials not found in .env or google-credentials.json. Falling back to SQLite.")
                return False
            with open(creds_path, "r", encoding="utf-8") as f:
                creds_info = json.load(f)
        else:
            creds_info = {
                "type": "service_account",
                "client_email": client_email,
                "private_key": private_key.replace("\\n", "\n"),
                "token_uri": "https://oauth2.googleapis.com/token"
            }

        credentials = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        if not sheet_id:
            print("GOOGLE_SHEET_ID not provided.")
            return False

        spreadsheet = gc.open_by_key(sheet_id)
        is_connected = True
        print(f"[OK] Connected to Google Sheet: {spreadsheet.title}")

        # Setup TypingLessons worksheet
        try:
            worksheets = {ws.title: ws for ws in spreadsheet.worksheets()}
            if "TypingLessons" not in worksheets:
                ws = spreadsheet.add_worksheet(title="TypingLessons", rows=100, cols=10)
                ws.append_row(["LessonID", "Title", "Content"])
                ws.append_rows([
                    ["1", "ບົດຮຽນທີ 1: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຊ້າຍ (ກ ດ ເ)", "ກດເ ກດ ເດກ ກເ ດກ ດເ ກເດ ດເດ ກກເ ກດເ ດກເ ເດກ ກກດ ເເດ ກເດ"],
                    ["2", "ບົດຮຽນທີ 2: ນິ້ວຊີ້ ແລະ ນິ້ວກາງຂວາ (້ ່ າ)", "້າ ່້ ່າ້ ້່າ ່່າ ້າ່ ້່ າ້ າ່ ້້່ ່້າ ້່າ າ້່ ່່າ"],
                    ["3", "ບົດຮຽນທີ 3: ປະສົມນິ້ວຊີ້-ກາງ (Home Row Core)", "ກ້າ ດ່ ເກ ດາ ເ້ ກ່ ດ້ ດ່າ ເກ້ ກດາ ເ່າ ດກ້ ເ້າ ກດ່ ດ່າ ເ້ກ"],
                    ["4", "ບົດຮຽນທີ 4: ນິ້ວນາງ ແລະ ນິ້ວກ້ອຍ (ັ ຫ ສ ວ ງ)", "ຫສ ວງ ັສ ກວ ຫງ ດສ ເວ ຫກ ດວ ສງ ັວ ຫສ ດງ ກສ ເຫ ວັ"],
                    ["5", "ບົດຮຽນທີ 5: ເອື້ອມນິ້ວແຖວເທິງ (ພ ະ ິ ີ ຮ ນ)", "ພະ ິີ ຮນ ຍບ ລພ ະິ ີຮ ນຍ ບລ ພິ ະຍ ະຮ ນບ ລີ ພບ ລນ ຍຮ"],
                    ["6", "ບົດຮຽນທີ 6: ປະສົມພະຍັນຊະນະ ແລະ ສະຫຼະ", "ກະ ກາ ກິ ກີ ກຶ ກື ກຸ ກູ ຂະ ຂາ ຂິ ຂີ ຂຶ ຂື ຂຸ ຂູ"]
                ])
                print("[OK] Created TypingLessons sheet with default Lao lessons.")

            if "TypingResults" not in worksheets:
                ws = spreadsheet.add_worksheet(title="TypingResults", rows=500, cols=10)
                ws.append_row(["Date", "Username", "LessonTitle", "WPM", "CPM", "Accuracy", "TimeSeconds"])
                print("[OK] Created TypingResults sheet.")

            if "LearningVideos" not in worksheets:
                ws = spreadsheet.add_worksheet(title="LearningVideos", rows=100, cols=10)
                ws.append_row(["ID", "Category", "Title", "Flag", "Description", "VideoURL", "FlipbookURL"])
                ws.append_rows([
                    ["h1", "hmong", "Hmong Interactive Book", "📖", "Read and learn through our interactive Hmong flipbook experience.", "", "https://online.fliphtml5.com/dbsyx/qcqw/"],
                    ["h2", "hmong-video", "Video Learning", "▶️", "Watch expert advice and pronunciation guides directly from YouTube.", "https://www.youtube.com/embed/s8pboIhSURc", ""],
                    ["h3", "hmong", "Advanced Grammar", "H", "Deep dive into sentence structures and complex modifiers.", "", ""],
                    ["l1", "lao", "Lao Consonants", "🇱🇦", "Master the Lao alphabet consonants and their classes.", "", ""],
                    ["l2", "lao", "Vowels & Tones", "🇱🇦", "Understand how vowels interact with consonants and tone marks.", "", ""],
                    ["e1", "english", "Grammar Essentials", "🇬🇧", "Build a strong foundation with English tenses and parts of speech.", "", ""]
                ])
                print("[OK] Created LearningVideos sheet with default courses.")
        except Exception as sheet_err:
            print(f"[WARN] Could not setup Typing Test sheets: {sheet_err}")

        return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Google Sheets: {e}")
        is_connected = False
        return False

# Webview Links
def get_google_sheet_links():
    if not is_connected or not spreadsheet:
        return None
    try:
        sheet = spreadsheet.get_worksheet(0)
        records = sheet.get_all_records()
        return [{"id": idx, "title": r.get("Title", ""), "url": r.get("URL", "")} for idx, r in enumerate(records)]
    except Exception as e:
        print(f"Error reading links sheet: {e}")
        return None

def add_google_sheet_link(title: str, url: str):
    if not is_connected or not spreadsheet:
        return None
    try:
        sheet = spreadsheet.get_worksheet(0)
        sheet.append_row([title, url])
        records = sheet.get_all_records()
        return {"id": len(records) - 1, "title": title, "url": url}
    except Exception as e:
        print(f"Error adding sheet link: {e}")
        return None

def update_google_sheet_link(index_id: int, title: str, url: str):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.get_worksheet(0)
        row_num = int(index_id) + 2
        sheet.update(f"A{row_num}:B{row_num}", [[title, url]])
        return True
    except Exception as e:
        print(f"Error updating sheet link: {e}")
        return False

def delete_google_sheet_link(index_id: int):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.get_worksheet(0)
        row_num = int(index_id) + 2
        sheet.delete_rows(row_num)
        return True
    except Exception as e:
        print(f"Error deleting sheet link: {e}")
        return False

# Typing Lessons
def get_typing_lessons():
    if not is_connected or not spreadsheet:
        return []
    try:
        sheet = spreadsheet.worksheet("TypingLessons")
        records = sheet.get_all_records()
        return [{"id": str(r.get("LessonID", "")), "title": r.get("Title", ""), "content": r.get("Content", "")} for r in records]
    except Exception as e:
        print(f"Error get_typing_lessons: {e}")
        return []

def add_typing_lesson(title: str, content: str):
    if not is_connected or not spreadsheet:
        return None
    try:
        sheet = spreadsheet.worksheet("TypingLessons")
        records = sheet.get_all_records()
        next_id = "1"
        if records:
            last_id = records[-1].get("LessonID", 0)
            try:
                next_id = str(int(last_id) + 1)
            except ValueError:
                next_id = str(len(records) + 1)
        sheet.append_row([next_id, title, content])
        return {"id": next_id, "title": title, "content": content}
    except Exception as e:
        print(f"Error add_typing_lesson: {e}")
        return None

def update_typing_lesson(lesson_id: str, title: str, content: str):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.worksheet("TypingLessons")
        records = sheet.get_all_records()
        for idx, r in enumerate(records):
            if str(r.get("LessonID", "")) == str(lesson_id):
                row_num = idx + 2
                sheet.update(f"B{row_num}:C{row_num}", [[title, content]])
                return True
        return False
    except Exception as e:
        print(f"Error update_typing_lesson: {e}")
        return False

def delete_typing_lesson(lesson_id: str):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.worksheet("TypingLessons")
        records = sheet.get_all_records()
        for idx, r in enumerate(records):
            if str(r.get("LessonID", "")) == str(lesson_id):
                row_num = idx + 2
                sheet.delete_rows(row_num)
                return True
        return False
    except Exception as e:
        print(f"Error delete_typing_lesson: {e}")
        return False

# Typing Results & Leaderboard
def save_typing_result(username: str, lesson_title: str, cpm: int, wpm: int, accuracy: float, time_seconds: str):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.worksheet("TypingResults")
        date_str = datetime.now(timezone.utc).isoformat()
        sheet.append_row([date_str, username or "Anonymous", lesson_title, wpm, cpm, accuracy, time_seconds or ""])
        return True
    except Exception as e:
        print(f"Error save_typing_result: {e}")
        return False

def get_typing_leaderboard(lesson_title: str = None):
    if not is_connected or not spreadsheet:
        return []
    try:
        sheet = spreadsheet.worksheet("TypingResults")
        records = sheet.get_all_records()
        results = []
        for idx, r in enumerate(records):
            uname = r.get("Username") or r.get("User") or "Anonymous"
            lt = r.get("LessonTitle") or ""
            try:
                wpm_val = float(r.get("WPM") or 0)
            except (ValueError, TypeError):
                wpm_val = 0
            try:
                cpm_val = float(r.get("CPM") or 0)
            except (ValueError, TypeError):
                cpm_val = 0
            try:
                acc_val = float(r.get("Accuracy") or 0)
            except (ValueError, TypeError):
                acc_val = 0

            results.append({
                "id": idx + 1,
                "date": str(r.get("Date") or ""),
                "username": uname,
                "lessonTitle": lt,
                "wpm": wpm_val,
                "cpm": cpm_val,
                "accuracy": acc_val,
                "timeSeconds": str(r.get("TimeSeconds") or "")
            })

        if lesson_title and lesson_title != "All":
            results = [r for r in results if r["lessonTitle"] == lesson_title]

        results.sort(key=lambda x: (x["wpm"], x["accuracy"]), reverse=True)
        return [{"rank": idx + 1, **item} for idx, item in enumerate(results)]
    except Exception as e:
        print(f"Error get_typing_leaderboard: {e}")
        return []

# Learning Videos
def get_learning_videos():
    if not is_connected or not spreadsheet:
        return []
    try:
        sheet = spreadsheet.worksheet("LearningVideos")
        records = sheet.get_all_records()
        return [{
            "id": str(r.get("ID", "")),
            "category": r.get("Category", ""),
            "title": r.get("Title", ""),
            "flag": r.get("Flag", "▶️"),
            "description": r.get("Description", ""),
            "videoUrl": r.get("VideoURL", ""),
            "flipbookUrl": r.get("FlipbookURL", "")
        } for r in records]
    except Exception as e:
        print(f"Error get_learning_videos: {e}")
        return []

def add_learning_video(data: dict):
    if not is_connected or not spreadsheet:
        return None
    try:
        sheet = spreadsheet.worksheet("LearningVideos")
        new_id = data.get("id") or f"v_{int(datetime.now().timestamp() * 1000)}"
        sheet.append_row([
            new_id,
            data.get("category", ""),
            data.get("title", ""),
            data.get("flag", "▶️"),
            data.get("description", ""),
            data.get("videoUrl", ""),
            data.get("flipbookUrl", "")
        ])
        return {**data, "id": new_id}
    except Exception as e:
        print(f"Error add_learning_video: {e}")
        return None

def update_learning_video(video_id: str, data: dict):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.worksheet("LearningVideos")
        records = sheet.get_all_records()
        for idx, r in enumerate(records):
            if str(r.get("ID", "")) == str(video_id):
                row_num = idx + 2
                cat = data.get("category", r.get("Category", ""))
                title = data.get("title", r.get("Title", ""))
                flag = data.get("flag", r.get("Flag", "▶️"))
                desc = data.get("description", r.get("Description", ""))
                v_url = data.get("videoUrl", r.get("VideoURL", ""))
                fb_url = data.get("flipbookUrl", r.get("FlipbookURL", ""))
                sheet.update(f"B{row_num}:G{row_num}", [[cat, title, flag, desc, v_url, fb_url]])
                return True
        return False
    except Exception as e:
        print(f"Error update_learning_video: {e}")
        return False

def delete_learning_video(video_id: str):
    if not is_connected or not spreadsheet:
        return False
    try:
        sheet = spreadsheet.worksheet("LearningVideos")
        records = sheet.get_all_records()
        for idx, r in enumerate(records):
            if str(r.get("ID", "")) == str(video_id):
                row_num = idx + 2
                sheet.delete_rows(row_num)
                return True
        return False
    except Exception as e:
        print(f"Error delete_learning_video: {e}")
        return False
