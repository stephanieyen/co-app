# Object for a user
class User:
    def __init__(self, email, name, allergies, admin, days, coop):
        self._email = email
        self._name = name
        self._allergies = allergies
        self._admin = admin
        self._days = days
        self._coop = coop
    
    # Getter methods for user
    def get_email(self):
        return self._email

    def get_name(self):
        return self._name

    def get_allergies(self):
        return self._allergies

    def get_admin(self):
        return self._admin

    def get_days(self):
        return self._days
        
    def get_coop(self):
        return self._coop
    
    # Get string representation of user
    def __str__(self):
        str_self = "Name: " + self._name + ", Email: " + self._email 
        str_self += ", Allergies/Food Restrictions: " + self._allergies
        str_self += ", Preferred Days: " + self._days
        str_self += ", Co-op: " + self._coop
        if self._admin:
            str_self += ", Admin"
        else:
            str_self += ", Member"
        return str_self