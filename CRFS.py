from serial import Serial
from threading import Thread
from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus, ProtocolStats
from time import sleep


class CrfsInterface:

    def __init__(self):
        self._port = None
        self._package_received_callback = None
        self._on_status_changed_callback = None
        self._thread = None
        self._is_running = False
        self._current_status = ProtocolStats()

    def connect(self, port_name, baud_rate):
        try:
            self._port = Serial(port_name, baud_rate, timeout=2)
        except Exception as e:
            print(e)
            return False
        return True

    def on_packet_received(self, callback):
        self._package_received_callback = callback

    def on_status_update(self, callback):
        self._on_status_changed_callback = callback

    def _reformat_result_and_notify_callback(self, frame: Container, status: PacketValidationStatus):
        self._package_received_callback(frame.header.type, frame.payload)

    def listen(self):
        self._is_running = True
        self._thread = Thread(target=self._listen_uart)
        self._thread.start()

    def stop_listening(self):
        self._is_running = False
        self._thread.join()

    def _listen_uart(self):
        parser = CRSFParser(self._reformat_result_and_notify_callback)
        input = bytearray()
        i = 0
        while self._is_running:
            buf = self._port.read(100)
            input.extend(buf)
            parser.parse_stream(input)
            i += 1
            if i % 10 == 0:
                self._check_status_and_notify_callback(parser)

    def _check_status_and_notify_callback(self, parser):
        if self._on_status_changed_callback:
            status = parser.get_stats()
            if status != self._current_status:
                self._current_status = status
                self._on_status_changed_callback(status)

    def get_status(self):
        return self._current_status

