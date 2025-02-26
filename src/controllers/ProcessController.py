from .BaseController import BaseController
from .ProjectController import ProjectController

import os

from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BaseController):
    
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)[0]
        
    #get the file extantion from the file id that we were gentated in the files project folder
    def get_file_extantion(self, file_id:str ):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self,file_id: str):
        file_extantion = self.get_file_extantion(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)
        if file_extantion==ProcessingEnum.TXT.value:
            return TextLoader(file_path=file_path , encoding="utf-8")
        if file_extantion== ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        return None
    
    def get_file_content(self, file_id:str)->list:
        loader= self.get_file_loader(file_id=file_id)
        return loader.load()
    
    def process_file_content(self, file_content : list ,file_id : str, chunk_size:int, overlap_size:int):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap=overlap_size,
            length_function= len,
            
        )
        file_content_text=[
            rec.page_content
            for rec in file_content
        ]
        file_content_metadata=[
            rec.metadata
            for rec in file_content
        ]
        chunks= text_splitter.create_documents(texts=file_content_text , metadatas=file_content_metadata)
        
        return chunks
        
     
        