from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By

# driver = webdriver.Edge()
# driver = webdriver.Chrome()


dic_videojuegos = {}

# La clave del diccionario es el nombre del juego.
# El valor es una lista con: la lista de precios por vendedor; valoración de Metacritic; Tiempo de juego que proporciona al usuario.


dic_videojuegos = {"jurasic Park": [[(15, "Epic"), (16, "Steam")], 8.5, 40]}
print(dic_videojuegos)

