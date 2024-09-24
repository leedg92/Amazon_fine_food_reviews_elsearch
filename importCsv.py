import csv
import sqlite3
import warnings
from googletrans import Translator

from config import DB_PATH, CSV_PATH

warnings.filterwarnings("ignore", category=FutureWarning)

# SQLite 데이터베이스 연결
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# CSV 파일을 읽어 SQLite에 삽입 (번역 없이)
total_rows = 0
with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # 헤더 건너뛰기
    
    for row in csvreader:
        cursor.execute('''
            INSERT INTO AMAZON_FINE_FOOD_REVIEWS 
            (ID, PRODUCT_ID, USER_ID, PROFILE_NAME, HELPFULNESS_NUMERATOR, 
            HELPFULNESS_DENOMINATOR, SCORE, TIME, SUMMARY, TEXT, SUMMARY_KOR, TEXT_KOR)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row + ["", ""])  # SUMMARY_KOR와 TEXT_KOR는 빈 문자열로 초기화
        
        total_rows += 1
        if total_rows % 1000 == 0:
            conn.commit()
            print(f"{total_rows} 행 삽입 완료")

conn.commit()
print(f"총 {total_rows} 행의 데이터를 가져왔습니다.")
