import locust
import os

class QuantumApiUser(locust.HttpUser):
    wait_time = locust.between(1, 5)
    
    def on_start(self):
        # Use HTTPS and ignore SSL verification
        response = self.client.post("https://127.0.0.1:7777/api/auth",
                                  json={"api_key": "your-api-key"},
                                  verify=False)  # Ignore SSL certificate warnings
        self.token = response.json()["token"]
    
    @locust.task
    def process_signal(self):
        print (self.token)
        # Use HTTPS and ignore SSL verification
        self.client.post("https://127.0.0.1:7777/api/process-signal",
                        json={"signal_data": [1.0, 2.0, 3.0, 4.0]},
                        headers={"X-API-Key": f"{self.token}"},
                        verify=False)  # Ignore SSL certificate warnings

# Optional: Add host configuration in Locust run command
if __name__ == "__main__":
    locust.run()