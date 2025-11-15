# main que ejecuta la máquina de Turing alteradora
import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar MaquinaDeTuring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MaquinaDeTuring import ejecutar_simulacion

# Usar ruta absoluta relativa al archivo para que funcione desde cualquier cwd
archivo = str(Path(__file__).parent / "config_mt_alter.yaml")

def main():
    try:
        ejecutar_simulacion(archivo)
        print("\n" + "=" * 70)
    except FileNotFoundError:
        print(f" Error: No se encontró el archivo '{archivo}'")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()