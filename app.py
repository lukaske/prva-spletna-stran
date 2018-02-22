from string import ascii_lowercase
from random import randint

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import session

import baza

app = Flask(__name__)
app.secret_key = "akshfdgas"
ascii_crke = ascii_lowercase + "čžš"

@app.route("/")
def index():
    return render_template("domaca_stran.html")

@app.route("/druga_stran")
def druga():
    return render_template("druga_stran.html")

@app.route("/vislice/<znak>")
def ugibaj(znak):
    if len(znak) == 1 and znak.isalpha():
        session['ugibal'] += znak
        if znak not in session['beseda']:
            session['slika'] += 1
    for crka in session['beseda']:
        if crka not in session['ugibal']:
            break
    else:
        baza.vstavi_novo_igro(1, session['slika'], session['beseda'])
        return render_template('zmaga.html', session=session)

    return render_template(
        "vislice.html", session=session,
        vse_crke=ascii_crke)

@app.route("/vislice")
def vislice():
    session['beseda'] = "endlessness"
    with open('nove_besede.txt') as besede:
        for i in range(randint(1, 350747)):
            session['beseda'] = besede.readline().strip()
    session['slika'] = 0
    session['ugibal'] = ''
    return render_template("vislice.html", session=session, vse_crke=ascii_crke)

@app.route("/blog/<int:st_blog>")
def blog(st_blog):
    zadnji = request.cookies.get("blog_stevilka")
    result = render_template(
        "blog.html", stevilka=st_blog, prejsni=zadnji)
    result = make_response(result)
    result.set_cookie("blog_stevilka", str(st_blog))
    return result

@app.route("/lestvica")
def lestvica():
    najboljsi = baza.dobi_najboljse()
    return render_template("lestvica.html", najboljsi=najboljsi)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
