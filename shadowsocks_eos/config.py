import os
import json


class Config:

    path = os.path.expanduser('~') + '/.shadowsocks-eos/'
    config_file = path + 'gui-config.json'
    pac_file = path + 'gfwlist.js'
    user_rule = path + 'user-rule.txt'
    gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    gfwlist_tmp = '/tmp/gfwlist.txt'
    local_port = 1080


    def __init__(self):
        self.config = {}
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def get(self, key, default):
        if key in self.config:
            return self.config[key]
        else:
            self.config[key] = default
            return default

    def set(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent = 4)