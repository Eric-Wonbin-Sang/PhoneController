import socket

import Functions


class Server:

    def __init__(self):

        self.host_ip = ""
        self.port = 12345
        self.socket = self.get_socket()

        print("IP: \t{}\nhost: \t{}\nport: \t{}".format(
            socket.gethostbyname(socket.gethostname()), self.host_ip, self.port)
        )
        print("-----------------------")

        self.conn, self.address = self.get_conn_address()       # conn is new socket?

        self.accelerometer = [0, 0, 0]
        self.gyroscope = [0, 0, 0]

    def get_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host_ip, self.port))
        return s

    def get_conn_address(self):
        print("Searching for device...")
        self.socket.listen(1)
        conn, address = self.socket.accept()
        print('Connected to:', "\n\tconn: \t{}\n\taddress: \t{}".format(conn, address))
        print("-----------------------")
        return conn, address

    def update_dicts(self, client_data):
        sensor_data_list = client_data.split("|")
        for sensor_data in sensor_data_list:
            if sensor_data[0] == "a":
                self.accelerometer = [Functions.str_to_float(x) for x in sensor_data[3:-1].split(",")]
            elif sensor_data[0] == "g":
                self.gyroscope = [Functions.str_to_float(x) for x in sensor_data[3:-1].split(",")]

    def run(self):
        run_cond = True
        while run_cond:
            try:
                data = self.conn.recv(1024)
                if data:
                    data = data.decode("utf-8")
                    print("Client Says: " + data)
                    self.update_dicts(data)
                    self.conn.sendall(b"Server received data")
                    print("\ta:", self.accelerometer)
                    print("\tg:", self.gyroscope)

            except socket.error:
                print("Disconnected with device")
                self.socket.listen(1)
                self.conn, self.address = self.socket.accept()
        self.conn.close()


def main():

    server = Server()
    server.run()


main()
