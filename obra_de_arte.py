#Clase que representa una obra de arte del museo

from artista import Artista
from departamento import Departamento


class ObraDeArte:

#Inicializa un objeto ObraDeArte
    def __init__(self, id_obra, titulo, artista, departamento, clasificacion=None, 
                 fecha_objeto=None, url_imagen=None):
        self.id_obra = id_obra
        self.titulo = titulo
        self.artista = artista
        self.departamento = departamento
        self.clasificacion = clasificacion
        self.fecha_objeto = fecha_objeto
        self.url_imagen = url_imagen


#Representacion en string de la obra
    def __str__(self):
        return f"ID: {self.id_obra} - {self.titulo} por {self.artista.nombre}"



#Representacion en string de la obra (id, titulo y artista)
    def __repr__(self):
        return f"ObraDeArte(id={self.id_obra}, titulo='{self.titulo}', artista='{self.artista.nombre}')"


#Fncion que permite Comparar obraS por el id

    def __eq__(self, other):
        if isinstance(other, ObraDeArte):
            return self.id_obra == other.id_obra
        return False


#Funcion que muestra los detalles completos de la obra
    def mostrar_detalles(self):
        detalles = f"""
        ═══════════════════════════════════════════════
        DETALLES DE LA OBRA
        ═══════════════════════════════════════════════
        ID: {self.id_obra}
        Título: {self.titulo}
        Artista: {self.artista.nombre}
        Nacionalidad del artista: {self.artista.nacionalidad}
        Fecha de nacimiento: {self.artista.fecha_nacimiento or 'No disponible'}
        Fecha de muerte: {self.artista.fecha_muerte or 'No disponible'}
        Tipo: {self.clasificacion or 'No disponible'}
        Año de creación: {self.fecha_objeto or 'No disponible'}
        Departamento: {self.departamento.nombre}
        ═══════════════════════════════════════════════
        """
        return detalles



#Verifica si la obra tiene una imagen disponible
    def tiene_imagen(self):
        return self.url_imagen is not None and self.url_imagen.strip() != ''


#Genera un nombre de archivo para la imagen
    def obtener_nombre_archivo_imagen(self):
        return f"obra_{self.id_obra}"