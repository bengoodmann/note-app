from http.server import ThreadingHTTPServer
from handlers import APIRequestHandler

from db import initialize_database


def run(server_class=ThreadingHTTPServer, handler=APIRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler)
    print(f"Server started at port:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    initialize_database()
    run()
