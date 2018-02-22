import sqlite3

import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])


def naredi_povezavo():
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def ustvari_tabele():
    """ Naredi dve tabeli: Users in Scores. """
    # povezava = sqlite3.connect(IME_BAZE)
    povezava = naredi_povezavo()
    kazalec = povezava.cursor()
    kazalec.execute("CREATE TABLE Users (id int, username varchar(100))")
    kazalec.execute(
        "CREATE TABLE Scores (user_id int, napake int, beseda varchar(100))")
    povezava.commit()
    kazalec.close()
    povezava.close()


def napolni_tabele():
    """ Ustvari nekaj uporabnikov in nekaj iger. """
    from random import randint
    import uuid
    for i in range(10):
        vstavi_novega_uporabnika(i, f"Uporabnik {i}")
        for j in range(10):
            vstavi_novo_igro(i, randint(20, 100), str(uuid.uuid4()))


def dobi_najboljse():
    """ Najdi 10 iger z najmanj napakami. """
    # povezava = sqlite3.connect(IME_BAZE)
    povezava = naredi_povezavo()
    kazalec = povezava.cursor()
    kazalec.execute("""
        SELECT Users.username, Scores.napake, Scores.beseda
        FROM Scores
        JOIN Users ON Scores.user_id=Users.id
        ORDER BY Scores.napake
        """)
    return kazalec.fetchmany(10)


def vstavi_novega_uporabnika(user_id, username):
    # povezava = sqlite3.connect(IME_BAZE)
    povezava = naredi_povezavo()
    kazalec = povezava.cursor()
    kazalec.execute(
        "INSERT INTO Users VALUES (%s, %s)", (user_id, username))
    povezava.commit()
    kazalec.close()
    povezava.close()


def vstavi_novo_igro(user_id, napake, beseda):
    """ Vstavi novo igro v tabelo Scores. """
    # povezava = sqlite3.connect(IME_BAZE)
    povezava = naredi_povezavo()
    kazalec = povezava.cursor()
    kazalec.execute(
        "INSERT INTO Scores VALUES (%s, %s, %s)", (user_id, napake, beseda))
    povezava.commit()
    kazalec.close()
    povezava.close()


if __name__ == "__main__":
    # ustvari_tabele()
    napolni_tabele()
