# 2024-2ºC-510-PROGRAMACIÓN PYTHON AVANZADA-TU TECNOLOGÍAS DE PROGRAMACION
# CASBAS/CORONEL DORREGO-COM A
# Proyecto 2
# Alumno: Michael Anthony, Lema Jacinto
# Fecha Entrega: 11 de noviembre del 2024
# ---------------------------------------------------------------------------------

# Este programa fue diseñado para procesar imágenes desde directorios locales o URLs de internet, admitiendo diversos 
# formatos como JPG, PNG, y WEBP, entre otros usando la funcion convertir_a_rgb.
# En la función dibujar_boceto, se implementó una mejora significativa: se invierte la imagen a su positivo. 
# Esto significa que el fondo se muestra en blanco y las líneas en negro, permitiendo a los artistas aprovechar los 
# contornos oscuros para pintar o trabajar sobre el fondo blanco de manera más intuitiva.
# Además, se incorporaron múltiples validaciones para garantizar que el programa sea robusto y maneje adecuadamente 
# los datos de entrada proporcionados por el usuario. Esto incluye asegurarse de que las imágenes sean válidas y 
# compatibles, tanto en formato como en ruta. Por último, se utilizó la función clear_output para limpiar y refrescar 
# el menú principal, evitando que las opciones se sobreescriban y mejorando la experiencia de navegación.
#----------------------------------------------------------

# instalar en la terminal estas librerias: 
# python -m pip install requests  - requests se usa para cargar imágenes desde URLs de internet.
# python -m pip install Pillow   - permite abrir, manipular y guardar imágenes en diferentes formatos de archivo de manera sencilla.
# python -m pip install ipython  -  Para tener acceso a clear_output.                        


from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import requests
from io import BytesIO
from IPython.display import clear_output

#EL primer paso para que funcione el programa es cargar la imagen con la que se va a procesar.
def cargar_imagen(ruta):
    if ruta.startswith('http'):
        try:
            response = requests.get(ruta)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            return img
        except requests.exceptions.RequestException as e:
            print(f"Error al cargar la imagen desde la URL: {e}")
            return None
        except IOError as e:
            print(f"Error al abrir la imagen: {e}")
            return None
    else:
        try:
            img = Image.open(ruta)
            return img
        except IOError as e:
            print(f"Error al abrir la imagen: {e}")
            return None

def convertir_a_rgb(img):
    if img.mode in ['P', 'RGBA']:
        img = img.convert('RGB')
    return img

#En esta funcion cambiamos el tamaño segun las redes sociales que queremos usar la imagen seleccionada previamente
def redimensionar_imagen(ruta, plataforma):
    dimensiones = {
        "YOUTUBE": (1280, 720),
        "INSTAGRAM": (1080, 1080),
        "TWITTER": (1024, 512),
        "FACEBOOK": (1200, 630)
    }
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        input("Presiona Enter para continuar...")
        return
    img = convertir_a_rgb(img)
    plataforma = plataforma.upper()
    tamaño = dimensiones.get(plataforma)
    if tamaño:
        img.thumbnail(tamaño, Image.LANCZOS)
        img.show()
        img.save(f"redimensionada_{plataforma}.jpg")
    else:
        print("Plataforma no soportada. Usa 'YOUTUBE', 'INSTAGRAM', 'TWITTER' o 'FACEBOOK'.")
        input("Presiona Enter para continuar...")

#Con esta funcion ajustamos un contraste a la imagen cargada previamente.
def ajustar_contraste(ruta):
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        input("Presiona Enter para continuar...")
        return
    img = convertir_a_rgb(img)
    img_eq = ImageOps.equalize(img)
    img.show(title="Original")
    img_eq.show(title="Ecualizada")
    img.save("original_contraste.jpg")
    img_eq.save("contraste_ajustado.jpg")

#En esta funcion aplicamos un filtro seleccionado por el usuario para luego generarlo.
def aplicar_filtro(ruta, filtro):
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        input("Presiona Enter para continuar...")
        return False
    img = convertir_a_rgb(img)
    filtro = filtro.upper()
    filtros = {
        "BLUR": ImageFilter.BLUR,
        "CONTOUR": ImageFilter.CONTOUR,
        "DETAIL": ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
        "EMBOSS": ImageFilter.EMBOSS,
        "FIND_EDGES": ImageFilter.FIND_EDGES,
        "SHARPEN": ImageFilter.SHARPEN,
        "SMOOTH": ImageFilter.SMOOTH,
    }
    if filtro in filtros:
        img_filtrada = img.filter(filtros[filtro])
        img_filtrada.show(title=f"Filtro: {filtro}")
        img_filtrada.save(f"filtrada_{filtro}.jpg")
        print("Filtro aplicado",[filtro])
        return True
            
    
    else:
        print("Filtro no soportado. Los filtros válidos son:") 
        print(" BLUR, CONTOUR, DETAIL, EDGE_ENHANCE,") 
        print("EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES,") 
        print("SHARPEN, SMOOTH.") 
        return False 

