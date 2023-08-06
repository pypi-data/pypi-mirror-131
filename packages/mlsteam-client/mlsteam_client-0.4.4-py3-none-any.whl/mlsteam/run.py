

class Run(object):
    def __init__(self, run_id, backend, batch_processor, background_jobs, run_lock, project_uuid):
        self._run_id = run_id
        self._backend = backend
        self._processor = batch_processor
        self._background_jobs = background_jobs
        self._run_lock = run_lock
        self._project_uuid = project_uuid

    