#-------------------------------------------------------------------------------
class DTO_User(object):
    #...........................................................................
    """ DB Table. companies. """
    #...........................................................................
    def __init__(self, id=0,  email="-", fname="-",  lname="-",  password="-", status="-", token="-"):
        self.id             = id
        self.email          = email
        self.fname          = fname
        self.lname          = lname
        self.password       = password
        self.status         = status
        self.token          = token
#-------------------------------------------------------------------------------