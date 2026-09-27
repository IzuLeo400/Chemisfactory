class InventoryItemManagementError(Exception):
    """Exception raised for errors during inventory item management.
       ie. adding or removing nonexistent items from the inventory."""
    pass