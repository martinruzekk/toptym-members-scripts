from os import name, remove, replace
from bs4 import BeautifulSoup
import string
import random
import csv
from bs4.dammit import chardet_type


members = []

with open('members.html', 'r') as html:
    content = html.read()
    soup = BeautifulSoup(content, 'lxml')
    members_html = soup.find_all('tr', class_='active-membership')
    members_html += soup.find_all('tr', class_='near-end-membership')

    for member in members_html:
        member_email = member.find('td', class_='grid-cell-email').text.strip()

        members.append(member_email)


with open('emails.txt', 'a') as f:
    for member in members:
        f.write(f"{member},")

with open('members.csv', 'w', newline='', encoding="utf8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for member in members:
        spamwriter.writerow(member)

# print(members)
