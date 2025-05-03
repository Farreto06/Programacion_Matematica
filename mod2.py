import numpy as np
from scipy.optimize import linear_sum_assignment

class ServerRequestAssignment:
    def __init__(self, cost_matrix, server_capacities, request_priorities):
        """
        Inicializa el problema de asignación de solicitudes a servidores.

        Args:
            cost_matrix (np.array): Matriz de costos C[S][R], donde C[i][j] es el tiempo estimado de procesamiento.
            server_capacities (list): Vector con la capacidad máxima de cada servidor.
            request_priorities (list): Vector con las prioridades de cada solicitud (menor valor = mayor prioridad).
        """
        self.cost_matrix = cost_matrix
        self.server_capacities = server_capacities
        self.request_priorities = request_priorities
        self.num_servers = len(server_capacities)
        self.num_requests = len(request_priorities)

    def adjust_cost_matrix_for_priorities(self):
        """
        Ajusta la matriz de costos para reflejar las prioridades de las solicitudes.
        Las solicitudes con mayor prioridad (menor valor) tendrán costos más bajos.
        """
        # Normalizar las prioridades para que sean un factor multiplicativo
        max_priority = max(self.request_priorities)
        priority_factors = [(max_priority - priority + 1) for priority in self.request_priorities]

        # Ajustar la matriz de costos multiplicando por los factores de prioridad
        adjusted_cost_matrix = self.cost_matrix * np.array(priority_factors)
        return adjusted_cost_matrix

    def balance_problem(self):
        """
        Balancea el problema si el número de servidores y solicitudes no coincide.
        Agrega servidores o solicitudes ficticias con costos altos para evitar asignaciones no deseadas.
        """
        if self.num_servers > self.num_requests:
            # Agregar solicitudes ficticias
            extra_requests = self.num_servers - self.num_requests
            high_cost = np.max(self.cost_matrix) + 1
            self.cost_matrix = np.hstack((self.cost_matrix, np.full((self.num_servers, extra_requests), high_cost)))
            self.request_priorities.extend([float('inf')] * extra_requests)
        elif self.num_requests > self.num_servers:
            # Agregar servidores ficticios
            extra_servers = self.num_requests - self.num_servers
            high_cost = np.max(self.cost_matrix) + 1
            self.cost_matrix = np.vstack((self.cost_matrix, np.full((extra_servers, self.num_requests), high_cost)))
            self.server_capacities.extend([0] * extra_servers)

    def solve_assignment(self):
        """
        Resuelve el problema de asignación utilizando el Método Húngaro.

        Returns:
            tuple: (list, float, dict) - Lista de asignaciones [(servidor, solicitud)],
                                        tiempo total de procesamiento,
                                        carga de trabajo por servidor.
        """
        self.balance_problem()

        # Ajustar la matriz de costos para reflejar las prioridades
        adjusted_cost_matrix = self.adjust_cost_matrix_for_priorities()

        # Aplicar el Método Húngaro
        row_ind, col_ind = linear_sum_assignment(adjusted_cost_matrix)

        # Reconstruir las asignaciones originales
        assignments = [(row, col) for row, col in zip(row_ind, col_ind) if col < self.num_requests]

        # Calcular el tiempo total de procesamiento
        total_processing_time = sum(self.cost_matrix[row, col] for row, col in assignments)

        # Calcular la carga de trabajo por servidor
        workload = {i: 0 for i in range(self.num_servers)}
        for server, request in assignments:
            workload[server] += 1

        return assignments, total_processing_time, workload

    def display_results(self, assignments, total_processing_time, workload):
        """
        Muestra los resultados de la asignación.

        Args:
            assignments (list): Lista de asignaciones [(servidor, solicitud)].
            total_processing_time (float): Tiempo total de procesamiento.
            workload (dict): Carga de trabajo por servidor.
        """
        print("\n--- Resultados de la Asignación ---")
        print("\nLista de asignaciones (Servidor -> Solicitud):")
        for server, request in assignments:
            print(f"Servidor {server} -> Solicitud {request} | Tiempo de procesamiento: {self.cost_matrix[server, request]:.2f}")

        print(f"\nTiempo Total de Procesamiento: {total_processing_time:.2f}")

        print("\nCarga de Trabajo por Servidor:")
        for server, load in workload.items():
            print(f"Servidor {server}: {load} solicitudes asignadas")

        print("\nVerificación de Prioridades y Restricciones:")
        for server, request in assignments:
            print(f"Solicitud {request} (Prioridad: {self.request_priorities[request]}) asignada al Servidor {server}")

