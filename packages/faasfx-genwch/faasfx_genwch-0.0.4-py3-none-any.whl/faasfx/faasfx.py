from abc import ABC

class faasfx(ABC):
    """FaaS Function Class

    Returns:
        Class: FaaS Function
    """
    _req: dict

    def __init__(self, req: str = None) -> None:
        """init

        Args:
            req (str, optional): req from handle.py. Defaults to None.
        """
        if req != None:
            self._req = self.req(req=req)
        else:
            self._req = {}
        pass

    def req(self, req: str) -> dict:
        """function for handling req

        Args:
            req (str): req from handle.py

        Returns:
            dict: req in dict format
        """
        import json
        try:
            return json.loads(req)
        except:
            return req

    def path(self) -> str:
        """fucntion for handling url path

        Returns:
            str: path of url
        """
        import os
        return os.getenv("Http_Path")

    def query(self) -> str:
        """function for handling url query

        Returns:
            str: query of url
        """
        import os
        return os.getenv("Http_Query")

    def respond(self, code: int = 200, data: list = []) -> dict:
        """function for handling http respond

        Args:
            code (int, optional): http code. Defaults to 200.
            data (list, optional): data return. Defaults to [].

        Returns:
            dict: http respond return
        """
        import json
        rtn = {"code": code}

        if code == 200:
            rtn.update({"msg": "OK"})
        elif code == 400:
            rtn.update({"msg": "Bad Request"})
        elif code == 401:
            rtn.update({"msg": "Unauthorized"})
        elif code == 403:
            rtn.update({"msg": "Forbidden"})
        elif code == 404:
            rtn.update({"msg": "Not Found"})
        elif code == 500:
            rtn.update({"msg": "Internal Server Error"})
        elif code == 502:
            rtn.update({"msg": "Bad Gateway"})
        elif code == 503:
            rtn.update({"msg": "Service Unavailable"})

        if data != []:
            rtn.update({"data": data})
        return json.dumps(rtn)

    def apikey(self, env: str = "Http_X_Api_Key", file: str = "secret-api-key") -> bool:
        """function for handling apikey

        Args:
            env (str, optional): http header key. Defaults to "Http_X_Api_Key".
            file (str, optional): secret file. Defaults to "secret-api-key".

        Returns:
            bool: success - true, fail - false
        """
        def read_secret(secretName: str) -> str:
            """sub function to read secret file

            Args:
                secretName (str): secret name

            Returns:
                str: return secret
            """
            path = "/var/openfaas/secrets"
            file = f"{path}/{secretName}"
            tfile = open(file, "r")
            rtn = tfile.read()
            tfile.close()
            return rtn

        import os

        apikey = os.getenv(env)
        secert = read_secret(file)
        return apikey == secert
