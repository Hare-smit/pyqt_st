import sys
import time

from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QScrollArea
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class MyThread(QThread):
    def __init__(self):
        super().__init__()

class MainWindow(QWidget):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.msg_history = list()

        # 窗体标题和尺寸
        self.setWindowTitle('优惠券新增监测系统')

        # 窗体的尺寸
        self.resize(980, 450)

        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        layout = QVBoxLayout()  #垂直
        #头部按钮
        layout.addLayout(self.init_header())

        #表单区域
        layout.addLayout(self.init_form("请复制放入cookies"))
        layout.addLayout(self.init_form1())

        # #表格区域
        layout.addLayout(self.init_msg())
        #
        # #底部按钮·
        layout.addLayout(self.init_footer())

        self.setLayout(layout)  #让当前窗口使用上面的排列规则

        self.my_signal.connect(self.my_print)


    def my_print(self,str):
        # 更新内容
        print(str)
        self.msg_history.append(str)
        self.msg.setText("<br>".join(self.msg_history))
        self.msg.resize(960, self.msg.frameSize().height() + 15)
        self.msg.repaint()  # 更新内容，如果不更新可能没有显示新内容

    def get_key(self):
        for _ in range(5):
            for i in range(10):
                self.my_signal.emit(str(i))
            time.sleep(1)

    def init_header(self):
        header = QHBoxLayout()
        header.addWidget(QPushButton("开始"))
        header.addWidget(QPushButton("停止"))
        header.addStretch(1)
        return header

    def init_form(self,str,num=None):
        form = QHBoxLayout()
        txt = QLineEdit()
        txt.setPlaceholderText(str)
        form.addWidget(txt)
        if num ==1:
            form.addWidget(QPushButton("确认"))
        return form

    def init_form1(self):
        form = QHBoxLayout()
        txt = QLineEdit()
        txt1 = QLineEdit()
        txt2 = QLineEdit()
        txt3 = QLineEdit()
        txt.setPlaceholderText("关键词：(多个以，分隔开)")
        txt1.setPlaceholderText("价格上限：")
        txt2.setPlaceholderText("价格下限：")
        txt3.setPlaceholderText("免运:100,天猫:105,消保:110,正保:115,七退:120,到付:125")
        btn = QPushButton("确认")
        btn.clicked.connect(self.get_key)
        form.addWidget(txt)
        form.addWidget(txt1)
        form.addWidget(txt2)
        form.addWidget(txt3)
        form.addWidget(btn)
        return form

    def init_msg(self):
        messager = QHBoxLayout()
        self.msg = QLabel("")
        self.msg.resize(960,15)
        self.msg.setWordWrap(True)#自动换行
        self.msg.setAlignment(Qt.AlignTop) #靠上
        # self.msg.setStyleSheet("background-color: yellow; color: black;")
        scroll = QScrollArea()
        scroll.setWidget(self.msg)
        messager.addWidget(scroll)
        return messager


    # def init_table(self):
    #     headers = [("ID", 100), ("姓名", 100), ("邮箱", 200), ("标题", 50), ("状态", 50), ("频率", 100)]
    #     table = QHBoxLayout()
    #     t = QTableWidget(9, len(headers))
    #     for idx, ele in enumerate(headers):
    #         text, width = ele
    #         item = QTableWidgetItem()
    #         item.setText(text)
    #         t.setHorizontalHeaderItem(idx, item)
    #         t.setColumnWidth(idx, width)
    #     table.addWidget(t)
    #     return table

    def init_footer(self):
        footer = QHBoxLayout()
        footer.addWidget(QLabel("待执行"))
        footer.addStretch(1)
        footer.addWidget(QPushButton("初始化"))
        footer.addWidget(QPushButton("重新监测"))
        footer.addWidget(QPushButton("清零"))
        footer.addWidget(QPushButton("邮箱"))
        footer.addWidget(QPushButton("代理"))
        return footer



if __name__ == '__main__':
    app = QApplication(sys.argv)    #创建子对象
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())       #程序进入循环等待状态