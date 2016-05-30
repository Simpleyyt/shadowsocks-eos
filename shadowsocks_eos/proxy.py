from gi.repository import Gtk, Gio


proxy = Gio.Settings.new('org.gnome.system.proxy')

def set_no_proxy():
	proxy.set_string('mode', 'none')

def set_whole_proxy(ip, port):
	proxy.set_string('mode', 'manual')
	ftp = Gio.Settings.new('org.gnome.system.proxy.ftp')
	http = Gio.Settings.new('org.gnome.system.proxy.http')
	https = Gio.Settings.new('org.gnome.system.proxy.https')
	socks = Gio.Settings.new('org.gnome.system.proxy.socks')

	ftp.set_string('host', '')
	ftp.set_int('port', 0)

	http.set_string('host', '')
	http.set_int('port', 0)

	https.set_string('host', '')
	https.set_int('port', 0)

	socks.set_string('host', ip)
	socks.set_int('port', int(port))

def set_auto_proxy(pac_url):
	proxy.set_string('mode', 'auto')
	proxy.set_string('autoconfig-url', pac_url)