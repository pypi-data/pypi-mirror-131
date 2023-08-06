from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from aisy_database.db_tables import *


class DBUpdate:

    def __init__(self, database_path, analysis_id):
        self.db_update = None
        self.analysis_id = analysis_id
        self.engine = create_engine('sqlite:///{}'.format(database_path), echo=False)
        self.metadata = MetaData(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def db_update_elapsed_time(self, elapsed_time):
        """
        :param elapsed_time: elapsed time for the analysis (obtained with time.time())
        :return: None
        """
        self.session.query(Analysis).filter(Analysis.id == self.analysis_id).update({"elapsed_time": elapsed_time})
        self.session.commit()

    def db_update_settings(self, settings):
        self.session.query(Analysis).filter(Analysis.id == self.analysis_id).update({"settings": settings})
        self.session.commit()

    def db_update_key_rank_label(self, old_label, new_label):
        self.session.query(GuessingEntropy).filter(and_(
            GuessingEntropy.analysis_id == self.analysis_id,
            GuessingEntropy.label == old_label)).update({"label": new_label})
        self.session.commit()

    def db_update_success_rate_label(self, old_label, new_label):
        self.session.query(SuccessRate).filter(and_(
            SuccessRate.analysis_id == self.analysis_id,
            SuccessRate.label == old_label)).update({"label": new_label})
        self.session.commit()

    def db_update_metric_label(self, old_label, new_label):
        self.session.query(Metric).filter(and_(
            Metric.analysis_id == self.analysis_id,
            Metric.label == old_label)).update({"label": new_label})
        self.session.commit()

    def db_update_random_state_label(self, old_label, new_label):
        self.session.query(RandomStatesHyperParameter).filter(and_(
            RandomStatesHyperParameter.analysis_id == self.analysis_id,
            RandomStatesHyperParameter.label == old_label)).update({"label": new_label})
        self.session.commit()

    def db_update_hyperparameters(self, new_hp, hp_id, column_name):
        self.session.query(HyperParameter).filter(
            and_(HyperParameter.id == hp_id, HyperParameter.analysis_id == self.analysis_id)).update({column_name: new_hp})
        self.session.commit()

    def get_db_update(self):
        """
        :return: db_update object
        """
        return self.db_update

    def get_db_session(self):
        """
        :return: db session object
        """
        return self.session
