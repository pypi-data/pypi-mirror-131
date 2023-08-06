from dwa import *


server_name = "root"


class root_html(handlers.HTML):
    server = server_name


def template_page(_file_name):
    class _(root_html):
        file_name = _file_name
    return _


class static_page(handlers.File):
    server = server_name


def get_root_settings():
    return (
        server_name,
        [
            [r"/", template_page("index")],
            [r"/((?:img|js|css|common)/.*)", static_page],
        ]
    )
