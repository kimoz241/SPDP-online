from flask.ext.mysqldb import MySQL
from flask import Flask, render_template, url_for, redirect, request, session
from werkzeug import secure_filename
import netifaces as ni
import time
import datetime
import os, random


app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='ta_spdp'

app.config['UPLOAD_PP'] = 'static/img/profile/'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg'])

mysql = MySQL(app)
global alip
alip =""
ni.ifaddresses('lo')
alip = ni.ifaddresses('lo')[2][0]['addr']


@app.route('/')
def index():
    if 'username' in session:
        username_session = session['username']
        if session['level_akses'] == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s",[str(username_session)])
            rows =cur.fetchall()

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM profil_kapolsek")
            rowskapolsek =cur.fetchall()
            return render_template('insert_spdp.html',rows=rows, rowskapolsek=rowskapolsek, session_user_name=username_session, leve_akses=session['level_akses'])
        elif session['level_akses'] == 2:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s",[str(username_session)])
            rows =cur.fetchall()
            return render_template('dashboard_admin.html',rows=rows, session_user_name=username_session, leve_akses=session['level_akses'])
        elif session['level_akses'] == 3:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s",[str(username_session)])
            rows =cur.fetchall()
            return render_template('dashboard_jaksa.html',rows=rows, session_user_name=username_session, leve_akses=session['level_akses'])
        else:
            return render_template('index_mysql.html')
    else:
        return render_template('signin.html')
#
# @app.route('/pengajuan')
# def pengajuan():
#     return render_template('pengajuan_spdp.html')

@app.route('/user')
def user():
    return render_template('dashboard_user.html')

@app.route('/profile')
def profile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profil_kapolsek")
    rows =cur.fetchall()
    return render_template('profile.html', rows = rows)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_pp/<pp>', methods=['GET','POST'])
def upload_pp(pp):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PP'], filename))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE profil_kapolsek SET photo_profile=%s WHERE nrp_kapolsek=%s", (filename,pp))
        mysql.connection.commit()
        return redirect(url_for('profile'))

@app.route('/upload_ttd/<ttd>', methods=['GET','POST'])
def upload_ttd(ttd):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PP'], filename))
        cur = mysql.connection.cursor()
        cur.execute("UPDATE profil_kapolsek SET photo_ttd=%s WHERE nrp_kapolsek=%s", (filename,ttd))
        mysql.connection.commit()
        return redirect(url_for('profile'))


@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    if request.method == 'POST':
        nrp_kapolsek = request.form['nrp_kapolsek']
        nama_kapolsek = request.form['nama_kapolsek']
        jabatan_kapolsek = request.form['jabatan_kapolsek']
        alamat_kapolsek = request.form['alamat_kapolsek']
        tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE profil_kapolsek SET nrp_kapolsek=%s, nama_kapolsek=%s, jabatan_kapolsek=%s, alamat_kapolsek=%s, tempat_tanggal_lahir=%s WHERE kode=%s", (nrp_kapolsek,nama_kapolsek,jabatan_kapolsek,alamat_kapolsek,tempat_tanggal_lahir,1))
        mysql.connection.commit()
        return redirect(url_for('profile'))



@app.route('/send')
def send():
    return render_template('send.html')


@app.route('/spdp')
def spdp():
    return render_template('coba.html')

@app.route('/alldata')
def alldata():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp  order by tanggal DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('alldata.html', rows = rows)

@app.route('/percobaan')
def percobaan():
    return render_template('percobaan2.html')

@app.route('/simpan')
def simpan():
    return render_template('simpan.html')

@app.route('/insert_spdp')
def insert_spdp():
    return render_template('insert_spdp.html')


@app.route('/admin')
def admin():
    return render_template('dashboard_admin.html')

@app.route('/modal')
def modal():
    return render_template('fariz_modal.html')

