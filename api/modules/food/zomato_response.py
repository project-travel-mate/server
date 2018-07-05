class Zomato_Response(object):
    """
    Specifies the response to be sent for the zomato details.
    """

    def __init__(self, *args, **kwargs):

        self.restaurant_id = kwargs.get("id", -1)
        self.restaurant_name = kwargs.get("name", "")
        self.restaurant_url = kwargs.get("url", "#")
        self.restaurant_latitude = kwargs.get("latitude", 0)
        self.restaurant_longitude = kwargs.get("longitude", 0)
        self.avg_cost_2 = kwargs.get("avg2", 0)
        self.currency = kwargs.get("currency", "")
        self.restaurant_image = kwargs.get("image", "")
        self.aggregate_rating = kwargs.get("rating", 0)
        self.votes = kwargs.get("votes", 0)
        self.phone_numbers = kwargs.get("phone_numbers", 0)

    def to_json(self):
        """
        Return as a python dictionary
        """

        return self.__dict__
