from sqlalchemy.orm import sessionmaker
from aisy_database.db_tables import *


class DBDelete:

    def __init__(self, database_path):
        self.db_select = None
        self.engine = create_engine('sqlite:///{}'.format(database_path), echo=False)
        self.metadata = MetaData(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def soft_delete_analysis_from_table(self, table_class, analysis_id):
        self.session.query(table_class).filter_by(id=analysis_id).update({"deleted": True})
        self.session.commit()
        return

    def hard_delete_row_from_table(self, table_class, row_id, analysis_id):
        self.session.query(table_class).filter(and_(table_class.id == row_id, table_class.analysis_id == analysis_id)).delete()
        self.session.commit()
        return
