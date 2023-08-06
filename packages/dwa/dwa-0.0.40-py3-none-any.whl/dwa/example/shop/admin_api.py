def api_get(**kwargs):
    html_template = '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Admin</title>
    <link rel="stylesheet" type="text/css" href="shop/css/min/style.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script async defer src="shop/js/min/admin.js"></script>
</head>
<body>
    {}
</body>
</html>
'''
    try:
        import os
        from urllib.parse import quote as _encodeURIComponent
        from html import escape as _html_escape
        def encodeURIComponent(s):
            return _encodeURIComponent(str("" if s is None else s))
        def html_escape(s):
            return _html_escape(str("" if s is None else s))
        export_functions = kwargs["export_functions"]
        app_root = kwargs["app_root"]
        domain = kwargs["domain"]
        server_name = kwargs["server_name"]
        test_server = kwargs["test_server"]
        params = kwargs["params"]
        cookies = kwargs["cookies"]
        SQL = kwargs["sql"]
        writer = kwargs["writer"]
        username = None
        htmls = "Error! Not implemented yet."
        tabs = '''
<table>
    <td><a rel='noreferrer' href="?db=_sql">SQL</a></td>
    <td><a rel='noreferrer' href="?db=test">test</a></td>
</table><br/>'''
        def db_test():
            return tabs+'''<form method='post' target='_blank'>
    <input type='hidden' name='db' value='test'/>
    <input name='a' />
    <input type='submit' value='Submit'/>
    </form>'''
        def db__sql():
            return tabs+'''
            <form style='text-align:center'>
                <textarea name='_sql' style='width: 100%; height: 30%; font-size: 2vh;'></textarea>
                <input id='db__sql_execute' type='button' value='Execute' />
            </form>
            <br/>
            <div id='_sql_result'></div>
            '''
        if len(params) == 0:
            htmls = tabs
        elif params["db"][0] == "test":
            htmls = db_test()
        elif params["db"][0] == "_sql":
            htmls = db__sql()
        return html_template.format(htmls)
    except:
        import traceback
        traceback.print_exc()
        return html_template.format(tabs+html_escape(traceback.format_exc()).replace("\n", "<br/>"))


def api_post(**kwargs):
    try:
        import os
        import re
        import json
        params = kwargs["params"]
        cookies = kwargs["cookies"]
        SQL = kwargs["sql"]
        writer = kwargs["writer"]
        app_root = kwargs["app_root"]
        export_functions = kwargs["export_functions"]
        username = None
        exec(open(os.path.join(app_root, "common", "api_utils.py"), "rb").read(), locals())
        _myfunc2 = locals()["myfunc2"]
        def db_test():
            return _myfunc2(params["a"][0])
        def db__sql():
            if "op" in params:
                _sql = ""
                if "_sql" in params:
                    _sql = params["_sql"][0]
                if params["op"][0] == "execute":
                    return SQL(_sql)
        jsons = "Error! Not implemented yet."
        if params["db"][0] == "test":
            jsons = db_test()
        elif params["db"][0] == "_sql":
            jsons = db__sql()
        return json.dumps(jsons) or "true"
    except:
        import traceback
        traceback.print_exc()
        return json.dumps(traceback.format_exc())
