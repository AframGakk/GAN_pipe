from sqlalchemy import create_engine
import traceback
import configparser

from Repositories.SqlConnector.SqlEngine import SqlEngine
from Models.Entities.DataEntities import gan_parameters, sound_type, gan_job
from Models.DTO.JobDTO import JobDTO


config = configparser.ConfigParser()

class JobRepo:
    def __init__(self):
        self.engine = SqlEngine()

    def getAllJobs(self):
        '''
        Get all gan jobs in database.
        :return: list, a list of jobs
        '''
        session = self.engine.session()
        jobList = []
        job_returns = session.query(gan_job).all()

        for job in job_returns:
            jobList.append(JobDTO(job.id,
                                  job.version,
                                  job.date_time_start,
                                  job.date_time_stop,
                                  job.model_location,
                                  job.sound_type,
                                  job.parameters))

        return jobList



    def getJobById(self, id):
        '''
        Get a job by id from the database
        :param id: int, the id of the job
        :return: JobDTO, a data transfer object of Job
        '''
        session = self.engine.session()
        job = session.query(gan_job).filter(gan_job.id == id).scalar()
        return JobDTO(job.id,
                                  job.version,
                                  job.date_time_start,
                                  job.date_time_stop,
                                  job.model_location,
                                  job.sound_type,
                                  job.parameters)



    def insertJob(self, modelInput):
        '''
        Create a new job in database
        :param modelInput: JobInputModel, an input object for job.
        :return: int, the id of the newly created job.
        '''
        session = self.engine.session()
        param = gan_parameters(batch_size=64, noise_dim=100)
        session.add(param)
        session.commit()
        param.id

        #User.query.get(23)
        sound_id = session.query(sound_type.id).filter(sound_type.name == modelInput.sound_type).scalar()

        job = gan_job(sound_type=sound_id, parameters=param.id)
        session.add(job)
        session.commit()

        retJobDto = JobDTO(job.id,
                           job.version,
                           job.date_time_start,
                           job.date_time_stop,
                           job.model_location,
                           job.sound_type,
                           job.parameters)

        return retJobDto


    def deleteJobById(self, id):
        '''
        Delete a job by id.
        :param id: int, the id of the job to delete
        :return: None
        '''
        session = self.engine.session()
        jobToDelete = session.query(gan_job).filter(gan_job.id==id).one()
        session.delete(jobToDelete)
        session.commit()


    def putJob(self, inputModel):
        '''
        Update a job in database
        :param inputModel: JobInputModel, an input object for a Job
        :return: None
        '''
        session = self.engine.session()
        job = session.query(gan_job).filter(gan_job.id == inputModel.id).one()

        job.version = inputModel.version
        job.date_time_start = inputModel.date_time_start
        job.date_time_stop = inputModel.date_time_stop
        job.model_location = inputModel.model_location
        job.sound_type = inputModel.sound_type
        job.parameters = inputModel.parameters

        session.add(job)
        session.commit()









