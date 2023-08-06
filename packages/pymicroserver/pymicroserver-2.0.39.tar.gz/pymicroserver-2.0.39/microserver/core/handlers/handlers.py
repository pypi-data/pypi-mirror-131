# @Time    : 2018/3/23 16:34
# @Author  : Niyoufa
from http import HTTPStatus
from tornado import escape
from tornado.web import RequestHandler
from tornado import gen
from tornado.web import authenticated
from tornado.log import access_log
from microserver.conf import settings
from microserver.utils import http_status
responses = {v: v.phrase for v in HTTPStatus.__members__.values()}
responses.update({v: v.phrase for v in http_status.HTTPStatus.__members__.values()})

from microserver.core.exceptions import HandlerError
from microserver.core.exceptions import MissingArgumentError
from microserver.core.exceptions import ArgumentTypeError
from microserver.core.exceptions import AuthError
from microserver.utils import decorator

from microserver.files.parse import RequestFile

class BaseHandler(RequestHandler):
    """请求和响应处理基类
以下是注释模板
@name 多轮问答
@description 根据用户上下文会话，
@description 识别用户问题意图，推荐合理答案

@path
  /qa_port/qa:
    get:
      tags:
      - "多轮问答"

      summary: ""

      description: ""

      operationId: ""

      consumes:
      - "application/json"

      produces:
      - "application/json"

      parameters:
      - name: "uid"
        in: "body"
        description: "用户id"
        example: {"uid":"niyoufa"}
      - name: "content"
        in: "query"
        description: "用户问题描述"
        required: true
        example: "我要离婚, 房子怎么分"

      responses:
        200:
          description: "返回成功"
          schema:
            $ref: "#definitions/ResponseData"
        400:
          description: "请求参数错误"
@endpath

@definitions
  ResponseData:
    type: "object"
    example: {
      type: 0,
      answer: xxx, 
      law_ids: [xxx, xxxx],
      case_ids: [xxx, xxx]
    }
    required:
    - "type"
    - "answer"
    - "options"
    - "law_ids"
    - "case_ids"
    properties:
      type:
        type: "integer"
        description: "回答的类型"
      answer:
        type: "string"
        description: "回答给出的文本，依据类型不同，可能是追问的内容，也可能是答案"
        example: "请问房子的购买时间？"
      options:
        type: "array"
        description: "提供给用户的选项。回答类型为追问时可能具有选项。"
      law_ids:
        type: "array"
        description: "法条id列表"
      case_ids:
        type: "array"
        description: "案件id列表"
@enddefinitions

"""

    SUPPORTED_METHODS = RequestHandler.SUPPORTED_METHODS + ()

    HandlerError = HandlerError
    ArgumentTypeError = ArgumentTypeError
    AuthError = AuthError

    access_log = access_log
    access_logger = access_log

    def initialize(self, **kwargs):
        """作为URL规范的第三个参数会作为关键词参数传给该方法"""
        pass

    @decorator.future_except
    def prepare(self):
        """在请求方法 get、post等执行前调用，进行通用的初始化，支持协程"""
        if settings.AUTH:
            username = self.get_current_user()
            if not username:
                raise self.AuthError("用户未登录")

    def on_finish(self):
        """请求方法结束发送响应给客户端后调用，和prepare对应，进行清理，日志处理"""
        pass

    def on_connection_close(self):
        """客户端关闭连接后调用，清理和长连接相关的资源"""
        pass

    def set_default_headers(self):
        """在请求开始时设置请求头部"""

    def _get_argument(self, name, default, source, strip=True):
        """获取参数"""
        args = self._get_arguments(name, source, strip=strip)
        if not args:
            if default is self._ARG_DEFAULT:
                raise MissingArgumentError(name)
            return default
        return args[-1]

    def set_status(self, status_code, reason=None):
        self._status_code = status_code
        if reason is not None:
            self._reason = escape.native_str(reason)
        else:
            try:
                self._reason = responses[status_code]
            except KeyError:
                raise ValueError("未知状态码 %d", status_code)

    def files(self):
        files = []
        if self.request.files:
            request_files = self.request.files.get("file")
            for file in request_files:
                content_type = file.get("content_type")
                filename = file.get("filename")
                body = file.get("body")
                request_file = RequestFile(filename, content_type, body)
                files.append(request_file)
        return files

    def parse_file_body(self, file):
        file.get("body").decode()

    def init_response_data(self):
        """初始化返回参数"""
        result = {'code': 200, 'msg': '返回成功'}
        return result

    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if username:
            return username.decode()

    def get_current_user_id(self):
        user_id = self.get_secure_cookie("user_id")
        if user_id:
            return user_id.decode()


class NoXsrfHandler(BaseHandler):
    """不需要进行xsrf检查"""

    def check_xsrf_cookie(self):
        pass


class NoAuthHandler(NoXsrfHandler):
    """不需要认证"""

    def prepare(self):
        pass
