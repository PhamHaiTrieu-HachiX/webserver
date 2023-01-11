from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import psycopg2

# Generate App
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'trieu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@localhost/trieu'

if __name__ == "__main__":
  app.run(debug=True)   # Only in developement mode, not for Production



# Set up database connection
with open("info.json", "r", encoding="utf8") as ff:
    info = ff.read()
info_json = json.loads(info)
conn = psycopg2.connect(
    host= info_json["hostname"],
    port= info_json["port"],
    dbname= info_json["database"],
    user= info_json["user"],
    password= info_json["password"]
)
cursor = conn.cursor()

# Index page
@app.route('/', methods=['POST', 'GET'])
def index():
  return render_template("index.html")

# API Bank
@app.route('/bank', methods=['POST', 'GET'])
def index_bank():
  if request.method == 'POST':
    try:
        return redirect('/')
    except Exception as e:
        str_ = '<h1>There was an error with your request.</h1>\n'
        str_ += '<div><p>{}</p></div>'.format(e)
        return str_

  elif request.method == 'GET':
    datas = list()
    param = request.args
    value_ = param['search']
    query  = "SELECT * FROM public.bank"
    query += " WHERE kata_name LIKE '%{}%' OR kanji_name LIKE '%{}%'".format(value_,value_)
    query += " OR hira_name LIKE '%{}%' OR romanji_name LIKE '%{}%'".format(value_,value_)
    query += " ORDER BY id LIMIT 10"
    cursor.execute(query)
    conn.commit()
    get_datas = cursor.fetchall()
    for i in get_datas:
      datas.append(i[3])
    return datas
      
  else:
    return render_template("index.html")
    
# API Branch
@app.route('/branch', methods=['POST', 'GET'])
def index_branch():
  if request.method == 'POST':
    try:
        return redirect('/')
    except Exception as e:
        str_ = '<h1>There was an error with your request.</h1>\n'
        str_ += '<div><p>{}</p></div>'.format(e)
        return str_

  elif request.method == 'GET':
    datas = list()
    param = request.args
    value_ = param['search']
    bank_ = param['bank']

    bank_where  = "kata_name = '{}' OR kanji_name = '{}' ".format(bank_,bank_)
    bank_where += "OR hira_name = '{}' OR romanji_name = '{}'".format(bank_,bank_)
    query  = "SELECT * FROM public.branch"
    query += " WHERE (kata_name LIKE '%{}%' OR kanji_name LIKE '%{}%'".format(value_,value_)
    query += " OR hira_name LIKE '%{}%' OR romanji_name LIKE '%{}%')".format(value_,value_)
    query += " AND bank_id IN (SELECT id FROM public.bank WHERE {})".format(value_,value_)
    query += " ORDER BY id LIMIT 10"
    cursor.execute(query)
    conn.commit()
    get_datas = cursor.fetchall()
    for i in get_datas:
      datas.append(i[3])
    return datas
      
  else:
    return render_template("index.html")
