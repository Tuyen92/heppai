import sqlite3
import os

conn = sqlite3.connect("D:\\talent_pool_db\\Talent_Sourcing.db")

cur = conn.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS Talent_Pool 
            (talent_id INTEGER, fullname TEXT, linkedin_link TEXT, position TEXT)''')
conn.commit()

file_path = "D:\\talent_pool_db\\Talent_Sourcing.sql"

# Kiểm tra xem tập tin có tồn tại không
if not os.path.exists(file_path):
    # Nếu không tồn tại, tạo một file mới với nội dung mặc định
    with open(file_path, 'w') as file:
        file.write("Initial content")  # Nội dung mặc định của file

# Sau đó mở file để đọc nội dung
with open(file_path) as file:
    sql_script = file.read()

talent_pool = [
  {
    "fullname": "Kevin Van Katwyk",
    "linkedin_path": "https://www.linkedin.com/in/ACoAAAMe8g4BJ0yJE3EuhEB81IDD7ryPUETVD7A",
    "position": "Principal Project Manager"
  },
  {
    "fullname": "Syam Gopalakrishnan B.E(Civil),MBA(UK)",
    "linkedin_path": "https://www.linkedin.com/in/syam-gopalakrishnan-b-e-civil-mba-uk-856348153",
    "position": "Senior Officer - Operations"
  }
]

cur.executemany('''INSERT INTO Talent_Pool (fullname, linkedin_link, position) VALUES (?, ?, ?)''', talent_pool)
conn.commit()

cur.close()
conn.close()