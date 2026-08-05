import csv
import os
import time
import plotext as plt
C_HEADER = '\033[1;96m'  # Cyan negrita
C_PROMPT = '\033[92m'    # Verde
C_INPUT = '\033[93m'     # Amarillo
C_ERROR = '\033[91m'     # Rojo
C_TEXTO = '\033[97m'   # Blanco
RESET = '\033[0m'        # Reset
C_FECHA = '\033[96m'  # Cyan
C_REPS = '\033[94m'   # Azul
C_PESO = '\033[95m'   # Magenta
C_EXIT = '\033[90m'      # Gris oscuro

    
def main():
    menu()

def proximo_id():
    archivo = "ejercicios.csv"
    if os.path.exists("next_id.txt"):
        with open("next_id.txt", "r") as file:
            contenido = file.read().strip()
            
            if contenido == "":
                return 0
            else:
                return int(contenido)
    else:
        datos = cargar_datos(archivo)
        ids = []
        for dato in datos:
            ids.append(int(dato["id"]))
        ultimo = max(ids)
        return ultimo+1

#guardar ejercicios en un archivo
def guardar_ejercicios():
    while True:
        try:
            cantidad = int(input("Introduce el número de ejercicios que deseas guardar: "))
            if cantidad > 0: 
                break
            print("Por favor, introduce un número mayor que 0.")
        except ValueError:
            print("Por favor, introduce un número válido.")
    
    
    
    #verificar si el archivo existe
    if os.path.exists("ejercicios.csv"):
        archivo_existe = True
        id_inicial = proximo_id()
        
        #agregar un id al nuevo registro basado en el último registro
        #ve si el archivo solo tiene header, si es así, inicia el id en 0
        with open("next_id.txt", "w") as file:
            file.write(str(id_inicial + cantidad))
        datos = [{"id": str(id_inicial + i), "fecha": "", "ejercicio": "", "sets": "", "reps": "", "peso": "", "nota": ""} for i in range(cantidad)]
           
    else:
        #inicia el id en 0 si el archivo no existe
        archivo_existe = False
        datos = [{"id": str(i), "fecha": "", "ejercicio": "", "sets": "", "reps": "", "peso": "", "nota": ""} for i in range(cantidad)]
        with open("next_id.txt", "w") as file:
            file.write(str(cantidad))

        

    
   # input de datos 
    for i in range(cantidad):
        print(f"\n{C_HEADER}--- Registrando Ejercicio {i + 1} de {cantidad} ---{RESET}")
        datos[i]["fecha"] = time.strftime("%Y-%m-%d")
        
        datos[i]["ejercicio"] = input(f"{C_PROMPT}Ingresar ejercicio: {C_INPUT}")
        print(RESET, end="") # Resetea el color amarillo después de que el usuario da Enter
        
        while True:
            try:
                sets = int(input(f"{C_PROMPT}Ingresar sets: {C_INPUT}"))
                print(RESET, end="")
                if 1 <= sets:
                    break
                print(f"{C_ERROR}El número de sets debe ser mayor o igual a 1.{RESET}")
            except ValueError:
                # El RESET al inicio evita que el error se pinte de amarillo si falla el casteo a int()
                print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los sets.{RESET}")
        datos[i]["sets"] = str(sets)
        
        while True:
            try:
                reps = int(input(f"{C_PROMPT}Ingresar reps: {C_INPUT}"))
                print(RESET, end="")
                if 1 <= reps:
                    break
                print(f"{C_ERROR}El número de reps debe ser mayor o igual a 1.{RESET}")
            except ValueError:
                print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los reps.{RESET}")
        datos[i]["reps"] = str(reps)
        
        while True:
            try:
                peso = float(input(f"{C_PROMPT}Ingresar peso: {C_INPUT}"))
                print(RESET, end="")
                if 0 <= peso:
                    break
                print(f"{C_ERROR}El peso debe ser mayor o igual a 0.{RESET}")
            except ValueError:
                print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para el peso.{RESET}")
        datos[i]["peso"] = str(peso)
        
        datos[i]["nota"] = input(f"{C_PROMPT}Ingresar nota: {C_INPUT}")
        print(RESET, end="")
    with open("ejercicios.csv", "a", newline="", encoding="utf-8") as file:
        titulos_columnas = ["id", "fecha", "ejercicio", "sets", "reps", "peso", "nota"]
        writer = csv.DictWriter(file, fieldnames=titulos_columnas)
        if not archivo_existe:
            writer.writeheader()
            print("Archivo creado y encabezado escrito.")    
        for dato in datos:
            writer.writerow(dato)
    # seria el "volumen" de entrenamiento, que es la suma de (sets * reps * peso) para todos los ejercicios guardados
    suma_tonelage = sum(int(dato["sets"]) * int(dato["reps"]) * float(dato["peso"]) for dato in datos)
    
    print(f"\n{C_HEADER}--- Ejercicios guardados correctamente ---{RESET}\n")
    print(f"Volumen de entrenamiento: {C_PROMPT}{suma_tonelage}{RESET}")
    pausar()
        

 
        
