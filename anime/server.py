from flask import Flask, jsonify, render_template, request
import psycopg2

app = Flask(__name__)

@app.route('/ajax/search')
def search():
  print "searching"
  conn = psycopg2.connect("host=localhost dbname=recs user=cdsboy")
  cur = conn.cursor()

  genres = request.args.get('genres', None)
  if genres:
    genres = tuple([int(genre) for genre in genres.split(",")])
  leasts = request.args.get('leasts', None)
  if leasts:
    leasts = tuple([int(genre) for genre in leasts.split(",")])
  sex = request.args.get('sex', None)
  age = request.args.get('age', None)
  demo = request.args.get('demo', None, type=int)

  qry = ("select show.show_name, count(entry.entry_id) "
         "from entries entry, shows show "
         "where entry.show_id = show.show_id ")
  args = []

  if genres:
    qry += "and entry.fav_genre in %s "
    args.append(genres)
  if leasts:
    qry += "and entry.least_genre in %s "
    args.append(leasts)
  if age:
    qry += "and entry.age = %s "
    args.append(age)
  if sex:
    qry += "and entry.sex = %s "
    args.append(sex)
  if demo:
    qry += "and entry.demo_id = %s "
    args.append(demo)

  qry += "group by show.show_name order by count desc"
  print cur.mogrify(qry, args)

  cur.execute(qry, args)
  result = cur.fetchall()

  cur.close()
  conn.close()

  return jsonify(result=result)

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0')
