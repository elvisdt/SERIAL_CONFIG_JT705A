# tools/serial_cli_test.py
import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtSerialPort import QSerialPort
from app.core.serial_manager import SerialManager

def hexdump(b: bytes) -> str:
    return " ".join(f"{x:02X}" for x in b)

def main():
    app = QtWidgets.QApplication(sys.argv)
    mgr = SerialManager(scan_interval_ms=1500, auto_reconnect=False)

    mgr.ports_updated.connect(lambda ports: print("[ports]", ports))
    mgr.connection_changed.connect(lambda ok, p: print(f"[conn] {'OPEN' if ok else 'CLOSED'} {p}"))
    mgr.error_occurred.connect(lambda msg, p: print(f"[error] {p}: {msg}"))
    mgr.data_received.connect(lambda data, p: print(f"[rx {p}] {hexdump(data)} | {data!r}"))
    mgr.data_sent.connect(lambda data, p: print(f"[tx {p}] {hexdump(data)} | {data!r}"))

    if len(sys.argv) < 2:
        print("Puertos disponibles:")
        for p in mgr.get_list_ports():
            print(" -", p, mgr.get_port_info(p))
        print("\nUso: python -m test.test_serial COMx [baud]")
        # python -m test.test_serial COM1 115200
        sys.exit(0)

    port = sys.argv[1]
    baud = int(sys.argv[2]) if len(sys.argv) > 2 else 115200

    ok = mgr.open_port(port, settings={'baud_rate': baud})
    if not ok:
        sys.exit(2)

    # envía ping cada 2s
    timer = QTimer()
    timer.timeout.connect(lambda: mgr.send_data_str("PING"))
    timer.start(2000)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
