import googleapiclient.discovery
import traceback

from Repositories.JobRepo.JobRepo import JobRepo

_jobRepo = JobRepo()
TRAINER = '153671080191723390'
ZONE = 'us-west1-b'
PROJECT_ID = 'samplergan'

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
            return None

        if self.active_jobs > 3:
            self.job_queue.append(jobDto)
            return None
        else:
            self.deployJob(jobDto)

        return jobDto


    def deployJob(self, jobDto):

        # TODO: if instance off then turn on
        if self._learnerInstance_status() == 'TERMINATED':
            self._turnOn_learner()

        self.job_pool.add(jobDto)
        self.active_jobs += 1


    def jobRetrieval(self, jobDto):
        self.job_pool.remove(jobDto)
        self.active_jobs -= 1
        self.updateJob(jobDto)

        if self.job_queue:
            self.deployJob(self.pop_queue())
            return jobDto
        else:
            if self.active_jobs <= 0:
                # TODO: shutdown learner
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












