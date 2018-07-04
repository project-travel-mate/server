class ContributorResponse(object):
    """
    Specifies the response to be sent for one github contributor object.
    """
    def __init__(self, *args, **kwargs):
        self.username = kwargs.get('username', None)
        self.url = kwargs.get('url', None)
        self.avatar_url = kwargs.get('avatar_url', None)
        self.contributions = kwargs.get('contributions', None)
        self.repository_name = kwargs.get('repository_name', None)

    def to_json(self):
        """
        Return ContributorResponse object as python dictionary.
        :return:
        """
        return self.__dict__
