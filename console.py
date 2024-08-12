#!/usr/bin/python3
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


class HBNBCommand(cmd.Cmd):
    """ command interpreter for the HBNB PROJECT """
    prompt = " (hbnb) "  # custom prompt
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
        "City": City

    }

    def onecmd(self, line: str):
        match = re.match(r'(\w+)\.(\w+)\((.*)\)', line)
        if match:
            class_name, method_name, args = match.groups()

            if class_name in HBNBCommand.__classes:
                method = getattr(self, f'do_{method_name}', None)
                if method:
                    clean_args = args.strip()  # Strips whitespace, not quotes
                    return method(f"{class_name} {clean_args}")
                else:
                    print(f"** method {method_name} doesn't exist **")
            else:
                print(f"** class {class_name} doesn't exist **")
        return super().onecmd(line)

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """ EOF command to exit the program """
        print()  # to add newline before exiting
        return True

    def emptyline(self):
        """ DO nothing on empty input line """
        pass

    def do_help(self, line):
        """ Call a default help method for a specific command"""
        if line:
            super().do_help(line)
        else:
            print("Documented commands (type help <topic>): ")
            print("======================================== ")
            print("EOF help quit")

    def do_create(self, line):
        """Create a new instance of the class and print its ID."""
        parts = line.split()
        if len(parts) == 0:
            print("** class_name doesn't exit")
            return
        class_name = parts[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        class_obj = HBNBCommand.__classes[class_name]
        if not issubclass(class_obj, BaseModel):
            print("** class doesn't exist **")
            return

        new_instance = class_obj()
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_show(self, line):
        print(line)
        """Show the string representation of an instance based on the class name and ID."""
        parts = line.split()
        if len(parts) < 2:
            print("** class name missing **" if len(parts) == 0 else "** instance id missing **")
            return

        class_name, obj_id = parts[0], parts[1].strip('"')
        print(class_name)
        print(obj_id)
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{obj_id}"
        print(key)
        obj = storage.all().get(key)

        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        parts = line.split()
        if len(parts) < 2:
            if len(parts) == 0:
                print("** class name missing **")
            elif len(parts) == 1:
                print("** instance id missing **")
            return

        class_name, obj_id = parts[0], parts[1]

        if class_name not in HBNBCommand.__classes:
            print(" ** class doesn't exist ** ")
            return

        obj_key = f'{class_name}.{obj_id}'
        obj = storage.all().get(obj_key)

        if obj:
            del storage.all()[obj_key]
            storage.save()
        else:
            print(" ** no instance found ** ")

    def do_all(self, line):
        """ Prints all string representation of all instances based or not on the class name. Ex: """
        parts = line.split()

        class_name = parts[0] if parts else None
        if class_name:
            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            cls = HBNBCommand.__classes[class_name]

            instances_list = [str(obj) for obj in storage.all().values() if isinstance(obj, cls)]
        else:
            instances_list = [str(obj) for obj in storage.all().values()]
        print(instances_list)

    def do_count(self, line):
        parts = line.split()

        if len(parts) == 0:
            print("** class doesn't exist **")
            return
        class_name = parts[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exit")

        # get the class from the class_name
        class_obj = HBNBCommand.__classes[class_name]

        # check if the class is a subclass of Basemodel
        if not issubclass(class_obj, BaseModel):
            print("** Class doesn't exist **")
            return
        # count the instances
        count = sum(1 for key in storage.all() if key.startswith(class_name + '.'))
        print(count)

    def do_update(self, line):
        """Updates an instance based on the class name and ID by adding or updating attributes."""
        # Use regex to match class name, ID, attribute name, and value or a dictionary
        print(line)
        match = re.match(r'(\w+)\s+"(\S+)",\s*(.*)', line)
        if not match:
            print("** invalid syntax **")
            return

        class_name, obj_id, attributes = match.groups()
        obj_id = obj_id
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{obj_id}"
        obj = storage.all().get(key)

        if not obj:
            print("** no instance found **")
            return

        # Check if the attributes part is a dictionary
        if attributes.startswith('{') and attributes.endswith('}'):
            # Convert the string to a dictionary
            try:
                attributes_dict = eval(attributes)
            except (SyntaxError, ValueError):
                print("** invalid dictionary syntax **")
                return

            for attribute_name, attribute_value in attributes_dict.items():
                if attribute_name not in ["id", "created_at", "updated_at"]:
                    try:
                        current_value = getattr(obj, attribute_name, "")
                        attribute_type = type(current_value) if current_value else str
                        attribute_value = attribute_type(attribute_value)
                    except (ValueError, TypeError):
                        pass
                    setattr(obj, attribute_name, attribute_value)
            obj.save()

        else:
            print(f'Debug: {attributes}')
            # Split attributes string by commas, then clean up quotes and spaces
            parts = [part.strip('" ') for part in attributes.split(",")]

            if len(parts) < 2:
                print("** invalid syntax **")
                return

            attribute_name, attribute_value = parts[0], parts[1]
            if attribute_name not in ["id", "created_at", "updated_at"]:
                try:
                    current_value = getattr(obj, attribute_name, "")
                    attribute_type = type(current_value) if current_value else str
                    attribute_value = attribute_type(attribute_value)
                except (ValueError, TypeError):
                    pass
                setattr(obj, attribute_name, attribute_value)
                obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

