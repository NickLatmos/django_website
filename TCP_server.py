
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_website.settings'
import django
django.setup()
import socket
import threading
import urllib.request
import json

from weather_station.models import Valve

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self, num_of_clients):
        self.sock.listen(num_of_clients)
        while True:
            client, address = self.sock.accept()
            client.settimeout(2)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        '''
        A different thread services every connected client -- Not the best approach but good enough 
        for small scale systems and real time operations. 

        Request Format from weather station: VALVE?ID=<ID>\a
        Response Format from the TCP server: VALVE NO/NC\a
        '''
        size = 64
        ID = ''
        valve_status = ''

        while True:
            try:
                data = client.recv(size).decode('UTF-8')
                if data:
                    print('Received data: ' + data)
                    ID_index = data.find('ID=') + len('ID=')
                    #end_index = data.find('\a')  # Insert this when using the weather station
                    ID = data[ID_index:]
                    valve_status = self.receiveValveStatus(ID)
                    self.sendValveStatus(client, valve_status)
                else:
                    raise error('Client disconnected')
            except socket.timeout:
                # When a timeout happens check if there is any user input about the valve status
                # If there is send the new status from the TCP connection                                   
                # If not then do nothing
                new_valve_status = self.receiveValveStatus(ID)
                if(new_valve_status != valve_status and new_valve_status != ''):
                    valve_status = new_valve_status
                    self.sendValveStatus(client, valve_status)
            except:
                print('Closing client')
                client.close()
                return False

    def sendValveStatus(self, client, valve_status):
        '''
        Sends the valve status to the weather station
        Response format VALVE NO/NC\a
        '''
        data_to_send = "VALVE " + valve_status + '\a'
        client.send(data_to_send.encode('UTF-8'))

    def receiveValveStatus(self, ID):
        '''
        Get the valve status from the SQLlite database used from django models.
        Returns valve status 'NO' or 'NC' or '' in case the ID is invalid
        '''
        print('ID = ' + ID)
        if ID:
            try:
                valve = Valve.objects.get(ID=ID)
                return valve.valve_status   
            except:
                print('Exception occured')
        return '' 

'''
When you execute a Python script, it is treated as the main and its __name__ attribute is set to "__main__". 
If you import this script as a module in another script, the __name__ is set to the name of the script/module.
With this behavior any py file can exhibit dual behavior - it is a script as well as module.
'''
if __name__ == "__main__":
    port_num = input("Insert TCP server's port: ")
    num_of_clients = input("Max number of clients? ")
    ThreadedServer('',int(port_num)).listen(int(num_of_clients))