import beanstalkc
import json

# Wrapper class to talk to Beanstalk
BEANSTALK_CONNECTION_TIMEOUT = 30


class JobServerConnector(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

        self._beanstalk = beanstalkc.Connection(host=self._host, port=self._port, connect_timeout=BEANSTALK_CONNECTION_TIMEOUT)

    def send_job(self, job_cmd, job_mode, queue, params=[]):
        if job_mode != 'background' and job_mode != 'foreground':
            raise Exception('Job not sent - mode should be foreground or background')

        job_cmd = job_cmd.rstrip()

        command_request = {'job_cmd': job_cmd, 'job_mode': job_mode, 'queue': queue, 'params': params}
        job_id = self._beanstalk.put(json.dumps(command_request))
        return job_id

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def close(self):
        self._beanstalk.close()
