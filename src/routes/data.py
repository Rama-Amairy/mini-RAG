from fastapi import  APIRouter, Depends, UploadFile,File, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
import os
import aiofiles
import logging
from .schemes.data import ProcessRequest

from models import ResponseEnum
#from controllers import DataController,ProjectController
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from controllers.ProcessController import ProcessController

logger= logging.getLogger("uvicorn.error")

data_router= APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1_data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),  # Properly declare file as an instance of UploadFile
    app_settings: Settings = Depends(get_settings)
    ):
    data_object=DataController()

    #validate the file properties
    is_valid, ResponseSignal = data_object.validate_uploaded_file(file=file)

    #if the file validation failed return bad request
    if not is_valid:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
        "validation": is_valid,
        "Response Signal": ResponseSignal
        })
    
    project_file_path, FileResponseSignal=ProjectController().get_project_path(project_id=project_id)
    
    file_path, file_id= data_object.generate_unique_filepath(file_name=file.filename,project_id=project_id)

    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
        "Response Signal": ResponseEnum.FILE_UPLOADED_FAILED.value
        })


    #if the file validation succeed save the file in assets/files directory 
    return JSONResponse(content={
        "File validation": is_valid,
        "Response Signal": ResponseSignal,
       "Project Directory": project_file_path,
       "Project Response Signal": FileResponseSignal,
       "File path": file_path,
       "File id" : file_id})

    
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id : str , processRequest : ProcessRequest):    
    file_id = processRequest.file_id
    chunk_size= processRequest.chunk_size
    overlap_size =processRequest.overlap_size
    process_controller= ProcessController(project_id=project_id)
    file_content= process_controller.get_file_content(file_id=file_id)
    chunks= process_controller.process_file_content(file_content,file_id=file_id,chunk_size=chunk_size,overlap_size=overlap_size )
    if chunks is None or len(chunks)==0 :
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
        "Response Signal": ResponseEnum.FILE_PROCESSING_FAILED.value
        })
    return chunks
        

    
    