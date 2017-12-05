### Yet another task queue? Why?

We at e2enetworks manage multiple services and manage infrastructures across multiple providers including our inhouse one. Although our app is written in python/django, we needed a task queue that could handle the heterogeneity of our system. Hence, we went with the system where the business intelligenece is mostly handled in the client. Beanstalkd seemed like nice work queue and our solution is written on top of that.


### Installation

```
pip install -e git+https://github.com/E2ENetworksPrivateLimited/kamkaji.git#egg=kamkaji
```

#### Required Settings

- Beanstalk related:

```
BEANSTALK_HOST = "localhost"
BEANSTALK_PORT = 11300
```

- Job Command:

The backend command that will run on worker. This is essentially a django management command called run_job. You can configure this for your application.

```
JOB_BACKEND_COMMAND_FORMAT = "python manage.py run_job {job_name} --settings=<local settings>"
```

- Jobs Directory

Directory to look up jobs

```
JOBS_DIR = os.path.join(BASE_DIR_KEY, "jobs")
```


### Usage

#### Running the worker

```
python worker/worker.py <host> <port> <log_file> <job_log_dir> <queue>
```
Example:

```
python worker/worker.py  localhost 11300 /var/log/worker/worker_web.log /var/log/worker/ web
```

#### Adding jobs to the client

Add jobs in jobs directory in the root of the folder of your django project


### Contributors

- [Ashish Mukherjee](https://github.com/ashish-m-yh)
- [Amit Sethi](https://github.com/dusual)


### TODO and future:

- Better handling for retry
- Better handling for delayed jobs
- Suggestions??

