#-------------------------------------------------------------------------------
class DTO_Recipe(object):
    #...........................................................................
    """ DB Table. recipes. """
    #...........................................................................
    def __init__(self, id=0,  name="-",  description="-", image="-", info=dict()):
        self.id             = id
        self.name           = name
        self.description    = description
        self.image          = image
        self.ingredients    = info.pop("ingredients", "-")
        self.steps          = info.pop("steps", "-")
#-------------------------------------------------------------------------------