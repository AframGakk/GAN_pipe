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

        for job in job_returns:
            # TODO: make better
            params = session.query(gan_parameters).filter(gan_parameters.id == id).scalar()

            jobList.append(JobDTO(job.id,
                                  job.label,
                                  job.version,
                                  job.date_time_start,
                                  job.date_time_stop,
                                  job.model_location,
                                  job.record_location,
                                  job.sound_type,
                                  {
                                      'batch_size': params.batch_size,
                                      'adam_learning_rate': params.adam_learning_rate,
                                      'adam_beta': params.adam_beta,
                                      'lrelu_alpha': params.lrelu_alpha,
                                      'episodes': params.episodes
                                  },
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
        params = session.query(gan_parameters).filter(gan_parameters.id == id).scalar()


        return JobDTO(job.id,
                        job.label,
                        job.version,
                        job.date_time_start,
                        job.date_time_stop,
                        job.model_location,
                        job.record_location,
                        job.sound_type,
                        {
                            'batch_size': params.batch_size,
                            'adam_learning_rate': params.adam_learning_rate,
                            'adam_beta': params.adam_beta,
                            'lrelu_alpha': params.lrelu_alpha,
                            'episodes': params.episodes
                        },
                        job.status,
                        job.results,
                        job.description)



    def insertJob(self, modelInput):
        '''
        Create a new job in database
        :param modelInput: JobInputModel, an input object for job.
        :return: int, the id of the newly created job.
        '''
        session = self.engine.session()
        param = gan_parameters(batch_size=modelInput.parameters.batch_size,
                               adam_learning_rate=modelInput.parameters.adam_learning_rate,
                               adam_beta=modelInput.parameters.adam_beta,
                               lrelu_alpha=modelInput.parameters.lrelu_alpha,
                               episodes=modelInput.parameters.episodes)

        session.add(param)
        session.commit()
        param.id

        now = datetime.now()

        job = gan_job(label=modelInput.label, version=modelInput.version, date_time_start=now, sound_type=modelInput.sound_type, parameters=param.id)
        session.add(job)
        session.commit()

        retJobDto = JobDTO(job.id,
                           job.label,
                           job.version,
                           datetime.timestamp(now),
                           job.date_time_stop,
                           job.model_location,
                           job.record_location,
                           job.sound_type,
                           {
                               'id': param.id,
                               'batch_size': param.batch_size,
                               'adam_learning_rate': float(param.adam_learning_rate),
                               'adam_beta': float(param.adam_beta),
                               'lrelu_alpha': float(param.lrelu_alpha),
                               'episodes': param.episodes
                           },
                           job.status,
                           job.results,
                           job.description)

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
        job.date_time_start = date_start
        job.date_time_stop = date_stop
        job.model_location = inputModel.model_location
        job.record_location = inputModel.record_location
        job.sound_type = inputModel.sound_type
        job.parameters = inputModel.parameters['id']
        job.status = inputModel.status
        job.results = inputModel.results
        job.description = inputModel.description

        session.add(job)
        session.commit()









