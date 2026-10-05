# Time-management-tool
Ajanhallinta-sovellus TKT20019 kurssia varten Helsingin yliopistolla.

- [X] Tunnuksen luonti ja kirjautuminen.
- [X] Suunnitelmien lisääminen ja poistaminen.
- [] Käyttäjä näkee sovellukseen lisätyt oletusmenot (kuten uni ja lepo).
- [] Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät menot.
- [] Käyttäjä pystyy etsimään omia ja muiden menoja hakusanalla.
- [] Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja.
- [X] Käyttäjä pystyy valitsemaan menolleen yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
- [] Käyttäjä voi "tykätä" toisen käyttäjän menoista.

# Sovelluksen asennus

Asenna "flask"-kirjasto:
```
$ pip install flask
```

Luo tietokanta:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:
```
$ flask run
```