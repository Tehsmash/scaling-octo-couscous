import stun
from threading import Thread
import socket
import Queue

nat_type, external_ip, external_port = stun.get_ip_info('0.0.0.0', 60030)

print('Incoming IP and port %s:%s' % (external_ip, external_port))
send_ip = raw_input('Dest IP --> ')
send_port = raw_input('Dest Port --> ')
send_port = int(send_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 60030))

tosend = Queue.Queue()

def sock_processor():
    while True:
        incoming_data = None
        try:
            incoming_data, _ = sock.recvfrom(4096) 
        except socket.timeout:
            pass

        outgoing_data = None
        try:
            outgoing_data = tosend.get_nowait()
        except Queue.Empty:
            pass

        if incoming_data:
            print(incoming_data)

        if outgoing_data:
            sock.sendto(message, (send_ip, send_port))

t = Thread(target=sock_processor)
t.daemon = True
t.start()

while True:
    message = raw_input('Message --> ')
    tosend.put(message)
