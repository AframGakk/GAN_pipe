
from Repositories.JobRepo.JobRepo import JobRepo

_jobRepo = JobRepo()

def getAllJobs():
    return [ item.__dict__() for item in  _jobRepo.getAllJobs()]

def getJobById(id):
    return _jobRepo.getJobById(id).__dict__()
