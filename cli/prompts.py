from datetime import date


def prompt_text(label: str, required: bool = True) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value or not required:
            return value
        print("此欄位不可為空。")


def prompt_int(label: str) -> int:
    while True:
        value = input(f"{label}: ").strip()
        try:
            number = int(value)
            if number <= 0:
                print("請輸入大於 0 的整數。")
                continue
            return number
        except ValueError:
            print("請輸入有效的整數。")


def prompt_float(label: str) -> float:
    while True:
        value = input(f"{label}: ").strip()
        try:
            number = float(value)
            if number <= 0:
                print("請輸入大於 0 的數字。")
                continue
            return number
        except ValueError:
            print("請輸入有效的數字。")


def prompt_optional_float(label: str) -> float:
    while True:
        value = input(f"{label} (Enter 略過 = 0): ").strip()
        if not value:
            return 0.0
        try:
            number = float(value)
            if number < 0:
                print("請輸入大於等於 0 的數字。")
                continue
            return number
        except ValueError:
            print("請輸入有效的數字。")


def prompt_trade_date() -> str:
    today = date.today().isoformat()
    while True:
        value = input(f"交易日期 (YYYY-MM-DD, Enter = {today}): ").strip()
        if not value:
            return today
        if len(value) == 10 and value[4] == "-" and value[7] == "-":
            return value
        print("日期格式須為 YYYY-MM-DD。")
