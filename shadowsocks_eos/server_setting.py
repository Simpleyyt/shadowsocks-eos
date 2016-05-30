# coding: utf-8
import json
from gi.repository import Gtk


class ServerSetting(Gtk.Window):

    def __init__(self, app, *args, **kwargs):
        super(Gtk.Window, self).__init__(*args, **kwargs)
        self.app = app
        headerbar = Gtk.HeaderBar()
        headerbar.props.show_close_button = True
        headerbar.set_title('服务器设定')
        self.set_titlebar(headerbar)
        self.connect('delete-event', self.delete_event)
        self.build_ui()

        self.props.resizable = False
        self.set_size_request (640, 480)

    def run(self):
        self.show_all()
        self.load_config()

        if len(self.server_store) == 0:
            self.set_sensitive(False)
        else:
            self.server_list.set_cursor(0)

    def load_config(self):
        configs = self.app.get_config().get('configs', [])
        self.server_store.clear()
        for config in configs:
            self.server_store.append(['', json.dumps(config)])
        self.update_list()

    def commit(self, widget):
        if not self.is_validate():
            return
        model, path = self.server_list.get_selection().get_selected()
        self.update_model(model, path)
        configs = []
        for server in self.server_store:
            configs.append(json.loads(server[1]))
        self.app.get_config()['configs'] = configs
        self.app.get_config().save()
        self.app.load_servers()
        return self.hide_on_delete()

    def clear(self):
        self.port_entry.set_text('')
        self.ip_entry.set_text('')
        self.password_entry.set_text('')
        self.remarks_entry.set_text('')
        self.method_combo.set_active(0)

    def add_server(self, widget):
        if len(self.server_store) and not self.is_validate():
            return
        self.set_sensitive(True)
        self.server_store.append(['New Server', '{}'])
        self.server_list.set_cursor(len(self.server_store) - 1)
        self.clear()

    def update_model(self, model, path):
        port = self.port_entry.get_text()
        config = {
            'server': self.ip_entry.get_text(),
            'port': int(port) if port.isdigit() else 0,
            'password': self.password_entry.get_text(),
            'method': self.method_combo.get_active_text(),
            'remarks': self.remarks_entry.get_text()
        }
        model[path][1] = json.dumps(config)

    def update_list(self):
        for server in self.server_store:
            config = json.loads(server[1])
            if 'server' in config and config['server'] != '':
                server[0] = config['server']
        cursor = self.server_list.get_cursor()

    def update_entry(self):
        model, path = self.server_list.get_selection().get_selected()
        config = json.loads(model[path][1])
        self.port_entry.set_text(str(config.get('port', '')))
        self.ip_entry.set_text(config.get('server', ''))
        self.password_entry.set_text(config.get('password', ''))
        self.remarks_entry.set_text(config.get('remarks', ''))
        self.method_combo.set_active(self.methods.index(config.get('method', 'table')))


    def is_validate(self):
        if self.port_entry.get_text() == '' or \
                not self.port_entry.get_text().isdigit():
            return False
        if self.ip_entry.get_text() == '':
            return False
        if self.password_entry.get_text() == '':
            return False
        return True

    def select_func(self, selection, model, path, path_currently_selected):
        if path_currently_selected and not self.is_validate():
            return False
        if path_currently_selected:
            self.update_model(model, path)
            self.update_list()
        return True

    def remove_server(self, widget):
        if len(self.server_store) == 0:
            return
        model, path = self.server_list.get_selection().get_selected()
        model.remove(path)
        if len(self.server_store) == 0:
            self.clear()
            self.set_sensitive(False)
        else:
            self.method_combo.set_active(0)
            self.cursor_changed(self.method_combo)

    def cursor_changed(self, widget):
        if len(self.server_store) == 0:
            return
        self.update_entry()

    def build_ui(self):
        self.vbox = Gtk.VBox(spacing = 15, margin = 15)
        self.add(self.vbox)

        # ok and cancel button

        hbox = Gtk.HBox(spacing = 10)
        self.vbox.pack_end(hbox, False, False, 0)

        self.ok_button = Gtk.Button(label = '确定')
        self.ok_button.connect('clicked', self.commit)
        self.cancel_button = Gtk.Button(label = '取消')
        self.cancel_button.connect('clicked', self.delete_event)
        self.ok_button.set_size_request(85, 30)
        self.cancel_button.set_size_request(85, 30)

        hbox.pack_end(self.ok_button, False, False, 0)
        hbox.pack_end(self.cancel_button, False, False, 0)

        # main content

        self.grid = Gtk.Grid(column_spacing = 10)
        self.vbox.pack_start(self.grid, True, True, 0)

        # list view content

        frame = Gtk.Frame()
        vbox = Gtk.VBox(expand = True)

        vbox.set_halign(Gtk.Align.FILL)
        vbox.set_valign(Gtk.Align.FILL)

        self.server_store = Gtk.ListStore(str, str)
        self.server_list = Gtk.TreeView(self.server_store, expand = True)
        self.server_list.set_headers_visible(False)
        self.server_list.connect('cursor-changed', self.cursor_changed)
        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Server', cell, text = 0)
        self.server_list.get_selection().set_select_function(self.select_func)
        self.server_list.append_column(col)
        frame.add(self.server_list)

        # toolbar

        toolbar = Gtk.Toolbar()
        toolbar.set_icon_size(Gtk.IconSize.MENU)
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)

        add_button = Gtk.ToolButton()
        add_button.connect('clicked', self.add_server)
        add_button.set_icon_name("list-add-symbolic")

        remove_button = Gtk.ToolButton()
        remove_button.connect('clicked', self.remove_server)
        remove_button.set_icon_name("list-remove-symbolic")

        toolbar.insert(add_button, -1)
        toolbar.insert(remove_button, -1)

        vbox.pack_start(frame, True, True, 0)
        vbox.pack_end(toolbar, False, False, 0)

        self.grid.attach(vbox, 0, 0, 1, 1)

        # setting content

        grid = Gtk.Grid(expand = True, column_spacing = 5, row_spacing = 15)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.grid.attach(grid, 1, 0, 1, 1)

        label = Gtk.Label('地址：')
        grid.attach(label, 0, 0, 1, 1)
        self.ip_entry = Gtk.Entry()
        grid.attach(self.ip_entry, 1, 0, 1, 1)
        label = Gtk.Label('端口：')
        grid.attach(label, 0, 1, 1, 1)
        self.port_entry = Gtk.Entry(width_chars = 4)
        grid.attach(self.port_entry, 1, 1, 1, 1)

        self.methods = ['table',
                   'rc4', 
                   'rc4-md5', 
                   'aes-128-cfb',
                   'aes-192-cfb',
                   'aes-256-cfb',
                   'bf-cfb',
                   'camellia-128-cfb',
                   'camellia-192-cfb',
                   'camellia-256-cfb',
                   'cast5-cfb',
                   'des-cfb',
                   'idea-cfb',
                   'rc2-cfb',
                   'seed-cfb',
                   'salsa20',
                   'chacha20']

        label = Gtk.Label('加密：')
        grid.attach(label, 0, 2, 1, 1)
        self.method_combo = Gtk.ComboBoxText()
        renderer_text = Gtk.CellRendererText()
        self.method_combo.set_entry_text_column(0)
        for method in self.methods:
            self.method_combo.append_text(method)
        self.method_combo.set_active(0)
        grid.attach(self.method_combo, 1, 2, 1, 1)

        label = Gtk.Label('密码：')
        grid.attach(label, 0, 3, 1, 1)
        self.password_entry = Gtk.Entry()
        grid.attach(self.password_entry, 1, 3, 1, 1)

        label = Gtk.Label('备注：')
        grid.attach(label, 0, 4, 1, 1)
        self.remarks_entry = Gtk.Entry()
        grid.attach(self.remarks_entry, 1, 4, 1, 1)


    def delete_event(self, widget, event = None):
        return self.hide_on_delete()

    def set_sensitive(self, sensitive):
        self.ip_entry.set_sensitive(sensitive)
        self.port_entry.set_sensitive(sensitive)
        self.method_combo.set_sensitive(sensitive)
        self.password_entry.set_sensitive(sensitive)
        self.remarks_entry.set_sensitive(sensitive)