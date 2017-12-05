import logging
import traceback
from django.conf import settings

from jobs_manager.models import JobManager
from jobs_manager.job_server_connector import JobServerConnector
from jobs_manager.management.commands.run_job import get_full_job_command


MODE_TYPE_OPTIONS = ["background", "foreground"]
logger = logging.getLogger(__name__)

class JobClientException(Exception):
    pass


class JobClient(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        try:
            self._job_client = JobServerConnector(host, port)
        except Exception, e:
            error = traceback.format_exc()
            logger.error(error)
            self._job_client = None

    def command(self, job_name):
        return settings.JOB_BACKEND_COMMAND_FORMAT.format(job_name=job_name, environment=settings.ENVIRONMENT.lower())

    def send_job(self, job_name, params, queue, mode="foreground", type="Other", attempts=1):
        logger.debug("Attempting to add job {} with params {} to queue {}".format(job_name, params, queue))
        command = self.command(job_name)
        if mode not in MODE_TYPE_OPTIONS:
            raise JobClientException("Mode can only be background or foreground")

        job = JobManager(
            type=type,
            handler=job_name,
            command=command,
            mode=mode,
            status="Queued",
            queue=queue,
            params=params,
            attempts=attempts,
            queue_host =self._host
        )
        if not self._job_client:
            job.log = "There was an issue connecting with beanstalk service"
            job._save()
            return

        try:
            job_id = self._job_client.send_job(job.command, mode, job.queue, job.params)
        except Exception, e:
            error = traceback.format_exc()
            job.log = error
            job._save()
            return

        job.job_id = job_id
        job._save()

    def close(self):
        self._job_client.close()