#COn esta funcion mostramos la imagen subida con todos los filtros disponibles
def mostrar_todos_los_filtros(ruta):
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        input("Presiona Enter para continuar...")
        return
    img = convertir_a_rgb(img)
    filtros = {
        "BLUR": ImageFilter.BLUR,
        "CONTOUR": ImageFilter.CONTOUR,
        "DETAIL": ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
        "EMBOSS": ImageFilter.EMBOSS,
        "FIND_EDGES": ImageFilter.FIND_EDGES,
        "SHARPEN": ImageFilter.SHARPEN,
        "SMOOTH": ImageFilter.SMOOTH,
    }
    
    for nombre, filtro in filtros.items():
        img_filtrada = img.filter(filtro)
        img_filtrada.show(title=f"{nombre}")
        img_filtrada.save(f"filtrada_{nombre}.jpg")

#Aqui convertimos la imagen a fondo blanco y lineas negras.
def dibujar_boceto(ruta, persona=True):
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        input("Presiona Enter para continuar...")
        return
    # Convertir a modo RGB si es una imagen en modo de paleta
    if img.mode in ["P", "RGBA"]:
        img = convertir_a_rgb(img)
    
    if persona:
        img_boceto = img.filter(ImageFilter.FIND_EDGES)
        img_boceto = ImageOps.grayscale(img_boceto)
        
        # Invertir la imagen para que el fondo sea blanco y las líneas sean negras
        img_boceto = ImageOps.invert(img_boceto)
        
        img_boceto.show(title="Boceto")
        img_boceto.save("boceto.jpg")
    else:
        print("No se detectó una persona en la imagen.")

#Agregamos esta funcion extra para obtener la informacion técnica de la imagen.
def informacion_imagen(ruta):
    img = cargar_imagen(ruta)
    if img is None:
        print("Error: Imagen no encontrada o formato no soportado.")
        return
    print("Información de la imagen:")
    print(f"Formato: {img.format}")
    print(f"Modo: {img.mode}")
    print(f"Tamaño: {img.size} px")
    if img.mode == "P":
        print(f"Paleta de colores: {img.getpalette()[:10]}...")  # Solo mostramos los primeros 10 valores de la paleta
    print(f"Información adicional: {img.info}")

#Creamos la funcion de un menú para que el usuario pueda interacturar dando opciones.
def menu():
    imagen_cargada = False
    ruta = None

    while True:            
        print("\n--Menú de Procesamiento de Imágenes--")
        print("1. Subir Imagen")
        print("2. Redimensionar Imagen")
        print("3. Ajustar Contraste")
        print("4. Aplicar Filtro")
        print("5. Dibujar Boceto")
        print("6. Mostrar Información de la Imagen")
        print("7. Salir")
        clear_output(wait=True)
        # Limpiar solo los mensajes anteriores, mantener menú visible        
        opcion = input("Selecciona una opción: ")

        if opcion == "7":
            print("Programa terminado.")
            clear_output(wait=False)
            break
        elif opcion == "1":
            while imagen_cargada:
                confirmacion = input("Una imagen ya ha sido cargada. ¿Deseas reemplazarla? (si/no): ").strip().lower()
                if confirmacion in ["no", "n"]:
                    print("Operación cancelada. Selecciona otra opción.")
                    clear_output(wait=False)
                    break
                elif confirmacion in ["si", "s"]:
                    ruta = input("Ingrese la ruta o URL de la imagen: ")
                    if cargar_imagen(ruta) is None:
                        print("Error: Imagen no encontrada o formato no soportado.")
                    else:
                        imagen_cargada = True
                        print("Imagen cargada correctamente.")
                    break
                else:
                    print("Por favor, ingrese 'si', 'no', 's' o 'n'.")
                    clear_output(wait=True)
            else:
                ruta = input("Ingrese la ruta o URL de la imagen: ")
                if cargar_imagen(ruta) is None:
                    print("Error: Imagen no encontrada o formato no soportado.")
                else:
                    imagen_cargada = True
                    print("Imagen cargada correctamente.")
        elif opcion in ["2", "3", "4", "5", "6"] and not imagen_cargada:
            print("Por favor, suba una imagen primero seleccionando la opción 1.")
        elif opcion in ["2", "3", "4", "5","6"] and imagen_cargada:
            if opcion == "2":
                plataforma = input("Ingrese la plataforma (Youtube, Instagram, Twitter, Facebook): ")
                plataforma_upper = plataforma.upper()
                if plataforma_upper in ["YOUTUBE", "INSTAGRAM", "TWITTER", "FACEBOOK"]:
                    redimensionar_imagen(ruta, plataforma)
                else:
                    print("Plataforma no soportada. Use 'YOUTUBE', 'INSTAGRAM', 'TWITTER' o 'FACEBOOK'.")
            elif opcion == "3":
                ajustar_contraste(ruta)
            elif opcion == "4":
                while True: 
                    filtro = input("Ingrese el nombre del filtro (BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH): ").strip().upper() 
                    if aplicar_filtro(ruta, filtro):
                        print("Filtro aplicado correctamente.")                        
                        input("Presiona Enter para continuar...")                        
                        break
                    else:
                        clear_output(wait=True)#Esto limpia el mensaje para mostrar de nuevo el menu                     
                    
            elif opcion == "5":
                dibujar_boceto(ruta, persona=True)
            elif opcion == "6":
                informacion_imagen(ruta)
                input("Presiona Enter para continuar...") 
            else: 
                print("Opción no válida. Intente de nuevo.")                   
        else:
            print("Opción no válida. Intente de nuevo.")