import os
from flask import Flask, render_template, jsonify, send_file, send_from_directory
from flask_apscheduler import APScheduler
import sqlite3
from wall.photos import importPhotos
import json
import io
from PIL import Image
from flask import g

DATABASE = 'photowall.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class Config:
    SCHEDULER_API_ENABLED = True

IMGROOT = "imgs"
MaxWidth = 1920
MaxHeight = 1080

app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@scheduler.task('interval', id='imageImport', seconds=900, misfire_grace_time=900)
def imageImport():
    print('Job 1 executed')
    #importPhotos(IMGROOT)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/imgs/<imgname>")
def imghandle(imgname):
    cur = get_db().cursor()
    cur.execute("select fname, mime from photowall where name=:name", {"name": imgname})
    #photo = next(item for item in app.photos if item["name"] == imgname)
    photo = cur.fetchone()
    print(photo)
    return send_file(photo[0], mimetype=photo[1])

@app.route("/api/wall.json")
def wallApi():
    cur = get_db().cursor()
    cur.execute("select name, width, height, mime from photowall")
    resp = cur.fetchall()
    photos = []
    for img in resp:
        photos.append({"name": img[0],
                       "width": img[1],
                       "height": img[2],
                       "mime": img[3]
        })
    return jsonify(photos)

@app.route("/slide")
def slide():
    return render_template("slide.html")

@app.route("/")
def index():
    return render_template("wall.html")


if __name__ == '__main__':
    app.run(debug = True)