def get_input_from_console():
    """Obtiene los datos de entrada desde la consola."""
    while True:
        try:
            s = int(input("Ingrese el número de servidores (S): "))
            if s > 0:
                break
            else:
                print("S debe ser un entero positivo.")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")

    while True:
        try:
            r = int(input("Ingrese el número de solicitudes (R): "))
            if r > 0:
                break
            else:
                print("R debe ser un entero positivo.")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")

    print(f"Ingrese la matriz de costos ({s}x{r}). Ingrese los costos separados por espacios para cada fila:")
    cost_matrix = np.zeros((s, r))
    for i in range(s):
        while True:
            try:
                row_input = input(f"Costos para servidor {i}: ")
                costs = list(map(float, row_input.split()))
                if len(costs) == r:
                    cost_matrix[i, :] = costs
                    break
                else:
                    print(f"Error: Se esperaban {r} costos, pero se ingresaron {len(costs)}. Intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingrese números (pueden ser decimales) separados por espacios.")

    print(f"Ingrese el vector de capacidades de los servidores de tamaño {s}:")
    while True:
        try:
            server_capacities = list(map(int, input("Capacidades (separadas por espacios): ").split()))
            if len(server_capacities) == s:
                break
            else:
                print(f"Error: Se esperaban {s} valores, pero se ingresaron {len(server_capacities)}. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese números enteros separados por espacios.")

    print(f"Ingrese el vector de prioridades de las solicitudes de tamaño {r}:")
    while True:
        try:
            request_priorities = list(map(int, input("Prioridades (separadas por espacios): ").split()))
            if len(request_priorities) == r:
                break
            else:
                print(f"Error: Se esperaban {r} valores, pero se ingresaron {len(request_priorities)}. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese números enteros separados por espacios.")

    return cost_matrix, server_capacities, request_priorities


def get_input_from_file(filepath):
    """Obtiene los datos de entrada desde un archivo."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print(f"Error: El archivo {filepath} debe contener al menos S, R, la matriz de costos, capacidades y prioridades.")
                return None, None, None

            try:
                s = int(lines[0].strip())
                r = int(lines[1].strip())
            except ValueError:
                print(f"Error: Las primeras dos líneas del archivo {filepath} deben ser S y R (enteros).")
                return None, None, None

            if s <= 0 or r <= 0:
                print("Error: S y R deben ser positivos.")
                return None, None, None

            if len(lines) < 2 + s + 2:
                print(f"Error: Faltan filas de costos, capacidades o prioridades en el archivo.")
                return None, None, None

            cost_matrix = np.zeros((s, r))
            for i in range(s):
                try:
                    costs = list(map(float, lines[i + 2].strip().split()))
                    if len(costs) == r:
                        cost_matrix[i, :] = costs
                    else:
                        print(f"Error en la línea {i + 3}: Se esperaban {r} costos, se encontraron {len(costs)}.")
                        return None, None, None
                except ValueError:
                    print(f"Error en la línea {i + 3}: Contiene valores no numéricos.")
                    return None, None, None

            try:
                server_capacities = list(map(int, lines[2 + s].strip().split()))
                if len(server_capacities) != s:
                    print(f"Error: El vector de capacidades debe tener {s} valores, pero tiene {len(server_capacities)}.")
                    return None, None, None
            except ValueError:
                print(f"Error en la línea {2 + s + 1}: Contiene valores no numéricos.")
                return None, None, None

            try:
                request_priorities = list(map(int, lines[3 + s].strip().split()))
                if len(request_priorities) != r:
                    print(f"Error: El vector de prioridades debe tener {r} valores, pero tiene {len(request_priorities)}.")
                    return None, None, None
            except ValueError:
                print(f"Error en la línea {3 + s + 1}: Contiene valores no numéricos.")
                return None, None, None

            return cost_matrix, server_capacities, request_priorities

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filepath}")
        return None, None, None
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return None, None, None

# Ejemplo de uso
if __name__ == "__main__":
    choice = input("¿Desea ingresar datos por consola (C), desde archivo (A) o valores por defecto (D)? ").strip().upper()

    cost_matrix = None
    server_capacities = None
    request_priorities = None

    if choice == 'C':
        cost_matrix, server_capacities, request_priorities = get_input_from_console()
    elif choice == 'A':
        filepath = input("Ingrese la ruta del archivo de entrada: ")
        cost_matrix, server_capacities, request_priorities = get_input_from_file(filepath)
    elif choice == 'D':
        # Valores por defecto
        cost_matrix = np.array([
            [10, 20, 30],
            [15, 25, 35],
            [20, 30, 40]
        ])
        server_capacities = [2, 2, 2]  # Capacidad máxima de cada servidor
        request_priorities = [3, 2, 1]  # Prioridades de las solicitudes (1 = más urgente)
        print("Valores por defecto utilizados.")
    else:
        print("Opción no válida. Saliendo.")
        exit()

    # Crear el problema de asignación
    problem = ServerRequestAssignment(cost_matrix, server_capacities, request_priorities)

    # Resolver el problema
    assignments, total_processing_time, workload = problem.solve_assignment()

    # Mostrar los resultados
    problem.display_results(assignments, total_processing_time, workload)