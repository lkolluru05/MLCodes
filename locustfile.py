from locust import HttpUser, task
import json

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        d={"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1],"data":["I am going"]}]}
        resp=self.client.post("/llama7b/infer", data='{"inputs": [{"name":"text_input","datatype":"BYTES","shape":[1],"data":["I am going"]}]}')



#locust --headless --users 100 -r 100 -H http://127.0.0.1:8000/v2/models