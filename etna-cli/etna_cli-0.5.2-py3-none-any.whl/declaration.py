import click
from datetime import datetime, date, timedelta
from etna_cli import config


@click.group(name="declare")
def main():
    """Declaration."""


@main.command(name="list")
@click.option("-n", "--number", type=int,
              help="number of declarations to list")
def list_declarations(number: int):
    """List declarations."""
    wrapper = config.setup_api()
    declarations = wrapper.get_declarations()
    cnt = 0
    for declaration in declarations['hits']:
        print("========================")
        print("UV name     : {}".format(declaration['uv_name']))
        print("started at  : {}".format(declaration['start']))
        print("ended at    : {}".format(declaration['end']))
        print("description : {}".format(declaration['metas']['description']))
        print("declared at : {}".format(declaration['metas']['declared_at']))
        cnt += 1
        if number is not None and cnt == number:
            break


def get_begining_of_run() -> datetime:
    """Get the begining of a run to list available modules."""
    wrapper = config.setup_api()
    logs = wrapper.get_logs()
    if len(logs['contracts'][0]['periods']) == 0:
        return None
    start = logs['contracts'][0]['periods'][0]['start'].split()[0]
    start_run = datetime.strptime(start.split()[0], '%Y-%m-%d') \
        + timedelta(days=1)
    return start_run


@main.command(name="modules")
def print_available_modules():
    """List available modules to declare for."""
    wrapper = config.setup_api()
    start_run = get_begining_of_run()
    if start_run is None:
        start_run = date.today()
    projects = wrapper.get_projects(date=start_run)
    for project in projects:
        if project['duration'] != 0:
            print("==============================")
            print("id         : {}".format(project['id']))
            print("name       : {}".format(project['name']))
            print("long name  : {}".format(project['long_name']))
            print("UV         : {}".format(project['uv_name']))
            print("starts on  : {}".format(project['date_start']))
            print("ends on    : {}".format(project['date_end']))
            print("duration   : {}".format(int(project['duration']) / 3600))
        else:
            pass


def get_uv_id(wrapper, UV_name: str) -> int:
    """Check if UV is available to declare
    then return the current UV id.
    """
    start_run = get_begining_of_run()
    if start_run is None:
        start_run = date.today()
    modules = wrapper.get_projects(date=start_run)
    for module in modules:
        if module['uv_name'].lower() == UV_name.lower():
            return module['id']
    return -1


@main.command(name="schedule")
def schedule():
    """List schedule."""
    schedules = get_declaration_schedule()
    if len(schedules) == 0:
        print("No schedule available for this run")

    for schedule in schedules:
        print("========================")
        print("starts at : {}".format(schedule['start']))
        print("ends at   : {}".format(schedule['end']))


def get_declaration_schedule() -> dict:
    wrapper = config.setup_api()
    logs = wrapper.get_logs()
    # there could me multipe contracts.
    # at this point just use the last one
    return logs['contracts'][0]['schedules']


def str2time(date_str) -> datetime:
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date_obj


def find_current_slot() -> str:
    schedules = get_declaration_schedule()
    for schedule in schedules:
        start = str2time(schedule['start'])
        end = str2time(schedule['end'])

        if start < datetime.now() < end:
            slot = "{}, {}".format(start, end)
            return slot
    return None


def ask_content() -> str:
    data = {}
    data['objectives'] = input("objectives : ")
    data['actions'] = input("actions : ")
    data['results'] = input("results : ")
    data['difficulties'] = input("difficulties : ")

    for content in data:
        if data[content] == "":
            data[content] = "RAS"

    output = "Objectifs :\n{}\n".format(data['objectives'])
    output += "Actions :\n{}\n".format(data['actions'])
    output += "Résultats :\n{}\n".format(data['results'])
    output += "Difficultés rencontrées :\n{}\n".format(data['difficulties'])
    return output


@main.command(name="go")
@click.option("-u", "--uv", required=True, help="specify UV")
@click.option("-s", "--slot", help="specify time slot like: \
                              \"2020-05-6 09:00,2020-05-6 12:00\"")
@click.option("-c", "--content", help="specify content")
@click.option("-d", "--declaration", help="declare from file")
def do_declare(uv: str, slot: str, content: str, declaration: str):
    """Declare work."""
    wrapper = config.setup_api()
    uv_id = get_uv_id(wrapper, uv)
    if uv_id == -1:
        print("UV is not available for declaration")
        return
    if slot is None:
        slot = find_current_slot()
        if slot is None:
            print("no slot available for declaring")
            print("please specify a slot with -s")
            return

    print("declaring for {} ({})".format(uv, uv_id))
    print("declaration slot : {}".format(slot))

    if content is None and declaration is None:
        content = ask_content()
    elif content is not None and declaration is not None:
        print("you can't choose both content and declaration")
        return
    elif declaration is not None:
        content = open(declaration).read()
    else:
        pass
    payload = {}
    payload['module'] = uv_id
    payload['declaration'] = {}
    payload['declaration']['start'] = slot.split(',')[0]
    payload['declaration']['end'] = slot.split(',')[1]
    payload['declaration']['content'] = content
    wrapper.declare_log(uv_id, payload)
