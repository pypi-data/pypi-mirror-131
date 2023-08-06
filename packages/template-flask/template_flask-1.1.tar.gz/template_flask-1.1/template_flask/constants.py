REQUIREMENTS = [
    'flask',
    'flask_sqlalchemy',
    'flask_login',
    'flask_mail',
    'flask_wtf',
    'flask_debugtoolbar',
    'pytest',
    'pytest_cov'
]

INDEX_HTML = [
    ['<!DOCTYPE html>', False],
    ['<html lang="en">', False],
    ['<head>', False],
    ['\t<meta charset="UTF-8">', False],
    ['\t<title>NEW PROJECT: {app}</title>', True],
    ['</head>', False],
    ['<body>', False],
    ['\t<h1>Welcome to your new project: {app}</h1>', True],
    ['\t<p><h3>Checkout the Bootstrap Templates below to add to your project</h3></p>', False],
    ['\t<p><label>The HTML, CSS AND JS for these are located in the TEMPLATES AND STATIC folders</label></p> ', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='album') }}"><b>Album</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='blog') }}"><b>Blog</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='carousel') }}"><b>Carousel</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='cheatsheet') }}"><b>Cheatsheet</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='checkout') }}"><b>Checkout</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='cover') }}"><b>Cover</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='dashboard') }}"><b>Dashboard</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='grid') }}"><b>Grid</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='headers') }}"><b>Headers</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='heroes') }}"><b>Heroes</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='jumbotron') }}"><b>Jumbotron</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='masonry') }}"><b>Masonry</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='navbars') }}"><b>Navbars</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='navbar_bottom') }}"><b>Navbar Bottom</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='navbar_top_fixed') }}"><b>Navbar Top Fixed</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='navbar_top_static') }}"><b>Navbar Top Static</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='pricing') }}"><b>Pricing</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='product') }}"><b>Product</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='sidebars') }}"><b>Sidebars</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='sign_in') }}"><b>Sign In</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='starter_template') }}"><b>Starter Template</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='sticky_footer') }}"><b>Sticky Footer</b></a></p>''', False],
    ['''\t<p><a href="{{ url_for('bootstrap', bs_page='sticky_footer_navbar') }}"><b>Sticky Footer Navbar</b></a></p>''', False],
    ['</body>', False],
    ['</html>', False]
]

CONFIG_INIT = [
    ["", False]
]

CONFIG_CONFIG = [
    ['SECRET_KEY = """{secret_key}"""', True],
    ["SQLALCHEMY_DATABASE_URI = 'sqlite:///{app}_db.db'", True],
    ["# SQLALCHEMY_DATABASE_URI = 'postgresql://<your_username>:<your_password>@<host>:<port>/<database_name>'", False],
    ["# SQLALCHEMY_DATABASE_URI = 'mysql://<your_username>:<your_password>@<host>:<port>/<database_name>", False],
    ["# SQLALCHEMY_DATABASE_URI = 'oracle://<your_username>:<your_password>@<host>:<port>/<sid_name>", False]
]

MODEL_INIT_HINT = [
    ['', False]
]

MODEL_INIT = [
    ["# IMPORT ALL MODELS AND DB TO HERE AND THEN THE MAIN __INIT__.PY WILL", False],
    ["# IMPORT * FROM HERE", False],
    ["", False],
    ["", False],
    ["from {app}_app.models.db import db", True],
    ["from {app}_app.models.model1 import Model1", True],
    ["from {app}_app.models.model2 import Model2", True]
]

MODEL_DB = [
    ["from flask_sqlalchemy import SQLAlchemy", False],
    ["", False],
    ["", False],
    ["# SHARED DATABASE FOR MODELS IN SEPARATE .PY FILES.", False],
    ["# MODELS.__INIT__.PY IMPORTS DB (AS WELL AS OTHER MODELS) AND", False],
    ["# THEN THE MAIN __INIT__.PY FOR THE APP WILL IMPORT * FROM MODELS.__INIT__.PY.", False],
    ["", False],
    ["", False],
    ["db = SQLAlchemy()", False]
]

MODEL_MODEL1 = [
    ["from datetime import datetime", False],
    ["from {app}_app.models.db import db", True],
    ["", False],
    ["", False],
    ["# CREATE CUSTOM MODEL HERE", False],
    ["# IF CREATING MORE MODELS IN SEPARATE .PY FILES GO TO MODELS.__INIT__.PY AND IMPORT THE NEW MODEL", False],
    ["# THE MAIN __INIT__.PY FOR THE APP WILL IMPORT * FROM MODELS.__INIT__.PY", False],
    ["", False],
    ["", False],
    ["class Model1(db.Model):", False],
    ["\tid = db.Column(db.Integer, primary_key=True)", False]
]

MODEL_MODEL2 = [
    ["from datetime import datetime", False],
    ["from {app}_app.models.db import db", True],
    ["", False],
    ["", False],
    ["# CREATE CUSTOM MODEL HERE", False],
    ["# IF CREATING MORE MODELS IN SEPARATE .PY FILES GO TO MODELS.__INIT__.PY AND IMPORT THE NEW MODEL", False],
    ["# THE MAIN __INIT__.PY FOR THE APP WILL IMPORT * FROM MODELS.__INIT__.PY", False],
    ["", False],
    ["", False],
    ["class Model2(db.Model):", False],
    ["\tid = db.Column(db.Integer, primary_key=True)", False]
]

ROUTE_INIT = [
    ["", False]
]

ROUTE_ROUTE = [
    ["from flask import render_template, redirect, url_for, request, session, flash", False],
    ["from {app}_app import app, db, Model1, Model2", True],
    ["", False],
    ["", False],
    ["@app.route('/', methods=['POST', 'GET'])", False],
    ["@app.route('/home', methods=['POST', 'GET'])", False],
    ["def index():", False],
    ["\tif request.method == 'POST':", False],
    ["\t\tprint(request.form)", False],
    ["\t\tprint(request.files)", False],
    ["\treturn render_template('index.html')", False],
    ["", False],
    ["", False],
    ["@app.route('/bootstrap_<bs_page>')", False],
    ["def bootstrap(bs_page):", False],
    ["\treturn render_template(f'bootstrap/{bs_page}.html')", False],
]


RUN = [
    ["from {app}_app import app", True],
    ["", False],
    ["", False],
    ["if __name__ == '__main__':", False],
    ["\tapp.run(debug=True)", False]
]

INIT = [
    ["from flask import Flask", False],
    ["# from flask_login import ()", False],
    ["# from flask_mail import ()", False],
    ["# from flask_wft import ()", False],
    ["# from flask_debugtoolbar import ()", False],
    ["from {app}_app.config.app_config import *", True],
    ["from {app}_app.models import *", True],
    ["", False],
    ["", False],
    ["app = Flask(__name__)", False],
    ["app.config['SECRET_KEY'] = SECRET_KEY", False],
    ["app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI", False],
    ["app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False", False],
    ["# app.config[''] = ''", False],
    ["# app.config[''] = ''", False],
    ["# app.config[''] = ''", False],
    ["# app.config[''] = ''", False],
    ["", False],
    ["", False],
    ["with app.app_context():", False],
    ["\tdb.init_app(app)", False],
    ["\t# db.create_all()", False],
    ["", False],
    ["", False],
    ["from {app}_app.routes import routes", True]
]

