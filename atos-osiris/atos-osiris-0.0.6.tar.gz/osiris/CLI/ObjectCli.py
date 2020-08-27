import argparse
from osiris.Osiris import Osiris
from osiris.CLI.EnvironmentCli import EnvironmentCli
import json
from prettytable import PrettyTable
import csv
import datetime


def main():
    """
    Main function which allows to build the client for the object part of osiris. .

    :param : (String) The command entered by the user.
    :return: Nothing.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Osiris', usage='Osiris <object> <action> <option>')
    parser.add_argument('object', help="Object on which the actions will be done. \n Osiris object: vm, flavor...")
    ObjectSystemCli = parser.add_subparsers(title="Actions that can be executed on the object")

    # create the parser for the "introspect" command
    OsirisIntrospect = ObjectSystemCli.add_parser('introspect', usage='osiris <object> introspect : Introspect a specific object type on the target system')
    OsirisIntrospect.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisIntrospect.set_defaults(func=objectIntrospectCli)

    # create the parser for the "list" command
    OsirisList = ObjectSystemCli.add_parser('list', usage='osiris <object> list : List all object instances currently on the local database')
    OsirisList.add_argument('--json', "-j", action="store_true", help="Put the list in a json file in the user's home. ")
    OsirisList.add_argument('--csv', "-c", action="store_true", help="Put the list in a csv file in the user's home. ")
    OsirisList.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisList.set_defaults(func=objectListCli)

    # create the parser for the "create" command
    OsirisCreate = ObjectSystemCli.add_parser('create', usage='osiris <object> create [args...] : Create a new object instance (on the local database and on the target system)')
    OsirisCreate.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisCreate.add_argument("dictArgs", nargs='*', help="create an object instance")
    OsirisCreate.set_defaults(func=objectCreateCli)

    # create the parser for the "select" command
    OsirisSelect = ObjectSystemCli.add_parser('select', usage='osiris <object> select [<id>... | --all] : Select all or specifics instances of the given object')
    OsirisSelect.add_argument('id', nargs='*', help="instance id")
    OsirisSelect.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisSelect.add_argument('--all', "-a", action="store_true", help="select all objects")
    OsirisSelect.set_defaults(func=objectSelectCli)

    # create the parser for the "unselect" command
    OsirisUnselect = ObjectSystemCli.add_parser('unselect', usage='osiris <object> unselect [<id>... | --all] : Unselect  all or specifics instances of the given object')
    OsirisUnselect.add_argument('id', nargs='*', help="instance id")
    OsirisUnselect.add_argument('--all', "-a", action="store_true", help="select all objects")
    OsirisUnselect.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisUnselect.set_defaults(func=objectUnselectCli)

    # create the parser for the "delete" command
    OsirisDelete = ObjectSystemCli.add_parser('delete', usage='osiris <object> delete <id> : Delete an instance of an object (on the local database and on the target system)')
    OsirisDelete.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
    OsirisDelete.add_argument('id', type=str, help="instance id")
    OsirisDelete.set_defaults(func=objectDeleteCli)
    args = parser.parse_args()
    args.func(args)


def objectIntrospectCli(args):
    """
    Calls the osiris function which allows to introspect a specific object type on the target system.
    At this time, introspect an object remove previous introspects.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    objectName = args.object
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    osirirsSystemIntrospect = osiris.objectIntrospect(objectName)
    if osirirsSystemIntrospect >= 0:
        print("The " + objectName + " instropect has been successfully achieved.")
    else:
        print("The instropect hasn't come to an end.")


def objectListCli(args):
    """
    Calls the osiris function which allows to list all object instances currently on the local database.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    objectName = args.object
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    JsonObjectList = json.dumps(osiris.objectList(objectName), indent=4)
    listDictObjectName = json.loads(JsonObjectList)
    listCol = []
    for cle in listDictObjectName[0].keys():
        listCol.append(cle)

    valuesTableau = []
    for i in listDictObjectName:
        valuesTableau.append(list(i.values()))

    table = PrettyTable()
    table.field_names = listCol
    for i in valuesTableau:
        table.add_row(i)

    print(table)
    filename = datetime.datetime.now()
    if args.json:
        with open(filename.strftime("%d-%B-%Y") + "-" + objectName + "-OsirisList" + ".json", "w") as f:
            f.write(JsonObjectList + "\n")

    if args.csv:

        f = open(filename.strftime("%d-%B-%Y") + "-" + objectName + "-OsirisList" + ".csv", 'w')
        # create the csv writer object
        csvF = csv.writer(f)
        # Counter variable used for writing
        # headers to the CSV file
        count = 0

        for emp in listDictObjectName:
            if count == 0:
                # Writing headers of CSV file
                header = emp.keys()
                csvF.writerow(header)
                count += 1

            # Writing data of CSV file
            csvF.writerow(emp.values())

        f.close()


def objectCreateCli(args):
    """
    Calls the osiris function which allows to create a new object instance (on the local database and on the target system).

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    objectName = args.object
    objectArgs = args.dictArgs
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    dct = {}
    i = 0
    while i < len(objectArgs):
        dct[objectArgs[i]] = objectArgs[i + 1]
        i += 2
    print(dct)
    osiris.objectCreate(objectName, dct)


def objectSelectCli(args):
    """
    Calls the osiris function which allows to select all or specifics instances of the given object.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    objectName = args.object
    id = ' '.join(args.id)
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    if args.all:
        print("Here are the number of instances you have selected " + str(osiris.objectSelect(objectName)))
    else:
        print("Here are the number of instances you have selected " + str(osiris.objectSelect(objectName, id)))


def objectUnselectCli(args):
    """
    Calls the osiris function which allows to unselect all or specifics instances of the given object.

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    objectName = args.object
    id = ' '.join(args.id)
    verbose = args.verbose
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    if args.all:
        print("Here are the number of instances you have selected " + str(osiris.objectUnselect(objectName)))
    else:
        print("Here are the number of instances you have selected " + str(osiris.objectUnselect(objectName, id)))


def objectDeleteCli(args):
    """
    Calls the osiris function which allows to delete an instance of an object (on the local database and on the target system).

    :param args: List of the necessary arguments indicated by the user when the command is inputted.
    :return: Nothing
    """
    verbose = args.verbose
    idPlugin = args.id
    EnvironmentCli.verboseCli(verbose)
    osiris = Osiris(EnvironmentCli.getSystem(), EnvironmentCli.getPlugin())
    objectName = args.object
    osiris.objectDelete(objectName, idPlugin)


if __name__ == "__main__":
    main()
