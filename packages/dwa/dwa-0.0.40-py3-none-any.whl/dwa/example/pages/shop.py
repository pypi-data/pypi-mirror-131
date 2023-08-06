from dwa import *


server_name = "shop"


class HTML_template(handlers.HTML):
    server = server_name

    def get_what(self, og_title=None, og_description=None):
        css = '''<link rel="{{}}" href="/css/min/{}.css">'''
        css = css.format(self.file_name)
        css = css.format('preload" as="style')+css.format("stylesheet")
        js = '''<script async src="/js/min/{}.js" type="text/javascript"></script>'''
        js = js.format(self.file_name)
        fc = open(os.path.join(self.app_root, "{}.html".format(self.file_name)), "rb").read()
        string = b"</title>"
        index = fc.find(string)+len(string)
        head = fc[:index]
        if not og_title:
            og_title = head.split(b"<title>")[1].split(string)[0]
        if not og_description:
            og_description = head.splitlines()[0].split(b"\"")[-2]
        head += (css+js).encode()
        body = fc[index:]
        loader = tornado.template.Loader(self.app_root)
        og_image = "/img/asset/icon/test.svg"
        html = loader.load("template.html").generate(
            head=head,
            body=body,
            og_image=og_image,
            og_title=og_title,
            og_description=og_description
        )
        if self.test_server:
            pass
        return html


def template_page(_file_name):
    class _(HTML_template):
        file_name = _file_name
    return _


class shop_api_page(handlers.AJAX):
    server = server_name
    api_name = "shop"

    def check_xsrf_cookie(self):
        pass

    def get(self):
        raise tornado.web.HTTPError(405)


class admin_page(handlers.AJAX):
    server = server_name
    api_name = "admin"

    def check_xsrf_cookie(self):
        pass

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        super().prepare()


class static_page(handlers.File):
    server = server_name


def get_shop_settings():
    return [
        server_name,
        [
            [r"/", template_page("index")],
            [r"/api", shop_api_page],
            [r"/((?:js|css)/.*)", static_page],
        ]
    ]


def get_shop_admin_settings():
    return [
        [r"/admin/{}".format(server_name), admin_page],
        [r"/admin/{}/((?:js|css)/.*)".format(server_name), static_page],
    ]

