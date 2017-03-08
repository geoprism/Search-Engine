import os
import tornado.ioloop
import tornado.web
import whooshSearchEngine

class searchHandler(tornado.web.RequestHandler):
    def get(self, term):
        self.set_header("Access-Control-Allow-Origin", "*")
        test = whooshSearchEngine.whooshIndexer()
        content = test.makeSearch(term)

        self.write({"content":content})

def make_app():
    return tornado.web.Application([
        (r"/search/api/([^/]+)", searchHandler),
    ])


def main():
    app = make_app()
    port = int(os.environ.get("PORT", 5000))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
