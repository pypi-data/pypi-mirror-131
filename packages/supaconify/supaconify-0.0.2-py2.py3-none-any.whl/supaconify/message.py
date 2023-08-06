import os
from string import Template


def builder(template: Template):
    info = {"user": "", "job_id": "", "job_name": ""}
    try:
        # PBS
        info["user"] = os.environ["PBS_O_LOGNAME"]
        info["job_id"] = os.environ["PBS_JOBID"]
        info["job_name"] = os.environ["PBS_JOBNAME"]
    except Exception:
        print("Some variables could not be detected.")

    if template is None:
        template = Template("$user's $job_name(job id is $job_id) has finished.")

    return template.safe_substitute(info)
