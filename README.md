# Testna spletna stran na krožku Gimnazije Vič

Najprej se prepričaj, da imaš nameščeno knjižnico Flask
```
sudo pip3 install flask
```

Nato kloniraj spletno stran

```
git clone https://github.com/MKolman/prva-spletna-stran
```

Potem lahko zaženeš spletno stran

```
cd prva-spletna-stran
./start_server.sh
```

# Migracija na PostgreSQL

Namesti bazo in orodje za gledanje baze
```
sudo apt-get install postgresql pgadmin3
sudo pip3 install psycopg2-binary
```

Nastavi geslo za uporabnika baze
```
sudo passwd postgres
```

Ustvari novo bazo z imenom vislice
```
sudo -u postgres createdb vislice
```

> Če uporabljaš šolski USB, moraš spremeniti nastavitve v
> ```
> sudo subl /etc/postgresql/9.5/main/pg_hba.conf
> ```
> in spremeniš vrstico
> ```
> local   all             postgres                                     peer
> ```
> tako, da `peer` zamenjas z `md5`.
> Nato se podaj v postgres z ukazom
> ```
> sudo -u postgres psql
> ```
> Kjer zaženeš ukaz
> ```
> ALTER USER postgres PASSWORD 'asuna'; \q
> ```



Prenesi novo datoteko s kodo za ravnanje z bazo.
```
wget https://raw.githubusercontent.com/MKolman/prva-spletna-stran/master/baza.py -O baza.py
```
V datoteki `baza.py` nastavi geslo in ime podatkovne baze tako da spremeniš
spremenljivko `DATABASE_URL`.

Popravi še ostale dele kode v `main.py`, da bodo delovale z novo datoteko
`baza.py`

Nato lahko ustvariš nove tabele v bazi, tako da poženeš
```
python3 baza.py
```

Bazo si lahko sedaj ogledaš z orodjem `pgAdmin`.


# Objava strani na Heroku

Heroku je platforma, ki omogoča objavo raznih aplikacij brez skrbi za delovanje
strežnika.

Najprej si naredite račun na http://www.heroku.com in si namestite heroku ukaze
z
```
wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

prijavite se v Heroku z ukazom
```
heroku login
```

## Virtualno okolje
Namestite si orodje za delanje virtualnih okolij
```
sudo apt-get install python3-virtualenv
```

Naredite si virtualno okolje z imenom `venv` in vanj vstopite
```
virtualenv venv
source venv/bin/activate
```
*Opozorilo*: Mapo `venv` dodajte v `.gitignore`, da je po nesreči ne commitate
ali pushate.

*Opomba*: Za izhod iz virtualnega okolja imate na voljo ukaz
```
deactivate
```

Sedaj si morate ponovno namestiti knjižnici (brez sudo)
```
pip install flask psycopg2-binary gunicorn
```

poglej vse nameščene knjižnice
```
pip freeze
```

shrani vse knjižnice v `requirements.txt`

```
pip freeze > requirements.txt
```

*Opomba*: Naslednjič lahko vse pakete namestiš z
```
pip install -r requirements.txt
```

## Heroku aplikacija
Naredi novo datoteko `runtime.txt` in vanjo napiši
```
python-3.6.4
```
Naredi še eno datoteko `Procfile` in vanjo napiši
```
web: gunicorn main:app --log-file=-
```

Izberi si ime aplikacije in jo ustvari (program lahko zaženeš brez imena in ti
ime izbere Heroku)
```
heroku create ime-vase-aplikacije
```

Ko imaš vse spremembe commitane jih lahko pushaš na Heroku z ukazom
```
git push heroku master
```
