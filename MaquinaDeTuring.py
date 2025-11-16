import yaml
from typing import List, Dict, Tuple, Optional

class MaquinaDeTuring:
    def __init__(self, estados, alfabeto_lenguaje, alfabeto_cinta, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.alfabeto_lenguaje = alfabeto_lenguaje
        self.alfabeto_cinta = alfabeto_cinta
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.cinta = []
        self.cabezal = 0
        self.estado_actual = estado_inicial
        
        # Validaciones
        if not isinstance(transiciones, list):
            raise ValueError("Las transiciones deben ser una lista.")
        
        for t in transiciones:
            if not isinstance(t, dict):
                raise ValueError("Cada transición debe ser un diccionario.")
            keys = ['state', 'read', 'write', 'move', 'next']
            if not all(key in t for key in keys):
                raise ValueError(f"Cada transición debe contener: {', '.join(keys)}")

    def iniciar_cinta(self, entrada: str):
        # Agregar blank al inicio para marcar inicio de la cinta
        self.cinta = ['_'] + list(entrada) if entrada else ['_']
        # Agregar blanks al final
        self.cinta.extend(['_'] * 50)
        self.cabezal = 1  # Comenzar después del blank inicial
        self.estado_actual = self.estado_inicial

    def obtener_transicion(self, estado: str, simbolo: str) -> Optional[Dict]:
        for t in self.transiciones:
            if t['state'] == estado:
                # Verificar si el símbolo leído coincide
                read_symbols = t['read'] if isinstance(t['read'], list) else [t['read']]
                if simbolo in read_symbols:
                    return t
        return None

    def obtener_descripcion_instantanea(self) -> str:
        # Encontrar el último símbolo a la derecha que no sea blank
        ultimo_no_blanco = len(self.cinta) - 1
        while ultimo_no_blanco > self.cabezal and self.cinta[ultimo_no_blanco] == '_':
            ultimo_no_blanco -= 1
        
        if ultimo_no_blanco < self.cabezal:
            ultimo_no_blanco = self.cabezal
        
        # Construir la descripción instantánea
        izquierda = ''.join(self.cinta[:self.cabezal])
        simbolo_actual = self.cinta[self.cabezal] if self.cabezal < len(self.cinta) else '_'
        derecha = ''.join(self.cinta[self.cabezal + 1:ultimo_no_blanco + 1])
        #Formato: izquierda [estado actual] simbolo actual derecha
        id_str = f"{izquierda}[{self.estado_actual}]{simbolo_actual}{derecha}"
        
        return id_str

    def ejecutar(self, entrada: str, max_pasos: int = 1000) -> Tuple[bool, List[str]]:
        self.iniciar_cinta(entrada)
        ids = []
        # Agregar ID inicial
        ids.append(self.obtener_descripcion_instantanea())

        pasos = 0
        seen = set()
        seen.add(ids[0])

        while pasos < max_pasos:
            # Verificar si estamos en estado de aceptación
            if self.estado_actual in self.estados_aceptacion:
                return True, ids

            # Leer símbolo actual
            simbolo_actual = self.cinta[self.cabezal] if self.cabezal < len(self.cinta) else '_'

            # Buscar transición
            transicion = self.obtener_transicion(self.estado_actual, simbolo_actual)

            if transicion is None:
                # rechazar si no hay transición válida
                return False, ids

            # Aplicar transición y escribir en la cinta
            write_symbols = transicion['write'] if isinstance(transicion['write'], list) else [transicion['write']]
            self.cinta[self.cabezal] = write_symbols[0]

            # Mover cabezal
            movimiento = transicion['move']
            if movimiento == 'R':
                self.cabezal += 1
                # Extender cinta si es necesario
                if self.cabezal >= len(self.cinta):
                    self.cinta.extend(['_'] * 50)
            elif movimiento == 'L':
                self.cabezal = max(0, self.cabezal - 1)

            # Cambiar estado
            self.estado_actual = transicion['next']

            # Agregar nueva descripción instantánea y detectar bucles
            id_str = self.obtener_descripcion_instantanea()
            if id_str in seen:
                # Bucle detectado: devolver rechazado y registros hasta el momento
                print(f"⚠️ Bucle detectado en paso {pasos+1}: estado={self.estado_actual}, cabezal={self.cabezal}")
                return False, ids

            ids.append(id_str)
            seen.add(id_str)

            pasos += 1

        # Límite de pasos alcanzado
        print(f"⚠️ Límite de pasos alcanzado ({max_pasos}). La MT no terminó en ese número de pasos.")
        return False, ids


def cargar_mt_desde_yaml(archivo: str) -> MaquinaDeTuring:
    with open(archivo, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    mt_config = data['mt']
    
    return MaquinaDeTuring(
        estados=mt_config['states'],
        alfabeto_lenguaje=mt_config['input_alphabet'],
        alfabeto_cinta=mt_config['tape_alphabet'],
        transiciones=mt_config['transitions'],
        estado_inicial=mt_config['initial_state'],
        estados_aceptacion=mt_config['accept_states']
    )


def ejecutar_simulacion(archivo_yaml: str):
    with open(archivo_yaml, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Cargar máquina de Turing
    mt = cargar_mt_desde_yaml(archivo_yaml)
    
    # Obtener inputs
    inputs = data.get('inputs', [])
    
    # Ejecutar cada input
    for i, entrada in enumerate(inputs, 1):
        print(f"\n{'=' * 60}")
        print(f"Cadena {i}: Entrada = '{entrada}'")
        print('=' * 60)
        
        aceptada, ids = mt.ejecutar(entrada)
        
        print("\nDescripciones Instantáneas:")
        print("-" * 60)
        for j, id_str in enumerate(ids):
            print(f"Paso {j}: {id_str}")
        
        print("-" * 60)
        if aceptada:
            print(f"La cadena '{entrada}' fue aceptada")
        else:
            print(f"La cadena '{entrada}' fue rechazada")
        print()