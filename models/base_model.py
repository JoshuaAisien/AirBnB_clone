import uuid
import datetime
import models
""" Initilization file """


class BaseModel:
    """defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """ Initializes the Basemodel instance """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        value = datetime.datetime.fromisoformat(value)
                    setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def __str__(self):
        """ print: [<class name>] (<self.id>) <self.__dict__> """
        return f"[{self.__class__.__name__}] ({self.id}) ({self.__dict__})"

    def save(self):
        """ updates the public instance attribute updated_at with the current datetime """
        self.updated_at = datetime.datetime.now()
        models.storage.save()  # call save on storage

    def to_dict(self):
        """  returns a dictionary containing all keys/values of __dict__ of the instance """
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = self.__class__.__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        return instance_dict

    def new_instance(self):
        """Add the instance to storage"""
        from models import storage








