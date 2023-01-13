from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import or_

data_ = {
  "romanji_name": "mitsui",
  "id": "0009"
}

or_expression = or_(*["0009" == item for key, item in data_.items()])
yield(or_expression)

a == b | c == d | e == f