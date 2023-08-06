from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QTimer

from ServerAPP.server.del_user import DelUserDialog
from ServerAPP.server.reg_user import RegisterUser


def create_stat_model(database):
    hist_list = database.message_history()
    dataset = QStandardItemModel()
    dataset.setHorizontalHeaderLabels(['Client Name', 'Last login', 'Sent messages', 'Received messages'])
    for row in hist_list:
        user, last_seen, sent, recvd = row
        user = QStandardItem(user)
        user.setEditable(False)
        last_seen = QStandardItem(str(last_seen.replace(microsecond=0)))
        last_seen.setEditable(False)
        sent = QStandardItem(str(sent))
        sent.setEditable(False)
        recvd = QStandardItem(str(recvd))
        recvd.setEditable(False)
        dataset.appendRow([user, last_seen, sent, recvd])
    return dataset


class MainWindow(QMainWindow):
    """
    Main server window class.
    """
    def __init__(self, database, server, config):
        super().__init__()
        self.database = database
        self.server_thread = server
        self.config = config
        self.initUI()

    def initUI(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.refresh_button = QAction('Refresh', self)
        self.config_btn = QAction('Server settings', self)
        self.register_btn = QAction('Register user', self)
        self.remove_btn = QAction('Remove user', self)
        self.show_history_button = QAction('Client history', self)
        self.statusBar()
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.remove_btn)
        self.setFixedSize(800, 600)
        self.setWindowTitle('Python-messenger. Release candidate.')
        self.label = QLabel('Online clients:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)
        self.timer = QTimer()
        self.timer.timeout.connect(self.gui_create_model)
        self.timer.start(1000)
        self.refresh_button.triggered.connect(self.gui_create_model)
        self.register_btn.triggered.connect(self.reg_user)
        self.remove_btn.triggered.connect(self.rem_user)
        self.show()

    def reg_user(self):
        """
        Register user window create method.
        :return:
        """
        global reg_window
        reg_window = RegisterUser(self.database, self.server_thread)
        reg_window.show()

    def rem_user(self):
        """
        Remove user window create method.
        :return:
        """
        global rem_window
        rem_window = DelUserDialog(self.database, self.server_thread)
        rem_window.show()

    def gui_create_model(self):
        """
        Fill active users table method.
        :return:
        """
        list_users = self.database.active_users_list()
        dataset = QStandardItemModel()
        dataset.setHorizontalHeaderLabels(['Client name', 'IP address', 'Port', 'Login time'])
        for row in list_users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            dataset.appendRow([user, ip, port, time])
        self.active_clients_table.setModel(dataset)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()


class HistoryWindow(QDialog):
    """
    History window class.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Client statistics')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.close_button = QPushButton('Close', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)
        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)
        self.show()


class ConfigWindow(QDialog):
    """
    Configuration window class.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Server settings')
        self.db_path_label = QLabel('Database file path: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)
        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)
        self.db_path_select = QPushButton('Browse...', self)
        self.db_path_select.move(275, 28)
        self.db_path_select.clicked.connect(self.open_file_dialog)
        self.db_file_label = QLabel('Database filename: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)
        self.db_file = QLineEdit(self)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)
        self.port_label = QLabel('Bind port:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)
        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)
        self.ip_label = QLabel('Bind IP:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)
        self.ip_label_note = QLabel('Blank this field to bind all IP.', self)
        self.ip_label_note.move(10, 168)
        self.ip_label_note.setFixedSize(500, 30)
        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)
        self.save_btn = QPushButton('Save' , self)
        self.save_btn.move(190 , 220)
        self.close_button = QPushButton('Close', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)
        self.show()

    def open_file_dialog(self):
        """
        Open file dialogue method.
        :return:
        """
        global dialog
        dialog = QFileDialog(self)
        path = dialog.getExistingDirectory()
        path = path.replace('/', '\\')
        self.db_path.insert(path)
