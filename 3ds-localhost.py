"""
List predefinied files from folder and generates a qr code for download with FBI
"""

import os
import socket
import socketserver
import http.server
import qrcode
import qrcode.image.svg


FOLDER = 'C:\\CIA\\FILES\\DIRECTORY\\'
PORT = 8080
IP_ADDR = socket.gethostbyname(socket.gethostname())
FILE_TYPES = ['.3dsx', '.cia']

with open('index.html', 'w') as html_file:
    html_file.write('<!DOCTYPE html>\
                        <html lang="en">\
                        <head>\
                            <meta charset="utf-8">\
                            <title>3DS fileserver</title>\
                            <link rel="stylesheet" href="style.css">\
                        </head>\
                        <body>')
    with os.scandir(FOLDER) as entries:
        for entry in entries:
            if os.path.splitext(entry.name)[1] in FILE_TYPES:
                img = qrcode.make(f'http://{IP_ADDR}:{PORT}/{entry.name}')
                img.save(f'{os.path.splitext(entry.name)[0]}.png')
                html_file.write(f"""<div class="file">
                                    <a href="#"><h3 onclick="show('{os.path.splitext(entry.name)[0]}')">
                                    {os.path.splitext(entry.name)[0]}{os.path.splitext(entry.name)[1]}</h3></a>
                                    <img style="display: none" id="{os.path.splitext(entry.name)[0]}"
                                     src="{os.path.splitext(entry.name)[0]}.png" />
                                  </div>""")
    html_file.write('   <script>\
                            function show(id) {\
                              var x = document.getElementById(id);\
                              if (x.style.display === "none") {\
                                x.style.display = "block";\
                              } else {\
                                x.style.display = "none";\
                              }\
                            }\
                            </script>\
                        </body>\
                    </html>')

Handler = http.server.SimpleHTTPRequestHandler
HTTPD = socketserver.TCPServer(("", PORT), Handler)
print(f'Running in {IP_ADDR}:{PORT}')
HTTPD.serve_forever()
