__author__ = 'schneg'

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import csv
from contextlib import closing

from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
