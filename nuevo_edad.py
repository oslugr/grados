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

Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
import json
import sys
from bs4 import BeautifulSoup


if len(sys.argv) != 2:
    sys.exit("Es necesario indicar el fichero de entrada")

filename = sys.argv[1]    
html_doc = open(filename, 'r')

soup = BeautifulSoup(html_doc)
tr_list = soup.body.tbody.find_all('tr')

male_data = {}
female_data = {}
"""
male_data = {
    'GRADO EN BELLAS ARTES': [
        230, # Total de hombres en el Grado en Bellas Artes
        {
            18: 19, # 19 hombres de 18 años
            19: 22, # 22 hombres de 19 años
            20: 7,  #  7 hombres de 20 años
            ...
        }
    ],
    ...
}
"""

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
        total_sexo = int(td_list[20].get_text().replace('.', ''))
        edades = {
            18: int(td_list[5].get_text().replace('.', '')),
        }
        return facultad, total, titulacion, total_titulacion, total_sexo, edades
    
    return None, None, None, None, None, None
    

for tr_male, tr_female in male_and_female(tr_list[7:]):
    td_male_list = tr_male.find_all('td')
    facultad, total, titulacion, total_titulacion, total_sexo, edades = parse_tr(td_male_list)
    male_data[titulacion] = [total_sexo, edades]
    
    td_female_list = tr_female.find_all('td')
    facultad, total, titulacion, total_titulacion, total_sexo, edades = parse_tr(td_female_list)
    female_data[titulacion] = [total_sexo, edades]


print()
print('GRADO EN BELLAS ARTES', male_data['GRADO EN BELLAS ARTES'])
print('GRADO EN BIOLOGÍA', male_data['GRADO EN BIOLOGÍA'])
print('GRADO EN CIENCIAS AMBIENTALES', male_data['GRADO EN CIENCIAS AMBIENTALES'])

print()
print('GRADO EN BELLAS ARTES', female_data['GRADO EN BELLAS ARTES'])
print('GRADO EN BIOLOGÍA', female_data['GRADO EN BIOLOGÍA'])
print('GRADO EN CIENCIAS AMBIENTALES', female_data['GRADO EN CIENCIAS AMBIENTALES'])

json_data = json.dumps([male_data, female_data])
print(json_data)
