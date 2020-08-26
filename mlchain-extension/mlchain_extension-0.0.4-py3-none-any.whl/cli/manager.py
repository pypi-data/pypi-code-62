import click


@click.command("manager", short_help="Run service manager.", context_settings={"ignore_unknown_options": True})
@click.argument('type', nargs=1, required=True, default=None)
def manager_comand(type):
    type = type.lower()
    if type == 'start':
        from mlchain_extension.queue.redis.queue_event import QueueEventManager
        QueueEventManager().run()
    elif type == 'api':
        from mlchain_extension.queue.redis.queue_manager import load_app
        app = load_app()
        app.run(host='0.0.0.0', port=8032)
    elif type == 'collect_database':
        from mlchain_extension.queue.redis.collect_database import CollectDatabase
        CollectDatabase().run()
    else:
        raise Exception("type must be start/api/collect_database")
