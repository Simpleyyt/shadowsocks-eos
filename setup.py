#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='shadowsocks-eos',
    version = '1.0.0',
    description = 'Shadowsocks client for elementaryOS or Ubuntu',
    author = 'Yitao Yao',
    author_email = 'simpleyyt@gmail.com',
    url = 'https://simpleyyt.github.io',
    packages = find_packages(),
    include_package_data = True,
    package_data = {
        'shadowsocks_eos': ['config/gfwlist.js', 'config/gui-config.json', 'config/user-rule.txt']
    },
    data_files = [
    	('/usr/share/applications', ['data/shadowsocks-eos.desktop']),
    	('/usr/share/icons/hicolor/scalable/apps/', ['data/icon/shadowsocks-eos.png']),
    	('/usr/share/icons/hicolor/scalable/status/', ['data/icon/indicator-shadowsocks-eos.png']),
    	('/usr/share/icons/hicolor/scalable/status/', ['data/icon/indicator-shadowsocks-eos-active.png'])
    ],
    entry_points={
        'console_scripts': [
            'shadowsocks-eos = shadowsocks_eos:start'
        ],
    },
     )