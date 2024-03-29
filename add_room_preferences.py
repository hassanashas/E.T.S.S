# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_room_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as mc
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from functools import partial

checkbox_stylesheet = """
QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
}
"""


class Ui_Add_Room_Preferences_Teacher_Window(object):
    def setupUi(self, Add_Room_Preferences_Teacher_Window):
        Add_Room_Preferences_Teacher_Window.setObjectName("Add_Room_Preferences_Teacher_Window")
        Add_Room_Preferences_Teacher_Window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Add_Room_Preferences_Teacher_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color: black; color: white;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(13, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignTop)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.room_preference_teacher_name = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.room_preference_teacher_name.setFont(font)
        self.room_preference_teacher_name.setObjectName("room_preference_teacher_name")
        self.horizontalLayout_2.addWidget(self.room_preference_teacher_name)
        self.updation_message_label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.updation_message_label.setFont(font)
       
        self.updation_message_label.setStyleSheet("color: white;\n"
"background-color: rgb(24, 184, 0);")
        self.updation_message_label.setObjectName("updation_message_label")
        self.horizontalLayout_2.addWidget(self.updation_message_label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignTop)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.updation_message_label.hide()
        self.verticalLayout.addWidget(self.frame_3)
        Add_Room_Preferences_Teacher_Window.setCentralWidget(self.centralwidget)

        self.retranslateUi(Add_Room_Preferences_Teacher_Window)
        QtCore.QMetaObject.connectSlotsByName(Add_Room_Preferences_Teacher_Window)
        try:
            self.DB = mc.connect(host="localhost", user="root", password="", database="timetable_manager")
        except mc.Error as e:
            print("Error")

    def launch_window(self, teacher_id):
        self.checkboxes = []
        self.checkbox_ids = []
        #self.addCheckBox()
        self.get_data(teacher_id)

    # def trigger_state_change(self, checkbox_id):
    #     print(checkbox_id)
    def addCheckBox(self, checkbox_text, checkbox_id, h_layout, checkboxState):
        checkbox = QtWidgets.QCheckBox()
        checkbox.setStyleSheet(checkbox_stylesheet)
        checkbox.setText(checkbox_text)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        checkbox.setFont(font)
        checkbox.setChecked(checkboxState)
        self.checkbox_ids.append(checkbox_id)
        self.checkboxes.append(checkbox)
        #checkbox.stateChanged.connect(partial(self.trigger_state_change, checkbox_id))
        h_layout.addWidget(checkbox)
    def get_data(self, teacher_id):
        mycursor = self.DB.cursor()
        query = "select room_id, room_type, room_name, room_for from tbl_room"
        mycursor.execute(query)
        tablerow = 0
        for row in mycursor.fetchall():
            checkboxState = False
            if tablerow % 4 == 0:
                self.frame_4 = QtWidgets.QFrame(self.frame_3)
                self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame_4.setObjectName("frame_4")
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
            mycur = self.DB.cursor()
            sql = "select * from junc_room_preferences where teacher_id = %s and room_id = %s"
            val = (int(teacher_id), int(row[0]))
            mycur.execute(sql, val)
            mycur.fetchall()
            if (mycur.rowcount > 0):
                checkboxState = True
            self.addCheckBox(str(row[2]), int(row[0]), self.horizontalLayout_3, checkboxState)
            self.horizontalLayout_4.addWidget(self.frame_4)
            tablerow += 1

    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def retranslateUi(self, Add_Room_Preferences_Teacher_Window):
        _translate = QtCore.QCoreApplication.translate
        Add_Room_Preferences_Teacher_Window.setWindowTitle(_translate("Add_Room_Preferences_Teacher_Window", "MainWindow"))
        self.label.setText(_translate("Add_Room_Preferences_Teacher_Window", "Room Preferences"))
        self.room_preference_teacher_name.setText(_translate("Add_Room_Preferences_Teacher_Window", "Teacher Name"))
        self.updation_message_label.setText(_translate("Add_Room_Preferences_Teacher_Window", "Updated Successfully."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Add_Room_Preferences_Teacher_Window = QtWidgets.QMainWindow()
    ui = Ui_Add_Room_Preferences_Teacher_Window()
    ui.setupUi(Add_Room_Preferences_Teacher_Window)
    Add_Room_Preferences_Teacher_Window.show()
    sys.exit(app.exec_())
