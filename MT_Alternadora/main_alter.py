# main que ejecuta la máquina de Turing alteradora
import sys
import os
from pathlib import Path

# Importar MaquinaDeTuring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MaquinaDeTuring import ejecutar_simulacion
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