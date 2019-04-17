import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import pymysql
import os

from tornado.options import define,options
define('port',default=8888,help='run on given port',type=int)
#
# class Application(tornado.web.Application):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        # self.set_secure_cookie('itcast','abc')
        # sel='select ui_user_id,ui_age,ui_mobile from it_usr_info'
        # app.db.execute(sel)
        # ret=app.db.fetchall()
        # # cookie_ret=self.get_cookie('itcast')
        # # self.clear_cookie('itcast')
        # ret=self.get_secure_cookie('itcast')
        # self.write(ret)

    def post(self):
        username=self.get_argument('username')
        password=self.get_argument('password')
        dic=dict(
            username=username,
            password=password
        )
        self.write(dic)

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


class SinaHandler(tornado.web.RequestHandler):

    def get(self):
        stu={
            'ret':1,
            'start':1,
            'end':1,
            'country':'中国',
            'provice':'北京',
            'city':'北京',
            'district':'',
            'isp':'',
            'type':'',
            'desc':''
        }
        self.write(stu)






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
        (r'/cookie',CookieHandler),
        (r'/sina',SinaHandler),
    ],
    debug=True,
    template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    static_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'statics'),
    cookie_secret='I17mosMgQM6He6POdlUkpow7C0XWdkB0v7bFz77vab8=',
    #开启xsrf保护，开启这个功能时，必须开启cookie_secret
    xsrf_cookies=True
)


if __name__=='__main__':
    tornado.options.parse_command_line()
    app=tornado.web.Application(**setting)
    app.db=SQL_Connection(host='127.0.0.1',port=3306,user='root',passwd='123456',db='itcast')
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()