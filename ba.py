import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def browser():
    opts = Options()
    # opts.set_headless()
    # assert opts.headless  # Operating in headless mode

    dir = os.path.dirname(__file__)
    chromedriver_path = os.path.join(dir,'chromedriver','chromedriver')

    browser = Chrome(executable_path=chromedriver_path, options=opts)
    browser.get('https://www.google.com/search?q=champions+league')
    table = browser.find_element_by_tag_name('table')
    print(table.text)


    return browser