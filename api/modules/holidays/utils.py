import requests


def load_url_content(url):
    """
    Returns the response text from given URL
    :param url:
    :return:
    """
    try:
        r = requests.get(url)
        if r.ok:
            return r.text
        else:
            return None
    except Exception:
        return None
