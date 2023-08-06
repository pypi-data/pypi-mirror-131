# @Time    : 2018/7/26 12:57
# @Author  : Niyoufa
import json, datetime
from microserver.db.mysql import BaseMySQL, Base, Column, CHAR, TEXT, Integer, DateTime
from microserver.conf import settings

TEST = 0
ADDITION = 1
CHANGE = 2
DELETION = 3


class LogEntry(Base, BaseMySQL):
    """用户操作日志"""
    __tablename__ = "django_admin_log"
    __table_args__ = (
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        }
    )

    _name = "%s.%s" % (settings.LOGENTRY_DATABASE, __tablename__)
    _alias_name = "mysql_log"

    id = Column(Integer, primary_key=True)
    action_time = Column(DateTime, nullable=False, default=datetime.datetime.now())
    object_id = Column(TEXT, nullable=True)
    object_repr = Column(TEXT, nullable=False)
    action_flag = Column(Integer, nullable=False)
    change_message = Column(TEXT, nullable=False)
    content_type_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)

    def create(self, vals, **kwargs):
        user_id = vals["user_id"]
        content_type_id = vals.get("content_type_id")
        object_id = vals.get("object_id")
        object_repr = vals["object_repr"]
        action_flag = vals["action_flag"]
        change_message = vals["change_message"]

        Session = self.get_session()
        session = Session()
        max_id = self.get_max_id(session=session)

        obj = LogEntry(**dict(
            id = max_id,
            user_id = user_id,
            content_type_id = content_type_id,
            object_id = object_id,
            object_repr = object_repr,
            action_flag = action_flag,
            change_message = change_message
        ))
        session.add(obj)
        session.commit()
        session.close()
        return max_id

    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        """
        记录日志
        :param user_id: 当前操作用户id，通过handler.get_current_user_id方法获取
        :param content_type_id: 模型id，可以为None
        :param object_id: 操作对象id，可以为None
        :param object_repr: 对象序列化字符， 可以为""
        :param action_flag: 操作类型，整型 ADDITION：添加 ， CHANGE：修改 DELETION：删除
        :param change_message: 操作消息
        :return: 
        """
        if isinstance(change_message, list):
            change_message = json.dumps(change_message)
        vals = dict(
            user_id=user_id,
            content_type_id=content_type_id,
            object_id=object_id,
            object_repr=object_repr[:200],
            action_flag=action_flag,
            change_message=change_message,
        )
        return self.create(vals)

