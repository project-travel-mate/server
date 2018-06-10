class ShoppingItem(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", None)
        self.url = kwargs.get("url", None)
        self.image = kwargs.get("image", None)
        self.value = kwargs.get("value", None)
        self.currency = kwargs.get("currency", None)

    def to_json(self):
        return self.__dict__
