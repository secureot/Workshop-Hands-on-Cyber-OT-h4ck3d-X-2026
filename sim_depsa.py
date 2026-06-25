#!/usr/bin/env python3
"""
DEPSA - Simulador del PLC del alimentador AL-07 (Modbus/TCP).
Workshop "Hands-on Cyber OT" (h4ck3d X 2026).

Levanta un servidor Modbus local que representa al PLC de DEPSA para las
partes activas del taller (reconocimiento con nmap y escritura en la Fase 3).

Estado inicial:
  - Bobina 0 = 1            -> interruptor AL-07 CERRADO (con energia).
  - Registros holding 0..2  -> 132, 87, 7  =  13,2 kV / 8,7 A / alimentador 7.

USO:
  python3 sim_depsa.py
  # En otra terminal, para confirmar que esta a la escucha:
  #   nmap -p 502 127.0.0.1     (debe figurar  502/tcp open)

NOTA:
  El 502 es el puerto estandar de Modbus. En macOS o Linux puede requerir
  privilegios; para evitarlo, cambiar 502 por 5020 en la ultima linea (y en
  los comandos del cliente). Requiere pymodbus==3.6.9 (la version fijada en
  el Bloque 0); las versiones 3.8 y posteriores cambian la API.
"""
from pymodbus.server import StartTcpServer
from pymodbus.datastore import (ModbusSlaveContext,
    ModbusServerContext, ModbusSequentialDataBlock)
store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(0, [1] + [0]*99),    # bobina 0 = 1: interruptor AL-07 CERRADO
    hr=ModbusSequentialDataBlock(0, [132,87,7]+[0]*97),  # 13,2 kV / 8,7 A / alimentador 7
    zero_mode=True)   # IMPORTANTE: direccion 0 = indice 0 (sin esto, pymodbus desfasa en 1)
ctx = ModbusServerContext(slaves=store, single=True)
StartTcpServer(context=ctx, address=("127.0.0.1", 502))
