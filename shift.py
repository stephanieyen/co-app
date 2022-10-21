# Object for a shift
class Shift:
    def __init__(self, id, name, type, item, time, creator, members, coop):
        self._id = id
        self._name = name
        self._type = type
        self._item = item
        self._time = time
        self._creator = creator
        self._members = members
        self._coop = coop
    
    # Get string representation of shift
    def __str__(self):
        str_self = "Name: " + self._name + ", Type: " + self._type
        str_self += ", Item: " + self._item
        time_split = self._time.split(" ")
        str_self += ", Time: " + time_split[0] + "/" + time_split[1]
        str_self += " " + time_split[2] + ":00 " + time_split[3]
        str_self += ", Creator: " + self._creator
        str_self += ", Members:"
        for member in self._members:
            str_self += " " + member
        str_self += ", Co-Op: " + self._coop
        return str_self