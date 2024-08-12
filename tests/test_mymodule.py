import datetime
import os.path
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import time
import json
from models.amenity import Amenity
from models.city import City
from models.place import Place,
from models.review import  Review
from models.state import State
from models.user import User


class TestBaseModel(unittest.TestCase):
    """ Test cases for the Basemodel class"""

    def setUP(self):
        self.model = BaseModel()

    def Test_default_initiliazation(self):
        """Tests default initialization without kwargs"""
        self.model = BaseModel()
        self.assertIsInstance(self.id, str)
        self.assertIsInstance(self.test_created_at, datetime.datetime)
        self.assertIsInstance(self.test_update_at, datetime.datetime)

    def test_id(self):
        """ Test that the id is valid uuid"""
        self.assertIsInstance(self.model.id, str)
        self.assertEqual(len(self.model.id), 36)

    def test_created_at(self):
        """ Test that created at is a datetime instance"""
        self.assertIsInstance(self.model.created_at, datetime.datetime)

    def test_update_at(self):
        """ Test that created at is a datetime instance"""
        self.assertIsInstance(self.model.updated_at, datetime.datetime)

    def test_save(self):
        """ tests id the save method updates the update_at attribute """
        old_update_at = self.model.updated_at
        time.sleep(0.001)
        self.model.save()
        self.assertNotEqual(old_update_at, self.model.updated_at)

    def to_dict(self):
        """ Test the Dict method """
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict['id'], self.model.id)
        self.assertEqual(model_dict['created_at'], self.model.created_at)
        self.assertEqual(model_dict['updated_at'], self.model.updated_at)
        self.assertTrue('created_at' in model_dict)
        self.assertTrue('updated_at' in model_dict)
        self.assertTrue('id' in model_dict)

    def test_initialization_with_kwargs(self):
        """ Test the initialization with kwargs"""

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()
        model = BaseModel(id="1234", created_at=datetime.datetime.isoformat(), updated_at=datetime.datetime.isoformat())

        self.assertEqual(model.id, "1234")
        self.assertEqual(model.updated_at, updated_at)
        self.assertEqual(model.created_at, created_at)


class TestFileStorage(unittest.TestCase):
    """ Test case for the file storage """

    @classmethod
    def setUpClass(cls):
        cls.storage = FileStorage()
        cls.base_model = BaseModel()

    def setUp(self):
        """ set Up for individual tests. """
        self.storage._FileStorage__objects = {}
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    def test_all(self):
        """ tests if __object exists"""
        self.assertTrue(self.storage.all(), {})

    def test_new(self):
        """ Test the new method """
        self.storage.new(self.base_model)
        key = f'{self.base_model.__class__.__name__}.{self.base_model.id}'
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], self.base_model)

    def test_save(self):
        """ Test the save method """
        self.storage.new(self.base_model)
        self.storage.save()
        if os.path.exists(self.storage._FileStorage__file_path):
            with open(self.storage._FileStorage__file_path, 'r') as file:
                dict_contents = json.load(file)
            key = f"BaseModel.{self.base_model.id}
            self.assertIn(key, dict_contents)
            self.assertEqual(dict_contents[key]['id'], self.base_model.id)

    def test_reload(self):
        """Test the reload method """
        self.storage.new(self.base_model)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        key = f"BaseModel.{self.base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key].id, self.base_model.id)


class TestCity(unittest.TestCase):
    """ Test case for place """
    def do_variables(self):
        """ Test all the class variables """
        self.assertIsInstance(City.state_id, str)
        self.assertIsInstance(City.name, str)

class TestAmenity(unittest.TestCase)
    """ TEst case for Amenity """

    def do_amenity_variables(self):
        """ Test all the class variables"""
        self.assertIsInstance(Amenity.name, str)

class Testreview(unittest.TestCase)
    """ Test case for Amenity """

    def do_review(self):
        """ Test all the class variables"""
        self.assertIsInstance(Review.place_id, str)
        self.assertIsInstance(Review.user_id, str)
        self.assertIsInstance(Review.text, str)

class TestPlace(unittest.TestCase)
    """ Test case for place """
    def do_place(self):
        """ Test case for all the variables"""

        place = Place()
        place.city_id = "SF"
        place.user_id = "user123"
        place.name = "Luxury Apartment"
        place.description = "A beautiful apartment with a view."
        place.number_rooms = 3
        place.number_bathrooms = 2
        place.max_guest = 6
        place.price_by_night = 200
        place.latitude = 37.7749
        place.longitude = -122.4194
        place.amenity_ids = ["amenity1", "amenity2"]

        self.assertEqual(place.city_id, "SF")
        self.assertEqual(place.user_id, "user123")
        self.assertEqual(place.name, "Luxury Apartment")
        self.assertEqual(place.description, "A beautiful apartment with a view.")
        self.assertEqual(place.number_rooms, 3)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 6)
        self.assertEqual(place.price_by_night, 200)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)
        self.assertEqual(place.amenity_ids, ["amenity1", "amenity2"])

class Teststate(unittest.TestCase):
    """ Test case for class state """
    def test_state(self):
        state_obj= State()
        state_obj.name = ""
        self.assertIsInstance(state_obj.name, str)
        self.assertEqual(state_obj.name, "")


if __name__ == "__main__":
    unittest.main()
