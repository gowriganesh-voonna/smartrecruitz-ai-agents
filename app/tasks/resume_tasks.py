from app.tasks.celery_app import celery


@celery.task
def process_resume_task(job_id: str, file_path: str):

    print(f"Processing resume {job_id}")
