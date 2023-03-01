from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel, QtGui
from PySide2.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QSizeGrip, QGridLayout, QInputDialog, QLineEdit
from jinja2 import Template
import sqlite3
import time
from D_scraper2 import to_do
import D_scraper3
import D_scraper4
import D_scraper5
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

try:
    os.remove(r'test.db')
except:
    print("Can't remove the file...")

try:
    conn = sqlite3.connect(r'test.db')
    conn.execute(
        """CREATE TABLE Classes (class VARCHAR(30), tag VARCHAR(30));""")
    conn.commit()
    conn.execute("""CREATE TABLE urls (id VARCHAR(30));""")
    conn.commit()
except:
    pass


def insert_url_to_sql(the_url):
    conn.execute(f"""INSERT INTO urls VALUES ("{the_url}");""")
    conn.commit()


class Element(QtCore.QObject):
    def __init__(self, name, parent=None):
        super(Element, self).__init__(parent)
        self._name = name

    @property
    def name(self):
        return self._name

    def script(self):
        return ""


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        self.loadFinished.connect(self.onLoadFinished)
        self._objects = []
        self._scripts = []

    def add_object(self, obj):
        self._objects.append(obj)

    @QtCore.Slot(bool)
    def onLoadFinished(self, ok):
        print("Finished loading: ", ok)
        if ok:
            self.load_qwebchannel()
            self.add_objects()

    def load_qwebchannel(self):
        file = QtCore.QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            self.runJavaScript(content.data().decode())
        if self.webChannel() is None:
            channel = QtWebChannel.QWebChannel(self)
            self.setWebChannel(channel)

    def add_objects(self):
        if self.webChannel() is not None:
            objects = {obj.name: obj for obj in self._objects}
            self.webChannel().registerObjects(objects)
            _script = """
            {% for obj in objects %}
            var {{obj}};
            {% endfor %}
            new QWebChannel(qt.webChannelTransport, function (channel) {
            {% for obj in objects %}
                {{obj}} = channel.objects.{{obj}};
            {% endfor %}
            }); 
            """
            self.runJavaScript(
                Template(_script).render(objects=objects.keys()))
            for obj in self._objects:
                if isinstance(obj, Element):
                    self.runJavaScript(obj.script())


class Helper(Element):
    elementClicked = QtCore.Signal(str, str)

    def script(self):
        js = ""
        file = QtCore.QFile(os.path.join(CURRENT_DIR, "xpath_from_element.js"))
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            js = content.data().decode()

        # var xpath = Elements.DOMPath.xPath(target, false);
        js += """
        document.addEventListener('click', function(e) {
            e = e || window.event;
            var target = e.target || e.srcElement;
            var className = target.className;
            var tagName = target.tagName;
            e.preventDefault()
            {{name}}.received_data(className, tagName);
        }, false);"""

        return Template(js).render(name=self.name)

    @QtCore.Slot(str, str)
    def received_data(self, className, tagName):
        self.elementClicked.emit(className, tagName)


class Form(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("test")
        self.setMinimumSize(320, 240)
        self.resize(640, 480)

        self.execute_btn = QtWidgets.QPushButton(self.tr("Execute"))
        self.load_btn = QtWidgets.QPushButton(self.tr("Load"))
        self.url_le = QtWidgets.QLineEdit()
        self.cb = QtWidgets.QComboBox()
        self.view = QtWebEngineWidgets.QWebEngineView()

        self.page = WebEnginePage(self)
        self.view.setPage(self.page)

        classname_helper = Helper("classname_helper")
        classname_helper.elementClicked.connect(self.on_clicked)

        self.page.add_object(classname_helper)

        gridlayout = QtWidgets.QGridLayout(self)
        gridlayout.addWidget(self.execute_btn, 0, 0)
        gridlayout.addWidget(self.url_le, 0, 1)
        gridlayout.addWidget(self.load_btn, 0, 2)
        gridlayout.addWidget(self.cb, 0, 3)
        gridlayout.addWidget(self.view, 1, 0, 4, 0)

        self.cb.addItems(["Select", "2", "3", "4", "5"])

        self.execute_btn.clicked.connect(self.run_myscript)
        self.load_btn.clicked.connect(self.load_the_url)
        self.cb.currentIndexChanged.connect(self.selectionchange)

    def run_myscript(self):
        if self.cb.currentIndex() == 0:
            print("Select something")
        elif self.cb.currentIndex() == 1:
            window.hide()
            app.quit()
            to_do()
        elif self.cb.currentIndex() == 2:
            window.hide()
            app.quit()
            D_scraper3.to_do()
        elif self.cb.currentIndex() == 3:
            window.hide()
            app.quit()
            D_scraper4.to_do()
            pass
        elif self.cb.currentIndex() == 4:
            window.hide()
            app.quit()
            D_scraper5.to_do()
            pass
        else:
            print("Fatal error")

    def selectionchange(self):
        print("Items in the list are :")
        self.combo_value = self.cb.currentText()
        print(self.combo_value)

    def load_the_url(self):
        self.urltext = self.url_le.text()
        for letter in ("(", ")", "'", ",", "True", " "):
            self.urltext = self.urltext.replace(letter, "")
        self.view.load(QtCore.QUrl(self.urltext))

    def on_clicked(self, className, tagName):
        if not className:
            className = ""
        else:
            className = "." + className
        print("on_clicked:", className, tagName)
        conn.execute(
            f"""INSERT INTO Classes VALUES ("{className}", "{tagName}");""")
        conn.commit()
        insert_url_to_sql(self.urltext)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec_())
