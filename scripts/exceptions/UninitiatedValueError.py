class UninitiatedValueError(Exception):
    """Exception raised for values that have not been initialized or set.
       ie. position or size of a tile being None"""
    pass