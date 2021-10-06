import pandas as pd
import os
import zipfile
from pathlib import Path

# Si no esta el directorio 'data_csv' lo crea
if not os.path.exists('./data_csv'):
    os.makedirs('./data_csv')

    for file in os.listdir('./source_zip/'):   # get the list of files
        with zipfile.ZipFile('./source_zip/'+file) as item: # treat the file as a zip
            item.extractall('./data_csv')  # extract it in the 'data_csv' directory
            

# Hay que hacer el siguiente truquito para parsear los csv descomprimidos.
p = Path('./data_csv/')
for file in p.glob('**/*.xlsx'):
    print(file.stem)
    df = pd.read_excel(file) # Archivo descomprimido
    
    # Guardar el csv
    df.to_csv('./data_csv/'+file.stem, index = False)
    
    # Remover el xlsx descomprimido
    os.remove(file)

## Arreglar nombres de archivos
for file in p.glob('**/*'):
#     print(file.stem)
    os.rename('./data/'+file.name, './data/'+file.name.replace(' ', '_').replace('__', '_'))
    
    
## Arreglar un problema de parseo originado en que ciertas filas estan entrecomilladas
for file in p.glob('**/*'):
    with open('./data/' + file.name) as r:
        text = r.read().replace('"', '')
    with open('./data/' + file.name, "w") as w:
        w.write(text)

## Arreglar otro problema de parseo, por comas al final de ciertas lineas.
for file in p.glob('**/*'):
    df = pd.read_csv('./data/' + file.name, ';')
    df.columns = [*df.columns[:-1], 'votos']
    df['votos'] = df['votos'].astype(str).str.replace(',', '').astype(int)
    df.to_csv('./data/' + file.name, index = False)
