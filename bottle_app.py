import os
import sqlite3
from bottle import get, post, template, request, redirect

# are we executing at PythonAnywhere?
ON_PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ

# assert ON_PYTHONANYWHERE == True

if ON_PYTHONANYWHERE:
    # on PA, set up to connect to the WSGI server
    from bottle import default_app
else:
    # on the development environment, import the development server
    from bottle import run, debug


@get('/')
def get_movies_list():
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()
    cursor.execute("select * from movies")
    result = cursor.fetchall()
    cursor.close()
    return template("show_movies_list", rows=result)


@get("/get_add_movie_template")
def get_add_movie_template():
    return template("add_movie")


@post("/add_movie")
def add_movie_to_db():
    name = request.forms.get("name").strip()
    director = request.forms.get("director").strip()
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()
    cursor.execute(
        "insert into movies (name, director) values (?,?)", (name, director))
    connection.commit()
    cursor.close()
    redirect("/")


if ON_PYTHONANYWHERE:
    # on PA, connect to the WSGI server
    application = default_app()
else:
    # on the development environment, run the development server
    debug(True)
    run(host='localhost', port=8080)
