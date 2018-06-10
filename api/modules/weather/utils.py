def to_celsius(temperature_in_kelvins):
    """
    Return temperature in celsius rounded off to 2 digits
    :param temperature_in_kelvins:
    :return:
    """
    return round(temperature_in_kelvins - 273.15, 2)


def icon_to_url(icon):
    """
    Changes icon identifier to client accessible link
    Reference: https://stackoverflow.com/a/44234308/5602759
    :param icon:
    :return:
    """
    return "http://openweathermap.org/img/w/{0}.png".format(icon)
