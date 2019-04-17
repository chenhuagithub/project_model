import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from utils import config
from utils.url import handlers
import pymysql
import redis

from tornado.options import define, options


define("port", default=8000,help='run on given port', type=int)


class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.db=pymysql.connect(**config.mysql_options).cursor(cursor=pymysql.cursors.DictCursor)

        self.redis=redis.Redis(
            connection_pool=redis.ConnectionPool(**config.redis_options)
        )

def main():
    #设置日志文件优先级
    options.logging= config.log_level
    # 日志文件存储路径
    options.log_file_prefix= config.log_file
    tornado.options.parse_command_line()
    app = Application(handlers, **config.settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
