from models.base_model import BaseModel


class User(BaseModel):
    """ contains all information of user """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

