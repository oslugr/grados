"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

--------------------------------------------------------------------------------

Data source: Acceso identificado de la Universidad de Granada
Date: 22 February 2013

--------------------------------------------------------------------------------

Copyright (c) 2013 Vicente Ruiz <vruiz2.0@gmail.com>

"""

"""
Descripción:
============
Parsea un fichero HTML indicado como argumento y muestra el resultado del
análisis en formato JSON.

El formato de la salida es un direccionario, en la cuál se incluye la
información por titulaciones. Para cada titulación se incluye el total de
matriculaciones y la información relativa a los sexos. Aquí podemos ver un
ejemplo de la estructura devuelta:

{
    'TITULACION': {
        'total': 230, # Total de personas matriculadas en TITULACION
        'hombres': {
            'total': 88, # Total de hombres matriculados en TITULACION
            'via_acceso': {
                'PAU': a, # a matriculaciones de PAU
                'Credencial': b, # y matriculaciones de Credencial
                'F.P.': c, # c matriculaciones de F.P.
                'Titulados': d, # d matriculaciones de Titulados
                'Mayores 25': e, # e matriculaciones de Mayores 25
                'Otros': f, # f matriculaciones de Otros
            }
        },
        'mujeres': {
            'total': 142, # Total de mujeres matriculadas en TITULACION
            'via_acceso': {
                'PAU': a, # a matriculaciones de PAU
                'Credencial': b, # y matriculaciones de Credencial
                'F.P.': c, # c matriculaciones de F.P.
                'Titulados': d, # d matriculaciones de Titulados
                'Mayores 25': e, # e matriculaciones de Mayores 25
                'Otros': f, # f matriculaciones de Otros
            }
        },
    },
    ...
}

Argumentos:
- input: Fichero de entrada que contiene la información ofrecida por la UGR
- output: Argumento opcional. Si se indica, los datos obtenidos se vuelcan al
  fichero indicado. En caso de que no se indique este argumento, se muestran
  por salida estándar.



Requisitos:
===========
- Python 3
- BeautifulSoup (versión 4)
"""

import json
import re
import sys
from bs4 import BeautifulSoup


# Comprobamos los argumentos
if len(sys.argv) < 2 or len(sys.argv) > 3:
    sys.exit('USO:', sys.argv[0], 'input [output]')

# Preparamos la salida
output = sys.stdout
if len(sys.argv) == 3:
    output = open(sys.argv[2], 'w+')

# Apertura del fichero de entrada
filename = sys.argv[1]    
html_doc = open(filename, 'r', encoding='latin-1')

# Cargamos el HTML con BeautifulSoup
soup = BeautifulSoup(html_doc)
tr_list = soup.body.tbody.find_all('tr')

# Estructuras para almacenar los datos
data = {}

def male_and_female(tr_list):
    it = iter(tr_list)
    while True:
        yield next(it), next(it)

def parse_tr(td_list):
    titulacion = td_list[2].get_text()
    if titulacion:
        facultad = td_list[0].get_text()
        try:
            total = int(td_list[1].get_text().replace('.', ''))
        except ValueError as e:
            total = None
        try:
            total_titulacion = int(td_list[3].get_text().replace('.', ''))
        except ValueError as e:
            total_titulacion = None
        
        # Es necesario salvar las irregularidades de la tabla (colspan)
        lista_accesos = [0, 0, 0, 0, 0, 0]
        lista_index = 0
        index = 5

        while index < len(td_list) - 2: # 1 porque empieza en 0 y otra por la ult. col.
            if 'colspan' in td_list[index].attrs:
                lista_index = lista_index + int(td_list[index].attrs['colspan'])
            else:
                if re.match('[0-9]+', td_list[index].get_text()):
                    lista_accesos[lista_index] = int(td_list[index].get_text().replace('.', ''))
                lista_index = lista_index + 1
            index = index + 1
        
        acceso = {
            'PAU': lista_accesos[0],
            'Credencial': lista_accesos[1],
            'F.P.': lista_accesos[2],
            'Titulados': lista_accesos[3],
            'Mayores 25': lista_accesos[4],
            'Otros': lista_accesos[5],
        }

        total_sexo = int(td_list[len(td_list) - 2].get_text().replace('.', ''))
        return facultad, total, titulacion, total_titulacion, total_sexo, acceso
    
    return None, None, None, None, None, None
    

for tr_male, tr_female in male_and_female(tr_list[11:]):
    td_male_list = tr_male.find_all('td')
    facultad, total, titulacion, total_titulacion, total_sexo, acceso = parse_tr(td_male_list)
    data[titulacion] = {
        'total': total_titulacion,
        'hombres': {
            'total': total_sexo,
            'via_acceso': acceso,
        }
    }
    
    td_female_list = tr_female.find_all('td')
    facultad, total, titulacion, total_titulacion, total_sexo, acceso = parse_tr(td_female_list)
    data[titulacion]['mujeres'] = {
        'total': total_sexo,
        'via_acceso': acceso,
    }

# Preparamos los datos en JSON
json_data = json.dumps(data)
# Mostramos el resultado
output.write(json_data)
output.close()
