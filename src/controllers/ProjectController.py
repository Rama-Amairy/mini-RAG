from controllers.BaseController import BaseController
import os
from models import ResponseEnum


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):

        project_dir= os.path.join(self.files_dir, project_id)
        folder_response= ""
        if not os.path.exists(project_dir): 
            os.makedirs(project_dir)
            folder_response=ResponseEnum.FOLDER_CREATED.value
            return project_dir, folder_response
            
        folder_response=ResponseEnum.FOLDER_EXIEST.value
        return project_dir, folder_response
