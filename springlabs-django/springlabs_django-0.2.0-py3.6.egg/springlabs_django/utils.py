import os
import re
import requests
from zipfile import ZipFile
import shutil
import random
import string

import pkgutil

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
    cloneTemplate,
    generateBackup,
    reverseChanges
)


def createDjango(name, database, url, name_git, path=os.getcwd()):
    """
        Función encargada de crear projecto django

        Función que descarga proyecto template de django-logic o django-physic
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            path            [String]    Directorio del proyecto
            url             [String]    Url de repositorio gitlab
            name_git        [String]    Nombre de proyecto en repositorio git
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = cloneTemplate(url=url, name=name_git)
    if result == True:
        errors = []
        # Cambiar nombre de la carpeta principal name_git to name
        try:
            os.rename(f"{path}/{name_git}", name)
            os.chdir(path + "/" + name)
            project_path = os.getcwd()
        except:
            message = "Error en cambiar nombre de carpeta original por nombre"
            errors.append([message, True])

        # Nombre de la carpeta settings --project_name-- to name
        try:
            os.rename(f"{project_path}/--project_name--", name)
        except:
            message = "Error en cambiar nombre de carpeta de proyecto por nombre"
            errors.append([message, True])
        # Modify SETTINGS.PY
        # Modify SECRET_KEY PROJECT
        chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace(
            '\'', '').replace('"', '').replace('\\', '')
        hash = ''.join([random.SystemRandom().choice(chars)
                        for i in range(50)])
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
            content=hash,
            find="SECRET_KEY_PROJECT",
            recursive=False)
        if result == False:
            errors.append([message, True])
        # Modify name in /name/settings.py
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
            content=name,
            find="--project_name--",
            recursive=True)
        if result == False:
            errors.append([message, True])

        # Modify database in /name/settings.py
        if database == "postgres":
            database_engine = "django.db.backends.postgresql_psycopg2"
        elif database == "mysql":
            database_engine = "django.db.backends.mysql"
        message, result = findNReplace(path=f"{project_path}/{name}/settings.py",
            content=database_engine,
            find="DATABASE_ENGINE",
            recursive=False)
        if result == False:
            errors.append([message, True])

        # Modify name in /name/wsgi.py
        message, result = findNReplace(path=f"{project_path}/{name}/wsgi.py",
            content=name,
            find="--project_name--",
            recursive=True)
        if result == False:
            errors.append([message, True])
        # Modify name in /core/documentation.py
        message, result = findNReplace(path=f"{project_path}/core/documentation.py",
            content=name,
            find="--project_name--",
            recursive=True)
        if result == False:
            errors.append([message, True])

        # Modify name in manage.py
        message, result = findNReplace(path=f"{project_path}/manage.py",
            content=name,
            find="--project_name--",
            recursive=True)
        if result == False:
            errors.append([message, True])

        # Revisa si hay errores en la modificación de archivos y saca el mensaje correcto
        for error in errors:
            if error[1] == True:
                os.chdir("..")
                os.chdir("..")
                shutil.rmtree(os.getcwd() + "/" + name)
                return error[0], False

        return "OK", True
    else:
        return message, False


def createFlask(name, database, url, name_git, path=os.getcwd()):
    """
        Función encargada de crear projecto flask

        Función que descarga proyecto template de flask-logic o flask-physic
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            path            [String]    Directorio del proyecto
            url             [String]    Url de repositorio gitlab
            name_git        [String]    Nombre de proyecto en repositorio git
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    message, result = cloneTemplate(url=url, name=name_git)
    if result == True:
        errors = []
        # Cambiar nombre de la carpeta principal name_git to name
        try:
            os.rename(f"{path}/{name_git}", name)
            os.chdir(path + "/" + name)
            project_path = os.getcwd()
        except:
            message = "Error en cambiar nombre de carpeta original por nombre"
            errors.append([message, True])

        # Modify APPLICATION.PY
        # Modify SECRET_KEY PROJECT
        chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace(
            '\'', '').replace('"', '').replace('\\', '')
        hash = ''.join([random.SystemRandom().choice(chars)
                        for i in range(50)])
        message, result = findNReplace(path=f"{project_path}/application.py",
            content=hash,
            find="SECRET_KEY_PROJECT",
            recursive=False)
        if result == False:
            errors.append([message, True])

        # Modify name in /apis/__init__.py
        message, result = findNReplace(path=f"{project_path}/apis/__init__.py",
            content=name,
            find="--project_name--",
            recursive=True)
        if result == False:
            errors.append([message, True])

        # Revisa si hay errores en la modificación de archivos y saca el mensaje correcto
        for error in errors:
            if error[1] == True:
                os.chdir("..")
                os.chdir("..")
                shutil.rmtree(os.getcwd() + "/" + name)
                return error[0], False

        return "OK", True
    else:
        return message, False


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
    errors = []

    # Crear version en project_name/urls.py
    # Importar public versions de nueva versión
    path = f"{project_name}/urls.py"
    find = "# PUBLIC VERSIONS URLS (Managed by SPRINGLABS_DJANGO)"
    content = f"from api.v{version}.public_urls import public_urls as public_urls_v{version}"
    message, result = appendContent(path=path,
                                    content=content,
                                    find=find)
    if result == False:
        errors.append([message, True])

    # Agregar nueva version a urls_versions
    find = "urls_versions ="
    for index, old_version in enumerate(old_versions):
        if index == 0:
            public_urls = f" public_urls_v{old_version}"
        else:
            public_urls = f" + public_urls_v{old_version}"
        find = find + public_urls
    content = find + f" + public_urls_v{version}"

    message, result = findNReplace(path=path,
        content=content,
        find=find)
    if result == False:
        errors.append([message, True])

    # Crear carpeta API nueva versión con archivos
    primary_package = "springlabs_django"
    os.chdir("api")
    new_version = f"v{version}"
    os.mkdir(new_version)
    base_urls_py = "/core/new_version/api/baseUrls.py"
    base_public_urls_py = "/core/new_version/api/basePublicUrls.py"
    base_private_urls_py = "/core/new_version/api/basePrivateUrls.py"
    base_serializers_py = "/core/new_version/api/baseSerializers.py"
    base_views_py = "/core/new_version/api/baseViews.py"

    template_urls_py = pkgutil.get_data(
        primary_package, base_urls_py).decode('utf-8')
    template_urls_py = template_urls_py.replace("name_version", new_version)

    template_public_urls_py = pkgutil.get_data(
        primary_package, base_public_urls_py).decode('utf-8')
    template_public_urls_py = template_public_urls_py.replace(
        "name_version", new_version)

    template_private_urls_py = pkgutil.get_data(
        primary_package, base_private_urls_py).decode('utf-8')
    template_private_urls_py = template_private_urls_py.replace(
        "name_version", new_version)

    template_serializers_py = pkgutil.get_data(
        primary_package, base_serializers_py).decode('utf-8')

    template_views_py = pkgutil.get_data(
        primary_package, base_views_py).decode('utf-8')

    with open(f"{new_version}/urls.py", "w") as file:
        file. write(template_urls_py)
    with open(f"{new_version}/public_urls.py", "w") as file:
        file. write(template_public_urls_py)
    with open(f"{new_version}/private_urls.py", "w") as file:
        file. write(template_private_urls_py)
    os.mkdir(f"{new_version}/users")
    with open(f"{new_version}/users/serializers.py", "w") as file:
        file. write(template_serializers_py)
    with open(f"{new_version}/users/views.py", "w") as file:
        file. write(template_views_py)

    for error in errors:
        if error[1] == True:
            message, result = reverseChanges(project_name=project_name)
            os.chdir("..")
            os.remove(project_name + ".zip")
            os.chdir(project_name)
            return error[0], False

    return "OK", True


def createFlaskProject(name, database, design):
    """
        Función encargada de crear projecto flask

        Función que descarga proyecto template de [design=[logico|fisico]]
        y realiza las modificaciones necesarias para nuevo proyecto

        Parámetros:
            name            [String]    Nombre del proyecto nuevo
            database        [String]    Motor de base de datos a utilizar
            design          [String]    Diseño de base de datos a utilizar
            path            [String]    Directorio del proyecto
        Retorno:
            message,result  [Tuple]     Mensaje[String] y result[Boolean]
    """
    try:
        os.mkdir(name)
    except:
        return f"Ya existe una carpeta con el nombre '{name}' en el directorio actual", False
    else:
        os.chdir(os.getcwd() + "/" + name)
        if design == "logico":
            url = "https://gitlab.com/AlejandroBarcenas/template-flask-logic.git"
            name_git = "template-flask-logic"
        message, result = createFlask(name=name,
            database=database,
            path=os.getcwd(),
            url=url,
            name_git=name_git)
        return message, result
