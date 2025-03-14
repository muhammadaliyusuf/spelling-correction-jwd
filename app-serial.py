from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_mysqldb import MySQL
from models.jarowinklerdistance import *
from utils.preprocessing import *
import time
# from math import floor, ceil

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'koreksikata'

mysql = MySQL(app)
daftar_kata = None
daftar_kata_stopword = None
nama_tempat = None


def load_daftar_kata():
    global daftar_kata
    if daftar_kata is not None:
        return

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM daftar_kata")
    daftar_kata = [x[1] for x in cur.fetchall()]


def load_daftar_kata_stopword():
    global daftar_kata_stopword
    if daftar_kata_stopword is not None:
        return

    cur = mysql.connection.cursor()
    cur.execute("SELECT stopword_wordlist FROM kata_stopword")
    daftar_kata_stopword = [x[0] for x in cur.fetchall()]


def load_nama_tempat():
    global nama_tempat
    if nama_tempat is not None:
        return

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM nama_tempat")
    nama_tempat = [x[1] for x in cur.fetchall()]


def suggest_fix(search):
    list_jwd_value = {}

    for word in daftar_kata:
        list_jwd_value[word] = jaroWinklerDistance(search, word)

    kata_koreksi = max(list_jwd_value, key=list_jwd_value.get)

    return kata_koreksi


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM berita_pariwisata")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', beritapariwisata=data)


def getberita(search: list[str]):
    cursor = mysql.connection.cursor()
    cursor.execute(
        # "SELECT * FROM berita_pariwisata WHERE judul LIKE '{}%'".format(
        #     "%"+search+"%")
        "SELECT berita_pariwisata.* FROM keyword_berita, berita_pariwisata, daftar_kata WHERE berita_pariwisata.id_berita = keyword_berita.kata_berita AND daftar_kata.id_kata = keyword_berita.kata_input AND daftar_kata.wordlist IN ({}) GROUP BY berita_pariwisata.id_berita HAVING count(*) = {}".format(
            ",".join(['"' + i + '"' for i in search]), len(search))
    )
    results = cursor.fetchall()
    cursor.close()
    return results


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        start = time.time()
        load_daftar_kata()
        load_daftar_kata_stopword()
        load_nama_tempat()
        data = dict(request.form)
        search = data["search"]
        search = [x if x.isalpha()
                else x for x in preprocessingtext(search, daftar_kata_stopword)]
        sugesti = [suggest_fix(x) for x in search]
        berita = getberita(search)
        session["search"] = ' '.join(search)
        sugesti = ' '.join(sugesti)
        end = time.time()
        waktu = round(end-start,2)
        
    else:
        berita = []

    return render_template("result.html", hasilcari=berita, search=session["search"], waktu=waktu, sugesti=sugesti)


if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/index', defaults={'page_num': 1})
# @app.route('/index/page_num/<int:page_num>')
# def employees(page_num):
#     per_page = 20
#     startat = page_num*per_page
#     db = mysql.connect('localhost', 'root', 'password', 'koreksikata')
#     cursor = db.cursor()
#     cursor.execute(
#         'SELECT * FROM berita_pariwisata limit %s, %s;', (startat, per_page))
#     employees = list(cursor.fetchall())
#     return render_template('index.html', employees=employees)
