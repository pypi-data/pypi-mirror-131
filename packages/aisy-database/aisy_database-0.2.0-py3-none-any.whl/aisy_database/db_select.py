from sqlalchemy.orm import sessionmaker
from aisy_database.db_tables import *
import json


class DBSelect:

    def __init__(self, database_path):
        self.db_select = None
        self.engine = create_engine('sqlite:///{}'.format(database_path), echo=False)
        self.metadata = MetaData(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def select_all(self, table_class):
        return self.session.query(table_class).all()

    def select_analysis(self, table_class, analysis_id):
        return self.session.query(table_class).filter_by(id=analysis_id).first()

    def select_from_analysis(self, table_class, analysis_id):
        return self.session.query(table_class).filter_by(analysis_id=analysis_id).first()

    def select_all_from_analysis(self, table_class, analysis_id):
        return self.session.query(table_class).filter_by(analysis_id=analysis_id).all()

    def select_accuracy_from_analysis(self, analysis_id):
        rows = self.session.query(Metric).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "accuracy" in row.label and "Best" not in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id
                })
        return rows_dict

    def select_best_accuracy_from_analysis(self, analysis_id):
        rows = self.session.query(Metric).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "accuracy" in row.label and "Best" in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id
                })
        return rows_dict

    def select_loss_from_analysis(self, analysis_id):
        rows = self.session.query(Metric).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "loss" in row.label and "Best" not in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id
                })
        return rows_dict

    def select_best_loss_from_analysis(self, analysis_id):
        rows = self.session.query(Metric).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "loss" in row.label and "Best" in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id
                })
        return rows_dict

    def select_guessing_entropy_from_analysis(self, analysis_id):
        rows = self.session.query(GuessingEntropy).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "Best" not in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id,
                    "report_interval": row.report_interval,
                    "guessing_entropy": int(values_list[len(values_list) - 1]),
                })

        return rows_dict

    def select_best_guessing_entropy_from_analysis(self, analysis_id):
        rows = self.session.query(GuessingEntropy).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "Best" in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id,
                    "report_interval": row.report_interval,
                    "guessing_entropy": int(values_list[len(values_list) - 1]),
                })
        return rows_dict

    def select_success_rate_from_analysis(self, analysis_id):
        rows = self.session.query(SuccessRate).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "Best" not in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id,
                    "report_interval": row.report_interval,
                    "success_rate": values_list[len(values_list) - 1],
                })

        return rows_dict

    def select_best_success_rate_from_analysis(self, analysis_id):
        rows = self.session.query(SuccessRate).filter_by(analysis_id=analysis_id).all()
        rows_dict = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            if "Best" in row.label:
                rows_dict.append({
                    "values": values_list,
                    "label": row.label,
                    "id": row.id,
                    "report_interval": row.report_interval,
                    "success_rate": values_list[len(values_list) - 1],
                })
        return rows_dict

    def select_metric_names_from_analysis(self, table_class, analysis_id):
        metric_names = self.session.query(table_class.label).filter_by(analysis_id=analysis_id).distinct().all()
        return [name for name, in metric_names]

    def select_guessing_entropy_from_id(self, table_class, guessing_entropy_id):
        row = self.session.query(table_class).filter_by(id=guessing_entropy_id).first()
        values_as_array = json.loads(row.values)
        values_list = []
        for index, value in values_as_array.items():
            values_list.append(values_as_array[str(index)])

        return {
            "values": values_list,
            "label": row.label,
            "id": row.id
        }

    def select_success_rate_from_id(self, table_class, success_rate_id):
        row = self.session.query(table_class).filter_by(id=success_rate_id).first()
        values_as_array = json.loads(row.values)
        values_list = []
        for index, value in values_as_array.items():
            values_list.append(values_as_array[str(index)])

        return {
            "values": values_list,
            "label": row.label,
            "id": row.id
        }

    def select_hyperparameter_from_metric(self, table_class, metric_id, analysis_id):
        return self.session.query(table_class).filter_by(metric_id=metric_id, analysis_id=analysis_id).first()

    def select_hyperparameter_from_guessing_entropy(self, table_class, guessing_entropy_id, analysis_id):
        return self.session.query(table_class).filter_by(guessing_entropy_id=guessing_entropy_id, analysis_id=analysis_id).first()

    def select_guessing_entropy_from_hyperparameter(self, table_class, hyperparameters_id, analysis_id):
        return self.session.query(table_class).filter_by(hyperparameters_id=hyperparameters_id, analysis_id=analysis_id).all()

    def select_hyperparameter_from_success_rate(self, table_class, success_rate_id, analysis_id):
        return self.session.query(table_class).filter_by(success_rate_id=success_rate_id, analysis_id=analysis_id).first()

    def select_success_rate_from_hyperparameter(self, table_class, hyperparameters_id, analysis_id):
        return self.session.query(table_class).filter_by(hyperparameters_id=hyperparameters_id, analysis_id=analysis_id).all()

    def select_metric_from_analysis(self, table_class, label, analysis_id):
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id, label=label).all()
        return_struct = []

        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            return_struct.append({
                "values": values_list,
                "label": row.label,
                "id": row.id
            })
        return return_struct

    def select_all_guessing_entropy_from_analysis(self, table_class, analysis_id):
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id).all()
        key_ranks = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            key_ranks.append({
                "values": values_list,
                "label": row.label,
                "report_interval": row.report_interval,
                "key_rank": int(values_list[len(values_list) - 1]),
                "id": row.id
            })

        return key_ranks

    def select_key_rank_by_label(self, table_class, label, analysis_id):
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id, label=label).all()
        key_rank = {}
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            key_rank["values"] = values_list
            key_rank["label"] = row.label
            key_rank["report_interval"] = row.report_interval
            key_rank["key_rank"] = int(values_list[len(values_list) - 1])

        return key_rank

    def select_all_success_rate_from_analysis(self, table_class, analysis_id):
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id).all()
        success_rates = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            success_rates.append({
                "values": values_list,
                "label": row.label,
                "report_interval": row.report_interval,
                "success_rate": values_list[len(values_list) - 1],
                "id": row.id
            })

        return success_rates

    def select_success_rate_by_label(self, table_class, label, analysis_id):
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id, label=label).all()
        success_rate = {}
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            success_rate["values"] = values_list
            success_rate["label"] = row.label
            success_rate["report_interval"] = row.report_interval
            success_rate["success_rate"] = values_list[len(values_list) - 1]

        return success_rate

    def select_values_from_confusion_matrix(self, table_class, analysis_id):
        values_all = []
        rows = self.session.query(table_class).filter_by(analysis_id=analysis_id).all()
        for row in rows:
            values_as_array = json.loads(row.y_pred)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            values_all.append({
                "values": values_list
            })

        return values_all

    def select_confusion_matrix_from_analysis(self, table_class, hyperparameters_id, analysis_id):
        values_all = []
        rows = self.session.query(table_class).filter_by(hyperparameters_id=hyperparameters_id, analysis_id=analysis_id).all()
        for row in rows:
            values_as_array = json.loads(row.y_pred)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            values_all.append({
                "values": values_list
            })

        return values_all

    def select_visualization_from_analysis(self, table_class, hyperparameters_id, analysis_id):
        rows = self.session.query(table_class).filter_by(hyperparameters_id=hyperparameters_id, analysis_id=analysis_id).all()
        values_struct = []
        for row in rows:
            values_as_array = json.loads(row.values)
            values_list = []
            for index, value in values_as_array.items():
                values_list.append(values_as_array[str(index)])

            values_struct.append({
                "values": values_list,
                "label": row.label
            })
        return values_struct
