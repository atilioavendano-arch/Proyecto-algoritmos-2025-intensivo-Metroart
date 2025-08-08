#Aqui creamos la clase catalogo (la principal del sistema maneja el catalogo del museo)

#importamos los modulos de la api del programa y las imagenes
from met_api_service import MetApiService
from image_service import ImageService


class CatalogoMetroArt:

    def __init__(self):
        self.api_service = MetApiService()
        self.image_service = ImageService()
        self.inicializado = False

    def inicializar(self):
#Inicializa el sistema cargando datos necesarios
#aqui realizamos diferentes comprobaciones en caso de no poder cargar los departamentos o las nacionalidades

        print("--Inicializando el  sistema de MetroArt--")
        print("Cargando Departamentos")
        
        if not self.api_service.cargar_departamentos():
            print("Error: No se pudieron cargar los departamentos")
            return False
            
        print("Cargando las nacionalidades")
        if not self.api_service.cargar_nacionalidades():
            print("Advertencia: Usando nacionalidades por defecto")
            
        self.inicializado = True
        print("--Sistema inicializado correctamente :)--")
        return True



#funcion buscar obras por departamento.

    def buscar_obras_por_departamento(self):        

        if not self.inicializado:
            print("Error: Sistema no inicializado")
            return []
            
        departamentos = self.api_service.get_departamentos()
        
        if not departamentos:
            print("No hay departamentos disponibles")
            return []
            
        # Mostrar lista de departamentos
        print("\n------------------")
        print("DEPARTAMENTOS DISPONIBLES")
        print("----------------")
        
        for i, dept in enumerate(departamentos, 1):
            print(f"{i}. ID: {dept.id_departamento} - {dept.nombre}")
            
        try:
            seleccion = int(input("\nSeleccione el número del departamento: ")) - 1
            
            if 0 <= seleccion < len(departamentos):
                dept_seleccionado = departamentos[seleccion]
                print(f"\nBuscando obras en: {dept_seleccionado.nombre}...")
                
                obras = self.api_service.buscar_obras_por_departamento(
                    dept_seleccionado.id_departamento
                )
                
                self._mostrar_lista_obras(obras)
                return obras
            else:
                print("Selección inválida")
                return []
                
        except ValueError:
            print("Por favor ingrese un número válido")
            return []



#Funcion para buscar obras por nacionalidad del artista.
    def buscar_obras_por_nacionalidad(self):

        if not self.inicializado:
            print("Error: Sistema no inicializado")
            return []
            
        nacionalidades = self.api_service.get_nacionalidades()
        
        if not nacionalidades:
            print("No hay nacionalidades disponibles")
            return []
            
        # Mostrar lista de nacionalidades
        print("\n--------------")
        print("NACIONALIDADES DISPONIBLES")
        print("-------------")
        
        for i, nacionalidad in enumerate(nacionalidades[1:225], 1):  
            print(f"{i}. {nacionalidad}")
            
        try:
            seleccion = int(input("\nSeleccione el número de la nacionalidad: ")) 
            
            if 0 <= seleccion < min(224, len(nacionalidades)):
                nacionalidad_seleccionada = nacionalidades[seleccion]
                print(f"\nBuscando obras de artistas de nacionalidad: {nacionalidad_seleccionada}...")
                
                obras = self.api_service.buscar_obras_por_nacionalidad(nacionalidad_seleccionada)
                
                self._mostrar_lista_obras(obras)
                return obras
            else:
                print("Selección inválida")
                return []
                
        except ValueError:
            print("Por favor ingrese un número válido")
            return []


    def buscar_obras_por_artista(self):

#Funcion para buscar obras por nombre del artista

        if not self.inicializado:
            print("Error: Sistema no inicializado")
            return []
            
        nombre_artista = input("Ingrese el nombre del artista: ").strip()
        
        if not nombre_artista:
            print("Debe ingresar un nombre de artista")
            return []
            
        print(f"\nBuscando obras de: {nombre_artista}...")
        obras = self.api_service.buscar_obras_por_artista(nombre_artista)
        
        self._mostrar_lista_obras(obras)
        return obras



    def mostrar_detalles_obra(self, lista_obras=None):

#funcion para mostrar los detalles completos de una obra específica.

        if not self.inicializado:
            print("Error: Sistema no inicializado")
            return
            
        try:
            id_obra = int(input("Ingrese el ID de la obra: "))
            
            print(f"Obteniendo detalles de la obra ID: {id_obra}...")
            obra = self.api_service.obtener_obra_completa(id_obra)
            
            if obra:
                print(obra.mostrar_detalles())
                
                # Preguntar si desea ver la imagen
                if obra.url_imagen:
                    respuesta = input("¿Desea ver la imagen de la obra? (s/n): ").lower()
                    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                        self.image_service.mostrar_imagen(obra.url_imagen, obra.id_obra)
                else:
                    print("Esta obra no tiene imagen disponible")
            else:
                print("No se encontró la obra con el ID especificado")
                
        except ValueError:
            print("Por favor ingrese un ID válido (número)")



 #funcion para obtener una lista de obras encontradas en el sistema
    def _mostrar_lista_obras(self, obras):


        if not obras:
            print("No se encontraron obras con los criterios especificados")
            return
            
        print(f"\n-------------------------")
        print(f"OBRAS ENCONTRADAS ({len(obras)} resultados)")
        print("-------------------------")
        
        for obra in obras:
            print(f"ID: {obra.id_obra} - {obra.titulo} - Autor: {obra.artista.nombre}")
            


# Limpia las imágenes descargadas del sistema

    def limpiar_imagenes_descargadas(self):

        self.image_service.limpiar_imagenes()