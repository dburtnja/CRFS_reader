import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFrame, QTableWidget


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._frame_widgets = dict()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self._v_layout = QVBoxLayout(self)
        central_widget.setLayout(self._v_layout)

        self._frames_widgets_holder = QVBoxLayout(self)
        # self._frames_widgets_holder.addWidget(CustomLabel("Status:", "Waiting for the update..."))

        self._status_label = CustomLabel("Status:", "Waiting for the update...")
        self._status_label.setFixedHeight(60)
        self._status_layout = QVBoxLayout(self)
        self._status_layout.addWidget(self._status_label)

        self._v_layout.addLayout(self._frames_widgets_holder, stretch=49)
        self._v_layout.addLayout(self._status_layout, stretch=1)

        self.showMaximized()
        self.setFixedSize(self.size())

    def change_status(self, status):
        self._status_label.set_text(status)

    def add_or_update_frame_widget(self, id, title, text):
        print("Updating", self._frame_widgets)
        if id in self._frame_widgets:
            self._frame_widgets[id].set_text(text)
        else:
            self._frame_widgets[id] = CustomLabel(title, text)
            self._add_frame_widget(self._frame_widgets[id])

    def _add_frame_widget(self, widget):
        MAX_W_WIDGETS = 4
        widget_w = self.size().width() / MAX_W_WIDGETS

        self._frames_widgets_holder.addWidget(widget)


class CustomLabel(QFrame):

    def __init__(self, title, default_text):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self._title_label = QLabel(title)
        self._text_label = QLabel(default_text)
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._title_label)
        self._layout.addWidget(self._text_label)
        self.setLayout(self._layout)

    def set_text(self, text):
        self._text_label.setText(text)
