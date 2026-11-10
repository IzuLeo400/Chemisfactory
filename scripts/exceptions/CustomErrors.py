class InventoryManagementError(Exception):
    """Exception raised for errors during inventory management.
       ie. no interactables being selected during item removal"""
    pass

class InventoryItemManagementError(Exception):
    """Exception raised for errors during inventory item management.
       ie. adding or removing nonexistent items from the inventory."""
    pass

class UninitiatedValueError(Exception):
    """Exception raised for values that have not been initialized or set.
       ie. position or size of a tile being None"""
    pass

class StractureManagementError(Exception):
    """Exception raised for internal management of a structure misbehaving
    ie: failed to actually create building or assign to Source because other checks fail"""