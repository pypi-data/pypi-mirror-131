# @Time    : 2018/5/2 10:16
# @Author  : Niyoufa
import unittest
from microserver.tests import print_testcase
from microserver.db.mysql import Base, MySQL, Column, CHAR, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import UniqueConstraint


class MysqlTestCase(unittest.TestCase):

    @print_testcase
    def test_session(self):
        class AegisUserModel(Base, MySQL):
            _name = "imonitor.aegis_user"
            _alias_name = "mysql_test"
            __tablename__ = "aegis_user"

            id = Column(CHAR(length=255), primary_key=True)
            name = Column(CHAR(length=255))

        laws_related_model = AegisUserModel()
        Session = laws_related_model.get_session()
        session = Session()
        self.assertIsInstance(session.query(AegisUserModel.id, AegisUserModel.name).first(), tuple)

    @print_testcase
    def test_insert(self):
        class LawsRelatedModel(Base, MySQL):
            _name = "xengine.xengine_laws_related"
            _alias_name = "mysql_test1"

            __tablename__ = "xengine_laws_related"
            __table_args__ = (
                UniqueConstraint("laws_id", "doc_id"),
                {
                    "mysql_engine": "InnoDB",
                    "extend_existing": True,
                }
            )

            laws_id = Column(CHAR(length=255), nullable=False)
            doc_id = Column(CHAR(length=255), nullable=False)
            related = Column(Integer, nullable=False)

        laws_related_model = LawsRelatedModel()
        insert_id = laws_related_model.insert(dict(
            id = laws_related_model.gen_objectid(),
            laws_id = laws_related_model.gen_objectid(),
            doc_id = laws_related_model.gen_objectid(),
            related=0,
        ))

        with self.assertRaises(IntegrityError):
            laws_related_model.insert(dict(
                id = insert_id,
                laws_id = "dfsfs",
                doc_id = "dsfsfa",
                related = 0
            ))

    @print_testcase
    def test_update(self):
        class LawsRelatedModel(Base, MySQL):
            _name = "xengine.xengine_laws_related"
            _alias_name = "mysql_test1"

            __tablename__ = "xengine_laws_related"
            __table_args__ = (
                UniqueConstraint("laws_id", "doc_id"),
                {
                    "mysql_engine": "InnoDB",
                    "extend_existing": True,
                }
            )

            laws_id = Column(CHAR(length=255), nullable=False)
            doc_id = Column(CHAR(length=255), nullable=False)
            related = Column(Integer, nullable=False)

        laws_related_model = LawsRelatedModel()

        insert_id = laws_related_model.insert(dict(
            id = laws_related_model.gen_objectid(),
            laws_id=laws_related_model.gen_objectid(),
            doc_id=laws_related_model.gen_objectid(),
            related=0,
        ))

        laws_related_model.update(insert_id, {"is_enable":False})

        obj = laws_related_model.find_one(insert_id)
        self.assertEqual(obj["is_enable"], False)

    @print_testcase
    def test_remove(self):
        class LawsRelatedModel(Base, MySQL):
            _name = "xengine.xengine_laws_related"
            _alias_name = "mysql_test1"

            __tablename__ = "xengine_laws_related"
            __table_args__ = (
                UniqueConstraint("laws_id", "doc_id"),
                {
                    "mysql_engine": "InnoDB",
                    "extend_existing": True,
                }
            )

            laws_id = Column(CHAR(length=255), nullable=False)
            doc_id = Column(CHAR(length=255), nullable=False)
            related = Column(Integer, nullable=False)

        laws_related_model = LawsRelatedModel()

        insert_id = laws_related_model.insert(dict(
            id = laws_related_model.gen_objectid(),
            laws_id=laws_related_model.gen_objectid(),
            doc_id=laws_related_model.gen_objectid(),
            related=0,
        ))

        laws_related_model.remove(insert_id)
        with self.assertRaises(NoResultFound):
            laws_related_model.find_one(insert_id)

    @print_testcase
    def test_search(self):
        class LawsRelatedModel(Base, MySQL):
            _name = "xengine.xengine_laws_related"
            _alias_name = "mysql_test1"

            __tablename__ = "xengine_laws_related"
            __table_args__ = (
                UniqueConstraint("laws_id", "doc_id"),
                {
                    "mysql_engine": "InnoDB",
                    "extend_existing": True,
                }
            )

            laws_id = Column(CHAR(length=255), nullable=False)
            doc_id = Column(CHAR(length=255), nullable=False)
            related = Column(Integer, nullable=False)

        laws_related_model = LawsRelatedModel()
        laws_related_model.insert(dict(
            id=laws_related_model.gen_objectid(),
            laws_id=laws_related_model.gen_objectid(),
            doc_id=laws_related_model.gen_objectid(),
            related=0,
        ))
        laws_related_model.insert(dict(
            id=laws_related_model.gen_objectid(),
            laws_id=laws_related_model.gen_objectid(),
            doc_id=laws_related_model.gen_objectid(),
            related=0,
        ))

        query = {"is_enable":True}
        project = {"id":1, "update_timestamp":1}
        sort = {"update_timestamp":-1}
        objs, pager = laws_related_model.search(query=query, project=project, sort=sort)
        self.assertLessEqual(objs[1]["update_timestamp"], objs[0]["update_timestamp"])

if __name__ == "__main__":
    unittest.main()