class MetromobiliteException(Exception):
    pass

class MetromobiliteInvalidDataException(Exception):
    def __init__(self):
        super(MetromobiliteInvalidDataException, self).__init__("Error while parsing json")


class MetromobiliteRequestException(MetromobiliteException):
     def __init__(self, status_code):
        super(MetromobiliteRequestException, self).__init__("Http Error : " + str(status_code))
