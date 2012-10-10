from openpyxl.reader.excel import load_workbook
import psycopg2

import shows

wb = load_workbook(filename = r'survey.xlsx')
ws = wb.worksheets[0]

conn = psycopg2.connect("dbname=recs user=postgres")

cur = conn.cursor()

def get_or_create_show(name):
  try:
    cur.execute("insert into shows(show_name) values(%s) returning show_id",
                (name,))
  except: #lol blanket excepts are bad mmmk
    cur.execute("select show_id from shows where show_name = %s" (name,))
  return cur.fetchone()[0]

def get_or_create_genre(name):
  try:
    cur.execute("insert into genres(genre_name) values(%s) returning genre_id",
                (name,))
  except:
    cur.execute("select genre_id from genres where genre_name = %s", (name,))
  return cur.fetchone()[0]

def get_or_create_demo(name):
  try:
    cur.execute("insert into demographics(demo_name) values(%s) returning "
                "demo_id", (name,))
  except:
    cur.execute("select demo_id from demographics where demo_name = %s",
                (name,))
  return cur.fetchone()[0]

for row in ws.rows:
  try:
    show_name = shows.shows[row[12].value.lower()]
  except:
    continue
  cur.execute("insert into entries(sex, age, show_id, demo_id, fav_genre, "
              "least_genre) values(%s, %s, %s, %s, %s, %s)", (row[1].value,
                row[2].value, get_or_create_show(show_name),
                get_or_create_demo(row[6].value),
                get_or_create_genre(row[7].value),
                get_or_create_genre(row[19].value)))

conn.commit()
cur.close()
conn.close()
