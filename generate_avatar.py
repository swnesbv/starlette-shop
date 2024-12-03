import os
from urllib.request import urlopen
from bs4 import BeautifulSoup


def generate_avatar(url):
    # ..
    with urlopen(url) as f:
        # ..
        save_path = "./static/avatar/user/"
        os.makedirs(save_path, exist_ok=True)
        # ..
        soup = BeautifulSoup(f, "html.parser")
        print(" user ..", dict(f.headers))
    with open(f"{save_path}" + "avatar.svg", "w", encoding="utf-8") as f:
        f.write(str(soup.svg))
    print(" avatar generated successfully..")

generate_avatar("http://localhost:8000/account/avatar")
