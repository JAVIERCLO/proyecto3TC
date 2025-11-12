# main que ejecuta las máquinas de Turing
from MaquinaDeTuring import ejecutar_simulacion


archivo = "config_mt_recon.yaml"

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