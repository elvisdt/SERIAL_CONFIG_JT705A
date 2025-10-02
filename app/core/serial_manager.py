# app/serial_manager.py
from __future__ import annotations

from typing import Optional, Dict, Any, List
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QIODevice
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo


class SerialManager(QObject):
    """
    Gestor de puerto serie con PyQt6 pensado para UI o CLI:
    - Escaneo periódico de puertos (emite `ports_updated`).
    - Apertura/cierre manual con ajustes (baud, parity, etc.).
    - Reconexión opcional si el mismo puerto reaparece (auto_reconnect=True).
      * Si el usuario cierra manualmente, NO reconecta.
    - Señales: data_received, data_sent, error_occurred, connection_changed, ports_updated.
    - Cierre seguro: limpia buffers, baja DTR/RTS, espera escritura, desconecta señales.
    """

    # Señales Qt
    data_received = pyqtSignal(bytes, str)           # datos, puerto
    data_sent = pyqtSignal(bytes, str)               # datos, puerto
    error_occurred = pyqtSignal(str, str)            # mensaje, puerto
    connection_changed = pyqtSignal(bool, str)       # estado, puerto
    ports_updated = pyqtSignal(list)                 # lista de puertos (["COM7", "COM8", ...])

    # Configuración por defecto
    DEFAULT_SETTINGS: Dict[str, Any] = {
        'baud_rate': 115200,
        'data_bits': QSerialPort.DataBits.Data8,
        'parity': QSerialPort.Parity.NoParity,
        'stop_bits': QSerialPort.StopBits.OneStop,
        'flow_control': QSerialPort.FlowControl.NoFlowControl,
    }

    # Mapa de errores comunes
    ERROR_MAP: Dict[QSerialPort.SerialPortError, str] = {
        QSerialPort.SerialPortError.DeviceNotFoundError: "Dispositivo no encontrado",
        QSerialPort.SerialPortError.PermissionError: "Permiso denegado",
        QSerialPort.SerialPortError.OpenError: "Error al abrir puerto",
        QSerialPort.SerialPortError.WriteError: "Error de escritura",
        QSerialPort.SerialPortError.ReadError: "Error de lectura",
        QSerialPort.SerialPortError.ResourceError: "Puerto desconectado",
        QSerialPort.SerialPortError.UnsupportedOperationError: "Operación no soportada",
        QSerialPort.SerialPortError.TimeoutError: "Timeout",
        QSerialPort.SerialPortError.NotOpenError: "Puerto no abierto",
    }

    def __init__(self, scan_interval_ms: int = 2000, auto_reconnect: bool = True):
        super().__init__()
        self.serial: Optional[QSerialPort] = None
        self.port_name: str = ""                     # puerto objetivo (puede estar cerrado)
        self._last_ports: List[str] = []             # cache para emitir ports_updated solo en cambios
        self._scan_interval_ms = scan_interval_ms
        self._auto_reconnect = auto_reconnect
        self._shutting_down = False

        self._scan_timer = QTimer(self)
        self._scan_timer.timeout.connect(self._scan_ports)
        self._scan_timer.start(self._scan_interval_ms)

    # QObjects y __del__ no son confiables, pero lo dejamos de red de seguridad
    def __del__(self):
        try:
            self.shutdown()
        except Exception:
            pass

    # --------------------
    # ESCANEO DE PUERTOS
    # --------------------
    def _scan_ports(self) -> None:
        ports = self.get_list_ports()
        if ports != self._last_ports:
            self._last_ports = ports
            self.ports_updated.emit(ports)
        self._try_reconnect()

    def get_list_ports(self) -> list[str]:
        """Devuelve los nombres de los puertos disponibles (p.ej., ['COM7', 'COM11'])."""
        return [port.portName() for port in QSerialPortInfo.availablePorts()]

    def get_port_info(self, port_name: str) -> Dict[str, Any]:
        """Devuelve información detallada de un puerto."""
        for port in QSerialPortInfo.availablePorts():
            if port.portName() == port_name:
                return {
                    'description': port.description(),
                    'manufacturer': port.manufacturer(),
                    'serial_number': port.serialNumber(),
                    'vendor_id': port.vendorIdentifier(),
                    'product_id': port.productIdentifier(),
                    'system_location': port.systemLocation(),
                }
        return {}

    # -------------
    # CONEXIÓN
    # -------------
    def open_port(self, port_name: str, settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        Abre un puerto con los ajustes dados o por defecto. Devuelve True/False.
        Si ya había un puerto abierto, lo cierra primero.
        """
        if not port_name:
            self.error_occurred.emit("Nombre de puerto vacío", "")
            return False

        # Prepara QSerialPort
        if self.serial is None:
            self.serial = QSerialPort()
            self.serial.readyRead.connect(self._handle_ready_read)
            self.serial.errorOccurred.connect(self._handle_error)
        elif self.serial.isOpen():
            self.close_port(user_requested=False)

        # Ajustes
        self.serial.setPortName(port_name)
        self.port_name = port_name  # recordar objetivo para posible reconexión
        cfg = {**self.DEFAULT_SETTINGS, **(settings or {})}
        try:
            self.serial.setBaudRate(cfg['baud_rate'])
            self.serial.setDataBits(cfg['data_bits'])
            self.serial.setParity(cfg['parity'])
            self.serial.setStopBits(cfg['stop_bits'])
            self.serial.setFlowControl(cfg['flow_control'])
        except Exception as e:
            self.error_occurred.emit(f"Ajustes inválidos: {e}", port_name)
            return False

        ok = self.serial.open(QIODevice.OpenModeFlag.ReadWrite)
        if ok:
            self.connection_changed.emit(True, port_name)
            # opcional: detener escaneo mientras está abierto (menos ruido)
            self._scan_timer.stop()
            return True

        self.error_occurred.emit(f"No se pudo abrir {port_name}", port_name)
        try:
            self.serial.close()
        except Exception:
            pass
        return False

    def close_port(self, _restart_scan: bool = True, user_requested: bool = True) -> None:
        """
        Cierra el puerto si está abierto y limpia correctamente.
        Si user_requested=True, se limpia `port_name` para no reconectar automáticamente.
        """
        if self.serial:
            try:
                # Evita callbacks durante cierre
                try:
                    self.serial.readyRead.disconnect(self._handle_ready_read)
                except Exception:
                    pass
                try:
                    self.serial.errorOccurred.disconnect(self._handle_error)
                except Exception:
                    pass

                if self.serial.isOpen():
                    # Señales de control (si están soportadas)
                    for fn in (self.serial.setDataTerminalReady, self.serial.setRequestToSend):
                        try:
                            fn(False)
                        except Exception:
                            pass
                    # Vaciar buffers
                    try:
                        self.serial.flush()
                    except Exception:
                        pass
                    try:
                        # clear(AllDirections) en Qt6; fallback a clear() si no está
                        self.serial.clear(QSerialPort.Direction.AllDirections)
                    except Exception:
                        try:
                            self.serial.clear()
                        except Exception:
                            pass
                    try:
                        self.serial.waitForBytesWritten(150)
                    except Exception:
                        pass

                    name = self.port_name
                    self.serial.close()
                    self.connection_changed.emit(False, name)
            finally:
                try:
                    self.serial.deleteLater()
                except Exception:
                    pass
                self.serial = None

        if user_requested:
            # El usuario cerró: no intentes reconectar a este puerto
            self.port_name = ""

        if _restart_scan and not self._shutting_down:
            self._scan_timer.start(self._scan_interval_ms)

    def restart_connection(self) -> None:
        """Reabre el puerto actual (si hay nombre recordado)."""
        if self.port_name:
            self.open_port(self.port_name)

    def _try_reconnect(self) -> None:
        """Reconecta automáticamente si `auto_reconnect=True` y el puerto reaparece."""
        if not self._auto_reconnect:
            return
        if not self.is_connected() and self.port_name:
            if self.port_name in self.get_list_ports():
                self.open_port(self.port_name)

    # -------------
    # ESTADO
    # -------------
    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.isOpen()

    def get_port_name(self) -> str:
        return self.port_name or ""

    def get_current_settings(self) -> Dict[str, Any]:
        if not self.is_connected():
            return {}
        return {
            'baud_rate': self.serial.baudRate(),
            'data_bits': self.serial.dataBits(),
            'parity': self.serial.parity(),
            'stop_bits': self.serial.stopBits(),
            'flow_control': self.serial.flowControl(),
        }

    # -------------
    # ENVÍO
    # -------------
    def send_data_bytes(self, data: bytes) -> None:
        """Envía bytes tal cual."""
        if not self.serial or not self.serial.isOpen():
            self.error_occurred.emit("Puerto no abierto", self.port_name)
            return
        n = self.serial.write(data)
        if n == -1:
            self.error_occurred.emit("Error al escribir datos", self.port_name)
            return
        try:
            self.serial.waitForBytesWritten(100)
        except Exception:
            pass
        if n == len(data):
            self.data_sent.emit(data, self.port_name)
        else:
            self.error_occurred.emit(f"Datos enviados parcialmente ({n}/{len(data)})", self.port_name)

    def send_data_str(self, data: str, append_newline: bool = True, encoding: str = "utf-8") -> None:
        """Envía string (opcionalmente asegura '\\n')."""
        if append_newline and not data.endswith('\n'):
            data += '\n'
        self.send_data_bytes(data.encode(encoding, errors="replace"))

    def send_hex(self, hex_str: str) -> None:
        """
        Envía datos en formato hex ("7E 01 02 7E" o "7E01027E").
        Ignora espacios y valida longitud par.
        """
        s = hex_str.replace(" ", "").strip()
        if len(s) % 2 != 0:
            self.error_occurred.emit("HEX inválido (longitud impar)", self.port_name)
            return
        try:
            data = bytes.fromhex(s)
        except Exception:
            self.error_occurred.emit("HEX inválido (caracteres no hex)", self.port_name)
            return
        self.send_data_bytes(data)

    # -------------
    # RECEPCIÓN
    # -------------
    def _handle_ready_read(self) -> None:
        if self.serial and self.serial.isOpen():
            data = bytes(self.serial.readAll())
            if data:
                self.data_received.emit(data, self.port_name)

    # -------------
    # ERRORES
    # -------------
    def _handle_error(self, error: QSerialPort.SerialPortError) -> None:
        if error == QSerialPort.SerialPortError.NoError:
            return
        msg = self.ERROR_MAP.get(error, f"Error desconocido ({error})")
        self.error_occurred.emit(msg, self.port_name)

        # Cierra ante desconexión del dispositivo o desaparición del puerto
        if error in (QSerialPort.SerialPortError.ResourceError,
                     QSerialPort.SerialPortError.DeviceNotFoundError):
            # user_requested=False -> mantiene port_name para posible reconexión
            self.close_port(user_requested=False)

    # -------------
    # APAGADO
    # -------------
    def shutdown(self) -> None:
        """Cierra y destruye recursos sin reactivar el escaneo."""
        self._shutting_down = True
        try:
            self._scan_timer.stop()
        except Exception:
            pass
        self.close_port(_restart_scan=False, user_requested=True)
