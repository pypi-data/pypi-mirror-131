# @Time    : 2018/6/15 12:29
# @Author  : Niyoufa
import time
import datetime
from microserver.conf import settings
from microserver.utils.common import is_chinese_string
from microserver.db.mysql import Base, BaseMySQL, Column, CHAR, TEXT, \
    UniqueConstraint, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from microserver.utils.crypto import md5
from microserver.addons.userauth.error import AuthError


class UserModel(Base, BaseMySQL):
    """
    用户表
    """

    __tablename__ = "auth_user"
    __table_args__ = (
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(CHAR(length=255), unique=True)
    password = Column(CHAR(length=255), nullable=False)
    last_login = Column(DateTime, default=datetime.datetime.now())
    email = Column(CHAR(length=255), unique=True, nullable=True)
    first_name = Column(CHAR(255), nullable=True, default="")
    last_name = Column(CHAR(255), nullable=True, default="")
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.datetime.now())


    def create_user(self, user_form):
        username = user_form["username"]
        password = self.make_password(user_form["password"])
        email = user_form.get("email")
        phone = user_form.get("phone")
        nickname = user_form.get("nickname")
        Session = self.get_session()
        session = Session()

        max_id = session.query(func.max(UserModel.id)).one()[0] + 1
        user = UserModel(**dict(
            id = max_id,
            username=username,
            password=password,
            email=email,
            is_superuser=False,
            is_staff=False
        ))
        session.add(user)

        max_id = session.query(func.max(UserProfileModel.id)).one()[0] + 1
        user_profile = dict(
            id = max_id,
            user_id=user.id,
        )
        if email:
            user_profile.update(dict(
                email = email
            ))
        if phone:
            user_profile.update(dict(
                phone = phone
            ))
        if nickname:
            user_profile.update(dict(
                nickname = nickname
            ))
        session.add(UserProfileModel(**user_profile))
        try:
            session.commit()
        except Exception as err:
            raise self.ArgumentTypeError("用户注册失败：%s"%err.args)

        session.close()
        return max_id

    def make_password(self, password):
        return md5((md5(password + settings.USERAUTH["slat"])))

    def check_password(self, user, password):
        return user.password == self.make_password(password)

    def set_password(self, user, password):
        if not password \
                or len(password) < 6 or len(password) > 16 \
                or is_chinese_string(password):
            raise AuthError("密码格式错误")
        password = self.make_password(password)
        self.update(user.id, {"password":password})

    def get_user_by_username(self, username):
        user = self.find_one_by_sql(
            "select id, username, password from auth_user where username='%s';"%username
        )
        return user

    def login(self, user, handler):

        # 登录状态过期设置
        if "login_expires_days" in settings.USERAUTH:
            login_expires_days = settings.USERAUTH["login_expires_days"]

            handler.set_secure_cookie('username', user.username.encode(),
                                   expires_days=login_expires_days)

            handler.set_secure_cookie("user_id", str(user.id).encode(),
                                      expires_days=login_expires_days)

        elif "login_expires" in settings.USERAUTH:
            login_expires = int(settings.USERAUTH["login_expires"])

            handler.set_secure_cookie('username', user.username.encode(),
                                      expires= int(time.time() + login_expires))

            handler.set_secure_cookie("user_id", str(user.id).encode(),
                                      expires=int(time.time() + login_expires))

        else:
            handler.set_secure_cookie('username', user.username.encode())
            handler.set_secure_cookie("user_id", str(user.id).encode())

        # token 过期设置
        if "csrf_expires_days" in settings.USERAUTH:
            csrf_expires_days = settings.USERAUTH["csrf_expires_days"]

            handler.set_cookie("csrf_token", handler.xsrf_token,
                               expires_days = csrf_expires_days)

        elif "csrf_expires" in settings.USERAUTH:
            csrf_expires = int(settings.USERAUTH["csrf_expires"])

            handler.set_cookie("csrf_token", handler.xsrf_token,
                               expires= int(time.time() + csrf_expires))

        else:
            handler.set_cookie("csrf_token", handler.xsrf_token)


    def logout(self, handler):
        handler.clear_all_cookies()


class UserProfileModel(Base, BaseMySQL):
    """
    用户扩展信息
    """

    __tablename__ = "auth_user_profile"
    __table_args__ = (
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(length=255), unique=True, nullable=False)
    nickname = Column(CHAR(length=255))
    phone = Column(CHAR(length=255), unique=True, nullable=True)
    email = Column(CHAR(length=255), unique=True, nullable=True)
    avator = Column(TEXT)
    qrcode = Column(TEXT)

    def get_current_user(self, handler):
        user_id = handler.get_secure_cookie("user_id")
        if not user_id:
            raise AuthError("用户未登录")
        else:
            user_id = int(user_id.decode())

        query = {"id": user_id}
        project = {"id":1, "username":1,
                   "last_login":1, "date_joined":1}
        user_obj = UserModel().find_one_by_query(query=query, project=project)
        user_obj["last_login"] = str(user_obj["last_login"])
        user_obj["date_joined"] = str(user_obj["date_joined"])

        query = {"user_id":user_id}
        project = {"nickname":1, "phone":1, "email":1}
        user_profile_obj = self.find_one_by_query(query=query, project=project)

        user = {}
        user.update(user_obj)
        user.update(user_profile_obj)

        return user


class GroupModel(Base, BaseMySQL):
    """
    组
    """

    __tablename__ = "auth_group"
    __table_args__ = (
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(CHAR(length=255), unique=True, nullable=False)


class UserGroupsModel(Base, BaseMySQL):
    """
    用户组
    """

    __tablename__ = "auth_user_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "group_id"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(length=255), nullable=False)
    group_id = Column(CHAR(length=255), nullable=False)


class PermissionModel(Base, BaseMySQL):
    """权限"""

    __tablename__ = "auth_permission"
    __table_args__ = (
        UniqueConstraint("content_type_id", "codename"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(CHAR(length=255), nullable=False)
    content_type_id = Column(CHAR(255), nullable=False)
    codename = Column(CHAR(length=255), nullable=False)


class GroupPermissionsModel(Base, BaseMySQL):
    """组权限"""

    __tablename__ = "auth_group_permissions"
    __table_args__ = (
        UniqueConstraint("group_id", "permission_id"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(CHAR(length=255), nullable=False)
    permission_id = Column(CHAR(length=255), nullable=False)

class UserPermissionsModel(Base, BaseMySQL):
    """用户权限"""

    __tablename__ = "auth_user_user_permissions"
    __table_args__ = (
        UniqueConstraint("user_id", "permission_id"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(length=255), nullable=False)
    permission_id = Column(CHAR(length=255), nullable=False)


class ContentTypeModel(Base, BaseMySQL):
    """应用模型"""

    __tablename__ = "django_content_type"
    __table_args__ = (
        UniqueConstraint("app_label", "model"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_label = Column(CHAR(length=255), nullable=False)
    model = Column(CHAR(length=255), nullable=False)


class UserActionModel(Base, BaseMySQL):
    """用户行为"""

    __tablename__ = "auth_user_action"
    __table_args__ = (
        UniqueConstraint("user_id", "obj_id", "action_type"),
        {
            "mysql_engine": "InnoDB",
            "extend_existing": True,
        },
    )

    _name = "auth.%s" % __tablename__
    _alias_name = "mysql_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(length=255), nullable=False)
    obj_type = Column(CHAR(length=255), nullable=False)
    obj_id = Column(CHAR(length=255), nullable=False)
    action_type = Column(CHAR(length=255), nullable=False)



