'''Collection of functions for interacting with JUNIQ-Service node.'''

import os
from time import sleep

from juqcs.authentication import _JUNIQ


# JUNIQ-service tools
PY_ALLOCATE   = 'juqcs-allocate'
PY_RUN        = 'juqcs-run' 
PY_DEALLOCATE = 'juqcs-deallocate'



def submit(job_description, inputs=[], blocking=True):
    """
    Submit {job_description} to {_JUNIQ}.
    Arguments:
        job_description (dict): UNICORE job description
        inputs (list): optional, files to upload together with job submission
        blocking (bool): if True, block execution until UNICORE confirms job is done
                         (safe but ~1-2 min latency)
                         if False, poll manually until 'UNICORE_SCRIPT_EXIT_CODE' 
                         appears in work directory
    Returns:
        job (pyunicore.client.Job): UNICORE job
    """
    job = _JUNIQ.new_job(job_description, inputs=inputs)
    if blocking:
        job.poll()
    else:  # TODO: find a faster way to poll if job is finished
        finished = False
        while not finished:
            sleep(2) # if max. nr. of connections exceeded this value should be incremented
            if 'UNICORE_SCRIPT_EXIT_CODE' in job.working_dir.listdir():
                finished = True

    return job

def retrieve(job, filename):
    """
    Retrieve {filename} from {job}'s working directory.
    Returns:
        contents (str)
    Raises:
        requests.exceptions.HTTPError: if {filename} not found
    """
    wd = job.working_dir
    contents = wd.stat(filename)\
                 .raw()\
                 .read()\
                 .decode('utf-8')
    return contents

def save_log(job):
    '''Save job log for error tracking.'''

    def write_file(filename, string):
        """Load a file and write string into it."""
        with open(filename, 'w') as f:
            f.write(string)
    filename = 'job.log' #f'{job.job_id}.log')
    log = '\n'.join(job.properties['log'])
    write_file(filename, log)
