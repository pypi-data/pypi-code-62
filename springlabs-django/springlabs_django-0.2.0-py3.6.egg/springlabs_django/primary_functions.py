import os
import re
from zipfile import ZipFile
import shutil


def appendContent(path, content, find=None, recursive=False):
    '''
    Agrega contenido al final del archivo especificado, si existe un valor en "find", agregará el contenido despues de la coincidencia.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            cadena a buscar, si es nulo el contenido se agregara al final
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al crear el archivo
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False
    if find == None:
        try:
            """ if not os.path.exists(path):
                    open(path, "x")
            with open(f'{path}.bak', "w") as f:
                    f.write(open(path).read()) """
            with open(path, "a") as f:
                newContent = f'\n{content}'
                f.write(newContent)
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido:{exc}', False
    else:
        if recursive == False:
            return notRecursiveModify(path, content, find, 'append')
        elif recursive == True:
            return recursiveModify(path, content, find, 'append')

        return f'Valor no válido para el parametro recursive', False


def replaceContent(path, content, start, end='--end', recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False

    starts = getRangeStr(path, start)
    ends = getRangeEnds(path, end)
    if ends == None or len(ends) == 0:
        return f'Tu archivo no cuenta con delimitadores de fin: "{end}"', False
    if starts == None or len(starts) == 0:
        return f'Tu archivo no cuenta con delimitadores de inicio: "{start}"', False
    textsReplace = []
    for idx, _ in enumerate(ends):
        if len(starts) <= idx or starts[idx][1] > ends[idx][0]:
            break
        textsReplace.append([starts[idx][1] + 1,  ends[idx][0] - 1])
    file = open(path).read()
    # print(textsReplace)
    # print(file[textsReplace[0][0]:textsReplace[0][1]])
    if len(textsReplace) == 0:
        return f'Tu archivo tiene mal los delimitadores de inicio "{start}" y/o los deliminatores de fin "{end}" , favor de verificar.', False
    if recursive == False:
        return notRecursiveModify(path, content, file[textsReplace[0][0]:textsReplace[0][1]], 'replace')
    elif recursive == True:
        try:
            for text in textsReplace:
                recursiveModify(
                    path, content, file[text[0]:text[1]], 'replace')
            return f'Se actualizó correctamente el archivo: {path}', True
        except Exception as exc:
            return f'Error al escribir el contenido: {exc}', False

    return f'Valor no válido para el parametro recursive', False


def findNReplace(path, content, find, recursive=False):
    '''
    Remplaza cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False
    if recursive == False:
        return notRecursiveModify(path, content, find, 'replace')
    elif recursive == True:
        return recursiveModify(path, content, find, 'replace')

    return f'Valor no válido para el parametro recursive', False


