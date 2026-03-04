import os
from fastapi import UploadFile

from app.tasks.resume_tasks import process_resume_task


class ResumeService:

    @staticmethod
    async def upload_resume(job_id: str, file: UploadFile):

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = f"{upload_dir}/{job_id}_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # trigger background processing
        process_resume_task.delay(job_id, file_path)

        return job_id

    @staticmethod
    async def get_processing_status(job_id: str):

        # later we will query database
        return "PROCESSING"
