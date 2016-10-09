# -*- coding:utf8 -*-

import os
import sys
import os.path
import time
import json
import requests

from asynchttp import Http
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    Response
    )

from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware

from CameraCapture import get_camera, take


camera = get_camera()

session_opts = {
    #'session.type': 'ext:memcached',
    'session.type': 'memory',
    #'session.url': '127.0.0.1:8000',
    #'session.data_dir': './cache',
}

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()

app = Flask(__name__)

app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()

def makedirs():
    dirs = ['advds', 'adimgs', 'info', 'commpics', 'commgov', 'commsqr', 'commuseum', 'breaking', 'convinient']
    for d in dirs:
        subf = os.path.join('static/', d)
        if not os.path.exists(subf):
            os.mkdir(subf)

@app.route("/")
def home():
    return redirect('/index')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/ads")
def ads():
    return render_template('ads.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form['regular']
        pas = request.form['pass']
        if 'checkbox1' in request.form:
            print request.form['checkbox1']
        else:
            print 'not checked'
        if usr == 'admin' and pas == 'admin':
            return redirect('/')
    return render_template('login.html')

@app.route("/logout")
def logout():
    return redirect('/login')

@app.route("/blank")
def blank():
    return render_template('blank.html')

@app.route("/user-query-old", methods=['POST'])
def userquery():
    cardno = request.form['cardno']
    print cardno
    return 'ok'

@app.route("/binusereport/<cid>")
def ad(cid):
    print 'lets save it ', cid
    take(camera, cid)
    http = Http()
    http.request('http://www.wscrum.tk:5013/bin/use/report/%s'%(cid,))
    return 'ok'

@app.route("/ad/videos")
def vedio():
    videos = []
    image = '/static/images/video-icon.png'
    did = 'video-frame'
    folder = os.path.join('static', 'advds')
    files = os.listdir(folder)
    for f in files:
        if sys.platform.startswith('win'):
            f = f.decode('gbk').encode('utf8')
        name, ext = os.path.splitext(f)
        print name, ext
        if ext.lower() == '.mp4':
            videos.append({
                'image': image,
                'id': did,
                'name': name,
                'src': os.path.join(folder, f).replace('\\', '/')
            })
    js = json.dumps(videos)
    print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'

    return resp

@app.route("/ad/pic")
def pic():
    return render_template('ad_pic.html')

@app.route("/commsrv")
def commsrv():
    return render_template('commsrv.html')

@app.route("/comm/museum")
def museum():
    mupics = []
    folder = os.path.join('static', 'commuseum')
    files = os.listdir(folder)
    txtfiles = [f for f in files if 'txt' in os.path.splitext(f)[1].lower()]
    images = [f for f in files if 'txt' not in os.path.splitext(f)[1].lower()]
    files = zip(txtfiles, images)
    for f in files:
        txt, img = f
        with open(os.path.join(folder, txt), 'rb') as txtfd:
            lns = txtfd.readlines()
            title = lns[0].strip()
            content = '<br>'.join([ln.strip() for ln in lns[1:]])
        if sys.platform.startswith('win'):
            img = img.decode('gbk').encode('utf8')
        mupics.append({
            'imgurl': os.path.join(folder, img).replace('\\', '/'),
            'title': title,
            'content': content
        })
    js = json.dumps(mupics)
    print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'

    return resp

@app.route("/comm/dance")
def dance():
    videos = []
    image = '/static/images/video-icon.png'
    did = 'comm-video'
    folder = os.path.join('static', 'commsqr')
    files = os.listdir(folder)
    for f in files:
        if sys.platform.startswith('win'):
            f = f.decode('gbk').encode('utf8')
        name, ext = os.path.splitext(f)
        if ext.lower() == '.mp4':
            videos.append({
                'image': image,
                'id': did,
                'name': name,
                'src': os.path.join(folder, f).replace('\\', '/')
            })
    js = json.dumps(videos)
    print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'

    return resp

@app.route("/comm/pics")
def pics():
    pics = []
    folder = os.path.join('static', 'commpics')
    files = os.listdir(folder)
    txtfiles = [f for f in files if 'txt' in os.path.splitext(f)[1].lower()]
    images = [f for f in files if 'txt' not in os.path.splitext(f)[1].lower()]
    files = zip(txtfiles, images)
    for f in files:
        txt, img = f
        with open(os.path.join(folder, txt), 'rb') as txtfd:
            lns = txtfd.readlines()
            title = lns[0].strip()
            content = '<br>'.join([ln.strip() for ln in lns[1:]])
        if sys.platform.startswith('win'):
            img = img.decode('gbk').encode('utf8')
        pics.append({
            'imgurl': os.path.join(folder, img).replace('\\', '/'),
            'title': title,
            'content': content
        })
    js = json.dumps(pics)
    print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'

    return resp

@app.route("/comm/governinfo")
def govern():
    pics = []
    folder = os.path.join('static', 'commgov')
    files = os.listdir(folder)
    for f in files:
        if sys.platform.startswith('win'):
            f = f.decode('gbk').encode('utf8')
        pics.append({
            'imgurl': os.path.join(folder, f).replace('\\', '/')
        })
    js = json.dumps(pics)
    print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'
    return resp

@app.route("/comm/infosrv")
def info():
    infos = []
    folder = os.path.join('static', 'info')
    files = os.listdir(folder)
    txtfiles = [f for f in files if 'txt' in os.path.splitext(f)[1].lower()]
    images = [f for f in files if 'jpg' in os.path.splitext(f)[1].lower() or 'png' in os.path.splitext(f)[1].lower() and '-qr' not in os.path.splitext(f)[0]]
    qrs = [f for f in files if '-qr' in os.path.splitext(f)[0] and 'jpg' in os.path.splitext(f)[1].lower() or 'png' in os.path.splitext(f)[1].lower()]
    print txtfiles
    print images
    print qrs
    files = zip(sorted(txtfiles), sorted(images), sorted(qrs))
    for f in files:
        with open(os.path.join(folder, f[0]), 'rb') as txtfd:
            content = ''.join([ln.strip('\n') for ln in txtfd.readlines()])
        img, qr = f[1:]
        if sys.platform.startswith('win'):
            img = img.decode('gbk').encode('utf8')
            qr = qr.decode('gbk').encode('utf8')
        infos.append({'infopic': os.path.join(folder, img).replace('\\', '/'),
                      'infoqr': os.path.join(folder, qr).replace('\\', '/'),
                      'infotext': content})
    print infos
    js = json.dumps(infos)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'
    return resp

@app.route("/opengovern/breaking")
def breaking():
    pics = []
    folder = os.path.join('static', 'breaking')
    files = os.listdir(folder)
    txtfiles = [f for f in files if 'txt' in os.path.splitext(f)[1]]
    imgfiles = [f for f in files if 'txt' not in os.path.splitext(f)[1]]
    files = zip(txtfiles, imgfiles)
    for f in files:
        with open(os.path.join(folder, f[0]), 'rb') as txtfd:
            content = '<br>'.join([ln.strip() for ln in txtfd.readlines()])
        f = f[1]
        print f
        if sys.platform.startswith('win'):
            f = f.decode('gbk').encode('utf8')
        pics.append({
            'imgurl': os.path.join(folder, f).replace('\\', '/'),
            'textcontent': content,
        })
    js = json.dumps(pics)
    #print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'
    return resp

@app.route("/opengovern/convinient")
def conv():
    pics = []
    folder = os.path.join('static', 'convinient')
    files = os.listdir(folder)
    txtfiles = [f for f in files if 'txt' in os.path.splitext(f)[1]]
    imgfiles = [f for f in files if 'txt' not in os.path.splitext(f)[1]]
    files = zip(txtfiles, imgfiles)
    for f in files:
        with open(os.path.join(folder, f[0]), 'rb') as txtfd:
            content = '<br>'.join([ln.strip() for ln in txtfd.readlines()])
        f = f[1]
        if sys.platform.startswith('win'):
            f = f.decode('gbk').encode('utf8')
        pics.append({
            'imgurl': os.path.join(folder, f).replace('\\', '/'),
            'textcontent': content,
        })
    js = json.dumps(pics)
    #print js
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'
    return resp

@app.route('/user-query', methods=['POST'])
def query():
    cardno = request.form['cardno']
    print cardno
    http = Http()
    #r = http.request('http://localhost:5000/user-query/%s'%(cardno,))
    r = requests.post('http://www.wscrum.tk:5013/user-query', data={'cardno': cardno})
    js = r.text
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:5001'
    return resp

if __name__ == "__main__":
    makedirs()
    #app.run(host='0.0.0.0', port=5001, debug=True)
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
