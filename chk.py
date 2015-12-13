import tornado
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os
import json

from tornado.options import options, define
define("port", default=8500, help="run at given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', var=self.application.settings["static_path"] + "/styles/loginstyle.css" )

    def post(self):
        user_id=self.get_argument('user')
        passw=self.get_argument('pword')
        if((user_id=="shubham14100" and passw=="hello") or (user_id=="akash14008" and passw=="bye")):
            self.render('setmap.html',var=self.application.settings["static_path"] + "/styles/loginstyle.css")
            #
            print "correct",user_id,passw
        else:
            self.render('login.html',var=self.application.settings["static_path"] + "/styles/loginstyle.css")
            print "incorrect",user_id,passw

class PiHandler(tornado.web.RequestHandler):
    def post(self):
        destiny = json.loads(self.get_argument('he'))
        #destiny=[float(destiny[0]),float(destiny[1])]
        destiny = [destiny['0'],destiny['1']]
        print destiny
        points=[]
        self.render("show.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers=[(r'/', IndexHandler), (r'/rpi',PiHandler), ]
        settings=dict(
            template_path=os.path.join(os.path.dirname(__file__)+"templates"),
            static_path=os.path.join(os.path.dirname(__file__)+"static"),
            debug=True,
        )
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()