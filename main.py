import numpy as np
import sys

def solve_assignment_problem(cost_matrix, n, m):
    """
    Asigna tareas a programadores minimizando el costo total.
    Cada tarea se asigna al programador con el menor costo para esa tarea específica.
    Un programador puede ser asignado a múltiples tareas.

    Args:
        cost_matrix (np.array): Matriz de costos C[N][M].
        n (int): Número de programadores.
        m (int): Número de tareas.

    Returns:
        tuple: (dict, float) - Un diccionario con la asignación de tareas por programador
                 y el costo total mínimo.
                 Ejemplo: {0: [1, 3], 1: [0, 2], ...}, 150.0
    """
    if n <= 0 or m <= 0:
        print("Error: El número de programadores y tareas debe ser positivo.")
        return {}, 0.0
    if cost_matrix.shape != (n, m):
        print(f"Error: La dimensión de la matriz de costos debe ser {n}x{m}.")
        return {}, 0.0

    assignment = {} # Diccionario para guardar las tareas asignadas a cada programador
    task_assignment = [-1] * m # Lista para guardar qué programador hace cada tarea
    total_cost = 0.0

    for j in range(m): # Iterar sobre cada tarea
        min_cost_for_task = float('inf')
        best_programmer_for_task = -1

        for i in range(n): # Encontrar el programador más barato para la tarea j
            if cost_matrix[i, j] < min_cost_for_task:
                min_cost_for_task = cost_matrix[i, j]
                best_programmer_for_task = i

        if best_programmer_for_task != -1:
            total_cost += min_cost_for_task
            task_assignment[j] = best_programmer_for_task
            # Añadir la tarea a la lista del programador asignado
            if best_programmer_for_task not in assignment:
                assignment[best_programmer_for_task] = []
            assignment[best_programmer_for_task].append(j)
        else:
            # Esto no debería ocurrir si los costos son finitos
            print(f"Advertencia: No se pudo asignar la tarea {j}.")

    # Asegurarse de que todas las tareas fueron asignadas
    if -1 in task_assignment:
         print("Error: No todas las tareas pudieron ser asignadas.")
         # Podría retornar un error o manejarlo según se necesite
         # Por ahora, se retorna la asignación parcial
         pass


    # Formatear la salida para que incluya programadores sin tareas asignadas
    final_assignment_output = {i: assignment.get(i, []) for i in range(n)}


    return final_assignment_output, total_cost

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

    return cost_matrix, n, m

def get_input_from_file(filepath):
    """Obtiene los datos de entrada desde un archivo."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print(f"Error: El archivo {filepath} debe contener al menos N, M y la matriz.")
                return None, 0, 0

            try:
                n = int(lines[0].strip())
                m = int(lines[1].strip())
            except ValueError:
                print(f"Error: Las primeras dos líneas del archivo {filepath} deben ser N y M (enteros).")
                return None, 0, 0

            if n <= 0 or m <= 0:
                print("Error: N y M deben ser positivos.")
                return None, 0, 0

            if len(lines) < 2 + n:
                print(f"Error: Faltan filas de costos en el archivo. Se esperaban {n} filas.")
                return None, 0, 0

            cost_matrix = np.zeros((n, m))
            for i in range(n):
                try:
                    costs = list(map(float, lines[i + 2].strip().split()))
                    if len(costs) == m:
                        cost_matrix[i, :] = costs
                    else:
                        print(f"Error en la línea {i + 3}: Se esperaban {m} costos, se encontraron {len(costs)}.")
                        return None, 0, 0
                except ValueError:
                    print(f"Error en la línea {i + 3}: Contiene valores no numéricos.")
                    return None, 0, 0
                except IndexError:
                     print(f"Error: Faltan líneas de costos en el archivo. Se esperaban {n} filas después de N y M.")
                     return None, 0, 0


            return cost_matrix, n, m

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filepath}")
        return None, 0, 0
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return None, 0, 0

def main():
    """Función principal del programa."""
    choice = input("¿Desea ingresar datos por consola (C) o desde archivo (A)? ").strip().upper()

    cost_matrix = None
    n = 0
    m = 0

    if choice == 'C' or choice == 'c':
        cost_matrix, n, m = get_input_from_console()
    elif choice == 'A' or choice == 'a':
        filepath = input("Ingrese la ruta del archivo de entrada: ")
        cost_matrix, n, m = get_input_from_file(filepath)
        if cost_matrix is None:
            sys.exit(1) # Salir si hubo error al leer el archivo
    else:
        print("Opción no válida. Saliendo.")
        sys.exit(1)

    # Resolver el problema de asignación
    assignment, total_cost = solve_assignment_problem(cost_matrix, n, m)

    # Mostrar resultados
    if assignment: # Verificar si la asignación no está vacía (indicador de éxito)
        print("\n--- Asignación Óptima ---")
        if not any(assignment.values()): # Si ninguna tarea fue asignada
             print("No se pudo realizar ninguna asignación con los datos proporcionados.")
        else:
            for programmer, tasks in assignment.items():
                if tasks: # Mostrar solo si el programador tiene tareas asignadas
                    task_list = ", ".join(map(str, tasks))
                    print(f"Programador {programmer}: Tareas asignadas -> [{task_list}]")
                else:
                    print(f"Programador {programmer}: Sin tareas asignadas.")

        print(f"\nCosto Total Mínimo de la Asignación: {total_cost:.2f}")

if __name__ == "__main__":
    main()