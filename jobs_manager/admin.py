from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from safedelete.admin import SafeDeleteAdmin

# Register your models here.
from jobs_manager.models import (
    JobManager
)
from jobs_manager.client import (
    JobClient
)

class JobManagerAdmin(SafeDeleteAdmin):
    search_fields = ('job_id', 'type', 'command', 'status', 'log', 'attempts', 'params', 'queue')
    ordering = SafeDeleteAdmin.list_display
    list_display = SafeDeleteAdmin.list_display + (
        'job_id', 'type', 'command', 'status', 'queue_host', 'log', 'attempts', 'params', 'queue', 'rerun'
    )

    def get_urls(self):
        urls = super(JobManagerAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<job_id>.+)/rerun/$',
                self.admin_site.admin_view(self.job_rerun),
                name='job-rerun',
            ),
        ]
        return custom_urls + urls

    def rerun(self, obj):
        if obj.status != "Success":
            return format_html(
                '<a class="button" href="{}">ReRun</a>&nbsp;',
                reverse('admin:job-rerun', args=[obj.pk]),
            )
        return "Successfully Run already"


    def job_rerun(self, request, job_id):
        job = JobManager.objects.get(id=job_id)
        cl = JobClient(settings.BEANSTALK_HOST, settings.BEANSTALK_PORT)
        cl.send_job(
            job.handler,
            job.params,
            queue=job.queue,
            mode=job.mode,
            type=job.type,
            attempts=job.attempts + 1
        )
        cl.close()
        self.message_user(request, 'Readded the job in queue with same params')
        url = reverse(
            'admin:jobs_manager_jobmanager_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

admin.site.register(JobManager, JobManagerAdmin)
