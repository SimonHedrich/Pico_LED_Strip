import network
import socket
import time
import json


class WiFiManager:
    def __init__(self, ssid:str, password:str):
        self.ssid = ssid
        self.password = password
        
    def connect_to_network(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])

    def setup_socket(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(addr)
        self.socket.listen(1)
        print('listening on', addr)
    
    def _handle_request(self, request):
        # Parse the request
        lines = request.split('\r\n')
        method, path, _ = lines[0].split(' ')
        
        # Define responses for each API route
        if path.startswith('/api/status'):
            # Implement status retrieval logic
            status = {"status": "on", "currentPattern": {"name": "Red Wave", "duration": 10}}
            return '200 OK', 'application/json', json.dumps(status)
        elif path.startswith('/api/power'):
            # Extract on/off command from the request body if method is POST
            if method == 'POST':
                # turn_led_on_off(True if path.endswith('/on') else False)
                return '200 OK', 'application/json', json.dumps({"message": "LED strip turned on/off successfully"})
            return '200 OK', 'application/json', json.dumps({"message": "LED strip turned on/off successfully"}) 
        # Add more elif blocks for other API routes like '/api/pattern', '/api/patterns/add', etc.
        else:
            return '404 Not Found', 'text/plain', 'Endpoint not found.'

    def listen_for_connections(self):
        try:
            cl, addr = self.socket.accept()
            print('client connected from', addr)
            request = cl.recv(1024).decode('utf-8')
            print(request)

            status_code, content_type, response_body = self._handle_request(request)

            response = f'HTTP/1.1 {status_code}\r\nContent-Type: {content_type}\r\n\r\n{response_body}'
            cl.sendall(response)
            cl.close()
        except OSError as e:
            cl.close()
            print('connection closed')
