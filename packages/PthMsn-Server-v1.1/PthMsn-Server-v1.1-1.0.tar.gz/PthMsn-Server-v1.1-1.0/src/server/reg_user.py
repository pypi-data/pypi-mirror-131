from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import hashlib
import binascii


class RegisterUser(QDialog):
    """
    User registration class.
    """
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server
        self.setWindowTitle('Registration')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.label_username = QLabel('Username:', self)
        self.label_username.move(10, 10)
        self.label_username.setFixedSize(150, 15)
        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)
        self.label_passwd = QLabel('Enter password:', self)
        self.label_passwd.move(10, 55)
        self.label_passwd.setFixedSize(150, 15)
        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)
        self.label_conf = QLabel('Retype password:', self)
        self.label_conf.move(10, 100)
        self.label_conf.setFixedSize(150, 15)
        self.client_conf = QLineEdit(self)
        self.client_conf.setFixedSize(154, 20)
        self.client_conf.move(10, 120)
        self.client_conf.setEchoMode(QLineEdit.Password)
        self.btn_ok = QPushButton('Save', self)
        self.btn_ok.move(10, 150)
        self.btn_ok.clicked.connect(self.save_data)
        self.btn_cancel = QPushButton('Exit', self)
        self.btn_cancel.move(90, 150)
        self.btn_cancel.clicked.connect(self.close)
        self.messages = QMessageBox()
        self.show()

    def save_data(self):
        """
        Validation and save data to DB method.
        :return:
        """
        if not self.client_name.text():
            self.messages.critical(self, 'Error', 'Input username.')
        elif self.client_passwd.text() != self.client_conf.text():
            self.messages.critical(self, 'Error', 'Passwords is not match.')
        elif self.database.check_user(self.client_name.text()):
            self.messages.critical(self, 'Error', 'Username is exist.')
        else:
            passwd_bytes = self.client_passwd.text().encode('utf-8')
            salt = self.client_name.text().lower().encode('utf-8')
            passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
            self.database.add_user(self.client_name.text(), binascii.hexlify(passwd_hash))
            self.messages.information(self, 'Success', 'Registration complete.')
            self.server.service_update_lists()
            self.close()
