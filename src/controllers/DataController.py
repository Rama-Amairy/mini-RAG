from .BaseController import BaseController
from .ProjectController import ProjectController

from fastapi import UploadFile
from models import ResponseEnum

import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 #convert MB to B

    #check the uploaded file (type and size)
    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale :
            return False, ResponseEnum.FILE_SIZE_EXCEEDED.value
        
        return True , ResponseEnum.FILE_UPLOADED_SUCCEEDED.value

    def generate_unique_filepath(self, file_name: str, project_id:str):
        random_Key= self.generate_random_string()
        project_path= ProjectController().get_project_path(project_id=project_id)[0]
        cleaned_file_name= self.clean_file_name(file_name = file_name)
        # Construct the new file path
        new_file_path = os.path.join(project_path, random_Key + "_" + cleaned_file_name)

        while os.path.exists(new_file_path):
            new_file_path= os.path.join(project_path, random_Key+"_"+cleaned_file_name)
        return new_file_path, random_Key+"_"+cleaned_file_name


    def clean_file_name(self, file_name: str) -> str:
        """
        Cleans a file name by removing special characters (except underscores and periods)
        and replacing spaces with underscores.

        Args:
         file_name (str): The original file name.

        Returns:
            str: The cleaned file name.
        """

        # Remove special characters except underscores and periods
        cleaned_name = re.sub(r"[^\w.]", "", file_name.strip())

        # Replace spaces with underscores
        cleaned_name = cleaned_name.replace(" ", "_")
        
        return cleaned_name

