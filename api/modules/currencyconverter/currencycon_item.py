class CurrencyItem(object):
    def __init__(self, *args, **kwargs):
        self.source = kwargs.get("source", None)
        self.target = kwargs.get("target", None)
        self.result = kwargs.get("result", None)

    def to_json(self):
        return self.__dict__