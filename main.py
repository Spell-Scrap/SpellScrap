import re
import ssl
from urllib.request import urlopen

from bs4 import BeautifulSoup

# Ignore SSL certificate errors
from spell_checker_collections.checker_collections import SpellChecker

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def scrap_link(url):
    # url = 'https://www.lexico.com/grammar/common-misspellings'
    # url = 'https://en.wikipedia.org/wiki/Commonly_misspelled_English_words'
    # url = 'https://www.englishclub.com/spelling/misspellings.htm'
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    # Retrieve all of the anchor tags
    # words = soup('li')
    text = [soup('s'), soup('li'), soup('td')]
    # text = [soup('s'), soup('li'), soup('td'), soup('p')]
    set_words = []

    for words in text:
        for word in words:
            check_content = str(word.contents[0])
            if check_content[0] == '<':
                continue
            set_words.append(check_content)
            # print(check_content)
    return set_words


checker = SpellChecker("big_text.txt")
# print(scrap_link('https://www.lexico.com/grammar/common-misspellings'))
list_of_word = scrap_link('https://www.lexico.com/grammar/common-misspellings')
list_for_correction = []
list_of_correction = []
list_spell_correction = []
for word in list_of_word:
    reformat_word = re.findall(r'\w+', word)
    for word_page in reformat_word:
        list_for_correction.append(word_page)
        word_corrected = checker.check(word_page)
        if not word_corrected:
            continue
        list_of_correction.append(word_corrected)
for correction in list_of_correction:
    list_spell_correction.append(correction[0][0])
print("for correction: ", list_for_correction)
print("Corrected: ", list_spell_correction)
# print(scrap_link('https://en.wikipedia.org/wiki/Commonly_misspelled_English_words'))

# from flask import Flask, render_template, request
#
# app = Flask(__name__)
#
#
# @app.route('/')
# @app.route('/home')
# def home_page():
#     return render_template('home.html')
#
#
# @app.route('/result-car', methods=['POST', 'GET'])
# def result_car():
#     output = request.form.to_dict()
#     car = output["car"]
#     image_name = car + '.jpg'
#     car_output = predict(car)
#     return render_template('home.html', car=car_output, imageCar=image_name)
#
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
