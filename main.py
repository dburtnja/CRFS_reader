import sys

from CRFS import CrfsInterface
from window import MainWindow
from PyQt6.QtWidgets import QApplication

from time import sleep

# if __name__ == "__main__":
#     crfs = CrfsInterface()
#
#     if not crfs.connect("COM9", 400000):
#         print("Failed to connect to COM9")
#         exit(-1)
#
#     crfs.on_packet_received(lambda type, payload: print(type, payload))
#     crfs.on_status_update(lambda status: print("Status updated:", status))
#
#     crfs.listen()
#
#     sleep(10)
#
#     crfs.stop_listening()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    crfs = CrfsInterface()

    if not crfs.connect("COM9", 400000):
        print("Failed to connect to COM9")
        exit(-1)

    crfs.on_packet_received(lambda type, payload: window.add_or_update_frame_widget(1, "Title", "text"))
    crfs.on_status_update(lambda status: window.change_status(f"{status}"))

    crfs.listen()

    app.exec()

    crfs.stop_listening()
