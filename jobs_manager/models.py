from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from safedelete import safedelete_mixin_factory

from utility_manager.jsonfield import JSONField
# Create your models here.


JOB_TYPE_OPTIONS = (("API", "API"), ("Other", "Other"))
MODE_TYPE_OPTIONS = (("foreground", "foreground"), ("background", "background"))

policy = settings.SAFE_DELETE_POLICY_SET[settings.SAFE_DELETE_POLICY]
safe_delete_mixin = safedelete_mixin_factory(policy=policy)


class JobManagerException(Exception):
    pass


class JobManager(safe_delete_mixin):
    job_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(choices=JOB_TYPE_OPTIONS, max_length=40, null=True)
    handler = models.CharField(null=True, blank=True, max_length=120)
    command = models.TextField(null=False, blank=False)
    mode = models.CharField(choices=MODE_TYPE_OPTIONS, max_length=30, null=True)
    status = models.CharField(max_length=40, null=False, blank=True)
    log = models.TextField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    params = JSONField(default={}, blank=True)
    queue = models.CharField(max_length=40, default="web", null=False, blank=False)
    queue_host = models.CharField(max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        raise JobManagerException("JobManager cannot be saved. Please used send_job to add jobs to the queue")

    def _save(self, *args, **kwargs):
        super(JobManager, self).save(*args, **kwargs)

