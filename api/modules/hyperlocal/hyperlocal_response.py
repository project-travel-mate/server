class HyperLocalResponse(object):
    """
    Specifies the response to be sent foo one place object.
    """
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title')
        self.address = kwargs.get('address')
        self.website = kwargs.get('website')

    def to_json(self):
        """
        Return PlaceResponse object as python dictionary.
        :return:
        """
        return self.__dict__
