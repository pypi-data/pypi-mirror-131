import pandas as pd
from sqlalchemy.orm import sessionmaker
import aisy_database.db_tables as tables
from aisy_database.db_tables import *


class DBSave:

    def __init__(self, database_path):
        self.db_save = None
        self.analysis_id = None
        self.engine = create_engine('sqlite:///{}'.format(database_path), echo=False)
        self.metadata = MetaData(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        tables.base().metadata.create_all(self.engine)

    def insert(self, row):
        """
        :param row: object to be inserted in the database table
        :return: id of the last inserted row
        """
        self.session.add(row)
        self.session.commit()
        return row.id

    def db_save_analysis(self, db_filename, dataset, settings, elapsed_time=0):
        """
        :param db_filename: string with database name
        :param dataset: string with dataset file name
        :param settings: dictionary containing analysis settings
        :param elapsed_time: elapsed time for analysis
        :return: id
        """
        new_insert = Analysis(db_filename=db_filename, dataset=dataset, settings=settings, elapsed_time=elapsed_time, deleted=False)
        self.analysis_id = self.insert(new_insert)
        return self.analysis_id

    def db_save_metric(self, metric, metric_label):
        """
        :param metric: list of metric values
        :param metric_label: string containing metric label
        :return: id
        """
        new_insert = Metric(values=pd.Series(metric).to_json(), label=metric_label, analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_key_rank(self, key_rank, key_rank_label, report_interval):
        """
        :param key_rank: list of key rank values
        :param key_rank_label: string containing the label for key rank
        :param report_interval: key rank report interval
        :return: id
        """
        new_insert = GuessingEntropy(values=pd.Series(key_rank).to_json(), report_interval=report_interval, label=key_rank_label,
                                     analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_success_rate(self, success_rate, success_rate_label, report_interval):
        """
        :param success_rate: list of success rate values
        :param success_rate_label: string containing the label for success rate
        :param report_interval: key rank report interval
        :return: id
        """
        new_insert = SuccessRate(values=pd.Series(success_rate).to_json(), report_interval=report_interval, label=success_rate_label,
                                 analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_probability_ranks(self, ranks, label, classes, correct_key_byte):
        """
        :param correct_key_byte: integer with good key byte value
        :param classes: number of classes in the classification problem (number of possible labels)
        :param ranks: 2D array: [[ranks_key_guess_0], [ranks_key_guess_1], ..., [ranks_key_guess_255]]
        :param label: label for the probability ranks
        :return: id's of all inserted rows
        """
        row_ids = []
        number_of_key_guesses = len(ranks)
        for key_guess in range(number_of_key_guesses):
            new_insert = ProbabilityRank(ranks=pd.Series(ranks[key_guess]).to_json(), classes=classes, correct_key_byte=correct_key_byte,
                                         key_guess=key_guess, label=label, analysis_id=self.analysis_id)
            row_ids.append(self.insert(new_insert))
        return row_ids

    def db_save_visualization(self, input_gradients_epochs, input_gradients_sum, label, hyperparameters_id):
        """
        :param input_gradients_epochs: 2D array: [[input_gradients_epoch1], [input_gradients_epoch2], ..., [input_gradients_epochN]]
        :param input_gradients_sum: list containing sum of input gradients from all epochs
        :param label: label for visualization entry
        :return: id
        """
        epochs = len(input_gradients_epochs)
        for epoch in range(epochs):
            new_insert = Visualization(values=pd.Series(input_gradients_epochs[epoch]).to_json(), epoch=epoch, label=label,
                                       hyperparameters_id=hyperparameters_id, analysis_id=self.analysis_id)
            self.insert(new_insert)
        new_insert = Visualization(values=pd.Series(input_gradients_sum / epochs).to_json(), epoch=epochs, label=label,
                                   hyperparameters_id=hyperparameters_id, analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_confusion_matrix(self, confusion_matrix, hyperparameters_id):
        """
        :param confusion_matrix: 2D array containing confusion matrix
        :return: id's of inserted rows
        """
        row_ids = []
        for y_true, y_pred in enumerate(confusion_matrix):
            new_insert = ConfusionMatrix(y_pred=pd.Series(y_pred).to_json(), y_true=y_true, hyperparameters_id=hyperparameters_id,
                                         analysis_id=self.analysis_id)
            row_ids.append(self.insert(new_insert))
        return row_ids

    def db_save_hyper_parameters(self, hyperparameters):
        """
        :param hyperparameters: dictionary of hyper-parameters
        :return: id
        """
        new_insert = HyperParameter(hyperparameters=hyperparameters, analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_neural_network(self, model_description, model_name, hyperparameters_id):
        """
        :param model_description: string containing keras model description
        :param model_name: string containing the name of the model
        :return: id
        """
        new_insert = NeuralNetwork(model_name=model_name, description=model_description, hyperparameters_id=hyperparameters_id,
                                   analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_leakage_model(self, leakage_model):
        """
        :param leakage_model: dictionary containing leakage model parameters
        :return: id
        """
        new_insert = LeakageModel(leakage_model=leakage_model, analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def db_save_metric_hyperparameter(self, metric_id, hyperparameters_id):
        """
        :param metric_id: metric_id
        :param hyperparameters_id: hyperparameters_id
        """
        new_insert = HyperParameterMetric(metric_id=metric_id, hyperparameters_id=hyperparameters_id, analysis_id=self.analysis_id)
        self.session.add(new_insert)
        self.session.commit()

    def db_save_guessing_entropy_hyperparameter(self, guessing_entropy_id, hyperparameters_id):
        """
        :param guessing_entropy_id: guessing_entropy_id
        :param hyperparameters_id: hyperparameters_id
        """
        new_insert = HyperParameterGuessingEntropy(guessing_entropy_id=guessing_entropy_id, hyperparameters_id=hyperparameters_id,
                                                   analysis_id=self.analysis_id)
        self.session.add(new_insert)
        self.session.commit()

    def db_save_success_rate_hyperparameter(self, success_rate_id, hyperparameters_id):
        """
        :param success_rate_id: success_rate_id
        :param hyperparameters_id: hyperparameters_id
        """
        new_insert = HyperParameterSuccessRate(success_rate_id=success_rate_id, hyperparameters_id=hyperparameters_id,
                                               analysis_id=self.analysis_id)
        self.session.add(new_insert)
        self.session.commit()

    def db_save_random_state_hyperparameter(self, label, index, r):
        """
        :param label: label
        :param index: index
        :param r: random states
        :return: id
        """
        new_insert = RandomStatesHyperParameter(random_states=pd.Series(r).to_json(), label=label, index=index,
                                                analysis_id=self.analysis_id)
        return self.insert(new_insert)

    def get_db_save(self):
        """
        :return: db_save object
        """
        return self.db_save

    def get_db_session(self):
        """
        :return: db session object
        """
        return self.session