#ver ejercicios
def ver_ejercicios():
    if not os.path.exists("ejercicios.csv"):
        print(f"\n{C_FECHA}--- Archivo no encontrado ---{RESET}")
        pausar()
    else:
        datos = cargar_datos("ejercicios.csv")
        if datos:
            mostrar_tabla(datos, False)
        else:
            print(f"\n{C_HEADER}--- No hay ejercicios registrados ---{RESET}")
        pausar()
        
        
    
def buscar_por_id(retornar=False):
   
    if not os.path.exists("ejercicios.csv"):
        print(f"\n{C_HEADER}--- Archivo no encontrado ---{RESET}")
        pausar()
    else:    
        while True:   
            valor = input(f"{C_PROMPT}Ingresa el ID a buscar: {C_INPUT}").strip() 
            if not valor.isdigit():  
                print(f"{C_ERROR}Por favor, ingresa un ID válido.{RESET}")  
            else:
                break

        datos_encontrados = []

        with open("ejercicios.csv", "r", newline="", encoding="utf-8") as file:
           reader = csv.DictReader(file)
           for row in reader:
               if row["id"] == valor:
                   datos_encontrados.append(row)
          
           if datos_encontrados:
               print(f"\n{C_HEADER}--- Ejercicios Encontrados ---{RESET}")
               mostrar_tabla(datos_encontrados, True)
           else:
               print(f"\n{C_ERROR}No se encontró un ejercicio con el ID '{valor}'.{RESET}\n")
               pausar()
           if not retornar:    
               pausar()
           else:
               return datos_encontrados

