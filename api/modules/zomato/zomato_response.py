class Zomato_Response(object):
    """
    Specifies the response to be sent for the zomato details.
    """

    def __init__(self,*args,**kwargs):

        self.id = kwargs.get("restaurant_id",-1)
        self.name = kwargs.get("restaurant_name","")
        self.url = kwargs.get("restaurant_url","#")
        self.lattitue = kwargs.get("restaurant.latitude",0)
        self.longitude = kwargs.get("restaurant_longitude",0)
        self.avg2 = kwargs.get("avg_cost_2",0)
        self.currency = kwargs.get("currency","")
        self.image = kwargs.get("restaurant_image","")
        self.rating = kwargs.get("aggregate_rating",0)
        self.votes = kwargs.get("votes",0)
        self.phone_numbers = kwargs.get("phone_numbers",0)
    
    def to_json(self):
        """
        Return as a python dictionary
        """
        
        return self.__dict__

