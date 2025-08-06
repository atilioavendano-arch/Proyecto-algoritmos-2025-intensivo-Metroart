
#Clase encargada de interactuar con la API del Metropolitan Museum.


import requests
from artista import Artista
from departamento import Departamento
from obra_de_arte import ObraDeArte


class MetApiService:
#Inicializa el servicio de API.   
    def __init__(self):
        self.base_url = "https://collectionapi.metmuseum.org/public/collection/v1"
        self.departamentos = []
        self.nacionalidades = []

# Carga los departamentos disponibles desde la API
    def cargar_departamentos(self):
        try:
            response = requests.get(f"{self.base_url}/departments")
            if response.status_code == 200:
                data = response.json()
                self.departamentos = []
                for dept_data in data.get('departments', []):
                    departamento = Departamento(
                        id_departamento=dept_data.get('departmentId'),
                        nombre=dept_data.get('displayName', 'Sin nombre')
                    )
                    self.departamentos.append(departamento)
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar departamentos: {e}")
            return False


#Funcion para Carga las nacionalidades desde el archivo drive
    def cargar_nacionalidades(self):
        try:
            # URL del archivo de nacionalidades
            url = "https://drive.google.com/uc?id=1tJEU6_VEeO6xFH8fssSfkw4M8MaN6U5A"
            response = requests.get(url)
            if response.status_code == 200:
                # Procesar el contenido del archivo
                nacionalidades_text = response.text
                self.nacionalidades = [
                    nacionalidad.strip() 
                    for nacionalidad in nacionalidades_text.split('\n') 
                    if nacionalidad.strip()
                ]
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar nacionalidades: {e}")
            # Nacionalidades por defecto en caso de error
            self._cargar_nacionalidades_por_defecto()
            return True


#Carga nacionalidades por defecto en caso de error al descargar el archivo
    def _cargar_nacionalidades_por_defecto(self):
        self.nacionalidades = [
            "American", "French", "Italian", "German", "Spanish", 
            "British", "Dutch", "Japanese", "Chinese", "Russian",
            "Greek", "Egyptian", "Indian", "Mexican", "Brazilian"
        ]


#Busca obras por ID de departamento
    def buscar_obras_por_departamento(self, id_departamento):
        try:
            # Limitar la búsqueda para evitar demasiados resultados
            url = f"{self.base_url}/search?departmentId={id_departamento}&q=*"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                object_ids = data.get('objectIDs', [])
                
                # Limitar a 20 obras para mejor rendimiento
                if object_ids:
                    object_ids = object_ids[:20]
                
                return self._obtener_obras_por_ids(object_ids)
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar obras por departamento: {e}")
            return []


#Busca obras por nacionalidad del artista
    def buscar_obras_por_nacionalidad(self, nacionalidad):
        try:
            # Buscar usando la nacionalidad como término de búsqueda
            url = f"{self.base_url}/search?q={nacionalidad}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                object_ids = data.get('objectIDs', [])
                
                # Limitar a 20 obras para mejor rendimiento
                if object_ids:
                    object_ids = object_ids[:20]
                
                obras_encontradas = []
                for obj_id in object_ids:
                    obra = self._obtener_obra_por_id(obj_id)
                    if obra and nacionalidad.lower() in obra.artista.nacionalidad.lower():
                        obras_encontradas.append(obra)
                
                return obras_encontradas
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar obras por nacionalidad: {e}")
            return []


#Busca obras por nombre del artista
    def buscar_obras_por_artista(self, nombre_artista):
        try:
            # Buscar usando el nombre del artista
            url = f"{self.base_url}/search?artistOrCulture=true&q={nombre_artista}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                object_ids = data.get('objectIDs', [])
                
                # Limitar a 20 obras para mejor rendimiento
                if object_ids:
                    object_ids = object_ids[:20]
                
                obras_encontradas = []
                for obj_id in object_ids:
                    obra = self._obtener_obra_por_id(obj_id)
                    if obra and nombre_artista.lower() in obra.artista.nombre.lower():
                        obras_encontradas.append(obra)
                
                return obras_encontradas
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error al buscar obras por artista: {e}")
            return []


# Obtiene los detalles completos de una obra especifica
    def obtener_obra_completa(self, id_obra):
        return self._obtener_obra_por_id(id_obra)


#Funcion  para obtener multiples obras por sus IDs
    def _obtener_obras_por_ids(self, object_ids):

        obras = []
        for obj_id in object_ids:
            obra = self._obtener_obra_por_id(obj_id)
            if obra:
                obras.append(obra)
        return obras


#Funcion para obtener una obra por su ID
    def _obtener_obra_por_id(self, object_id):

        try:
            url = f"{self.base_url}/objects/{object_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # Crear objeto artista
                artista = Artista(
                    nombre=data.get('artistDisplayName', 'Artista desconocido'),
                    nacionalidad=data.get('artistNationality', 'Desconocida'),
                    fecha_nacimiento=data.get('artistBeginDate', ''),
                    fecha_muerte=data.get('artistEndDate', '')
                )
                
                # Buscar departamento correspondiente
                dept_id = data.get('departmentId')
                departamento = self._buscar_departamento_por_id(dept_id)
                
                if not departamento:
                    departamento = Departamento(dept_id, 'Departamento desconocido')
                
                # Crear objeto obra
                obra = ObraDeArte(
                    id_obra=data.get('objectID'),
                    titulo=data.get('title', 'Sin título'),
                    artista=artista,
                    departamento=departamento,
                    clasificacion=data.get('classification', ''),
                    fecha_objeto=data.get('objectDate', ''),
                    url_imagen=data.get('primaryImage', '')
                )
                
                return obra
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener obra {object_id}: {e}")
            return None





    def _buscar_departamento_por_id(self, dept_id):
#Busca un departamento por su ID en la lista cargada.

        for dept in self.departamentos:
            if dept.id_departamento == dept_id:
                return dept
        return None




    def get_departamentos(self):
        
#Obtiene la lista de departamentos cargados.
        return self.departamentos



    def get_nacionalidades(self):

#Obtiene la lista de nacionalidades disponibles.

        return self.nacionalidades