def cargar_datos(archivo = "ejercicios.csv"):
    datos_encontrados = []

    with open(archivo, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:    
            datos_encontrados.append(row)
        return datos_encontrados


     
def buscar_por_nombre(retornar=False,imprimir=True):
    if not os.path.exists("ejercicios.csv"):
        print(f"\n{C_HEADER}--- Archivo no encontrado ---{RESET}")
        pausar()
    else:
        valor = input(f"{C_PROMPT}Ingresa el nombre del ejercicio a buscar: {C_INPUT}").strip()   
                
        datos_encontrados = []

        with open("ejercicios.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ejercicio"].lower() == valor.lower():
                    datos_encontrados.append(row)
            if datos_encontrados and imprimir:
                print(f"\n{C_HEADER}--- Ejercicios Encontrados ---{RESET}")
                mostrar_tabla(datos_encontrados, True)
            elif not datos_encontrados and imprimir:
                print(f"\n{C_ERROR}No se encontró un ejercicio con el nombre '{valor}'.{RESET}\n")
                pausar()
            if not retornar:    
                pausar()
                return
            else:
                return datos_encontrados,valor

#buscar ejercicios
def buscar_ejercicios():
    while True:
        # Menú enmarcado para consistencia visual
        print(f"\n{C_HEADER}================================={RESET}")
        print(f"{C_HEADER}        BUSCAR EJERCICIO         {RESET}")
        print(f"{C_HEADER}================================={RESET}")
        print(f"  [{C_INPUT}1{RESET}] {C_TEXTO}Buscar por ID{RESET}")
        print(f"  [{C_INPUT}2{RESET}] {C_TEXTO}Buscar por Nombre de Ejercicio{RESET}")
        print(f"  [{C_INPUT}0{RESET}] {C_TEXTO}Volver al menú principal{RESET}\n")
        
        opcion = input(f"{C_PROMPT}Selecciona el método de búsqueda: {C_INPUT}").strip()
        print(RESET, end="")
        
        match opcion:
            case "1":
                buscar_por_id()
                break  
            case "2":
                buscar_por_nombre()
                break
            case "0":
                break
            case _:
                # Error handling para opciones inválidas
                print(f"\n{C_ERROR}⚠ Opción inválida. Por favor, ingresa 1, 2 o 0.{RESET}") 
    
    
#eliminar ejercicios
def eliminar_ejercicios():

    while True:
        # Menú enmarcado para consistencia visual
        print(f"\n{C_HEADER}================================={RESET}")
        print(f"{C_HEADER}   BUSCAR PARA ELIMINAR EJERCICIO  {RESET}")
        print(f"{C_HEADER}================================={RESET}")
        print(f"  [{C_INPUT}1{RESET}] {C_TEXTO}Buscar por ID{RESET}")
        print(f"  [{C_INPUT}2{RESET}] {C_TEXTO}Buscar por Nombre de Ejercicio{RESET}")
        print(f"  [{C_INPUT}0{RESET}] {C_TEXTO}Volver al menú principal{RESET}\n")
        
        opcion = input(f"{C_PROMPT}Selecciona el método de búsqueda para eliminar: {C_INPUT}").strip()
        print(RESET, end="")
        
        match opcion:
            case "1":
                eliminar_por_id()
                break  
            case "2":
                eliminar_por_nombre()
                break
            case "0":
                break
            case _:
                # Error handling para opciones inválidas
                print(f"\n{C_ERROR}⚠ Opción inválida. Por favor, ingresa 1, 2 o 0.{RESET}") 
    
    
def eliminar_por_id():
    archivo = "ejercicios.csv"
    if not os.path.exists(archivo):
        print(f"\n{C_HEADER}--- Archivo no encontrado ---{RESET}")
        pausar()
    else:
        valor = input(f"{C_PROMPT}Ingresa el ID del ejercicio a eliminar: {C_INPUT}").strip()
        # guarda los datos 
        todos_los_datos = cargar_datos(archivo)
        registro_a_eliminar = []
        
        for row in todos_los_datos:
            if row['id'] == valor:
                registro_a_eliminar.append(row)  
        if not registro_a_eliminar:
            print(f"\n{C_ERROR}No se encontró un ejercicio con el ID '{valor}'.{RESET}\n")
            pausar()
            return
             
       
                        
        mostrar_tabla(registro_a_eliminar, True)
           
        while True:
            x = input(f"\n{C_PROMPT}¿Deseas eliminar este ejercicio? (s/n): {C_INPUT}").strip().lower()
            print(RESET, end="")
            if x == 's':
                break  # Salimos del bucle para proceder a eliminar
            elif x == 'n':
                print(f"\n{C_HEADER}Operación cancelada. No se eliminó ningún ejercicio.{RESET}\n")
                pausar()
                return
            else:
                print(f"{C_ERROR}Opción inválida. Por favor, ingresa 's' o 'n'.{RESET}")
                    
        updated_rows = [row for row in todos_los_datos if row["id"] != valor]  
        with open(archivo, "w", newline="", encoding="utf-8") as file:
            titulos_columnas = ["id", "fecha", "ejercicio", "sets", "reps", "peso", "nota"]
            writer = csv.DictWriter(file, fieldnames=titulos_columnas)
            writer.writeheader()
            for row in updated_rows:
                writer.writerow(row) 
        print(f"\n{C_HEADER}Ejercicio eliminado correctamente.{RESET}\n")
        pausar()


            
def mostrar_tabla(rows, con_id=True):
    """Imprime una lista de registros como tabla formateada."""
    # el header y el for de filas que ya escribiste, UNA vez
    if con_id:
        header = (
            f"{C_TEXTO}{'ID':<4}{RESET} | "
            f"{C_FECHA}{'Fecha':<12}{RESET} | "
            f"{C_PROMPT}{'Ejercicio':<20}{RESET} | "
            f"{C_INPUT}{'Sets':<6}{RESET} | "
            f"{C_REPS}{'Reps':<6}{RESET} | "
            f"{C_PESO}{'Peso':<8}{RESET} | "
            f"{C_TEXTO}Nota{RESET}"
        )
        
        # 1. Imprimimos el header y el separador UNA SOLA VEZ antes del bucle
        print("\n" + header)
        print("-" * 77)
        
        # 2. Iteramos sobre las filas
        for row in rows:
            row_id = f"{row.get('id', ''):<4}"
            fecha = f"{row.get('fecha', ''):<12}"
            ejercicio = f"{row.get('ejercicio', ''):<20}"
            sets = f"{row.get('sets', ''):<6}"
            reps = f"{row.get('reps', ''):<6}"
            peso = f"{row.get('peso', ''):<8}"
            nota = f"{row.get('nota', '')}"
            
            # 3. Imprimimos solo los datos en cada iteración
            print(f"{row_id} | {fecha} | {ejercicio} | {sets} | {reps} | {peso} | {nota}")
            
        print("\n") # Un salto de línea extra para separar el menú de la tabla
    else:
        header = (
            f"{C_FECHA}{'Fecha':<12}{RESET} | "
            f"{C_PROMPT}{'Ejercicio':<20}{RESET} | "
            f"{C_INPUT}{'Sets':<6}{RESET} | "
            f"{C_REPS}{'Reps':<6}{RESET} | "
            f"{C_PESO}{'Peso':<8}{RESET} | "
            f"{C_TEXTO}Nota{RESET}"
        )
        print("\n" + header)
        print("-" * 70) 
        for row in rows:
            fecha = f"{row.get('fecha', ''):<12}"
            ejercicio = f"{row.get('ejercicio', ''):<20}"
            sets = f"{row.get('sets', ''):<6}"
            reps = f"{row.get('reps', ''):<6}"
            peso = f"{row.get('peso', ''):<8}"
            nota = f"{row.get('nota', '')}"

            print(f"{fecha} | {ejercicio} | {sets} | {reps} | {peso} | {nota}")

        print("\n") # Un salto de línea extra para separar el menú de la tabla
    
    
def pausar():
    """Pausa la ejecución hasta que el usuario presione 'q'."""
    while True:
        print("Presiona 'q' para salir de este menú.")
        salir = input()
        if salir.lower() == 'q':
            break

def eliminar_id(valor, archivo="ejercicios.csv"):
    # guarda los datos 
    todos_los_datos = cargar_datos(archivo)
    
            
    updated_rows = [row for row in todos_los_datos if row["id"] != valor]  
    with open(archivo, "w", newline="", encoding="utf-8") as file:
        titulos_columnas = ["id", "fecha", "ejercicio", "sets", "reps", "peso", "nota"]
        writer = csv.DictWriter(file, fieldnames=titulos_columnas)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow(row) 
    print(f"\n{C_HEADER}Ejercicio eliminado correctamente.{RESET}\n")
    pausar() 
    return
    
    
def eliminar_por_nombre():
    archivo = "ejercicios.csv"
    if not os.path.exists(archivo):
        print(f"\n{C_HEADER}--- Archivo no encontrado ---{RESET}")
        pausar()
    else:
        valor = input(f"{C_PROMPT}Ingresa el nombre del ejercicio a buscar: {C_INPUT}").strip()
        # guarda los datos 
        todos_los_datos = cargar_datos(archivo)
        registro_a_eliminar = []
        opciones_permitidas = []
        
        for row in todos_los_datos:
            if row['ejercicio'].lower() == valor.lower():
                registro_a_eliminar.append(row)
                opciones_permitidas.append(row['id'])
                
        if not registro_a_eliminar:
            print(f"\n{C_ERROR}No se encontró un ejercicio con el nombre '{valor}'.{RESET}\n")
            pausar()
            return
        mostrar_tabla(registro_a_eliminar, True)
        mensage_error = generar_mensaje_error_opciones(opciones_permitidas)
        while True:
            eleccion = input(f"\n{C_PROMPT}¿Cual de estos ejercicio? (escribe el ID): {C_INPUT}").strip().lower()
            print(RESET, end="")
            if eleccion in opciones_permitidas:
                break
            print(f"{C_ERROR}{mensage_error}.{RESET}")  
        eliminar_id(eleccion,archivo)
    return
                
def generar_mensaje_error_opciones(opciones):
    
    elementos_por_linea = 6
    bloques = [
        ",".join(opciones[i:i + elementos_por_linea])
        for i in range(0, len(opciones),elementos_por_linea)
    ]
    opciones_formateadas = "\n".join(bloques)
    mensaje_error =("Opción inválida. Ingresa un número de las opciones permitidas:\n"
                    + opciones_formateadas 
                    )
    return mensaje_error
    
    
def cambiar_por_id():
    datos_encontrados = buscar_por_id(True)
    archivo = 'ejercicios.csv'
    if not datos_encontrados:
        return
    
    while True:
        x = input(f"\n{C_PROMPT}¿Deseas modificar este ejercicio? (s/n): {C_INPUT}").strip().lower()
        print(RESET, end="")
        if x == 's':
            break  # Salimos del bucle para proceder a eliminar
        elif x == 'n':
            print(f"\n{C_HEADER}Operación cancelada. No se eliminó ningún ejercicio.{RESET}\n")
            pausar()
            return
        else:
            print(f"{C_ERROR}Opción inválida. Por favor, ingresa 's' o 'n'.{RESET}")
    
    
    
    print(f"\n{C_HEADER}--- Registrando Ejercicio #id: {datos_encontrados[0]["id"]} ---{RESET}")
    
    datos_encontrados[0]["ejercicio"] = input(f"{C_PROMPT}Ingresar ejercicio: {C_INPUT}")
    print(RESET, end="") # Resetea el color amarillo después de que el usuario da Enter
    
    while True:
        try:
            sets = int(input(f"{C_PROMPT}Ingresar sets: {C_INPUT}"))
            print(RESET, end="")
            if 1 <= sets:
                break
            print(f"{C_ERROR}El número de sets debe ser mayor o igual a 1.{RESET}")
        except ValueError:
            # El RESET al inicio evita que el error se pinte de amarillo si falla el casteo a int()
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los sets.{RESET}")
    datos_encontrados[0]["sets"] = str(sets)
    
    while True:
        try:
            reps = int(input(f"{C_PROMPT}Ingresar reps: {C_INPUT}"))
            print(RESET, end="")
            if 1 <= reps:
                break
            print(f"{C_ERROR}El número de reps debe ser mayor o igual a 1.{RESET}")
        except ValueError:
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los reps.{RESET}")
    datos_encontrados[0]["reps"] = str(reps)
    
    while True:
        try:
            peso = float(input(f"{C_PROMPT}Ingresar peso: {C_INPUT}"))
            print(RESET, end="")
            if 0 <= peso:
                break
            print(f"{C_ERROR}El peso debe ser mayor o igual a 0.{RESET}")
        except ValueError:
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para el peso.{RESET}")
    datos_encontrados[0]["peso"] = str(peso)
    
    datos_encontrados[0]["nota"] = input(f"{C_PROMPT}Ingresar nota: {C_INPUT}")
    print(RESET, end="")
    
    todos_los_datos = cargar_datos(archivo)
    datos_actualizados = []
    for row in todos_los_datos:
        if row['id'] != datos_encontrados[0]["id"]:
            datos_actualizados.append(row)
        else:
            datos_actualizados.append(datos_encontrados[0])

    with open(archivo, "w", newline="", encoding="utf-8") as file:
        titulos_columnas = ["id", "fecha", "ejercicio", "sets", "reps", "peso", "nota"]
        writer = csv.DictWriter(file, fieldnames=titulos_columnas)
        writer.writeheader()
        for row in datos_actualizados:
            writer.writerow(row) 
        print(f"\n{C_HEADER}Ejercicio modificado correctamente.{RESET}\n")

    pausar()
    
def cambiar_por_nombre():
    # array de los nombres coincidentes que busca el usuario
    datos_encontrados = buscar_por_nombre(True)
    if not datos_encontrados:
        return
    archivo = "ejercicios.csv"
    opciones_permitidas = []
    for row in datos_encontrados:
        opciones_permitidas.append(row['id'])
    
    mensage_error = generar_mensaje_error_opciones(opciones_permitidas)
    while True:
        print("¿Cuál de estos deseas cambiar? (Usa los IDs para elegir).")
        eleccion = input(f"{C_PROMPT}Selecciona el ID: {C_INPUT}").strip()
        if eleccion  in opciones_permitidas:
            break
        print(f"{C_ERROR}{mensage_error}.{RESET}")  
    i = 0   
    for row in datos_encontrados:
        if row['id'] == eleccion:
            
            break
        i = i + 1
    
    dato_midificar = datos_encontrados[i]
    x = [dato_midificar]
    mostrar_tabla(x, True)
    while True:
            x = input(f"\n{C_PROMPT}¿Deseas modificar este ejercicio? (s/n): {C_INPUT}").strip().lower()
            print(RESET, end="")
            if x == 's':
                break  # Salimos del bucle para proceder a eliminar
            elif x == 'n':
                print(f"\n{C_HEADER}Operación cancelada. No se eliminó ningún ejercicio.{RESET}\n")
                pausar()
                return
            else:
                print(f"{C_ERROR}Opción inválida. Por favor, ingresa 's' o 'n'.{RESET}")
    
    
    print(f"\n{C_HEADER}--- Registrando Ejercicio #id: {dato_midificar["id"]} ---{RESET}")
        
    dato_midificar["ejercicio"] = input(f"{C_PROMPT}Ingresar ejercicio: {C_INPUT}")
    print(RESET, end="") # Resetea el color amarillo después de que el usuario da Enter
    
    while True:
        try:
            sets = int(input(f"{C_PROMPT}Ingresar sets: {C_INPUT}"))
            print(RESET, end="")
            if 1 <= sets:
                break
            print(f"{C_ERROR}El número de sets debe ser mayor o igual a 1.{RESET}")
        except ValueError:
            # El RESET al inicio evita que el error se pinte de amarillo si falla el casteo a int()
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los sets.{RESET}")
    dato_midificar["sets"] = str(sets)
    
    while True:
        try:
            reps = int(input(f"{C_PROMPT}Ingresar reps: {C_INPUT}"))
            print(RESET, end="")
            if 1 <= reps:
                break
            print(f"{C_ERROR}El número de reps debe ser mayor o igual a 1.{RESET}")
        except ValueError:
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para los reps.{RESET}")
    dato_midificar["reps"] = str(reps)
    
    while True:
        try:
            peso = float(input(f"{C_PROMPT}Ingresar peso: {C_INPUT}"))
            print(RESET, end="")
            if 0 <= peso:
                break
            print(f"{C_ERROR}El peso debe ser mayor o igual a 0.{RESET}")
        except ValueError:
            print(f"{RESET}{C_ERROR}Por favor, ingresa un número válido para el peso.{RESET}")
    dato_midificar["peso"] = str(peso)
    
    dato_midificar["nota"] = input(f"{C_PROMPT}Ingresar nota: {C_INPUT}")
    print(RESET, end="")
    
        
        
    todos_los_datos = cargar_datos(archivo)
    datos_actualizados = []
    for row in todos_los_datos:
        if row['id'] != eleccion:
            datos_actualizados.append(row)
        else:
            datos_actualizados.append(dato_midificar)

    with open(archivo, "w", newline="", encoding="utf-8") as file:
        titulos_columnas = ["id", "fecha", "ejercicio", "sets", "reps", "peso", "nota"]
        writer = csv.DictWriter(file, fieldnames=titulos_columnas)
        writer.writeheader()
        for row in datos_actualizados:
            writer.writerow(row) 
        print(f"\n{C_HEADER}Ejercicio modificado correctamente.{RESET}\n")

    pausar()
        
    

    
        
    
    
            
    
                    
    
    
    
    

#modificar ejercicios
def modificar_ejercicios():
    while True:
        print(f"\n{C_HEADER}================================={RESET}")
        print(f"{C_HEADER}        BUSCAR EJERCICIO         {RESET}")
        print(f"{C_HEADER}================================={RESET}")
        print(f"  [{C_INPUT}1{RESET}] {C_TEXTO}Buscar por ID{RESET}")
        print(f"  [{C_INPUT}2{RESET}] {C_TEXTO}Buscar por Nombre de Ejercicio{RESET}")
        print(f"  [{C_INPUT}0{RESET}] {C_TEXTO}Volver al menú principal{RESET}\n")
        
        opcion = input(f"{C_PROMPT}Selecciona el método de búsqueda: {C_INPUT}").strip()
        print(RESET, end="")
        
        match opcion:
            case "1":
                cambiar_por_id()
                break  
            case "2":
                cambiar_por_nombre()
                break
            case "0":
                break
            case _:
                # Error handling para opciones inválidas
                print(f"\n{C_ERROR}⚠ Opción inválida. Por favor, ingresa 1, 2 o 0.{RESET}") 
    

    

#análisis de ejercicios
def analisis_ejercicios():
    datos, valor = buscar_por_nombre(True, False)
    peso = {}
    for row in datos:
        yy_mm_dd = row["fecha"]
        peso[yy_mm_dd] = row["peso"]
    
    datos_ordenados =  sorted(peso.items())
    
    show_plot(datos_ordenados, valor)
    pausar()

def show_plot(data, nombre_ejercicio):
    plt.clear_figure()
    plt.date_form("Y-m-d") 
    fechas, pesos_texto = zip(*data)
    pesos_numeros = [float(peso) for peso in pesos_texto]
    
    plt.plot(fechas, pesos_numeros, marker="fhd", color="cyan", fillx=True)
    
    plt.title(f"Progreso de peso a lo largo del tiempo: {nombre_ejercicio}")
    plt.xlabel("Fecha")
    plt.ylabel("Peso")
    plt.show()
     
    



def menu():
    # Bucle principal del menú
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

    while True: 
        clear()
        
        # Encabezado del menú
        print(f"{C_HEADER}======================================={RESET}")
        print(f"{C_HEADER}       SISTEMA DE ENTRENAMIENTO        {RESET}")
        print(f"{C_HEADER}======================================={RESET}\n")
        
        # Opciones
        print(f"  [{C_INPUT}1{RESET}] {C_TEXTO}Guardar ejercicios{RESET}")
        print(f"  [{C_INPUT}2{RESET}] {C_TEXTO}Ver ejercicios{RESET}")
        print(f"  [{C_INPUT}3{RESET}] {C_TEXTO}Buscar ejercicios{RESET}")
        print(f"  [{C_INPUT}4{RESET}] {C_TEXTO}Eliminar ejercicios{RESET}")
        print(f"  [{C_INPUT}5{RESET}] {C_TEXTO}Modificar ejercicios{RESET}")
        print(f"  [{C_INPUT}6{RESET}] {C_TEXTO}Análisis de ejercicios{RESET}\n")
        print(f"  [{C_INPUT}0{RESET}] {C_EXIT}Salir{RESET}\n")
        
        while True:
            option = input(f"{C_TEXTO}Selecciona una opción: {C_INPUT}")
            print(RESET, end="")  
            
            if option in ["0", "1", "2", "3", "4", "5", "6"]:
                break
            print(f"{C_ERROR}Opción inválida. Ingresa un número del 0 al 6.{RESET}")  
        clear()
        match option:
            case "1":
                guardar_ejercicios()
            case "2":
                ver_ejercicios()
            case "3":
                buscar_ejercicios()
            case "4":
                eliminar_ejercicios()
            case "5":
                modificar_ejercicios()
            case "6":
                analisis_ejercicios()
            case "0":
                print(f"{C_EXIT}Saliendo del sistema...{RESET}")
            case _:
                print(f"{C_ERROR}Opción inválida{RESET}")     
        if option == "0":
            return  # Salir del bucle y terminar el programa
if __name__ == "__main__":
    main()



