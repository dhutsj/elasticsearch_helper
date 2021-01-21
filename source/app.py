import os
import cherrypy
import pandas as pd
from es_manipulation import csv_to_es


class ESHelper(object):

    def index(self):
        return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap 101 Template</title>
    <style>
    body {
       background: url("./img/starry.jpg");}
    .gray {
       color: rgb(192,192,192);
     }
    .size {
       font-size: 40px;
     }
    </style>
    <!-- Bootstrap -->
    <!-- bootstrap 4.x is supported. You can also use the bootstrap css 3.3.x versions -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
    <!-- if using RTL (Right-To-Left) orientation, load the RTL CSS file after fileinput.css by uncommenting below -->
    <!-- link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/css/fileinput-rtl.min.css" media="all" rel="stylesheet" type="text/css" /-->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <!-- piexif.min.js is needed for auto orienting image files OR when restoring exif data in resized images and when you 
    wish to resize images before upload. This must be loaded before fileinput.min.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/js/plugins/piexif.min.js" type="text/javascript"></script>
    <!-- sortable.min.js is only needed if you wish to sort / rearrange files in initial preview. 
    This must be loaded before fileinput.min.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/js/plugins/sortable.min.js" type="text/javascript"></script>
    <!-- popper.min.js below is needed if you use bootstrap 4.x. You can also use the bootstrap js 
   3.3.x versions without popper.min.js. -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <!-- bootstrap.min.js below is needed if you wish to zoom and preview file content in a detail modal
    dialog. bootstrap 4.x is supported. You can also use the bootstrap js 3.3.x versions. -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" type="text/javascript"></script>
    <!-- the main fileinput plugin file -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/js/fileinput.min.js"></script>
    <!-- optionally if you need a theme like font awesome theme you can include it as mentioned below -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/themes/fa/theme.js"></script>
    <!-- optionally if you need translation for your language then include  locale file as mentioned below -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.3/js/locales/(lang).js"></script>

    </head>
    <body>
    <h1 align="center" class="gray size">Please upload your csv or excel file</h1>
    <br />
    <br />
    <br />
    <form action="upload" method="post" enctype="multipart/form-data">
    <input id="input-id" type="file" class="file" name="myFile" data-preview-file-type="text" >
    </form>

    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
    </body>
    </html>
    """

    index.exposed = True

    def upload(self, myFile):
        out = """<html>
        <body>
            Uploaded file: %s<br />
        </body>
        </html>"""

        print(myFile.filename)
        if myFile.filename.__contains__("csv"):
            df = pd.read_csv(myFile.filename, encoding="latin1")
            df.to_csv('temp.csv', encoding="latin1")
            csv_to_es("temp.csv")
        elif myFile.filename.__contains__("xltx") or myFile.filename.__contains__("xlsx"):
            df = pd.read_excel(myFile.filename, encoding="latin1")
            new_data = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            new_data.to_excel("temp.xlsx", index=True)
            csv_to_es("temp.xlsx")
        else:
            raise TypeError("File type error")

        return out % myFile.filename

    upload.exposed = True


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './css'},
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './img'},
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './js'},
        'global': {
            'environment': 'production',
            'log.screen': True,
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
            'engine.autoreload_on': True,

        }}
    cherrypy.quickstart(ESHelper(), config=conf)
