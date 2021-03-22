import requests, json
  
URL = 'http://localhost:8079'
data1 =  { "state" : 1, "x" : 2, "y" : 5, "color" : "BLACK"}
data2 =  { "state" : 2, "x" : 1, "y" : 5, "color" : "GREEN"}
data3 =  { "state" : 3, "x" : 1, "y" : 3, "color" : "YELLOW"}

r = requests.post(url = URL, data=json.dumps(data1)) 
data = r.text
print("POST Returned:",data)

r = requests.post(url = URL, data=json.dumps(data2)) 
data = r.text
print("POST Returned:",data)

r = requests.post(url = URL, data=json.dumps(data3)) 
data = r.text
print("POST Returned:",data)

payload = {"state":1}
r = requests.get(url = URL, params=payload) 
data = r.text
print("GET Returned:",data)

payload = {"state":4}
r = requests.get(url = URL, params=payload) 
data = r.text
print("GET Returned:",data)