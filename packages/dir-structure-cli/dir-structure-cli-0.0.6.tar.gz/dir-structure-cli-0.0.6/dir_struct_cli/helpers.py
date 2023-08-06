import click


def skeleton_router(temps, *args):
    from .handlers import DjangoHandler

    """
    Skeleton_router is a helper function that maps the templates names
    to their corresponding functions

    Ex:
        django: django_handle(*args)

    """

    skeletons_router = {"django": DjangoHandler}  # router dict

    for temp in temps:  # excute the handle function of each template in "temps"
        try:
            router_instance = skeletons_router[temp](*args)
            router_instance.handle()
            print("router done..")
        except KeyError:
            click.secho(
                f"{temp} directory skeleton generation not implemented yet", fg="yellow"
            )
