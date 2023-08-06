class InternalRequestError(Exception):
    """
    Raised when getting content from a url fails. This could be due to a network error, bad url, bad request, bad status, etc.
    """


class UnknownContentType(Exception):
    """
    Raised when the content type of the response is not known.
    """
