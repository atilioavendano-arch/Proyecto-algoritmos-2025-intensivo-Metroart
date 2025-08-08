
#Programa principal del sistema MetroArt, aqui se controla todo el sistema


from catalogo import CatalogoMetroArt

#Muestra el menú principal del sistema.
def mostrar_menu():
    print("\n-------------------------------------------")
    print("         SISTEMA METROART - CATÁLOGO DE OBRAS")
    print("         Metropolitan Museum of Art")
    print("-------------------------------------------")
    print("1. Buscar obras por Departamento")
    print("2. Buscar obras por Nacionalidad del autor")
    print("3. Buscar obras por Nombre del autor")
    print("4. Mostrar detalles de una obra")
    print("5. Limpiar imágenes descargadas")
    print("6. Salir")
    print("------------------------------------")

#Validamos la opcion escogida, ademas de comprobar de que hayan escogido una opcion disponible
def obtener_opcion():

    try:
        opcion = int(input("Seleccione una opción (1-6): "))
        if 1 <= opcion <= 6:
            return opcion
        else:
            print("Opción inválida. Debe ser un número entre 1 y 6.")
            return 0
    except ValueError:
        print("Por favor ingrese un número válido.")
        return 0


# Función principal del programa
def main():

    # Crear instancia del catálogo
    catalogo = CatalogoMetroArt()
    
    # Inicializar el sistema
    print("Bienvenido al Sistema MetroArt")
    print("Inicializando sistema...")
    
    if not catalogo.inicializar():
        print("Error: No se pudo inicializar el sistema. Verifique su conexión a internet.")
        return
    
    # Variable para almacenar la última búsqueda
    ultima_busqueda = []
    
    # Bucle principal del programa
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        
        if opcion == 0:
            continue
            
        try:
            if opcion == 1:
                # Buscar por departamento
                print("\n--- BÚSQUEDA POR DEPARTAMENTO ---")
                ultima_busqueda = catalogo.buscar_obras_por_departamento()
                
            elif opcion == 2:
                # Buscar por nacionalidad
                print("\n--- BÚSQUEDA POR NACIONALIDAD ---")
                ultima_busqueda = catalogo.buscar_obras_por_nacionalidad()
                
            elif opcion == 3:
                # Buscar por artista
                print("\n--- BÚSQUEDA POR ARTISTA ---")
                ultima_busqueda = catalogo.buscar_obras_por_artista()
                
            elif opcion == 4:
                # Mostrar detalles
                print("\n--- DETALLES DE OBRA ---")
                catalogo.mostrar_detalles_obra(ultima_busqueda)
                
            elif opcion == 5:
                # Limpiar imágenes
                print("\n--- LIMPIEZA DE IMÁGENES ---")
                catalogo.limpiar_imagenes_descargadas()
                print("Imágenes limpiadas exitosamente")
                
            elif opcion == 6:
                # Salir
                print("\n¡Gracias por usar MetroArt!")
                print("Desarrollado para el Metropolitan Museum of Art")
                break
                
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario")
            continue
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("Por favor intente nuevamente")
            continue
        
        # Pausa para que el usuario pueda leer los resultados
        if opcion != 6:
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()