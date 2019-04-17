import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import pymysql
import os
from tornado.httpclient import AsyncHTTPClient
import json
import tornado.gen

from tornado.options import define,options
define('port',default=9000,help='run on given port',type=int)


class IndexHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        city=yield self.get_ip_city()
        self.write(city)

    @tornado.gen.coroutine
    def get_ip_city(self):
        client=AsyncHTTPClient()
        response=yield client.fetch('http://localhost:8888/sina')
        json_data=response.body
        data=json.loads(json_data.decode('utf8'))
        return data.get('city','')

    # @tornado.web.asynchronous
    # def get(self):
    #     http_client=tornado.httpclient.AsyncHTTPClient()
    #     http_client.fetch('http://localhost:8888/sina',callback=self.on_response)
    #
    #
    # # @tornado.gen.coroutine
    # def on_response(self,response):
    #     json_data=response.body
    #     data=json.loads(json_data.decode('utf8'))
    #     self.write(data.get('city',''))
    #     self.finish()








class CookieHandler(tornado.web.RequestHandler):
    def get(self):
        count=self.get_secure_cookie('count')
        if not count:
            self.set_secure_cookie('count','1')
        else:
            count=int(count)
            count+=1
            self.set_secure_cookie('count',str(count))
        self.write(str(count))




# 数据库连接
def SQL_Connection(host,port,user,passwd,db):
    conn=pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db)
    #设置游标
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor


#配置文件
setting=dict(
    handlers=[
        (r'/', IndexHandler),
        (r'/cookie',CookieHandler)
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'statics'),
    cookie_secret='I17mosMgQM6He6POdlUkpow7C0XWdkB0v7bFz77vab8='
)


if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application(**setting)
    app.db=SQL_Connection(host='127.0.0.1',port=3306,user='root',passwd='123456',db='itcast')
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()