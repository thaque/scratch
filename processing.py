import random
import requests
import bs4

file_name = '/Users/thaque/code/projects/zarin/zarin_wordbank.txt'
backup_file_name = '/Users/thaque/code/projects/zarin/zarin_wordbank_backup.txt'
wordbank = [line.rstrip('\n') for line in open(file_name, 'r')]


def generate_questions(no):
    questions = random.sample(wordbank, no)
    return questions


def get_definition(word):
    """
    It finds the definition and two examples (if exists) from Oxford Learner's Dictionary website and returns a list
    """
    link_word = word
    span_word = word
    while link_word.find(' ') > -1:
        link_word = link_word.replace(' ', '-')
    while span_word.find(' ') > -1:
        span_word = span_word.replace(' ', '')

    url = f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{link_word}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    for i in soup.select(f'#{span_word}_def_1'):
        definition = i.string
    for i in soup.select(f'#{span_word}_x_1'):
        example1 = i.string
    for i in soup.select(f'#{span_word}_x_2'):
        example2 = i.string
    try:
        definition
    except NameError:
        definition = None
    try:
        example1
    except NameError:
        example1 = None
    try:
        example2
    except NameError:
        example2 = None

    return [word, definition, example1, example2]


def generate_choices(definition):
    choices = []
    choices.append(definition[1])
    random_word_list = random.sample(wordbank, 3)
    for word in random_word_list:
        definition = get_definition(word)
        choices.append(definition[1])
    choices = random.sample(choices, 4)
    return choices
