
class InvalidTokenException(Exception):
    def __init__(self):
        super().__init__(
            "Token is invalid."
        )

class InvalidRulesException(Exception):
    def __init__(self):
        super().__init__(
            "Rules are invalids.\n" + \
            "Accepts list of dict with name and value not empty,\n" + \
            "ex: [{'name':'abc','value':'xpto'}]."
        )

class SameRulesValueException(Exception):
    def __init__(self):
        super().__init__(
            "Rules are invalids.\n" + \
            "Same value is defined in more than one rule."
        )