# @app.route('/form_spdp/<int:no_sprint>', methods=['GET' , 'POST'])
# def form_spdp(no_sprint):
#     cur = mysql.connection.cursor()
#     # cur.execute("SELECT * FROM spdp")
#     cur.execute("SELECT a.no_sprint, a.no_laporan, a.no_pol, a.nama_tsk, a.gender, a.tempat_lahir, a.tanggal_lahir, a.pekerjaan, a.agama, a.kewarganegaraan, a.alamat, a.kategori, a.pasal, a.tanggal, a.tampil_tgl, a.kapolsek, a.nrp, b.nrp, b.nm_penyidik, b.jbt_penyidik FROM spdp a INNER JOIN det_penyidik b ON a.no_sprint= b.no_sprint  WHERE a.no_sprint=%s;",[str(no_sprint)])
#
#     rows =cur.fetchall()
#     #return str(rows)
#     return render_template('f_spdp.html', rows = rows)

@app.route('/form_spdp/<int:no_sprint>', methods=['GET' , 'POST'])
def form_spdp(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp WHERE no_sprint=%s",[str(no_sprint)])
    rows =cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM det_penyidik WHERE no_sprint=%s",[str(no_sprint)])
    rowspenyidik =cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profil_kapolsek")
    rowskapolsek =cur.fetchall()

    return render_template('f_spdp.html',rows=rows,rowspenyidik=rowspenyidik,rowskapolsek=rowskapolsek)


@app.route('/pengajuan/<int:no_sprint>', methods=['GET' , 'POST'])
def pengajuan(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp WHERE no_sprint=%s",[str(no_sprint)])
    rows =cur.fetchall()


    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profil_kapolsek")
    rowskapolsek =cur.fetchall()

    return render_template('pengajuan_spdp.html',rows=rows,rowskapolsek=rowskapolsek)


@app.route('/surat_SPDP')
def surat_SPDP():
    return render_template('surat_SPDP.html')

@app.route('/aktivitas')
def aktivitas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM logaktivitas order by tgl_aktivitas DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('logaktivitas.html', rows = rows)

@app.route('/status')
def status():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM status order by tgl_terkirim DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('status.html', rows = rows)


@app.route('/simpanspdp', methods=['GET' , 'POST'])
def simpanspdp():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        nama1 = request.form['nama1']
        pangkat1 = request.form['pangkat1']
        jabatan1 = request.form['jabatan1']
        nama2 = request.form['nama2']
        pangkat2 = request.form['pangkat2']
        jabatan2 = request.form['jabatan2']
        nama3 = request.form['nama3']
        pangkat3 = request.form['pangkat3']
        jabatan3 = request.form['jabatan3']
        nama4 = request.form['nama4']
        pangkat4 = request.form['pangkat4']
        jabatan4 = request.form['jabatan4']
        penerima = request.form['penerima']


        tglsaiki = time.time()
        tmpltgl = time.time()

        kapolsek = request.form['kapolsek']
        nrp = request.form['nrp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pembuatanspdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,nama1,pangkat1,jabatan1,nama2,pangkat2,jabatan2,nama3,pangkat3,jabatan3,nama4,pangkat4,jabatan4,penerima,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,nama1,pangkat1,jabatan1,nama2,pangkat2,jabatan2,nama3,pangkat3,jabatan3,nama4,pangkat4,jabatan4,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(tglsaiki)),time.strftime("%d-%m-%Y", time.gmtime(tmpltgl)),kapolsek,nrp))
        mysql.connection.commit()

        skrg = time.time()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO logaktivitas VALUES(%s,%s,%s,%s,%s)",(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(skrg)),"Polsek Candi",alip,"Create",no_sprint))
        mysql.connection.commit()
        return redirect(url_for('dataspdp',no_pol=no_pol))

# @app.route('/savespdp', methods=['GET' , 'POST'])
# def savespdp():
#     if request.method == 'POST':
#         no_sprint = request.form['no_sprint']
#         no_laporan = request.form['no_laporan']
#         no_pol = request.form['no_pol']
#         nama_tsk = request.form['nama_tsk']
#         gender = request.form['gender']
#         tempat_lahir = request.form['tempat_lahir']
#         tanggal_lahir = request.form['tanggal_lahir']
#         pekerjaan = request.form['pekerjaan']
#         agama = request.form['agama']
#         kewarganegaraan = request.form['kewarganegaraan']
#         alamat = request.form['alamat']
#         kategori = request.form['kategori']
#         pasal = request.form['pasal']
#
#         penerima = request.form['penerima']
#
#
#         tglsaiki = time.time()
#         tmpltgl = time.time()
#
#         kapolsek = request.form['kapolsek']
#         nrp = request.form['nrp']
#
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO spdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(tglsaiki)),time.strftime("%d-%m-%Y", time.gmtime(tmpltgl)),kapolsek,nrp))
#         mysql.connection.commit()
#
#         # cur = mysql.connection.cursor()
#         # cur.execute("INSERT INTO pembuatanspdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(tglsaiki)),time.strftime("%d-%m-%Y", time.gmtime(tmpltgl)),kapolsek,nrp))
#         # mysql.connection.commit()
#
#         skrg = time.time()
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO logaktivitas VALUES(%s,%s,%s,%s,%s)",(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(skrg)),"Polsek Candi",alip,"Create",no_sprint))
#         mysql.connection.commit()
#         return redirect(url_for('dataspdp',no_sprint=no_sprint))

