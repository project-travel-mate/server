class CurrencyItem(object):
    """
    Specifies the response to be sent for a currency object.
    """
    def __init__(self, *args, **kwargs):
        """
        Set values for object.
        :param args:
        :param kwargs:
        """
        self.source = kwargs.get("source", None)
        self.target = kwargs.get("target", None)
        self.result = kwargs.get("result", None)

    def to_json(self):
        """
        Return Currency object as python dictionary.
        :return:
        """
        return self.__dict__


class CurrencyDate(object):
    """
    Specifies the response to be sent for a currency object.
    """

    def __init__(self, *args, **kwargs):
        """
        Set values for object.
        :param args:
        :param kwargs:
        """
        self.value = kwargs.get("value", None)

    def to_json(self):
        """
        Return Currency object as python dictionary.
        :return:
        """
        return self.__dict__
