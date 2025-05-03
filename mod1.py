import numpy as np
from scipy.optimize import linear_sum_assignment

class AssignmentProblem:
    def __init__(self, cost_matrix, supply, demand):
        """
        Inicializa el problema de asignación con restricciones de transporte.

        Args:
            cost_matrix (np.array): Matriz de costos C[N][M].
            supply (list): Vector S[N] con la capacidad máxima de tareas por programador.
            demand (list): Vector D[M] con la cantidad de programadores requeridos por cada tarea.
        """
        self.cost_matrix = cost_matrix
        self.supply = supply
        self.demand = demand
        self.n = len(supply)  # Número de programadores
        self.m = len(demand)  # Número de tareas

    def balance_problem(self):
        """
        Balancea el problema de transporte si la oferta y la demanda no coinciden.
        Agrega programadores o tareas ficticias con costo cero si es necesario.
        """
        total_supply = sum(self.supply)
        total_demand = sum(self.demand)

        if total_supply > total_demand:
            # Agregar tareas ficticias
            extra_demand = total_supply - total_demand
            self.cost_matrix = np.hstack((self.cost_matrix, np.zeros((self.n, 1))))
            self.demand.append(extra_demand)
        elif total_demand > total_supply:
            # Agregar programadores ficticios
            extra_supply = total_demand - total_supply
            self.cost_matrix = np.vstack((self.cost_matrix, np.zeros((1, self.m))))
            self.supply.append(extra_supply)

    def solve_transportation_problem(self):
        """
        Resuelve el problema de transporte utilizando el método de costo mínimo.

        Returns:
            tuple: (np.array, float) - Matriz de asignaciones y costo total mínimo.
        """
        self.balance_problem()
        n, m = len(self.supply), len(self.demand)
        allocation = np.zeros((n, m))
        cost_matrix = self.cost_matrix.astype(float)  # Asegurarse de que sea de tipo float
        supply = self.supply[:]
        demand = self.demand[:]

        while np.any(supply) and np.any(demand):
            # Encontrar el costo mínimo en la matriz
            min_cost = np.inf
            min_i, min_j = -1, -1
            for i in range(n):
                for j in range(m):
                    if supply[i] > 0 and demand[j] > 0 and cost_matrix[i, j] < min_cost:
                        min_cost = cost_matrix[i, j]
                        min_i, min_j = i, j

            # Asignar la cantidad máxima posible
            allocation_amount = min(supply[min_i], demand[min_j])
            allocation[min_i, min_j] = allocation_amount
            supply[min_i] -= allocation_amount
            demand[min_j] -= allocation_amount

            # Marcar la celda como procesada
            cost_matrix[min_i, min_j] = np.inf

        # Calcular el costo total
        total_cost = (allocation * self.cost_matrix).sum()
        return allocation, total_cost

    def display_results(self, allocation, total_cost):
        """
        Muestra los resultados de la asignación.

        Args:
            allocation (np.array): Matriz de asignaciones.
            total_cost (float): Costo total mínimo.
        """
        print("\n--- Resultados de la Asignación ---")
        
        # Lista de asignaciones de programadores a tareas con la ubicación correspondiente
        print("\nLista de asignaciones (Programador -> Tarea):")
        detailed_report = []
        for i in range(allocation.shape[0]):
            for j in range(allocation.shape[1]):
                if allocation[i, j] > 0:  # Solo mostrar asignaciones no nulas
                    cost = allocation[i, j] * self.cost_matrix[i, j]
                    detailed_report.append((i, j, allocation[i, j], self.cost_matrix[i, j], cost))
                    print(f"Programador {i} -> Tarea {j} | Cantidad: {allocation[i, j]} | Costo unitario: {self.cost_matrix[i, j]:.2f} | Costo total: {cost:.2f}")

        # Costo total mínimo de asignación y transporte
        print(f"\nCosto Total Mínimo de Asignación y Transporte: {total_cost:.2f}")

        # Reporte detallado de la optimización
        print("\n--- Reporte Detallado de la Optimización ---")
        print(f"{'Programador':<12}{'Tarea':<8}{'Cantidad':<10}{'Costo Unitario':<15}{'Costo Total':<12}")
        print("-" * 60)
        for programmer, task, quantity, unit_cost, total in detailed_report:
            print(f"{programmer:<12}{task:<8}{quantity:<10}{unit_cost:<15.2f}{total:<12.2f}")

        print("\nMatriz de Asignaciones:")
        print(allocation)

