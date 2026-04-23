from ingestion.deduplication import ingest_file

task_status={}


def ingest_file_with_status(db,file_path,job_id):
    try:
        task_status[job_id]="processing"
        ingest_file(db,file_path)

        task_status[job_id]="success"
    except Exception as e:
        print("Error in ingest_file_with_status", str(e))
        task_status[job_id]=f"failed: {str(e)}"

