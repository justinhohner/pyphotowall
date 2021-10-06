import os
from flask import Flask, render_template, jsonify, send_file, send_from_directory
from wall.photos import findPhotos
import json
import io
from PIL import Image

app = Flask(__name__)
IMGROOT = "imgs"
MaxWidth = 1920
MaxHeight = 1080
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/imgs/<imgname>")
def imghandle(imgname):
    photo = next(item for item in app.photos if item["name"] == imgname)
    """if (photo["width"] <= MaxWidth) and (photo["height"] <= MaxHeight):
        return send_file(photo["fname"], mimetype=photo["mime"])
    else:
        parts = photo["fname"].rsplit('.', 1)
        fname = parts[0] + ".png"
        with Image.open(photo["fname"]) as img:
            new_width = MaxWidth
            new_height = MaxHeight
            if img.width < MaxWidth:
                new_width = img.width
            if img.height < MaxHeight:
                new_height = img.height
            imgIO = io.BytesIO()
            img = img.resize((new_width, new_height), resample=Image.LANCZOS, box=(0,0,MaxWidth, MaxHeight))
            img.save(imgIO, "PNG")
            imgIO.seek(0)
            return send_file(imgIO, mimetype='image/png', as_attachment=True, download_name=fname)"""
    return send_file(photo["fname"], mimetype=photo["mime"])

@app.route("/api/wall.json")
def wallApi():
    return jsonify(app.photos)

@app.route("/slide")
def slide():
    return render_template("slide.html")

@app.route("/")
def index():
    return render_template("wall.html")


if __name__ == '__main__':
    app.photos = findPhotos(IMGROOT)
    app.run(debug = True)
