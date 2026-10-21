import requests

s = requests.Session()
url = "http://127.0.0.1"
N = 70

table = {
    "PHP" : 0,
    "Python" : 0,
    "NodeJS" : 0
}

for i in range(N):
    response = s.get(url)    
    words = response.text.rpartition(" ")
    table[words[-1]] += 1

print(f"This is table of worked services \n\n PHP worked {table["PHP"]} times \n Python worked {table['Python']} times \n NodeJS worked {table['NodeJS']} times\n")