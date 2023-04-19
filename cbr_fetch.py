"""
CBR FETCH - DOWNLOAD ALL YOUR CODEBREAKER SOLUTIONS!
Only works for solved problems, no partially solved ones.
Only works for CPP files at the moment. (if u use python on codebreaker ur a noob)
"""

from bs4 import BeautifulSoup
import requests
import json
import os

# create session and set cookie
session = requests.Session()
with open("cookie.json", "r") as r:
    cookie = json.load(r)[0]
    session.cookies.set(domain=cookie["domain"], name=cookie["name"], value=cookie["value"])

# get username and scrape profile
username = input("ENTER YOUR CODEBREAKER USERNAME: ")
r = session.get(f"https://codebreaker.xyz/profile/{username}")
soup = BeautifulSoup(r.text, "html.parser")
solved_problems = [elem.get_text().strip(" ") for elem in soup.find_all("td", {"style": "width: 25%"})]

# get code from every solved problem
for problem_name in [problem for problem in solved_problems if problem]:
    
    # get webpage and submission id
    r = session.get(f"https://codebreaker.xyz/submissions?problem={problem_name}&username={username}")
    soup = BeautifulSoup(r.text, "html.parser")
    submission_id = [elem.get_text() for elem in soup.find_all("a", {"href": lambda href: href.startswith("/submission/")})][0]

    # get submission page
    r = session.get(f"https://codebreaker.xyz/submission/{submission_id}")
    soup = BeautifulSoup(r.text, "html.parser")
    code = soup.find("textarea", {"id": "editor"})["innerhtml"]

    # write to file
    print(f"DOWNLOADING: {problem_name}, id={submission_id}")
    with open(f"{problem_name}.cpp", "wb") as w:
        w.write(code.encode("utf-8"))
        w.write(os.linesep.encode("utf-8")) # weird newlines added for no reason if i just write code into the file with w mode