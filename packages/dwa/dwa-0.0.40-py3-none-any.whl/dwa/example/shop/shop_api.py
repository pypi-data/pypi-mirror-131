def api_post(**kwargs):
    try:
        import os
        import json
        params = kwargs["params"]
        cookies = kwargs["cookies"]
        test_server = kwargs["test_server"]
        _sql = kwargs["sql"]
        domain = kwargs["domain"]
        server_name = kwargs["server_name"]
        writer = kwargs["writer"]
        app_root = kwargs["app_root"]
        export_functions = kwargs["export_functions"]
        username = cookies["get_secure"]("username")
        ip = kwargs["x_real_ip"]
        exec(open(os.path.join(app_root, "shop_utils.py"), "rb").read(), locals())
        exec(open(os.path.join(app_root, "common", "api_utils.py"), "rb").read(), locals())
        _myfunc = locals()["myfunc"]
        def request_test():
            return (
                export_functions("get_item_info", 0),
                export_functions("reserve_order", 1),
                _myfunc(params["a"][0]),
            )
        jsons = "Error! Not implemented yet."
        if params["request"][0] == "test":
            jsons = request_test()
        else:
            raise Exception(jsons)
        return json.dumps(jsons) or "true"
    except locals()["CustomException"] as e:
        return Exception(str(e))
    except:
        import traceback
        traceback.print_exc()
        return Exception(traceback.format_exc())
