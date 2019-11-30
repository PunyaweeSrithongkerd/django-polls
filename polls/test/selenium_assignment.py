from selenium import webdriver
import requests


def get_links(url: str):
    """Find all links on page at the given url.
       Return a list of all link addresses, as strings.
    """
    browser = webdriver.Chrome(executable_path=r'C:\Users\User\Desktop\Driver\chromedriver.exe')
    browser.get(url)
    link_divs = browser.find_elements_by_tag_name('a')
    links = []
    for link in link_divs:
        if link.tag_name == 'a':
            url = link.get_attribute('href')
            links.append(url)
    browser.close()
    return links


def invalid_urls(url_list: list):
    error_url: list = []
    for url in url_list:
        test_url = requests.head(url)
        if test_url.status_code is 404:
            error_url.append(url)
    return error_url


if __name__ == "__main__":
    target = get_links('https://cpske.github.io/ISP/')
    for url in target:
        print(url)
    error_url_list = invalid_urls(target)
    for url in error_url_list:
        print(url)
