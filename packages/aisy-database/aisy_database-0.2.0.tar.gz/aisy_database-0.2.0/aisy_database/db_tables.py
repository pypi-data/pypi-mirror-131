import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship

Base = declarative_base()


def base():
    return Base


class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    db_filename = Column(String)
    dataset = Column(String)
    settings = Column(JSON)
    elapsed_time = Column(Float)
    deleted = Column(Boolean)

    def __repr__(self):
        return "<Analysis(datetime=%s, script='%s')>" % (self.datetime, self.db_filename)


class HyperParameter(Base):
    __tablename__ = 'hyperparameter'
    id = Column(Integer, primary_key=True)
    hyperparameters = Column(JSON)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<HyperParemeters(id=%d)>" % self.id


class NeuralNetwork(Base):
    __tablename__ = 'neural_network'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    description = Column(String)
    hyperparameters_id = Column(Integer, ForeignKey('hyperparameter.id'))
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<NeuralNetwork(name=%s, description='%s')>" % (self.model_name, self.description)


class LeakageModel(Base):
    __tablename__ = 'leakage_model'
    id = Column(Integer, primary_key=True)
    leakage_model = Column(JSON)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<LeakageModel(id=%d)>" % self.id


class Metric(Base):
    __tablename__ = 'metric'
    id = Column(Integer, primary_key=True)
    values = Column(JSON)
    label = Column(String)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<Metric(id=%d)>" % self.id


class GuessingEntropy(Base):
    __tablename__ = 'guessing_entropy'
    id = Column(Integer, primary_key=True)
    values = Column(JSON)
    report_interval = Column(Integer)
    label = Column(String)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<GuessingEntropy(id=%d)>" % self.id


class SuccessRate(Base):
    __tablename__ = 'success_rate'
    id = Column(Integer, primary_key=True)
    values = Column(JSON)
    report_interval = Column(Integer)
    label = Column(String)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<SuccessRate(id=%d)>" % self.id


class Visualization(Base):
    __tablename__ = 'visualization'
    id = Column(Integer, primary_key=True)
    values = Column(JSON)
    epoch = Column(Integer)
    label = Column(String)
    hyperparameters_id = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<Visualization(id=%d)>" % self.id


class ConfusionMatrix(Base):
    __tablename__ = 'confusion_matrix'
    id = Column(Integer, primary_key=True)
    y_pred = Column(JSON)
    y_true = Column(Integer)
    hyperparameters_id = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<ConfusionMatrix(id=%d)>" % self.id


class ProbabilityRank(Base):
    __tablename__ = 'probability_rank'
    id = Column(Integer, primary_key=True)
    ranks = Column(JSON)
    classes = Column(Integer)
    correct_key_byte = Column(Integer)
    key_guess = Column(Integer)
    label = Column(String)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<ProbabilityRank(id=%d)>" % self.id


class HyperParameterMetric(Base):
    __tablename__ = 'hyperparameter_metric'
    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer)
    hyperparameters_id = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<HyperParameterMetric(id=%d)>" % self.id


class HyperParameterGuessingEntropy(Base):
    __tablename__ = 'hyperparameter_guessing_entropy'
    id = Column(Integer, primary_key=True)
    guessing_entropy_id = Column(Integer)
    hyperparameters_id = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<HyperParameterGuessingEntropy(id=%d)>" % self.id


class HyperParameterSuccessRate(Base):
    __tablename__ = 'hyperparameter_success_rate'
    id = Column(Integer, primary_key=True)
    success_rate_id = Column(Integer)
    hyperparameters_id = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<HyperParameterSuccessRate(id=%d)>" % self.id


class RandomStatesHyperParameter(Base):
    __tablename__ = 'random_states_hyperparameter'
    id = Column(Integer, primary_key=True)
    random_states = Column(JSON)
    label = Column(String)
    index = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    analysis = relationship("Analysis", cascade="all, delete")

    def __repr__(self):
        return "<RandomStatesHyperParameter(id=%d)>" % self.id


