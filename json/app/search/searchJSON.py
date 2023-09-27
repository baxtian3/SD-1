import grpc
import json
import time
import numpy as np
import random
from find_car_by_id import find_car_by_id

class Client:
    def __init__(self, host="master", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        

    def get(self, key, simulated=False):
        t_inicio = time.time()  # Inicio del temporizador

        if not simulated:
            # Simulamos un retraso aletorio de 1 a 3 segundos, con una distribución normal en 2
            delay = np.random.normal(2, 0.5)
            print(f"Key no encontrada en el caché. Esperando {delay:.5f} segundos...")
            time.sleep(delay)

        # Buscar en el JSON
        value = find_car_by_id(int(key))
        value = str(value)
        if value:
            print("Key encontrada en el JSON.")
                
            t_transcurrido = time.time() - t_inicio  # Calcula el tiempo transcurrido
            print(f"Tiempo transcurrido (JSON + delay): {t_transcurrido:.5f} segundos")          
            return value
        else:
            t_transcurrido = time.time() - t_inicio  # Calcula el tiempo transcurrido
            print(f"Tiempo transcurrido: {t_transcurrido:.5f} segundos")
            print("Key no encontrada.")
            return None
    def b_constante(self, n=100): #Consultas con frecuencia constante 1
        # Crear una lista de números únicos entre 1 y 100
        keys_aux = random.sample(range(1, 101), n)
        keys = [str(num) for num in keys_aux]

        ti_busqueda = []  # Lista para almacenar los tiempos individuales de búsqueda

        # Métricas
        t_ncache = 0 

        count = 0
        for key in keys:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Buscando : {count}/{n}")
            t_i = time.time()
            t_ncache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(key)
            t_transcurrido = time.time() - t_i
            ti_busqueda.append(t_transcurrido)

        t_bpromedio = sum(ti_busqueda) / len(ti_busqueda) if ti_busqueda else 0  # Calcula el tiempo medio de búsqueda
                
        print(f"Tiempo total transcurrido (solo JSON): {t_ncache}")
        print(f"Tiempo promedio de búsqueda: {t_bpromedio:.5f} seconds")

    def b_normal(self, n=100): #Consultas con distribución normal
        # Parámetros de la distribución normal
        media = 50  # Media de la distribución (centrada en el rango [1, 100])
        desviacion_estandar = 15  # Desviación estándar de la distribución

        keys_n = np.random.normal(loc=media, scale=desviacion_estandar, size=n) # Generar valores con distribución normal
        keys_a = np.clip(keys_n, 1, 100) # Ajustar los valores al rango [1, 100]
        keys_int = np.round(keys_a).astype(int) # Convertir los valores a enteros si es necesario
        keys = [str(num) for num in keys_int]
        ti_busqueda = []  # Lista para almacenar los tiempos individuales de búsqueda

        # Métricas
        t_ncache = 0 
        
        count = 0
        for key in keys:
            # clear console
            count += 1
            print("\033[H\033[J")
            print(f"Buscando : {count}/{n}")
            t_i = time.time()
            t_ncache += 3 + 0.001  # Estimado de tiempo de búsqueda en JSON
            self.get(key)
            t_transcurrido = time.time() - t_i
            ti_busqueda.append(t_transcurrido)

        t_bpromedio = sum(ti_busqueda) / len(ti_busqueda) if ti_busqueda else 0  # Calcula el tiempo medio de búsqueda
                
        print(f"Tiempo total empleado (solo JSON): {t_ncache}")
        print(f"Tiempo promedio de búsqueda: {t_bpromedio:.5f} seconds")
        

if __name__ == '__main__':

    client = Client()

    while True:
        print("\nEscoge una operación:")
        print("1. Obtener")
        print("2. Simular Búsquedas")
        print("3. Salir")

        choice = input("Ingrese su elección: ")

        if choice == "1":
            key = input("Igresar key: ")
            value = client.get(key)
            if value is not None:
                print(f"Valor: {value}")
        elif choice == "2":
            while True:
                print("\nEscoge una búsqueda:")
                print("1. Constante")
                print("2. Normal")
                print("3. Atrás")

                choice2 = input("Ingrese su elección: ")

                if choice2 == "1":
                    n = int(input("Ingrese el número de búsquedas que desea simular: "))
                    client.b_constante(n)

                elif choice2 == "2":
                    n = int(input("Ingrese el número de búsquedas que desea simular: "))
                    client.b_normal(n)

                elif choice2 == "3":
                    break
                else:
                    print("Elección inválida. Intente de nuevo.")   
        elif choice == "3":
            print("Adióssss!")
            break
        else:
            print("Elección inválida. Intente de nuevo.")