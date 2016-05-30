import os
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import config

PORT = 8090

class PacHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/proxy.pac'):
                fp = open(config.Config.pac_file)
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                self.wfile.write(fp.read())
                fp.close()
        except:
            self.send_error(404, 'Not Fouund File %s' % self.path)

server = None
server_thread = None
is_start = False

def init():
    global server
    server = HTTPServer(('127.0.0.1', PORT), PacHandler)

def start():
    global is_start
    if is_start or not server:
        return
    is_start = True
    global server_thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

def stop():
    global is_start
    if is_start and server:
        server.shutdown()
    is_start = False
    # server.server_close()
    if server_thread:
        server_thread.join()

def update():
    re = os.system('wget %s -O %s' % (config.Config.gfwlist_url, config.Config.gfwlist_tmp))

    if re != 0:
        return False

    re = os.system('gfwlist2pac -i %s -p "SOCKS5 %s:%d" -f %s --user-rule %s' % 
              (config.Config.gfwlist_tmp, '127.0.0.1', config.Config.local_port, 
               config.Config.pac_file, config.Config.user_rule))

    if re != 0:
        return False

    return True