def get_input_from_console():
    """Obtiene los datos de entrada desde la consola."""
    while True:
        try:
            n = int(input("Ingrese el número de programadores (N): "))
            if n > 0:
                break
            else:
                print("N debe ser un entero positivo.")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")

    while True:
        try:
            m = int(input("Ingrese el número de tareas (M): "))
            if m > 0:
                break
            else:
                print("M debe ser un entero positivo.")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número entero.")

    print(f"Ingrese la matriz de costos ({n}x{m}). Ingrese los costos separados por espacios para cada fila:")
    cost_matrix = np.zeros((n, m))
    for i in range(n):
        while True:
            try:
                row_input = input(f"Costos para programador {i}: ")
                costs = list(map(float, row_input.split()))
                if len(costs) == m:
                    cost_matrix[i, :] = costs
                    break
                else:
                    print(f"Error: Se esperaban {m} costos, pero se ingresaron {len(costs)}. Intente de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingrese números (pueden ser decimales) separados por espacios.")

    print(f"Ingrese el vector de oferta (capacidad máxima de tareas por programador) de tamaño {n}:")
    while True:
        try:
            supply = list(map(int, input("Oferta (separada por espacios): ").split()))
            if len(supply) == n:
                break
            else:
                print(f"Error: Se esperaban {n} valores, pero se ingresaron {len(supply)}. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese números enteros separados por espacios.")

    print(f"Ingrese el vector de demanda (programadores requeridos por cada tarea) de tamaño {m}:")
    while True:
        try:
            demand = list(map(int, input("Demanda (separada por espacios): ").split()))
            if len(demand) == m:
                break
            else:
                print(f"Error: Se esperaban {m} valores, pero se ingresaron {len(demand)}. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Ingrese números enteros separados por espacios.")

    return cost_matrix, supply, demand


def get_input_from_file(filepath):
    """Obtiene los datos de entrada desde un archivo."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print(f"Error: El archivo {filepath} debe contener al menos N, M, la matriz de costos, oferta y demanda.")
                return None, None, None

            try:
                n = int(lines[0].strip())
                m = int(lines[1].strip())
            except ValueError:
                print(f"Error: Las primeras dos líneas del archivo {filepath} deben ser N y M (enteros).")
                return None, None, None

            if n <= 0 or m <= 0:
                print("Error: N y M deben ser positivos.")
                return None, None, None

            if len(lines) < 2 + n + 2:
                print(f"Error: Faltan filas de costos, oferta o demanda en el archivo.")
                return None, None, None

            cost_matrix = np.zeros((n, m))
            for i in range(n):
                try:
                    costs = list(map(float, lines[i + 2].strip().split()))
                    if len(costs) == m:
                        cost_matrix[i, :] = costs
                    else:
                        print(f"Error en la línea {i + 3}: Se esperaban {m} costos, se encontraron {len(costs)}.")
                        return None, None, None
                except ValueError:
                    print(f"Error en la línea {i + 3}: Contiene valores no numéricos.")
                    return None, None, None

            try:
                supply = list(map(int, lines[2 + n].strip().split()))
                if len(supply) != n:
                    print(f"Error: El vector de oferta debe tener {n} valores, pero tiene {len(supply)}.")
                    return None, None, None
            except ValueError:
                print(f"Error en la línea {2 + n + 1}: Contiene valores no numéricos.")
                return None, None, None

            try:
                demand = list(map(int, lines[3 + n].strip().split()))
                if len(demand) != m:
                    print(f"Error: El vector de demanda debe tener {m} valores, pero tiene {len(demand)}.")
                    return None, None, None
            except ValueError:
                print(f"Error en la línea {3 + n + 1}: Contiene valores no numéricos.")
                return None, None, None

            return cost_matrix, supply, demand

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
    supply = None	
    demand = None

    if choice == 'C' or choice == 'c':
        cost_matrix, supply, demand = get_input_from_console()
    elif choice == 'A' or choice == 'a':
        filepath = input("Ingrese la ruta del archivo de entrada: ")
        cost_matrix, supply, demand = get_input_from_file(filepath)    
    elif choice == 'D' or choice == 'd':
        # Valores por defecto
        cost_matrix = np.array([
            [4, 8, 8],
            [2, 6, 7],
            [3, 5, 9]
        ])
        supply = [3, 2, 4]  # Capacidad máxima de tareas por programador
        demand = [2, 3, 4]  # Programadores requeridos por cada tarea
        print("Valores por defecto utilizados.")
    else:
        print("Opción no válida. Saliendo.")

    # Crear el problema de asignación
    problem = AssignmentProblem(cost_matrix, supply, demand)

    # Resolver el problema
    allocation, total_cost = problem.solve_transportation_problem()

    # Mostrar los resultados
    problem.display_results(allocation, total_cost)