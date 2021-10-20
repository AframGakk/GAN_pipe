from sqlalchemy import create_engine
import traceback
import configparser
from datetime import datetime

from Repositories.SqlConnector.SqlEngine import SqlEngine
from Models.Entities.DataEntities import gan_parameters, sound_type, gan_job, job_results
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

        session = self.engine.session()

        for job in job_returns:
            if job.parameters:
                para = session.query(gan_parameters).filter(gan_parameters.id == job.parameters).scalar()
                job.parameters = {
                    'id': para.id,
                    'batch_size': para.batch_size,
                    'adam_learning_rate': float(para.adam_learning_rate),
                    'adam_beta': float(para.adam_beta),
                    'lrelu_alpha': float(para.lrelu_alpha),
                    'episodes': para.episodes
                }

            if job.results:
                res = session.query(job_results).filter(job_results.id == job.results).scalar()
                job.results = {
                    'id': res.id,
                    'discriminator_loss': float(res.discriminator_loss),
                    'generator_loss': float(res.generator_loss),
                    'discriminator_accuracy': float(res.discriminator_accuracy),
                    'generator_accuracy': float(res.generator_accuracy)
                }

            jobList.append(JobDTO(job.id,
                                  job.label,
                                  job.version,
                                  job.date_time_start,
                                  job.date_time_stop,
                                  job.model_location,
                                  job.record_location,
                                  job.sound_type,
                                  job.parameters,
                                  job.status,
                                  job.results,
                                  job.description
                                  ))

        return jobList


    def getJobById(self, id):
        '''
        Get a job by id from the database
        :param id: int, the id of the job
        :return: JobDTO, a data transfer object of Job
        '''
        session = self.engine.session()

        job = session.query(gan_job).filter(gan_job.id == id).scalar()
        if job.parameters:
            para = session.query(gan_parameters).filter(gan_parameters.id == job.parameters).scalar()
            job.parameters = {
                'id': para.id,
                'batch_size': para.batch_size,
                'adam_learning_rate': float(para.adam_learning_rate),
                'adam_beta': float(para.adam_beta),
                'lrelu_alpha': float(para.lrelu_alpha),
                'episodes': para.episodes
            }

        session = self.engine.session()

        if job.results:
            res = session.query(job_results).filter(job_results.id == job.results).scalar()
            job.results = {
                'id': res.id,
                'discriminator_loss': float(res.discriminator_loss),
                'generator_loss': float(res.generator_loss),
                'discriminator_accuracy': float(res.discriminator_accuracy),
                'generator_accuracy': float(res.generator_accuracy)
            }

        return JobDTO(job.id,
                        job.label,
                        job.version,
                        job.date_time_start,
                        job.date_time_stop,
                        job.model_location,
                        job.record_location,
                        job.sound_type,
                        job.parameters,
                        job.status,
                        job.results,
                        job.description)


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

        if inputModel.results:
            res = job_results(discriminator_loss=inputModel.results['discriminator_loss'],
                              generator_loss=inputModel.results['generator_loss'],
                              discriminator_accuracy=inputModel.results['discriminator_accuracy'],
                              generator_accuracy=inputModel.results['generator_accuracy'])

            session.add(res)
            session.commit()
            inputModel.results = res.id

        date_start = None
        date_stop = None

        if inputModel.date_time_start:
            date_start = datetime.fromtimestamp(inputModel.date_time_start)

        if inputModel.date_time_stop:
            date_stop = datetime.fromtimestamp(inputModel.date_time_stop)

        job.label = inputModel.label
        job.version = inputModel.version
        job.date_time_start = date_start  # inputModel.date_time_start
        job.date_time_stop = date_stop  # inputModel.date_time_stop
        job.model_location = inputModel.model_location
        job.record_location = inputModel.record_location
        job.sound_type = inputModel.sound_type
        job.parameters = inputModel.parameters['id']
        job.status = inputModel.status
        job.results = inputModel.results
        job.description = inputModel.description

        session.add(job)
        session.commit()









