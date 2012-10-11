from openpyxl.reader.excel import load_workbook
import psycopg2

import shows

wb = load_workbook(filename = r'survey.xlsx')
ws = wb.worksheets[0]

conn = psycopg2.connect("host=localhost dbname=recs user=cdsboy")

cur = conn.cursor()

def get_or_create_show(name):
  cur.execute("select show_id from shows where show_name = %s", (name,))
  result = cur.fetchone()
  if not result:
    cur.execute("insert into shows(show_name) values(%s) returning show_id",
                (name,))
    result = cur.fetchone()
  return result[0]

def get_or_create_genre(name):
  cur.execute("select genre_id from genres where genre_name = %s", (name,))
  result = cur.fetchone()
  if not result:
    cur.execute("insert into genres(genre_name) values(%s) returning genre_id",
                (name,))
    result = cur.fetchone()
  return result[0]

def get_or_create_demo(name):
  cur.execute("select demo_id from demographics where demo_name = %s", (name,))
  result = cur.fetchone()
  if not result:
    cur.execute("insert into demographics(demo_name) values(%s) returning "
                "demo_id", (name,))
    result = cur.fetchone()
  return result[0]

GENRES = ["Action", "Comedy", "Drama", "Dystopian", "Ecchi", "Fantasy", "Game",
          "Harem", "Hentai", "Horror", "Mahou Shoujo", "Mecha", "Music",
          "Mystery", "Romance", "Sci-Fi", "Slice of life", "Sports"]

for row in ws.rows:
  try:
    show_name = shows.shows[row[12].value.lower()]
    if not show_name:
      continue
  except KeyError:
    continue
  
  genre = row[7].value
  least = row[19].value
  if not genre in GENRES or not least in GENRES:
    continue

  cur.execute("insert into entries(sex, age, show_id, demo_id, fav_genre, "
              "least_genre) values(%s, %s, %s, %s, %s, %s)", (row[1].value,
                row[2].value, get_or_create_show(show_name),
                get_or_create_demo(row[6].value),
                get_or_create_genre(genre),
                get_or_create_genre(least)))

conn.commit()
cur.close()
conn.close()
