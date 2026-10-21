#!/bin/sh
# Abre el cuaderno completo (con índice, estilos e imágenes) en http://localhost:8000
cd "$(dirname "$0")" && echo "Abrí http://localhost:8000 en el navegador (Ctrl+C para cerrar)" && python3 -m http.server 8000
