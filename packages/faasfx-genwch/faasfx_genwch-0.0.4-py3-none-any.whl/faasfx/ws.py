class ws:
    _html = None
    _url = ""

    def __init__(self, url: str = "") -> None:
        self._url = url
        if url != "":
            self._html = self.html(url=url)
        pass

    def get(self, url: str = None):
        import requests
        url = self._url if url == None else url
        rtn = requests.get(url=url)
        return rtn

    def html(self, url: str = None, status_code: int = 200):
        from lxml.html import fromstring
        import re
        _o = self.get(url=url)
        if _o.status_code != status_code:
            return None
        rtn = str(_o.text)
        rtn = re.sub(r"\n", "", rtn)
        rtn = re.sub(r"\t", "", rtn)
        return fromstring(rtn)

    def xpath(self, xpath: str, html=None) -> list:
        _html = (self.html() if self._html ==
                 None else self._html) if html == None else html
        rtn = _html.xpath(xpath)
        return rtn


    def attr(self, xpath: str, attr: str, default=None, reval: dict={}, key: str=None, html=None, unique: bool = True, ignnone:bool = True) -> list:
        def _reval(val: str, reval: dict={}) -> str:
            import re
            rtn = val
            for f, t in reval.items():
                rtn = re.sub(f, t, rtn)
            return rtn

        import json
        if attr == "text":
            rtn = [_reval(_o.text, reval)
                   for _o in self.xpath(xpath, html=html)]
        elif attr == "json":
            rtn = [json.loads(_reval(_o.text, reval)).get(key, default)
                   for _o in self.xpath(xpath, html=html)]
        elif attr == "tail":
            rtn = [_reval(_o.tail, reval)
                   for _o in self.xpath(xpath, html=html)]
        else:
            rtn = [_reval(_o.attrib.get(attr, default), reval)
                   for _o in self.xpath(xpath, html=html)]
        if unique:
            rtn = list(set(rtn))
        if ignnone:
            rtn = [r for r in rtn if r != None]
        return rtn

    def match(self, xpath: str, attr: str, pattern=str, default=None, html=None) -> list:
        import re
        rtn = []
        for _o in self.attr(xpath=xpath, attr=attr, default=default, html=html):
            if re.match(pattern, _o) != None:
                rtn.append(_o)
        return rtn