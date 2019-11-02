import googleapiclient.discovery
import traceback
from datetime import datetime
import os

from Repositories.JobRepo.JobRepo import JobRepo

_jobRepo = JobRepo()
TRAINER = os.environ['TRAINER']
ZONE = os.environ['ZONE']
PROJECT_ID = os.environ['PROJECT_ID']

class JobService:
    def __init__(self):
        self.job_queue = []
        self.job_pool = set()
        self.active_jobs = 0

    def pop_queue(self):
        if not self.job_queue:
            return None

        next_job = self.job_queue[0]
        self.job_queue = self.job_queue[1:]
        return next_job

    def createJob(self, jobInput):
        try:
            jobDto = _jobRepo.insertJob(jobInput)
        except Exception:
            print('Could not create a new job')
            traceback.print_exc()
            return None

        return jobDto


    def deployJob(self, jobDto):

        jobDto.status = 1
        self.updateJob(jobDto)

        if self._learnerInstance_status() == 'TERMINATED':
            self._turnOn_learner()

        if self.active_jobs > 3:
            self.job_queue.append(jobDto)
            return None
        else:
            #self.deployJob(jobDto)
            self.job_pool.add(jobDto)
            self.active_jobs += 1
            return jobDto


    def jobRetrieval(self, jobDto):
        if jobDto in self.job_pool:
            self.job_pool.remove(jobDto)
        self.active_jobs -= 1
        jobDto.date_time_stop = datetime.timestamp(datetime.now())
        jobDto.status = 2
        self.updateJob(jobDto)

        if self.job_queue:
            self.deployJob(self.pop_queue())
            return jobDto
        else:
            if self.active_jobs <= 0:
                self._turnOff_learner()
            return None


    def updateJob(self, jobDto):
        _jobRepo.putJob(jobDto)


    def _turnOn_learner(self):
        try:
            compute = googleapiclient.discovery.build('compute', 'v1')
            result = compute.instances().start(project=PROJECT_ID, zone=ZONE, instance=TRAINER).execute()
        except Exception:
            #logger.error(__name__, 'Instance {} was not found in the list of available resources at GCP'.format(instance))
            print('Instance {} was not found in the list of available resources at GCP'.format(TRAINER))
            return False
        return True

    def _turnOff_learner(self):
        try:
            compute = googleapiclient.discovery.build('compute', 'v1')
            result = compute.instances().stop(project=PROJECT_ID, zone=ZONE, instance=TRAINER).execute()
        except Exception:
            #logger.error(__name__, 'Instance {} was not found in the list of available resources at GCP'.format(instance))
            print('Instance {} was not found in the list of available resources at GCP'.format(TRAINER))
            return False
        return True

    def _learnerInstance_status(self):
        compute = googleapiclient.discovery.build('compute', 'v1')
        instStatus = compute.instances().get(
            project=PROJECT_ID,
            zone=ZONE,
            instance=TRAINER).execute()

        return instStatus['status']












