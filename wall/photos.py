import os
from datetime import datetime
from PIL import Image
import sqlite3

supported_files = ['jpg', 'png']

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

def processPhoto(con, fname):
    cur = con.cursor()
    with Image.open(fname) as im:
        width, height = im.size
        img = (os.path.basename(fname), #"name":
               fname, #"fname":
               width, #"width":
               height, #"height":
               Image.MIME[im.format], #"mime":
               datetime.now().isoformat() #"created_at":
        )
        cur.execute("insert into photowall(name, fname, width, height, mime, created_at) values(?,?,?,?,?,?)", img)
        con.commit()
    return True

def importPhotos(dirname):
    con = sqlite3.connect('photowall.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS photowall(fname PRIMARY KEY, name, width INTEGER, height INTEGER, mime, created_at)");

    newPhotos = []

    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            parts = name.rsplit('.', 1)
            if len(parts) < 2:
                continue
            ext = parts[1]
            if ext.lower() in supported_files:
                fname = os.path.join(root, name)
                newPhotos.append(fname)

    cur.execute("select fname from photowall")
    for img in cur.fetchall():
        fname = img[0]
        if fname not in newPhotos:
            cur.execute("delete from photowall where fname=:fname", {"fname": img[0]})
            con.commit()

    for img in newPhotos:
        cur.execute("select count(fname) from photowall where fname=:fname", {"fname": img})
        resp = cur.fetchone()[0]
        if resp < 1:
            processPhoto(con, img)

    return True
