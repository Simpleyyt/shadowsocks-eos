# coding: utf-8
import os
import subprocess
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from config import Config
from server_setting import ServerSetting
import sslocal
import proxy
import gfwpac
import sys

class Shadowsocks:

    def __init__(self):
        self.config = Config()
        self.server_setting = ServerSetting(self)
        self.enabled = self.config.get('enabled', True)
        self.indicator = appindicator.Indicator.new (
            "shadowsocks-eos",
            "indicator-shadowsocks-eos-active",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_attention_icon("indicator-shadowsocks-eos")
        print self.indicator.get_icon()
        self.build_menu()
        self.indicator.set_menu(self.menu)
        self.stop()
        gfwpac.init()
        if self.enabled:
            self.start()
            self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        else:
            self.indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
            

    def server_activate(self, widget, server, index):
        if not widget.get_active():
            return
        self.index = index
        self.config['index'] = index
        self.config.save()
        if not self.enabled:
            sslocal.stop()
            return
        sslocal.start(server['server'], server['port'],
                      server['password'], server['method'],
                      self.config.local_port)

    def load_servers(self):
        for child in self.server_submenu.get_children():
            self.server_submenu.remove(child)
        servers = self.config.get('configs', '[]')
        index = self.config.get('index', 0)
        group = []
        i = 0
        for server in servers:
            name = server['remarks'] + '(' + server['server'] + ':' + str(server['port']) + ')'
            item = Gtk.RadioMenuItem.new_with_label(group, name)
            item.connect('activate', self.server_activate, server, i)
            self.server_submenu.append(item)
            group = item.get_group()
            if i == index:
                item.set_active(True)
                self.server_activate(item, server, i)
            i = i + 1

        self.server_submenu.append(Gtk.SeparatorMenuItem())

        self.open_server_item = Gtk.MenuItem('打开服务器设定...')
        self.open_server_item.connect('activate', self.show_server_setting)
        self.server_submenu.append(self.open_server_item)
        self.server_submenu.show_all()

    def get_config(self):
        return self.config

    def start_proxy(self):
        _global = self.config.get('global', False)
        if _global:
            proxy.set_whole_proxy('127.0.0.1', Config.local_port)
            gfwpac.stop()
        if not _global:
            gfwpac.start()
            proxy.set_auto_proxy('http://127.0.0.1:8090/proxy.pac')

    def stop_proxy(self):
        proxy.set_no_proxy()
        gfwpac.stop()

    def stop(self):
        sslocal.stop()
        self.stop_proxy()

    def start(self):
        self.start_proxy()
        self.load_servers()

    def update_proxy(self):
        self.stop_proxy()
        if self.enabled:
            self.start_proxy()

    def proxy_active(self, widget):
        if not widget.get_active():
            return
        gb = self.wholeproxy_item.get_active()
        if not self.enabled:
            return
        self.config['global'] = gb
        self.config.save()
        self.update_proxy()

    def update_pac(self, widget):
        if gfwpac.update():
            dialog = Gtk.MessageDialog(self.server_setting, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "成功")
            dialog.format_secondary_text(
                "GFWList 更新成功！")
            dialog.run()
            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(self.server_setting, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.OK, "错误")
            dialog.format_secondary_text(
                "GFWList 更新失败！")
            dialog.run()
            dialog.destroy()

    def build_menu(self):
        self.menu = Gtk.Menu()

        self.status_item = Gtk.MenuItem('Shadowsocks：关闭')
        self.status_item.set_sensitive(False)
        self.menu.append(self.status_item)

        self.switch_item = Gtk.MenuItem('打开 Shadowsocks')
        self.switch_item.connect('activate', self.switch)
        self.menu.append(self.switch_item)

        self.update_status()

        self.menu.append(Gtk.SeparatorMenuItem())

        group = []
        self.autoproxy_item = Gtk.RadioMenuItem.new_with_label(group, '自动代理模式')
        self.menu.append(self.autoproxy_item)
        self.autoproxy_item.connect('activate', self.proxy_active)

        group = self.autoproxy_item.get_group()
        self.wholeproxy_item = Gtk.RadioMenuItem.new_with_label(group, '全局模式')
        self.menu.append(self.wholeproxy_item)
        self.wholeproxy_item.connect('activate', self.proxy_active)

        gb = self.config.get('global', False)


        self.autoproxy_item.set_active(not gb)
        self.wholeproxy_item.set_active(gb)


        self.menu.append(Gtk.SeparatorMenuItem())

        self.server_item = Gtk.MenuItem('服务器')
        self.menu.append(self.server_item)
        self.server_submenu = Gtk.Menu()
        self.server_item.set_submenu(self.server_submenu)

        self.menu.append(Gtk.SeparatorMenuItem())

        self.editpac_item = Gtk.MenuItem('编辑自动模式的 PAC...')
        self.editpac_item.connect('activate', self.open_pac_folder)
        self.menu.append(self.editpac_item)

        self.updatepac_item = Gtk.MenuItem('从 GFWList 更新 PAC')
        self.updatepac_item.connect('activate', self.update_pac)
        self.menu.append(self.updatepac_item)

        self.editrule_item = Gtk.MenuItem('编辑 GFWList 的用户规则...')
        self.editrule_item.connect('activate', self.open_pac_folder)
        self.menu.append(self.editrule_item)

        self.menu.append(Gtk.SeparatorMenuItem())

        self.exit_item = Gtk.MenuItem('退出')
        self.menu.append(self.exit_item)
        self.exit_item.connect('activate', self.exit)

    def exit(self, widget):
        self.stop()
        Gtk.main_quit()
        sys.exit()

    def show_server_setting(self, widget):
        self.server_setting.run()

    def open_pac_folder(self, widget):
        subprocess.Popen(['xdg-open', self.config.path])

    def show_all(self):
        self.menu.show_all()

    def update_status(self):
        if self.enabled:
            self.status_item.set_label('Shadowsocks：打开')
            self.switch_item.set_label('关闭 Shadowsocks')
        else:
            self.status_item.set_label('Shadowsocks：关闭')
            self.switch_item.set_label('打开 Shadowsocks')

    def switch(self, widget):
        self.enabled = not self.enabled
        self.config['enabled'] = self.enabled
        self.config.save()
        self.update_status()
        if self.enabled:
            self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.stop()
            self.start()
        else:
            self.indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
            self.stop()