@app.route('/save_spdp', methods=['GET' , 'POST'])
def save_spdp():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']




        tglsaiki = time.time()
        tmpltgl = time.time()

        kapolsek = request.form['kapolsek']
        nrp = request.form['nrp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO spdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(tglsaiki)),time.strftime("%d-%m-%Y", time.gmtime(tmpltgl)),kapolsek,nrp))
        mysql.connection.commit()

        skrg = time.time()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO logaktivitas VALUES(%s,%s,%s,%s,%s)",(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(skrg)),"Polsek Candi",alip,"Create",no_sprint))
        mysql.connection.commit()
        return redirect(url_for('dataspdp',no_sprint=no_sprint))

@app.route('/insertpenyidik/<int:no_sprint>', methods=['GET' , 'POST'])
def insertpenyidik(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp WHERE no_sprint=%s",[str(no_sprint)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('insert_penyidik.html', rows = rows)

@app.route('/dataspdp/<int:no_sprint>', methods=['GET' , 'POST'])
def dataspdp(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp WHERE no_sprint=%s",[str(no_sprint)])
    # cur.execute("SELECT a.no_sprint, a.no_laporan, a.no_pol, a.nama_tsk, a.gender, a.tempat_lahir, a.tanggal_lahir, a.pekerjaan, a.agama, a.kewarganegaraan, a.alamat, a.kategori, a.pasal, a.tanggal, a.tampil_tgl, a.kapolsek, a.nrp, b.nrp, b.nm_penyidik, b.jbt_penyidik FROM spdp a INNER JOIN det_penyidik b ON a.no_sprint= b.no_sprint  WHERE a.no_sprint=%s;",[str(no_sprint)])

    rows =cur.fetchall()
    #return str(rows)
    return render_template('dataspdp_user.html', rows = rows)


@app.route('/success', methods=['GET' , 'POST'])
def success():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        penerima = request.form['penerima']


        saiki = time.time()

        tampil_tgl = request.form['tampil_tgl']
        kapolsek = request.form['kapolsek']
        nrp = request.form['nrp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notifspdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(saiki)),tampil_tgl,kapolsek,nrp))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO status (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_terkirim, tgl_cek, keterangan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint, no_laporan, no_pol ,nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(saiki)),"","ON PROCESS"))
        mysql.connection.commit()
        return render_template('send.html')


@app.route('/editspdp', methods=['GET' , 'POST'])
def editspdp():
    no_pol = request.form['no_pol']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pembuatanspdp WHERE no_pol=%s",[str(no_pol)])
    rows =cur.fetchall()

    return render_template('edit_spdp.html', rows = rows)




@app.route('/godelete', methods=['GET' , 'POST'])
def godelete():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']

        jamskrg = time.time()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO logaktivitas VALUES(%s,%s,%s,%s,%s)",(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(jamskrg)),"Polsek Candi",alip,"Delete",no_sprint))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM pembuatanspdp WHERE no_sprint=(%s)",[no_sprint])
        mysql.connection.commit()
        return redirect(url_for('alldata'))

@app.route('/updatespdp', methods=['GET','POST'])
def updatespdp():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint]']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        nama1 = request.form['nama1']
        pangkat1 = request.form['pangkat1']
        jabatan1 = request.form['jabatan1']
        nama2 = request.form['nama2']
        pangkat2 = request.form['pangkat2']
        jabatan2 = request.form['jabatan2']
        nama3 = request.form['nama3']
        pangkat3 = request.form['pangkat3']
        jabatan3 = request.form['jabatan3']
        nama4 = request.form['nama4']
        pangkat4 = request.form['pangkat4']
        jabatan4 = request.form['jabatan4']
        penerima = request.form['penerima']
        nama_kapolsek = request.form['nama_kapolsek']
        nrt = request.form['nrt']

        tglsaiki = time.time()

        cur = mysql.connection.cursor()
        cur.execute("UPDATE pembuatanspdp SET no_laporan=%s,nama1=%s,pangkat1=%s,jabatan1=%s,nama2=%s,pangkat2=%s,jabatan2=%s,nama3=%s,pangkat3=%s,jabatan3=%s,nama4=%s,pangkat4=%s,jabatan4=%s,kategori=%s,kasus=%s,penerima=%s,tanggal=%s WHERE no_pol=%s", (no_laporan,nama1,pangkat1,jabatan1,nama2,pangkat2,jabatan2,nama3,pangkat3,jabatan3,nama4,pangkat4,jabatan4,kategori,kasus,penerima,time.strftime("%d-%m-%Y", time.gmtime(tglsaiki)),no_pol))
        mysql.connection.commit()
        return redirect(url_for('dataspdp',no_pol=no_pol))

@app.route('/save_det_penyidik', methods=['GET','POST'])
def save_det_penyidik():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        nrp = request.form['nrp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO det_penyidik (no_sprint,nrp) VALUES(%s,%s)",(no_sprint,nrp))
        mysql.connection.commit()
        return redirect(url_for('show_penyidik', nrp=nrp))

@app.route('/show_penyidik/<int:nrp>', methods=['GET' , 'POST'])
def show_penyidik(nrp):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_penyidik WHERE nrp=%s",[str(nrp)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()

    #return str(rows)
    return render_template('show_penyidik.html', rows = rows)



@app.route('/update_det_penyidik', methods=['GET','POST'])
def update_det_penyidik():
    if request.method == 'POST':
        nrp = request.form['nrp']
        nm_penyidik = request.form['nm_penyidik']
        jbt_penyidik = request.form['jbt_penyidik']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE det_penyidik SET nm_penyidik=%s,jbt_penyidik=%s WHERE nrp=%s", (nm_penyidik,jbt_penyidik,nrp))
        mysql.connection.commit()
        return redirect(url_for('detail_penyidik',nrp=nrp))


@app.route('/detail_penyidik/<int:nrp>', methods=['GET' , 'POST'])
def detail_penyidik(nrp):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM det_penyidik WHERE nrp=%s",[str(nrp)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('detail_penyidik.html', rows = rows)


# @app.route('/detail_penyidik')
# def detail_penyidik():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT a.nrp, b.nm_penyidik, b.jbt_penyidik FROM det_penyidik a JOIN data_penyidik b ON a.nrp = b.nrp")
#     rows =cur.fetchall()
#     #return str(rows)
#     return render_template('detail_penyidik.html', rows = rows)

@app.route('/cancel', methods=['GET' , 'POST'])
def cancel():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        nrp = request.form['nrp']
        nm_penyidik = request.form['nm_penyidik']
        jbt_penyidik = request.form['jbt_penyidik']

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM det_penyidik WHERE nrp=(%s)",[nrp])
        mysql.connection.commit()
        return redirect(url_for('tugas_penyidik',no_sprint=no_sprint))

@app.route('/penyidik/<int:no_sprint>', methods=['GET' , 'POST'])
def penyidik(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM det_penyidik WHERE no_sprint=%s",[str(no_sprint)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)

    return render_template('penyidik.html', rows = rows)

@app.route('/tugas_penyidik/<int:no_sprint>', methods=['GET' , 'POST'])
def tugas_penyidik(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM det_penyidik WHERE no_sprint=%s",[str(no_sprint)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)

    return render_template('tugas_penyidik.html', rows = rows)








@app.route('/savepengajuan', methods=['GET','POST'])
def savepengajuan():
    if request.method == 'POST':
        no_pengajuan = request.form['no_pengajuan']
        klarifikasi = request.form['klarifikasi']
        perihal = request.form['perihal']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kpl_penyidik = request.form['kpl_penyidik']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pengajuanspdp (no_pengajuan,klarifikasi,perihal,no_laporan,no_pol,kategori,pasal,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kpl_penyidik) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (no_pengajuan,klarifikasi,perihal,no_laporan,no_pol,kategori,pasal,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kpl_penyidik))
        mysql.connection.commit()
        return redirect(url_for('datapengajuan',no_pengajuan=no_pengajuan))

@app.route('/datapengajuan/<int:no_pengajuan>', methods=['GET' , 'POST'])
def datapengajuan(no_pengajuan):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pengajuanspdp WHERE no_pengajuan=%s",[str(no_pengajuan)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('datapengajuan.html', rows = rows)

@app.route('/editpengajuan', methods=['GET' , 'POST'])
def editpengajuan():
    no_pengajuan = request.form['no_pengajuan']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pengajuanspdp WHERE no_pengajuan=%s",[str(no_pengajuan)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('edit_pengajuan.html', rows = rows)

@app.route('/updatepengajuan', methods=['GET','POST'])
def updatepengajuan():
    if request.method == 'POST':
        no_pengajuan = request.form['no_pengajuan']
        klarifikasi = request.form['klarifikasi']
        perihal = request.form['perihal']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        kpl_penyidik = request.form['kpl_penyidik']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE pengajuanspdp SET klarifikasi=%s,perihal=%s,no_laporan=%s,no_pol=%s,kategori=%s,pasal=%s,nama_tsk=%s,gender=%s,tempat_lahir=%s,tanggal_lahir=%s,pekerjaan=%s,agama=%s,kewarganegaraan=%s,alamat=%s,kpl_penyidik=%s WHERE no_pengajuan=%s",(klarifikasi,perihal,no_laporan,no_pol,kategori,pasal,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kpl_penyidik,no_pengajuan))
        mysql.connection.commit()
        return redirect(url_for('datapengajuan',no_pengajuan=no_pengajuan))


@app.route('/notifreject')
def notifreject():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reject  order by tgl_reject DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('notifreject.html', rows = rows)


@app.route('/lihat_kategori', methods=['GET' , 'POST'])
def lihat_kategori():
     if request.method == 'POST':
         kategori = request.form['kategori']

         return redirect(url_for('show_kategori',bts_penyidikan=bts_penyidikan))

        #  cur = mysql.connection.cursor()
        #  cur.execute("SELECT * FROM accept WHERE bts_penyidikan=%s", bts_penyidikan)
        #  rows =cur.fetchall()
        #  return render_template('batas.html', rows = rows)

@app.route('/show_kategori/<kategori>', methods=['GET' , 'POST'])
def show_kategori(kategori):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accept WHERE bts_penyidikan=%s",[(bts_penyidikan)])
    rows =cur.fetchall()
    return render_template('batas.html', rows = rows)

# ========================================================================================================================================
# ===============================================================ADMIN====================================================================
# ========================================================================================================================================

@app.route('/notification')
def notification():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notifspdp order by tanggal DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('notification.html', rows = rows)


@app.route('/terima/<int:no_sprint>', methods=['GET' , 'POST'])
def terima(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notifspdp WHERE no_sprint=%s",[str(no_sprint)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('terima.html', rows = rows)

@app.route('/accept', methods=['GET' , 'POST'])
def accept():
# @app.route('/godelete/<no_sprint>', methods=['GET' , 'POST'])
# def godelete(no_sprint):
        if request.method == 'POST':
            no_sprint = request.form['no_sprint']
            no_laporan = request.form['no_laporan']
            no_pol = request.form['no_pol']
            nama_tsk = request.form['nama_tsk']
            gender = request.form['gender']
            tempat_lahir = request.form['tempat_lahir']
            tanggal_lahir = request.form['tanggal_lahir']
            pekerjaan = request.form['pekerjaan']
            agama = request.form['agama']
            kewarganegaraan = request.form['kewarganegaraan']
            alamat = request.form['alamat']
            kategori = request.form['kategori']
            pasal = request.form['pasal']
            penerima = request.form['penerima']
            tampil_tgl = request.form['tampil_tgl']
            kapolsek = request.form['kapolsek']
            nrp = request.form['nrp']


            terima = time.time()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO accept (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tampil_tgl,kapolsek,nrp))
            mysql.connection.commit()
            # cur = mysql.connection.cursor()
            # cur.execute("INSERT INTO accept (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,tampil_tgl,kapolsek,nrp))
            # mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO data_diterima (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_diterima, tgl_disetujui, keterangan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint, no_laporan, no_pol ,nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y", time.gmtime(terima)),"","TUNGGU"))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("UPDATE status SET keterangan=%s, tgl_cek=%s WHERE no_sprint=%s",("ACCEPT", time.strftime("%d-%m-%Y", time.gmtime(terima)),no_sprint))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO notif_jaksa (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_terkirim, tgl_cek, keterangan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint, no_laporan, no_pol ,nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(terima)),"","ON PROCESS"))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM notifspdp WHERE no_sprint=(%s)",[no_sprint])
            mysql.connection.commit()
            return redirect(url_for('notification'))

@app.route('/tolak/<int:no_sprint>', methods=['GET' , 'POST'])
def tolak(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notifspdp WHERE no_sprint=%s",[str(no_sprint)])
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('tolak.html', rows = rows)

@app.route('/save_reject', methods=['GET' , 'POST'])
def save_reject():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        alasan = request.form['alasan']

        tolak = time.time()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reject (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_reject, alasan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y", time.gmtime(tolak)),alasan))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data_reject (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_reject, alasan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y", time.gmtime(tolak)),alasan))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("UPDATE status SET keterangan=%s, tgl_cek=%s WHERE no_sprint=%s",("REJECT", time.strftime("%d-%m-%Y", time.gmtime(tolak)),no_sprint))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM notifspdp WHERE no_sprint=(%s)",[no_sprint])
        mysql.connection.commit()
        return redirect(url_for('notification'))

@app.route('/check_spdp/<int:no_sprint>', methods=['GET' , 'POST'])
def check_spdp(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notifspdp WHERE no_sprint=%s",[str(no_sprint)])
    rows =cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM det_penyidik WHERE no_sprint=%s",[str(no_sprint)])
    rowspenyidik =cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profil_kapolsek")
    rowskapolsek =cur.fetchall()

    return render_template('f_spdp.html',rows=rows,rowspenyidik=rowspenyidik,rowskapolsek=rowskapolsek)

@app.route('/check_pengajuan/<int:no_sprint>', methods=['GET' , 'POST'])
def check_pengajuan(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notifspdp WHERE no_sprint=%s",[str(no_sprint)])
    rows =cur.fetchall()


    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profil_kapolsek")
    rowskapolsek =cur.fetchall()

    return render_template('pengajuan_spdp.html',rows=rows,rowskapolsek=rowskapolsek)

@app.route('/edit_reject', methods=['GET' , 'POST'])
def edit_reject():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']

    return redirect(url_for('data_reject_spdp',no_sprint=no_sprint))

@app.route('/data_reject_spdp/<int:no_sprint>', methods=['GET' , 'POST'])
def data_reject_spdp(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spdp WHERE no_sprint=%s",[str(no_sprint)])
    # cur.execute("SELECT a.no_sprint, a.no_laporan, a.no_pol, a.nama_tsk, a.gender, a.tempat_lahir, a.tanggal_lahir, a.pekerjaan, a.agama, a.kewarganegaraan, a.alamat, a.kategori, a.pasal, a.tanggal, a.tampil_tgl, a.kapolsek, a.nrp, b.nrp, b.nm_penyidik, b.jbt_penyidik FROM spdp a INNER JOIN det_penyidik b ON a.no_sprint= b.no_sprint  WHERE a.no_sprint=%s;",[str(no_sprint)])

    rows =cur.fetchall()
    #return str(rows)
    return render_template('dataspdp_reject.html', rows = rows)


@app.route('/edit_data_reject', methods=['GET' , 'POST'])
def edit_data_reject():
    if request.method == 'POST':
        no_sprint = request.form['no_sprint']
        no_laporan = request.form['no_laporan']
        no_pol = request.form['no_pol']
        nama_tsk = request.form['nama_tsk']
        gender = request.form['gender']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        pekerjaan = request.form['pekerjaan']
        agama = request.form['agama']
        kewarganegaraan = request.form['kewarganegaraan']
        alamat = request.form['alamat']
        kategori = request.form['kategori']
        pasal = request.form['pasal']
        penerima = request.form['penerima']


        saiki = time.time()

        tampil_tgl = request.form['tampil_tgl']
        kapolsek = request.form['kapolsek']
        nrp = request.form['nrp']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE spdp SET no_laporan=%s, no_pol=%s, nama_tsk=%s, gender=%s, tempat_lahir=%s, tanggal_lahir=%s, pekerjaan=%s, agama=%s, kewarganegaraan=%s, alamat=%s, kategori=%s, pasal=%s, penerima=%s, tanggal=%s, tampil_tgl=%s, kapolsek=%s, nrp=%s WHERE no_sprint=%s",(no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(saiki)),tampil_tgl,kapolsek,nrp,no_sprint))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notifspdp (no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,tanggal,tampil_tgl,kapolsek,nrp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint,no_laporan,no_pol,nama_tsk,gender,tempat_lahir,tanggal_lahir,pekerjaan,agama,kewarganegaraan,alamat,kategori,pasal,penerima,time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(saiki)),tampil_tgl,kapolsek,nrp))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM status WHERE no_sprint=(%s)",[no_sprint])
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO status (no_sprint,no_laporan,no_pol, nama_tsk, kategori, pasal, tgl_terkirim, tgl_cek, keterangan) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(no_sprint, no_laporan, no_pol ,nama_tsk, kategori, pasal, time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime(saiki)),"","ON PROCESS"))
        mysql.connection.commit()
        return render_template('send.html')

@app.route('/data_diterima')
def data_diterima():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accept order by tampil_tgl DESC ")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('data_diterima.html', rows = rows)

@app.route('/status_jaksa')
def status_jaksa():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_diterima order by tgl_diterima DESC")
    #cur.execute("SELECT * FROM nota")
    rows =cur.fetchall()
    #return str(rows)
    return render_template('status_jaksa.html', rows = rows)


@app.route('/data_reject')
def data_reject():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_reject order by tgl_reject DESC")
    rows =cur.fetchall()
    return render_template('data_reject.html', rows = rows)



#
# ===================================================================================================
# =========================================KEJAKSAAN=================================================
# ===================================================================================================


@app.route('/pemberitahuan')
def pemberitahuan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notif_jaksa order by tgl_terkirim DESC")
    rows =cur.fetchall()
    return render_template('pemberitahuan.html', rows = rows)

@app.route('/insert_batas/<int:no_sprint>', methods=['GET' , 'POST'])
def insert_batas(no_sprint):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accept WHERE no_sprint=%s",[str(no_sprint)])
    # cur.execute("SELECT a.no_sprint, a.no_laporan, a.no_pol, a.nama_tsk, a.gender, a.tempat_lahir, a.tanggal_lahir, a.pekerjaan, a.agama, a.kewarganegaraan, a.alamat, a.kategori, a.pasal, a.tanggal, a.tampil_tgl, a.kapolsek, a.nrp, b.nrp, b.nm_penyidik, b.jbt_penyidik FROM spdp a INNER JOIN det_penyidik b ON a.no_sprint= b.no_sprint  WHERE a.no_sprint=%s;",[str(no_sprint)])

    rows =cur.fetchall()
    #return str(rows)
    return render_template('insert_batas.html', rows = rows)

@app.route('/save_batas', methods=['GET' , 'POST'])
def save_batas():
# @app.route('/godelete/<no_sprint>', methods=['GET' , 'POST'])
# def godelete(no_sprint):
        if request.method == 'POST':
            no_sprint = request.form['no_sprint']
            # no_laporan = request.form['no_laporan']
            # no_pol = request.form['no_pol']
            # nama_tsk = request.form['nama_tsk']
            # gender = request.form['gender']
            # tempat_lahir = request.form['tempat_lahir']
            # tanggal_lahir = request.form['tanggal_lahir']
            # pekerjaan = request.form['pekerjaan']
            # agama = request.form['agama']
            # kewarganegaraan = request.form['kewarganegaraan']
            # alamat = request.form['alamat']
            # kategori = request.form['kategori']
            # pasal = request.form['pasal']
            # tampil_tgl = request.form['tampil_tgl']
            # penerima = request.form['penerima']
            # kapolsek = request.form['kapolsek']
            # nrp = request.form['nrp']
            bts_penyidikan = request.form['bts_penyidikan']


            cek_jaksa = time.time()

            cur = mysql.connection.cursor()
            cur.execute("UPDATE data_diterima SET tgl_disetujui=%s, keterangan=%s WHERE no_sprint=%s",(time.strftime("%d-%m-%Y", time.gmtime(cek_jaksa)),"DITERIMA", no_sprint))
            mysql.connection.commit()

            cekselesai= time.time()

            cur = mysql.connection.cursor()
            cur.execute("UPDATE accept SET bts_penyidikan=%s, tgl_cek=%s WHERE no_sprint=%s",(bts_penyidikan, time.strftime("%d-%m-%Y", time.gmtime(cekselesai)),no_sprint))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM notif_jaksa WHERE no_sprint=(%s)",[no_sprint])
            mysql.connection.commit()
            return redirect(url_for('pemberitahuan'))

@app.route('/data_tersimpan')
def data_tersimpan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accept order by tampil_tgl DESC")
    rows =cur.fetchall()
    return render_template('data_tersimpan.html', rows = rows)

@app.route('/batas_penyidikan')
def batas_penyidikan():
    return render_template('batas_penyidikan.html')

@app.route('/lihat_batas', methods=['GET' , 'POST'])
def lihat_batas():
     if request.method == 'POST':
         bts_penyidikan = request.form['bts_penyidikan']

         return redirect(url_for('batas',bts_penyidikan=bts_penyidikan))

        #  cur = mysql.connection.cursor()
        #  cur.execute("SELECT * FROM accept WHERE bts_penyidikan=%s", bts_penyidikan)
        #  rows =cur.fetchall()
        #  return render_template('batas.html', rows = rows)

@app.route('/batas/<bts_penyidikan>', methods=['GET' , 'POST'])
def batas(bts_penyidikan):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accept WHERE bts_penyidikan=%s",[(bts_penyidikan)])
    rows =cur.fetchall()
    return render_template('batas.html', rows = rows)

@app.route("/gosignin", methods=['GET','POST'])
def gosignin():
      if request.method == 'POST':
          username_form = request.form['username']
          password_form = request.form['password']

          cur = mysql.connection.cursor()
          cur.execute("SELECT COUNT(1) FROM users WHERE username=(%s)",[username_form])

          if cur.fetchone()[0]:
              cur.execute("SELECT password, level_akses FROM users WHERE username=(%s)",[username_form])
              for row in cur.fetchall():
                  if password_form==row[0]:
                      session['username'] = request.form['username']
                      session['level_akses'] = row[1]

                      return redirect(url_for('index'))
                  else:
                      error = "Invalid Credential"
          else:
             error = "Invalid Credential"

          return render_template('signin.html', error=error)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


app.secret_key = 'fariz'

if __name__ == "__main__":
    app.run(debug="True")
