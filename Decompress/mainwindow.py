import sys
import time
from turtle import update
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QHBoxLayout,QWidget,QFormLayout,QLineEdit,QRadioButton,QPushButton,QLabel,QScrollArea
from decompress import DecompressThread
import os

class MainWindow(QWidget):

    def __init__(self,support_type=['zip']):
        super().__init__()
        self.setWindowTitle('自动批量解压软件')
        self.resize(600,400)
        self.support_type=support_type
        self.logs = list()
        self.init_ui()
        self.btnOk.clicked.connect(self.click_ok)
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 表单布局
        formLayout = QFormLayout()
        # 压缩文件所在目录
        self.etSourceDir = QLineEdit()
        self.etSourceDir.setPlaceholderText('注意:根目录太长可能会出现bug')
        formLayout.addRow('压缩文件所在目录',self.etSourceDir)
        # 输出文件夹目录
        self.etDestDir = QLineEdit()
        self.etDestDir.setPlaceholderText('注意:根目录太长可能会出现bug')
        formLayout.addRow('输出文件目录',self.etDestDir)
        # 解压密码
        self.etPassword = QLineEdit()
        self.etPassword.setPlaceholderText('没有密码不填即可')
        formLayout.addRow('解压密码',self.etPassword)
        # 支持压缩文件类型
        supported = '、'.join(self.support_type)
        formLayout.addRow('支持压缩文件类型:',QLabel(supported))
        layout.addLayout(formLayout)

        # log信息
        self.lbLog = QLabel("")
        # self.lbLog.resize(440,15)
        self.lbLog.setWordWrap(True)
        self.scroll = QScrollArea()
        self.scroll.verticalScrollBar().rangeChanged.connect(
            lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )
        ) # 始终显示最后一行
        self.scroll.setWidget(self.lbLog)
        vbLayoutLog = QVBoxLayout()
        vbLayoutLog.addWidget(self.scroll)
        layout.addLayout(vbLayoutLog)
        
        # 确认按钮
        hbLayoutOk = QHBoxLayout()
        hbLayoutOk.addStretch(1)
        self.btnOk = QPushButton('确定')
        hbLayoutOk.addWidget(self.btnOk)
        hbLayoutOk.addStretch(1)
        layout.addLayout(hbLayoutOk)
        self.setLayout(layout)
    
    def click_ok(self):
        sourceDir = self.etSourceDir.text()
        destDir = self.etDestDir.text()
        password = self.etPassword.text()
        if not os.path.isdir(sourceDir):
            self.update_log('无效根目录')
            return
        self.btnOk.setEnabled(False)
        self.decompressThread = DecompressThread(sourceDir,destDir,password)
        self.decompressThread.logSignal.connect(self.update_log)
        self.decompressThread.start()
    
    def update_log(self,text):
        if text=='解压完成！':
            self.btnOk.setEnabled(True)
        self.logs.append(text)
        self.lbLog.setText('<br>'.join(self.logs))
        self.lbLog.adjustSize()
        self.lbLog.repaint()


if __name__=='__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
