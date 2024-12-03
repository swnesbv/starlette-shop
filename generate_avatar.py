import os
from urllib.request import urlopen
from bs4 import BeautifulSoup


def generate_avatar(url):
    # ..
    with urlopen(url) as response:
        # ..
        save_path = "./static/avatar/user/"
        os.makedirs(save_path, exist_ok=True)
        # ..
        soup = BeautifulSoup(response, "html.parser")
        with open(f"{save_path}" + "avatar.svg", "w", encoding="utf-8") as file:
            file.write(str(soup.svg))
    print(" avatar generated successfully..")

generate_avatar("http://localhost:8000/account/avatar")
