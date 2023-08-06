# @Time    : 2018/5/4 14:21
# @Author  : Niyoufa
import docx2txt
from microserver.db.base import BaseModel


class FileParser(object):

    def parse_txt(self, body):
        return body.decode()

    def parse_docx(self, body):
        r_id = BaseModel.gen_objectid()
        file_dir = "/tmp/%s.docx"%r_id
        with open(file_dir, "wb") as f:
            f.write(body)
        text = docx2txt.process(file_dir)
        return text

    def parse_file(self, file_dir):
        text = docx2txt.process(file_dir)
        return text


class RequestFile(object):

    def __init__(self, filename, content_type, body):
        self.filename = filename
        self.content_type = content_type
        self.body = body
        self.file_parser = FileParser()

    def parse_body(self):
        try:
            file_type = self.filename.split(".")[-1]
        except:
            file_type = "txt"
        return getattr(self.file_parser, "parse_%s"%file_type)(self.body)

    def tojson(self):
        return dict(
            filename = self.filename,
            content_type = self.content_type,
            body = self.parse_body()
        )

