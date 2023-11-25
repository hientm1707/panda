import json
import logging
import openai
from typing import Annotated
from app.schemas.responses import GenerateCVResponse, JobDoc
from fastapi import APIRouter, HTTPException, UploadFile, File, Body
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from app.CV_Builder.CVBuilder import do_generate_cv_and_cl
logger = logging.getLogger(__name__)


router = APIRouter()

OUTPUT_FILE_PATH = '.'

@router.get("/", response_model=dict)
async def hello():
    return dict(msg='Hello')

@router.post("/generate-cv", response_model=GenerateCVResponse)
def generate_cv_and_cl(jds: Annotated[str, Body()], cv: UploadFile = File(...) ):
    if cv.content_type != 'application/pdf':
        raise RequestValidationError('Not a valid file type')
    try:
        jds = json.loads(jds)
    except json.JSONDecodeError:
        raise RequestValidationError('Not a valid jds input')
    response = []
    jobs = [[cv, jd] for jd in jds]
    for job in jobs:
        cv = job[0]
        jd = job[1]
        try:
            task_id = do_generate_cv_and_cl(cv.file, jd)
        except openai.error.RateLimitError as e:
            logger.error(f"Rate limit reached or out of quota: {str(e)}")
            raise HTTPException(status_code=429, detail=f"Rate limit reached or out of quota!")
        except Exception as e:
            logger.error(f"Something happened when trying to generate cvs and cls: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Something happened when trying to generate cvs and cls")
        if not task_id:
            logger.error(f"Could generate cv and cl.")
            raise HTTPException(status_code=500, detail="Could generate cv and cl.")
        response.append(JobDoc(
            task_id=task_id
        ))
    return GenerateCVResponse(docs=response)

@router.get("/get-new-cv")
async def get_new_cv(task_id: str):
    SAVE_FILE_PATH=f'{OUTPUT_FILE_PATH}/newCV-{task_id}.pdf'
    try:
        return FileResponse(
            path=SAVE_FILE_PATH,
            media_type="application/octet-stream",
            filename='CurriculumVitae.pdf'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-new-cl")
async def get_new_cl(task_id: str):
    SAVE_FILE_PATH=f'{OUTPUT_FILE_PATH}/CoverLetter-{task_id}.pdf'
    try:
        return FileResponse(
            path=SAVE_FILE_PATH,
            media_type="application/octet-stream",
            filename='CoverLetter.pdf'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
