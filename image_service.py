
#Clase para manejar la descarga y visualización de imágenes de obras de arte

import requests
from PIL import Image
import os


class ImageService:

    def __init__(self):
#Inicializa el objeto encargado de las imágenes
        self.carpeta_imagenes = "imagenes_obras"
        self._crear_carpeta_imagenes()

    def _crear_carpeta_imagenes(self):
#Crea la carpeta para almacenar las imágenes si no existe.
        if not os.path.exists(self.carpeta_imagenes):
            os.makedirs(self.carpeta_imagenes)


#Descarga una imagen desde una URL y la guarda en un archivo.
    def guardar_imagen_desde_url(self, url, nombre_archivo):
        if not url:
            print("No hay URL de imagen disponible")
            return None
            
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Determinar la extensión del archivo
            content_type = response.headers.get('Content-Type')
            extension = '.png'  # Valor por defecto
            
            if content_type:
                if 'image/png' in content_type:
                    extension = '.png'
                elif 'image/jpeg' in content_type:
                    extension = '.jpg'
                elif 'image/svg+xml' in content_type:
                    extension = '.svg'
            
            # Crear el nombre del archivo completo
            nombre_archivo_final = f"{self.carpeta_imagenes}/{nombre_archivo}{extension}"
            
            # Guardar la imagen
            with open(nombre_archivo_final, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"Imagen guardada exitosamente como '{nombre_archivo_final}'")
            return nombre_archivo_final
            
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen: {e}")
            return None
        except IOError as e:
            print(f"Error al escribir el archivo: {e}")
            return None


#Descarga y muestra una imagen de obra de arte---> esto toma la  url_imagen y id_obra, ademas comprueba a traves de un bool si se muestra correctamente

    def mostrar_imagen(self, url_imagen, id_obra):


        if not url_imagen:
            print("Esta obra no tiene imagen disponible")
            return False
            
        try:
            # Crear nombre del archivo basado en el ID de la obra
            nombre_archivo = f"obra_{id_obra}"
            
            # Descargar y guardar la imagen
            ruta_archivo = self.guardar_imagen_desde_url(url_imagen, nombre_archivo)
            
            if ruta_archivo:
                # Abrir y mostrar la imagen
                img = Image.open(ruta_archivo)
                img.show()
                print(f"Mostrando imagen de la obra ID: {id_obra}")
                return True
            else:
                print("No se pudo descargar la imagen")
                return False
                
        except Exception as e:
            print(f"Error al mostrar la imagen: {e}")
            return False




#Funcion extra creada para eliminar todas las imágenes descargadas de la carpeta donde se alojan luego de descargar (inspirado en una funcion encontada en internet para eliminar cosas del sistema operativo)
    def limpiar_imagenes(self):
        try:
            if os.path.exists(self.carpeta_imagenes):
                for archivo in os.listdir(self.carpeta_imagenes):
                    ruta_archivo = os.path.join(self.carpeta_imagenes, archivo)
                    if os.path.isfile(ruta_archivo):
                        os.remove(ruta_archivo)
                print("Imágenes limpiadas exitosamente")
        except Exception as e:
            print(f"Error al limpiar imágenes: {e}")