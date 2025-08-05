#Aqui creamos la clase departamento


class Departamento:

# Inicializa un objeto departamento

    def __init__(self, id_departamento, nombre):
        self.id_departamento = id_departamento
        self.nombre = nombre

# retorna string del nombre departamento
    def __str__(self):
        return self.nombre

# retorna el id y nombre departamento
    def __repr__(self):

        return f"Departamento(id={self.id_departamento}, nombre='{self.nombre}')"

#Funcion para comparar el id de dos departamentos y determinar si son el mismo
    def __eq__(self, other):
        
        if isinstance(other, Departamento):
            return self.id_departamento == other.id_departamento
        return False
    
    
