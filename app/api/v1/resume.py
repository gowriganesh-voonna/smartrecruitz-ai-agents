from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4

from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload resume and start processing.
    """

    job_id = str(uuid4())

    try:
        await ResumeService.upload_resume(job_id, file)

        return {
            "job_id": job_id,
            "message": "Resume uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}")
async def get_processing_status(job_id: str):
    """
    Check resume processing status.
    """

    status = await ResumeService.get_processing_status(job_id)

    return {
        "job_id": job_id,
        "status": status
    }
