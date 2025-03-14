from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
from models.jarowinklerdistance import *
from utils.preprocessing import *
from multiprocessing import Pool, cpu_count
import time

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW" 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'koreksikata'

mysql = MySQL(app)
daftar_kata = None
daftar_kata_stopword = None
pool_worker = None

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


def suggest_fix(search):
    global daftar_kata
    list_jwd_value = {}

    for word in daftar_kata:
        list_jwd_value[word] = jaroWinklerDistance(search, word)

    kata_koreksi = max(list_jwd_value, key=list_jwd_value.get)

    return kata_koreksi

def init_worker(shared_daftar_kata):
    # declare scope of a new global variable
    global daftar_kata
    # store argument in the global variable for this process
    daftar_kata = shared_daftar_kata

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
        """SELECT berita_pariwisata.* FROM keyword_berita, berita_pariwisata, daftar_kata 
        WHERE berita_pariwisata.id_berita = keyword_berita.kata_berita 
        AND daftar_kata.id_kata = keyword_berita.kata_input 
        AND daftar_kata.wordlist IN ({}) 
        GROUP BY berita_pariwisata.id_berita HAVING count(*) = {}""".format(
            ",".join(['"' + i + '"' for i in search]), len(search))
    )
    results = cursor.fetchall()
    cursor.close()
    return results


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        global pool_worker
        load_daftar_kata()
        load_daftar_kata_stopword()
        if not pool_worker:
            pool_worker = Pool(cpu_count(), init_worker, [daftar_kata])
        start = time.time()
        data = dict(request.form)
        search = data["search"]
        sugesti = []
        # search = p.map(lambda x: preprocessingtext(x, daftar_kata_stopword), list(search))
        search = [x for x in preprocessingtext(search, daftar_kata_stopword)]
        sugesti = pool_worker.map(suggest_fix, search)
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
