#Aqui creamos la clase Artista.

class Artista:
    def __init__(self, nombre, nacionalidad, fecha_nacimiento=None, fecha_muerte=None):
        
# Inicializa un objeto Artista
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_muerte = fecha_muerte

# retorna string del nombre artista
    def __str__(self):
        return self.nombre

# retorna string del nombre artista y su nacionalidad
    def __repr__(self):
        return f"Artista(nombre='{self.nombre}', nacionalidad='{self.nacionalidad}')"
    
    
