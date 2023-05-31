from Server import Server

def main():
    host = "localhost"
    port = 1234

    #run server functions -> from Server object.
    server = Server(host, port, "users")
    server.start()


if __name__ == '__main__':
    main()
