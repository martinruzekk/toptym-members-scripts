from os import name, remove, replace
from bs4 import BeautifulSoup
import string
import random
import csv
from bs4.dammit import chardet_type

print('Zadej kraj (např. "Karlovarský" - bez "kraj"): ')
kraj = input()


def password_generator():
    passwd_chars = list(string.ascii_letters + string.digits + "!@#$%&*()")
    random.shuffle(passwd_chars)
    password = []
    for i in range(12):
        password.append(random.choice(passwd_chars))

    random.shuffle(password)

    return "".join(password)


def remove_dia(text):
    result = text.lower()
    zMala = "á ä č ď é ě í ľ ĺ ň ó ö ő ô ř ŕ š ť ú ů ü ű ý ž".split(' ')

    naMala = ['a', 'a', 'c', 'd', 'e', 'e', 'i', 'l', 'l', 'n', 'o',
              'o', 'o', 'o', 'r', 'r', 's', 't', 'u', 'u', 'u', 'u', 'y', 'z']

    for char in result:
        if char in zMala:
            result = result.replace(char, naMala[zMala.index(char)])
    return result


def phone_numbers(input):
    number = ""
    if "+420" not in input:
        number = "\"+420" + input.replace(' ', '') + "\""
    else:
        number = "\"" + input.replace(' ', '') + "\""
    return number


members = []

with open('members.html', 'r') as html:
    content = html.read()
    soup = BeautifulSoup(content, 'lxml')
    active = soup.find_all(
        'tr',
        class_='active-membership'
    )
    near_end = soup.find_all(
        'tr',
        class_='near-end-membership'
    )
    members_html = active + near_end

    for member in members_html:
        member_firstname = member.find(
            'td', class_='grid-cell-name').text.strip().split(' ')[0]
        member_lastname = member.find(
            'td', class_='grid-cell-name').text.strip().split(' ')[1]
        member_email = member.find('td', class_='grid-cell-email').text.strip()
        member_tt_email = ""
        member_phone = member.find(
            'td', class_='grid-cell-phone').text.strip()

#'""' + phone_numbers(member_phone) + '"',
        member_final = [member_firstname,
                        member_lastname,
                        remove_dia(member_firstname).lower(
                        ) + "." + remove_dia(member_lastname).lower() + "@toptym.cz", password_generator(),
                        '',
                        '/' + kraj + " kraj",
                        '',
                        member_email,
                        member_email,
                        f"{phone_numbers(member_phone)}",
                        kraj + ' kraj']

        members.append(member_final)

with open('members-' + kraj + '.csv', 'w', newline='', encoding="utf8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['First Name [Required]', 'Last Name [Required]', 'Email Address [Required]', 'Password [Required]', 'Password Hash Function [UPLOAD ONLY]',
                        'Org Unit Path [Required]', 'New Primary Email [UPLOAD ONLY]', 'Recovery Email', 'Home Secondary Email', 'Recovery Phone [MUST BE IN THE E.164 FORMAT]', 'Department'])
    for member in members:
        spamwriter.writerow(member)
    exit()

# print(members)
