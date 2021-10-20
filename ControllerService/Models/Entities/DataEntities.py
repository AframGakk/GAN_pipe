from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Numeric

Base = declarative_base()

class gan_parameters(Base):
   __tablename__ = 'gan_parameters'

   id = Column(Integer, primary_key=True)
   batch_size = Column(Integer, nullable=False)
   adam_learning_rate = Column(Numeric, nullable=False)
   adam_beta = Column(Numeric, nullable=False)
   lrelu_alpha = Column(Numeric, nullable=False)
   episodes = Column(Integer, nullable=False)


class sound_type(Base):
    __tablename__ = 'sound_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class job_status(Base):
    __tablename__ = 'job_status'

    id = Column(Integer, primary_key=True)
    status = Column(String(32), nullable=False)

class job_results(Base):
    __tablename__ = 'job_results'
    id = Column(Integer, primary_key=True)
    generator_accuracy = Column(Numeric)
    discriminator_accuracy = Column(Numeric)
    generator_loss = Column(Numeric)
    discriminator_loss = Column(Numeric)


class gan_job(Base):
    __tablename__ = 'gan_jobs'

    id = Column(Integer, primary_key=True)
    label = Column(String(128), nullable=False)
    version = Column(Integer)
    date_time_start = Column(TIMESTAMP)
    date_time_stop = Column(TIMESTAMP)
    model_location = Column(String(256))
    record_location = Column(String(128))
    sound_type = Column(Integer, ForeignKey('sound_type.id'))
    parameters = Column(Integer, ForeignKey('gan_parameters.id'))
    status = Column(Integer, ForeignKey('job_status.id'), default=4)
    results = Column(Integer, ForeignKey('job_results.id'))
    description = Column(String(512))