def findNDelete(path, find, recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False
    if recursive == False:
        return findNReplace(path, '', find)
    elif recursive == True:
        return findNReplace(path, '', find, recursive=True)

    return f'Valor no válido para el parametro recursive', False


def deleteContent(path, start, end='--end', recursive=False):
    '''
    Elimina cierto contenido del archivo especificado.

    Atributos:
            path            [String]            Ruta de archivo a editar
            start           [String]            Parametro a partir del cual se iniciará el remplazo hasta encontrar el parametro "end"
            recursive       [Boolean]           Indica si la operación será recursiva
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if not os.path.exists(path):
        return f'El archivo no existe', False
    if recursive == False:
        return replaceContent(path, '', start, end)
    elif recursive == True:
        return replaceContent(path, '', start, end, recursive=True)

    return f'Valor no válido para el parametro recursive', False


def notRecursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" (solo primera coincidencia).

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    file = open(path).read()
    matchFound = False
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        matchFound = True
        break
    if matchFound == False:
        return f'No se encontraron coincidencias de "{find}"', False
    if type == 'append':
        newContent = f'{file[: m.end()]}  \n{content} \n{file[m.end() + 1:]}'
    elif type == 'replace':
        newContent = f'{file[: m.start()]}{content}{file[m.end():]}'
    else:
        return f'Tipo de remplazo no válido', False
    try:
        '''with open(f'{path}.bak', "w") as f:
                f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(newContent)
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


def recursiveModify(path, content, find, type):
    '''
    Modifica un archivo dado, en la coincidencia "find" con el contenido de "content" de manera recursiva.

    Atributos:
            path            [String]            Ruta de archivo a editar
            content         [String]            Nuevo contenido a agregar
            find            [String]            Se hará un "search & replace de la valor dado
            type	        [String]            Indica el tipo de operación
    Retorno:
            result          [Tupla]             Resultado de operación
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    if type == 'append':
        newContent = f'{find} \n{content}\n'
    elif type == 'replace':
        newContent = content
    else:
        return f'Tipo de remplazo no válido', False
    try:
        file = open(path).read()
        '''with open(f'{path}.bak', "w") as f:
			f.write(open(path).read())'''
        with open(path, "w") as f:
            f.write(file.replace(find, newContent))
        return f'Se actualizó correctamente el archivo: {path}', True
    except Exception as exc:
        return f'Error al escribir el contenido: {exc}', False


def getRangeStr(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter del valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un search de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    arr = []
    file = open(path).read()
    find = find.replace("(", r'\(')
    find = find.replace(")", r'\)')
    find = find.replace("{", r'\{')
    find = find.replace("}", r'\}')
    find = find.replace("[", r'\[')
    find = find.replace("]", r'\]')
    find = find.replace("+", r'\+')
    find = find.replace("<", r'\<')
    find = find.replace("-", r'\-')
    find = find.replace("!", r'\!')
    find = find.replace("*", r'\*')
    find = find.replace("~", r'\~')
    find = find.replace("¬", r'\¬')
    find = find.replace(",", r'\,')
    find = find.replace(":", r'\:')
    find = find.replace(".", r'\.')

    matches = re.finditer(find, file)
    for m in matches:
        arr.append([m.start(), m.end()])
    return arr


def getRangeEnds(path, find):
    '''
    Obtiene los indices del primer y ultimo caracter de la linea donde se encuentre el valor de "find".

    Atributos:
            path            [String]            Ruta de archivo a editar
            find            [String]            Se hará un "search & replace de la valor dado
    Retorno:
            arr          	[Lista]            Indices
    Excepciones:
            OSError                             Error al escribir el contenido
    '''
    with open(path) as file:
        for line in file:
            if find in line:
                return getRangeStr(path, line)


def cloneTemplate(url, name):
    """
        Función encargada de clonar proyecto template

        Función que clona proyecto template de gitlab, con credenciales de
        usuario ProgramacionSpringlabs y elimina registro de repositorio
        template.

        Parámetros:
            url             [String]    URL de repositorio git
            name            [String]    Nombre del proyecto en repositorio y clone
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    username = "ProgramacionSpringlabs"
    token = "rysMXSPyMbmTtG3W3Afq"
    url = url.replace("//", f"//{username}:{token}@")
    clone = f"git clone --quiet {url}"
    os.system(clone)
    shutil.rmtree(os.getcwd() + f"/{name}/.git")
    try:
        os.remove(os.getcwd() + f"/{name}/.gitignore")
    except:
        pass
    return "OK", True


def generateBackup(project_name, path=os.getcwd()):
    try:
        oldPath = path
        os.chdir("..")
        shutil.make_archive(project_name, 'zip', base_dir=project_name)
        os.chdir(oldPath)
        return "OK", True
    except Exception as e:
        return str(e), False


def reverseChanges(project_name, path=os.getcwd()):
    try:
        oldPath = path
        os.chdir("..")
        shutil.rmtree(project_name)
        botZip = f'{project_name}.zip'
        with ZipFile(botZip, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        os.chdir(oldPath)
        return "OK", True
    except Exception as e:
        return str(e), False

