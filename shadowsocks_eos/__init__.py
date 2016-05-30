# coding: utf-8
import os
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from shadowsocks import Shadowsocks
from config import Config

def load_config():
    if not os.path.exists(Config.path):
        os.makedirs(Config.path)
    config_file_dir = os.path.join(os.path.dirname(__file__), 'config')
    if not os.path.exists(Config.config_file):
        with open(Config.config_file, 'w') as fi, \
                open(config_file_dir + '/gui-config.json', 'r') as fo:
            fi.write(fo.read())
    if not os.path.exists(Config.pac_file):
        with open(Config.pac_file, 'w') as fi, \
                open(config_file_dir + '/gfwlist.js', 'r') as fo:
            fi.write(fo.read())
    if not os.path.exists(Config.user_rule):
        with open(Config.user_rule, 'w') as fi, \
                open(config_file_dir + '/user-rule.txt', 'r') as fo:
            fi.write(fo.read())


def start():
    load_config()
    app = Shadowsocks()
    app.show_all()
    Gtk.main()
