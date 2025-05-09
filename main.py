import sys
import os
user_name = 'Артём'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = f'C:/Users/{user_name}/PycharmProjects/PythonProject/.venv/Lib/site-packages/PyQt5/Qt5/plugins'
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo
from ui_main import PasswordManager
from db import init_db


def set_qt_plugin_path():
    if 'QT_QPA_PLATFORM_PLUGIN_PATH' in os.environ:
        return

    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'Qt', 'plugins'),
        os.path.join(QLibraryInfo.location(QLibraryInfo.PrefixPath), 'plugins'),
        os.path.join(QLibraryInfo.location(QLibraryInfo.PrefixPath), 'qt5', 'plugins'),
    ]

    for path in possible_paths:
        platforms_path = os.path.join(path, 'platforms')
        if os.path.exists(platforms_path):
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path
            break


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    set_qt_plugin_path()

    if not os.path.exists('data'):
        os.makedirs('data')

    init_db()

    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec_())