# Hands-on Cyber OT

*h4ck3d X 2026 · Universidad de Palermo + Securetia*

**Una evaluación de Red Team OT contra la distribuidora eléctrica ficticia DEPSA.**

> Conviene leer esta guía **antes** del workshop y llegar con todo funcionando. El equipamiento es liviano (megabytes, no gigabytes) y se ejecuta en la propia notebook: **no hace falta descargar ninguna máquina virtual**. Si se completa el *control previo* del final, todo está listo.

---

## 1. Qué traer

- **Notebook** con permisos de **administrador** (necesarios para instalar y para que Wireshark capture tráfico).
- **~1 GB de disco libre** (las herramientas son pequeñas).
- **No se necesita** una máquina virtual pesada ni un adaptador USB-Ethernet: el hardware real de DEPSA lo opera el instructor en una demostración guiada.

---

## 2. El modelo de laboratorio

Durante el workshop se trabaja sobre dos elementos livianos:

- **Un conjunto de capturas (PCAP):** tráfico de la red OT de DEPSA, que se analiza en Wireshark.
- **Un simulador Modbus** que se levanta en la notebook y representa al **PLC de DEPSA** para la parte activa (escaneo y lectura de registros).

De este modo, todos practican en paralelo, sin tocar ni poner en riesgo equipos reales.

---

## 3. Qué instalar

Todo es gratuito y multiplataforma. Seguir la sección del sistema operativo correspondiente.

**Herramientas:**

| Herramienta | Para qué |
|---|---|
| **Wireshark** | Análisis de tráfico (incluye los disectores de Modbus y S7comm de fábrica). |
| **nmap** | Descubrimiento y scripts NSE industriales (`modbus-discover`, `s7-info`). |
| **Python 3** y `pip` | Entorno para el cliente y el simulador. |
| **pymodbus** | Cliente y servidor/simulador Modbus. **Fijar la versión `3.6.9`** (ver nota abajo). |
| **ModRSSim2** *(opcional)* | Simulador Modbus liviano (ejecutable). Alternativa al servidor de `pymodbus`. Incluido en el repositorio. |
| **python-snap7** *(opcional)* | Interacción con PLC Siemens S7 (requiere la librería nativa `libsnap7`). |

> **Versión de pymodbus:** debe ser **`3.6.9`**. Las versiones 3.8 y posteriores cambiaron la API (nombres de clases y parámetros) y el código del taller no se ejecuta tal cual.

El **conjunto de capturas (PCAP)** del workshop está incluido en el repositorio.

### Windows

1. Instalar **Wireshark** (el instalador incluye **Npcap**; aceptar su instalación).
2. Instalar **nmap** (su instalador también ofrece Npcap).
3. Instalar **Python 3** desde [python.org](https://www.python.org) y marcar la opción **«Add Python to PATH»**.
4. En PowerShell:
```powershell
   py -m pip install pymodbus==3.6.9
```
5. Descargar **ModRSSim2** (ejecutable, incluido en el repositorio).

> **Comandos de Python en Windows:** usar **`py`** (el *Python Launcher*) o **`python`**, **no `python3`**. En Windows, `python3` abre el instalador de la Microsoft Store aunque Python ya esté instalado. Equivalencias: donde se indique `python3 archivo.py`, en Windows es `py archivo.py`; y `pip install ...` es `py -m pip install ...`. Si `python` o `python3` abren la Store, desactivar los alias en **Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones**.

### macOS

```bash
brew install --cask wireshark
brew install nmap python
pip3 install pymodbus==3.6.9
```

*(ModRSSim2 es de Windows; en macOS, utilizar el servidor de `pymodbus` del control previo.)*

### Linux (Debian / Ubuntu / Kali)

```bash
sudo apt update && sudo apt install -y wireshark nmap python3-pip
pip3 install pymodbus==3.6.9

# Para capturar sin sudo, agregar el usuario al grupo wireshark:
sudo usermod -aG wireshark "$USER"   # cerrar sesión y volver a entrar

# (opcional) S7:
sudo apt install -y libsnap7-1 && pip3 install python-snap7
```

---

## 4. Reglas de trabajo (importante)

- **El OSINT es observación:** consultar información pública es admisible; iniciar sesión o interactuar con un sistema ajeno, no lo es.
- El **reconocimiento activo** se realiza **únicamente contra el simulador local** (`127.0.0.1`).
- En OT, un **escaneo agresivo puede dejar un equipo fuera de servicio**. La demostración destructiva la realiza **solo el instructor**, sobre hardware de sacrificio.
- El objetivo es **analizar de forma responsable, no dañar**. La disponibilidad y la seguridad operacional están por encima de todo.

---

## 5. Control previo

Abrir una terminal y ejecutar estos comandos. Si responden sin error, todo va bien:

```bash
wireshark --version
nmap --version
python3 -c "import pymodbus; print('pymodbus OK', pymodbus.__version__)"
```

> En **Windows**, la última línea es: `py -c "import pymodbus; print('pymodbus OK', pymodbus.__version__)"`

**Prueba del simulador Modbus** (representa al PLC de DEPSA). En una terminal se levanta el servidor; en otra se confirma el puerto:

```bash
# Terminal 1: levantar un servidor Modbus local en el puerto 502
#   macOS / Linux:
sudo python3 -c "from pymodbus.server import StartTcpServer; StartTcpServer(address=('127.0.0.1', 502))"
#   Windows (PowerShell, sin sudo):
py -c "from pymodbus.server import StartTcpServer; StartTcpServer(address=('127.0.0.1', 502))"

# Terminal 2: confirmar que el puerto está abierto
nmap -p 502 127.0.0.1
```

El **502** es el puerto estándar de Modbus (aparece en las capturas y en el hardware). En **Windows** no requiere administrador; en **macOS o Linux**, abrir el 502 requiere `sudo`. Para evitarlo, levantar el servidor en **5020** (quitar el `sudo` y sustituir `502` por `5020` también en el `nmap`).

Si el puerto aparece abierto, el simulador funciona.

**Prueba de Wireshark y PCAPs:** abrir cualquier archivo del conjunto en Wireshark y confirmar que se ven los paquetes. Si no abre o no captura, revisar **Npcap** (Windows) o el grupo **`wireshark`** (Linux).

Con el simulador a la escucha y un PCAP abierto en Wireshark, todo está listo.

### Checklist

- [ ] `wireshark --version` responde
- [ ] `nmap --version` responde
- [ ] `pymodbus` importa y muestra la versión `3.6.9`
- [ ] El simulador abre el puerto 502 (visible con `nmap`)
- [ ] Un PCAP del conjunto abre en Wireshark

---

## 6. En caso de problemas

Si algo del control previo falla, conviene escribir **antes** del workshop para llegar con todo resuelto. Resolverlo el día del evento consume tiempo de práctica.
