import os
from datetime import datetime
from PIL import Image
imname = 'imgs/IMG_20141105_212028308.jpg'

supported_files = ['jpg', 'png']

#"name":"100_0002.JPG","width":4000,"height":3000,"created_at":"2021-10-03 16:19:09.96598 -0500 CDT m=+0.006012901"
def findPhotos(dirname):
    photos = []
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            parts = name.rsplit('.', 1)
            if len(parts) < 2:
                continue
            ext = parts[1]
            if ext.lower() in supported_files:
                #wall.AddPhotoFromFile(path, time.Now())
                with Image.open(os.path.join(root, name)) as im:
                    width, height = im.size
                    # XXX clean up the file path so it isnt sent to the UI
                    img = {"name": name,
                           "fname": os.path.join(root, name),
                           "width": width,
                           "height": height,
                           "mime": Image.MIME[im.format],
                           "created_at": datetime.now().isoformat()
                    }
                    #os.path.join(root, name)
                    photos.append(img)
    return photos
