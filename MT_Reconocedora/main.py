# main.py - MT Reconocedora
# Este archivo debe estar en la carpeta MT_Reconocedora/

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar MaquinaDeTuring
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MaquinaDeTuring import ejecutar_simulacion

archivo = str(Path(__file__).parent / "config_mt_recon.yaml")

def main():
    print("\n" + "=" * 70)
    print(" MÁQUINA DE TURING RECONOCEDORA - PALÍNDROMOS")
    print("=" * 70)
    print("\nEsta MT reconoce palíndromos sobre el alfabeto {a, b}")
    print("Un palíndromo se lee igual de izquierda a derecha que de derecha a izquierda\n")
    
    try:
        ejecutar_simulacion(archivo)
        print("\n" + "=" * 70)
        print(" FIN DE LA SIMULACIÓN")
        print("=" * 70 + "\n")
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el archivo '{archivo}'")
        print("Asegúrate de que el archivo esté en la misma carpeta que este script.\n")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}\n")

if __name__ == "__main__":
    main()