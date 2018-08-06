class FoodResponse(object):
    """
    Specifies the response to be sent for the zomato details.
    """

    def __init__(self, *args, **kwargs):
        self.restaurant_id = int(kwargs.get("id", -1))
        self.restaurant_name = kwargs.get("name", "")
        self.restaurant_url = kwargs.get("url", "#")
        self.restaurant_latitude = float(kwargs.get("latitude", 0))
        self.restaurant_longitude = float(kwargs.get("longitude", 0))
        self.avg_cost_2 = kwargs.get("avg2", 0)
        self.currency = kwargs.get("currency", "")
        self.restaurant_image = kwargs.get("image", "")
        self.aggregate_rating = float(kwargs.get("rating", 0))
        self.votes = int(kwargs.get("votes", 0))
        self.address = kwargs.get("address", "")

    def to_json(self):
        """
        Return as a python dictionary
        """
        return self.__dict__


class FoodDetailedResponse(object):
    """
    Specifies the response to be sent for a given restaurant id
    """

    def __init__(self, *args, **kwargs):
        self.restaurant_id = int(kwargs.get("id", -1))
        self.restaurant_name = kwargs.get("name", "")
        self.restaurant_url = kwargs.get("url", "")
        self.restaurant_address = kwargs.get("address", "")
        self.restaurant_longitude = float(kwargs.get("longitude", 0))
        self.restaurant_latitude = float(kwargs.get("latitude", 0))
        self.avg_cost_2 = kwargs.get("avg2", 0)
        self.price_range = kwargs.get("price_range", 0)
        self.currency = kwargs.get("currency", "")
        self.featured_image = kwargs.get("img", "")
        self.user_aggregate_rating = kwargs.get("agg_rating", 0)
        self.user_rating_votes = kwargs.get("votes", 0)
        self.is_delivering_now = bool(kwargs.get("deliver", 0))
        self.has_table_booking = bool(kwargs.get("booking", 0))
        self.cuisines = kwargs.get("cuisines", "")
        self.phone_numbers = kwargs.get("phone_numbers", "")

    def to_json(self):
        """
        Return a python dictionary
        """
        return self.__dict__
