import os
import json

from .primary_functions import (
    appendContent,
    replaceContent,
    findNReplace,
    findNDelete,
    deleteContent,
    notRecursiveModify,
    recursiveModify,
    getRangeStr,
    getRangeEnds,
    generateBackup,
    reverseChanges,
    modifyFilesNewVersion,
    createDirectoriesNewVersion
)

def createVersion(version, project_name, old_versions):
    """
        Función encargada de crear nueva version en proyecto django

        Función encargada de crear nueva versión en proyecto django

        Parámetros:
            version         [String]    Nueva versión del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = generateBackup(project_name=project_name)
    if result == False:
        message = "Ocurrió un error interno al crear respaldo"
        return message, False

    errors = []
    # Modifica archivos para nueva versión
    message, result = modifyFilesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al escribir archivos se agrega a arreglo
    if result == False:
        errors.append([message, True])
    
    # Crea directorios y archivos dentro para nueva versión
    message, result = createDirectoriesNewVersion(version=version,
        project_name=project_name,
        old_versions=old_versions)
    
    # Si falla al modificar directorios se agrega a arreglo
    if result == False:
        errors.append([message, True])
    try:
        with open('springlabs_django.json') as file:
            data = json.load(file)
    except Exception as e:
        message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
        errors.append([message, True])
    else:
        objVersionDetail = {
            "version": version,
            "groups": ["users"]
        }
        data["versions"].append(version)
        data['versions_detail'].append(objVersionDetail)
        try:
            with open("springlabs_django.json", "w") as file:
                file.write(json.dumps(data))
        except:
            message = "Ocurrio un error interno al actualizar archivo springlabs_django.json"
            errors.append([message, True])

    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False
    


    return "OK", True