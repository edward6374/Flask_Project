import psutil
import flaskwebgui
from flask import Flask, render_template

import dbus
session_bus = dbus.SessionBus()
screensaver_list = ['org.gnome.ScreenSaver',
                    'org.cinnamon.ScreenSaver',
                    'org.kde.screensaver',
                    'org.freedesktop.ScreenSaver']

for each in screensaver_list:
    try:
        object_path = '/{0}'.format(each.replace('.', '/'))
        get_object = session_bus.get_object(each, object_path)
        get_interface = dbus.Interface(get_object, each)
        status = bool(get_interface.GetActive())        
        print(status)
    except dbus.exceptions.DBusException:
        pass

app = Flask(__name__)
gui = flaskwebgui.FlaskUI(app=app, server="flask")

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/api/cpu')
def api():
    return str(psutil.cpu_percent(interval=0.1))

if __name__ == "__main__":
#    app.run(debug=True)
    gui.run()
