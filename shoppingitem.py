# Object for a shopping item
class ShoppingItem:
    def __init__(self, id, type, name, quantity, accepted, reason, user, coop):
        self._id = id
        self._type = type
        self._name = name
        self._quantity = quantity
        self._accepted = accepted
        self._reason = reason
        self._user = user
        self._coop = coop

    # Get string representation of shopping list item
    def __str__(self):
        str_self = "Name: " + self._name + ", Type: "
        if self._type:
            str_self += "Food"
        else:
            str_self += "Equipment" 
        str_self += ", Quantity: " + self._quantity
        if self._accepted:
            str_self += ", Accepted: Yes"
        else:
            str_self += ", Accepted: No"
        str_self += ", Reason: " + self._reason
        str_self += ", Requesting User: " + self._user
        str_self += ", Co-Op: " + self._coop
        return str_self
    