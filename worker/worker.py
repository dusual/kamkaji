import beanstalkc

import subprocess
import time
import sys
import json
import os
import pipes
import traceback


def main():
    host = sys.argv[1]
    port = sys.argv[2]
    log_file = sys.argv[3]
    job_log_dir = sys.argv[4]
    queue = sys.argv[5]


    fh = open(log_file, "w", 0)

    beanstalk = beanstalkc.Connection(host=host, port=int(port))

    while True:
        if beanstalk is not None:
            job = None

            try:
                job = beanstalk.reserve(timeout=3600)
            except Exception:
                fh.write("A job timed out\n")
                continue

            job_id = job.jid
            job_body = json.loads(job.body)

            job_command = job_body['job_cmd']
            job_mode = job_body['job_mode']
            job_queue = job_body['queue']
            job_params = job_body['params']

            if job_queue != queue:
                fh.write(str(job_id) + "\t" + job.body + " is not my job. Putting back in queue" + "\n")
                beanstalk.release(job_id)
                time.sleep(BACKOFF)
                continue

            args = job_command.split()
            if job_params is not None and len(job_params) > 0:
                args.extend([json.dumps(job_params)])

            args.append(str(job_id))

            job_log_file = open(job_log_dir + os.sep + str(job_id) + '.log', 'w')

            try:
                p = subprocess.Popen(args, stdout=job_log_file, stderr=subprocess.STDOUT, shell=False)
            except Exception, e:
                job.delete()
                print traceback.print_exc()
                continue

            rv = None

            # foreground process will call wait and block till it finishes
            if job_mode == 'foreground':
                rv = p.wait()
                job_log_file.close()
            else:
                # background process will set an alarm ro check status and make an entry in proc_table
                signal.alarm(WAIT_SECS)
                proc_table[p.pid] = [p, job_log_file]

            fh.write(str(job_id) + "\t" + job.body + "\t" + str(args) + "\t" + str(rv) + "\t" + str(time.asctime(time.localtime())) + "\n")
            job.delete()

    fh.close()
    beanstalk.close()


if __name__ == '__main__':
    if len(sys.argv) < 5:
        raise Exception("Usage: <host> <port> <log_file> <job_log_dir> <queue>")
    main()
