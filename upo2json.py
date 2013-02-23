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
Date: 23 February 2013

--------------------------------------------------------------------------------

Copyright (c) 2013 Vicente Ruiz <vruiz2.0@gmail.com>

"""

"""
Descripción:
============
Parsea un fichero CSV indicado como argumento y muestra el resultado del
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
            'edades': {
                18: x, # x matriculaciones de 18 años o menos
                19: y, # y matriculaciones de 19 años
                ...
                30: a, # a matriculaciones de 30 a 34 años
                35: b, # b matriculaciones de 35 a 39 años
                40: c, # c matriculaciones de 40 años o más
            },
            'via_acceso': {
                'PAU': a, # a matriculaciones de PAU
                'Credencial': b, # y matriculaciones de Credencial
                'F.P.': c, # c matriculaciones de F.P.
                'Titulados': d, # d matriculaciones de Titulados
                'Mayores 25': e, # e matriculaciones de Mayores 25
                'Otros': f, # f matriculaciones de Otros
            },
        },
        'mujeres': {
            'total': 142, # Total de mujeres matriculadas en TITULACION
            'edades': {
                18: x, # x matriculaciones de 18 años o menos
                19: y, # y matriculaciones de 19 años
                ...
                30: a, # a matriculaciones de 30 a 34 años
                35: b, # b matriculaciones de 35 a 39 años
                40: c, # c matriculaciones de 40 años o más
            },
            'via_acceso': {
                'PAU': a, # a matriculaciones de PAU
                'Credencial': b, # y matriculaciones de Credencial
                'F.P.': c, # c matriculaciones de F.P.
                'Titulados': d, # d matriculaciones de Titulados
                'Mayores 25': e, # e matriculaciones de Mayores 25
                'Otros': f, # f matriculaciones de Otros
            },
        },
    },
    ...
}

Argumentos:
- input: Fichero CSV que contiene la información ofrecida por la UPO
- output_dir: Directorio donde se almacenarán los ficheros JSON.
"""
import csv
import json
import os
import sys



# Comprobamos los argumentos
if len(sys.argv) != 3:
    sys.exit('USO:', sys.argv[0], 'input output_dir')

# Estructuras para almacenar los datos
data = {}

# Apertura del fichero de entrada por edades
filename = sys.argv[1]    
reader = csv.reader(open(filename, "r"))

for row in reader:
    curso, titulacion, ingreso, edad, sexo, pais_nacionalidad, \
        pais_familiar, ccaa_familiar, provincia_familiar, poblacion_familiar, \
        familia_numerosa = row
    
    titulacion_data = data.setdefault(curso, {}).setdefault(titulacion, {
        'total': 0,
        'hombres': { 'total': 0 },
        'mujeres': { 'total': 0 },
    })
    
    titulacion_data['total'] = titulacion_data['total'] + 1
    # ... por terminar ...

for year, year_data in data.items():
    filename = os.path.join(output_dir, 'upo'+year+'.json')
    output = open(filename, 'w+')
    # Preparamos los datos en JSON
    json_data = json.dumps(year_data)
    # Mostramos el resultado
    output.write(json_data)
    output.close()
