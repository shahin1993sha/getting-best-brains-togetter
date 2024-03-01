import csv

import nltk
import textract
from pdfminer.high_level import extract_text
import os

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def data_load(file, filename):
    """
    This function reads different types of source files.
    Input: Multiple file types like docx, pdf, txt
    Output: text string
    """
    split_filename = os.path.splitext(filename)
    # print(split_filename)
    file_extension = split_filename[1]
    # print("File Extension: ", file_extension)
    if file_extension == '.docx':
        data = str(textract.process(file), 'UTF-8')
    elif file_extension == '.pdf':
        data = extract_text(file)
    else:
        print("Invalid file format")
        quit()

    return data


def nltk_keywords(data):
    """
    This function contains the NLTK pipeline to detect keywords from input text data.
    Input: Text data
    Output: Keywords
    """
    data = clean_text(data)
    tokens = nltk_tokenizer(data)
    pos_tagged_tokens = nltk_pos_tag(tokens)
    keywords = filter_token_tag(pos_tagged_tokens, ['NNP', 'NN', 'VBP', 'JJ'])
    keywords = nltk_stopwords_removal(keywords)
    keywords = unique_tokens(keywords)
    # print('NLTK Keywords: ', keywords)
    return keywords


def clean_text(text):
    """
    This function cleans non-ASCII special characters from input text data.
    Input: Text string
    Output: Text string
    """
    import re
    cleaned_data = re.sub(r'[^a-zA-Z0-9\s\/]', '', text)
    cleaned_data = cleaned_data.replace('/', ' ')
    return cleaned_data


def nltk_tokenizer(text):
    """
    This function uses the NLTK tokeniser to tokenise the input text.
    Input: Text string
    Output: Tokens
    """
    from nltk import word_tokenize
    nltk.download('punkt')
    tokens = word_tokenize(text)
    # tokens = text.split()
    return tokens


def nltk_pos_tag(token_list):
    """
    This function uses the NLTK parts of speech tagger to apply tags to the input token list.
    Input: Token List
    Output: Tagged token list
    """
    from nltk import pos_tag
    nltk.download('averaged_perceptron_tagger')
    tagged_list = pos_tag(token_list)
    return tagged_list


def nltk_stopwords_removal(token_list):
    """
    This function removes stopwords from the input token list using the NLTK stopwords dictionary.
    Input: Token List
    Output: Stopwords filtered list
    """
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    stopwords_filtered_list = [w for w in token_list if w not in stop_words]
    return stopwords_filtered_list


def filter_token_tag(tagged_token_list, filter_tag_list):
    """
    This function filters the tagged token list present in the filter tag list.
    Input: Tagged token list, filter tag list
    Output: List containing tokens corresponding to tags present in the filter tag list
    """
    filtered_token_list = [t[0] for t in tagged_token_list if t[1] in filter_tag_list]
    filtered_token_list = [str(item) for item in filtered_token_list]
    return filtered_token_list


def unique_tokens(token_list):
    """
    This function removes duplicate tokens from the input token list.
    Input: Token list
    Output: Unique token list
    """
    unique_token_list = []
    for x in token_list:
        x = x.lower()
        if x not in unique_token_list:
            unique_token_list.append(x)
    return unique_token_list


def scrape_job_details():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Provide the path to your ChromeDriver executable
    webdriver_service = "C:\\Users\\shahi\\chromedriver\\chromedriver.exe"

    # Start the WebDriver
    driver = webdriver.Chrome(executable_path=webdriver_service, options=chrome_options)

    url = "https://jobs.ubs.com/TGnewUI/Search/home/HomeWithPreLoad?partnerid=25008&siteid=5012&PageType=searchResults&SearchType=linkquery&LinkID=4017#jobDetails=291121_5012"

    # Load the page
    driver.get(url)
    try:
        css_selector = "#content > div.homeContentLiner > div.clearfix.homeContent.MainContent > div:nth-child(4) > div.clearfix.jobDetailsMainDiv.ng-scope > div > div.questionClass.ng-scope > div:nth-child(10) > p.answer.ng-scope.section2LeftfieldsInJobDetails.jobDetailTextArea"

        # Find the element by the full CSS selector

        job_description_element = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        job_description = job_description_element.text.strip()

        job_title_element = driver.find_element("css selector",
                                                "#content > div.homeContentLiner > div.clearfix.homeContent.MainContent > div:nth-child(4) > div.clearfix.jobDetailsMainDiv.ng-scope > div > div.questionClass.ng-scope > div:nth-child(1) > span > h1")

        # Extract the job title
        job_title = job_title_element.text.strip()

        # Print the extracted job description
        #print(f"Job Title: {job_title}")
        #print(f"Job Description: {job_description}")
        return job_title, job_description

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()


def load_skills_dataset(file_path):
    skills = set()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            skills.update(row)
    return skills

def matchKeywords(keywords, skills):
    matched_skills = [skill for skill in skills if any(keyword.lower() == skill.lower() for keyword in keywords)]
    return matched_skills
