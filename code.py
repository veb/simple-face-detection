import web, sys, os, subprocess, uuid
import cv2
from shutil import copy

def detectObjects(image, imagefile):
    image_read = cv2.imread(imagefile)
    gray_image = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        '/usr/local/Cellar/opencv3/3.2.0/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)

    for (x, y, w, h) in faces:
        print("found a face: [(%d,%d) -> (%d,%d)]" % (x, y, x+w, y+h))
        foundFace(imagefile, (x, y, w, h))

    return faces

def foundFace(imagefile, (x, y, w, h)):
    os.system("convert {image} -draw \"image SrcOver {a},{b} {c},{d} biglazer.png\" {output}".format(
                    image=imagefile,
                    a=x+6,
                    b=y,
                    c=w,
                    d=h,
                    output=imagefile));

urls = (
    '/upload', 'Upload',
)

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html><head><link rel="shortcut icon" href="/static/favicon.ico"
type="image/x-icon"></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = 'uploads/'
        if 'myfile' in x:
            filepath=x.myfile.filename.replace('\\','/')

            filename = str(uuid.uuid4())
            fout = open(filedir +'/'+ filename,'w')
            fout.write(x.myfile.file.read())
            fout.close()

            imagefile = filedir +'/'+ filename;

            image = cv2.imread(imagefile);
            unique_name = str(uuid.uuid4())
            output_path = 'static/%s.png' % unique_name
            got_objects = detectObjects(image, imagefile)
            print got_objects[0]
            if (got_objects.any()):
                copy(imagefile, output_path)
                web.header("Content-Type", "images/png")
                raise web.seeother("/static/%s.png" % unique_name)
            else:
                return
        raise web.seeother('/upload')

if __name__ == "__main__":
   app = web.application(urls, globals(), True)
   app.run()
