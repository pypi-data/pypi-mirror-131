from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class DelUserDialog(QDialog):
    """
    Remove user dialogue class.
    """
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server
        self.setFixedSize(350, 120)
        self.setWindowTitle('Remove user')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.selector_label = QLabel('Choose user to remove:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)
        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)
        self.btn_ok = QPushButton('Remove', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_ok.clicked.connect(self.remove_user)
        self.btn_cancel = QPushButton('Chancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)
        self.messages = QMessageBox()
        self.all_users_fill()

    def all_users_fill(self):
        """
        Fill all user list method.
        :return:
        """
        self.selector.addItems([item[0] for item in self.database.users_list()])

    def remove_user(self):
        """
        Remove user handler method.
        :return:
        """
        self.database.remove_user(self.selector.currentText())
        if self.selector.currentText() in self.server.names:
            sock = self.server.names[self.selector.currentText()]
            del self.server.names[self.selector.currentText()]
            self.server.remove_client(sock)
        self.server.service_update_lists()
        self.messages.information(self, 'Success', 'User removed.')
        self.close()
