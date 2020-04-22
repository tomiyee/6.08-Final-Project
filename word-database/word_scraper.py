from bs4 import BeautifulSoup
import requests
import re
import sys, os
import subprocess

raw_dictionary_directory = "raw_dictionary_by_letter"
full_dict_file = "raw_full_dictionary.txt"

try:
    os.mkdir(raw_dictionary_directory)
except:
    pass

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = "http://phrontistery.info/{}.html".format(letter)
    r = requests.get(url)
    html_doc = r.text

    soup = BeautifulSoup(html_doc, "lxml")

    table = soup.find("table", {"class":"words"})

    output = ""
    for i, row in enumerate(table.findAll("tr")):
        if i == 0:
            continue
        pair = row.findAll("td")
        word, meaning = [w.get_text() for w in pair]
        meaning = meaning.strip()
        output += "{}={}\n".format(word, meaning)

    with open("{}/{}_words.txt".format(raw_dictionary_directory, letter), "w", encoding='utf-8') as out:
        out.write(output)
    print("done with words starting with {}".format(letter))

i = 'bash -c "cat {}/*.txt > {}"'.format(raw_dictionary_directory, full_dict_file)
os.system(i)
