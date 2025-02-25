from helpers.config import get_settings
import os
import random
import string

class BaseController:
    
    def __init__(self):
        self.app_settings= get_settings()
        self.base_dir= os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets/Files")
    

    def generate_random_string(self, length: int = 12) -> str:
        """
        Generates a random string of a specified length.

        Args:
            length (int): The length of the random string to generate. Default is 10.

        Returns:
            str: A random string containing uppercase letters, lowercase letters, and digits.
        """
        # Define the characters to use for generating the random string
        characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
    
        # Generate the random string
        random_string = ''.join(random.choices(characters,k=length))
    
        return random_string