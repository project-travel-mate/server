class WeatherResponse(object):
    def __init__(self, *args, **kwargs):
        self.temp = kwargs.get("temp", None)
        self.temp_units = kwargs.get("temp_units", "C")

        self.max_temp = kwargs.get("max_temp", None)
        self.min_temp = kwargs.get("min_temp", None)

        self.description = kwargs.get("description", None)
        self.icon = kwargs.get("icon", None)

        self.humidity = kwargs.get("humidity", None)
        self.humidity_units = kwargs.get("humidity_units", "%")
        self.pressure = kwargs.get("pressure", None)
        self.pressure_units = kwargs.get("pressure_units", "hPa")

    def to_json(self):
        return self.__dict__
