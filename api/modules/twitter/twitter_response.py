class SearchTweetResponse(object):
    """
    Specifies the response to be sent for one search result tweet object.
    """
    def __init__(self, *args, **kwargs):
        self.created_at = kwargs.get('created_at', None)
        self.text = kwargs.get('text', None)
        self.username = kwargs.get('username', None)
        self.user_screen_name = kwargs.get('user_screen_name', None)
        self.user_profile_image = kwargs.get('user_profile_image', None)
        self.retweet_count = kwargs.get('retweet_count', None)
        self.favorite_count = kwargs.get('favorite_count', None)
        self.tweet_url = kwargs.get('tweet_url', None)

    def to_json(self):
        """
        Return SearchTweetResponse object as python dictionary.
        :return:
        """
        return self.__dict__
