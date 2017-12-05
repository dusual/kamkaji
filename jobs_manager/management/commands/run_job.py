import imp
import os
import sys

from django.core.management.base import BaseCommand
from django.conf import settings
from jobs_manager.models import JobManager

from django_extensions.management.utils import signalcommand


def get_job(job_directory, job_name):
    return os.path.join(job_directory, job_name) + ".py"

def get_full_job_command(job_name):
    full_job_path = get_job(settings.JOBS_DIR, job_name)
    return full_job_path

# Hack for command line args in worker jobs
COMMAND_LINE_ARGS = sys.argv[4:]
sys.argv = sys.argv[:4]

class JobException(Exception):
    pass

class Command(BaseCommand):
    help = "Helper for running my_account jobs through the beanstalk worker"
    missing_args_message = "test"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('job_name', nargs='?')
        parser.add_argument(
            '--list', '-l', action="store_true", dest="list_jobs",
            help="List all jobs with their description")

    def save_job_run(self, job_id, job_status, log):
        jobs = JobManager.objects.filter(job_id=job_id)
        if jobs:
            job = jobs.latest("id")
            job.status = job_status
            job.log = log
            # Default save is override to stop admin usage
            job._save()
        else:
            raise Exception("Could not find job with job_id {}".format(job_id))

    def run_job(self, job_name, options):
        # add job id to the given job
        # change job status to executing
        job_status = "Error"
        log = ""
        job_params = COMMAND_LINE_ARGS[0]
        job_id = COMMAND_LINE_ARGS[1]

        try:
            job_path = get_full_job_command(job_name)
            module = imp.load_source('jobs', job_path)
        except IOError:
            error = "Could not find the job %s, Use -l option to view available jobs" %(job_name)
            print("ERROR OCCURED IN JOB: %s" % (job_name))
            print("START TRACEBACK:")
            print error
            print("END TRACEBACK\n")
            log = error
            self.save_job_run(job_id, job_status, log)
            return

        try:
            result = module.run(job_params, job_id)
            log = result
            job_status = "Success"
            print log
        except Exception:
            # add exception
            # change job status to error
            import traceback
            print("ERROR OCCURED IN JOB: %s" % (job_name))
            print("START TRACEBACK:")
            error = traceback.format_exc()
            print error
            print("END TRACEBACK\n")
            log = error

        self.save_job_run(job_id, job_status, log)
        return

    def run_from_argv(self, argv):
        argv = argv[:4]
        super(Command, self).run_from_argv(argv)

    def list_jobs(self):
        for each_file in os.listdir(settings.JOBS_DIR):
            if each_file.endswith(".py"):
                job_name = each_file[:-3]
                module = imp.load_source("jobs", get_job(settings.JOBS_DIR, job_name))
                try:
                    description = module.description()
                except AttributeError:
                    description = ""

                print job_name + ":"
                print "\t" + description +"\n"

    @signalcommand
    def handle(self, *args, **options):
        if options.get('list_jobs'):
            self.list_jobs()
            return

        # hack since we are using job_name nargs='?' for -l to work
        job_name = options.get('job_name')
        if not job_name:
            raise JobException("Could not find job with the given name")

        self.run_job(job_name, options)
