#-------------------------------------------------------------------------------
class DTO_Recipe(object):
    #...........................................................................
    """ DB Table. recipes. """
    #...........................................................................
    def __init__(self, id=0,  name="-",  description="-", image="-", info=dict(), price="0.0", location="-", place_name="-"):
        self.id             = id
        self.name           = name
        self.description    = description
        self.image          = image
        self.ingredients    = info.pop("ingredients", "-")
        self.steps          = info.pop("steps", "-")
        self.price          = price
        self.location       = location
        self.place_name     = place_name
#-------------------------------------------------------------------------------