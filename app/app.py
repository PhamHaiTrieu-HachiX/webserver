from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import psycopg2
from sqlalchemy.sql.expression import or_

from utils.utils import *
import inspect
import os

# Generate App
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'trieu'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@my_db:5432/trieu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@localhost:5432/trieu'


db = SQLAlchemy(app)

class Bank(db.Model):
  index = db.Column(db.Integer, primary_key= True)
  id = db.Column(db.String(25), unique= True)
  kata_name = db.Column(db.Text, default='123')
  kanji_name = db.Column(db.Text)
  hira_name = db.Column(db.Text)
  romanji_name = db.Column(db.Text)

  def index_0(self):
    primary_key= True


class Branch(db.Model):
  index = db.Column(db.Integer, primary_key= True)
  id = db.Column(db.String(25), unique= True)
  bank_id = db.Column(db.String(25))
  kata_name = db.Column(db.Text)
  kanji_name = db.Column(db.Text)
  hira_name = db.Column(db.Text)
  romanji_name = db.Column(db.Text)

  def index_0(self):
    primary_key= True


# Set up database connection
with open("info.json", "r", encoding="utf8") as ff:
  info = ff.read()
info_json = json.loads(info)

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

    get_datas = select_broad(Bank, value_=value_, limit=10)
    to_log("Bank data: ", "bank")
    to_log(get_datas, "bank")
    for i in get_datas:
      datas.append(i['kanji_name'])
    return datas
      
  else:
    return render_template("index.html")
    
# API Branch
@app.route('/branch', methods=['POST', 'GET'])
def index_branch():
  # conn = psycopg2.connect(
  #     host= info_json["hostname"],
  #     port= info_json["port"],
  #     dbname= info_json["database"],
  #     user= info_json["user"],
  #     password= info_json["password"]
  # )
  # cursor = conn.cursor()
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
    branch_ = param['search']
    bank_ = param['bank']

    # bank_where  = "kata_name = '{}' OR kanji_name = '{}' ".format(bank_,bank_)
    # bank_where += "OR hira_name = '{}' OR romanji_name = '{}'".format(bank_,bank_)
    # query  = "SELECT * FROM public.branch"
    # query += " WHERE (kata_name LIKE '%{}%' OR kanji_name LIKE '%{}%'".format(value_,value_)
    # query += " OR hira_name LIKE '%{}%' OR romanji_name LIKE '%{}%')".format(value_,value_)
    # query += " AND bank_id IN (SELECT id FROM public.bank WHERE {})".format(bank_where)
    # query += " ORDER BY id LIMIT 10"
    # cursor.execute(query)
    # conn.commit()
    # get_datas = cursor.fetchall()
    # conn.close()
    # for i in get_datas:
    #   datas.append(i[3])
    
    get_datas = select_broad(Branch, value_=branch_)
    where_bank = {
      "kanji_name": bank_
    }
    # to_log("Branch data: ", "branch")
    get_bank = select_precise(Bank, where_bank)
    to_log("get_bank: ", "branch")
    to_log(get_bank, "branch")
    bank_ids = [str(i["id"]) for i in get_bank]
    # to_log(bank_ids, "branch")
    get_branch = get_list_from_list_by_field(get_datas, "bank_id", bank_ids)
    # to_log(get_branch, "branch")
    for i in get_branch:
      datas.append(i['kanji_name'])
    return datas
  
  else:
    return render_template("index.html")


######################### Start Flask Sqlalchemy utilities #########################

def select_broad(model_= None, value_= '', limit=None):
  if not model_:
    return False
  
  columns = get_columns(model_, primary_key=False)
  query = db.session.query(model_).filter(or_(*[getattr(model_,column).like(f"%{value_}%") for column in columns])).limit(limit)

  return [i.__dict__ for i in query]

def select_precise(model_= None, data_= dict()):
  if not data_ or not model_:
    return False
  
  query = None
  for k, v in data_.items():
    if not query:
      query = db.session.query(model_).filter(getattr(model_,k) == str(v))
    else:
      query = query.filter(getattr(model_,k) == str(v))

  return [i.__dict__ for i in query]

def get_columns(model_, primary_key=True):
  if primary_key == True:
    columns = [b[0] for b in inspect.getmembers(model_()) if (not b[0].startswith("_") and b[1] == None)]
  else:
    columns = [b[0] for b in inspect.getmembers(model_()) if (not b[0].startswith("_") and (b[1] == None or inspect.ismethod(b[1])))]
    prim = list()
    for col in columns:
      if col[-2] == '_' and col[-1] == '0':
        prim.append(col.strip('_0'))
        prim.append(col)
    if prim:
      a = [b for b in columns if b not in prim]
      return a
  return columns

######################### End Flask Sqlalchemy utilities #########################


if __name__ == "__main__":
  # Only run debug=True in developement mode, not for Production
  app.run(port=5000, host="0.0.0.0",debug=True)
