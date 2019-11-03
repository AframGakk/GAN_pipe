from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP

Base = declarative_base()

class gan_parameters(Base):
   __tablename__ = 'gan_parameters'

   id = Column(Integer, primary_key=True)
   batch_size = Column(Integer, nullable=False)
   noise_dim = Column(Integer, nullable=False)


class sound_type(Base):
    __tablename__ = 'sound_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

class job_status(Base):
    __tablename__ = 'job_status'

    id = Column(Integer, primary_key=True)
    status = Column(String(32), nullable=False)


class gan_job(Base):
    __tablename__ = 'gan_jobs'

    id = Column(Integer, primary_key=True)
    version = Column(Integer)
    date_time_start = Column(TIMESTAMP)
    date_time_stop = Column(TIMESTAMP)
    model_location = Column(String(256))
    sound_type = Column(Integer, ForeignKey('sound_type.id'))
    parameters = Column(Integer, ForeignKey('gan_parameters.id'))
    status = Column(Integer, ForeignKey('job_status'), default=4)

