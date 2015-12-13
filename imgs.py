import tornado
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os
import json
import pygame.camera
import pygame.image
import time

from tornado.options import options, define
define("port", default=8700, help="run at given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print "coming"
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
        img = cam.get_image()
        pygame.image.save(img, self.application.settings["static_path"] + "/images/photo.bmp")
        pygame.camera.quit()
        cam.stop()
        self.write("ok")

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[(r'/', IndexHandler), ]
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