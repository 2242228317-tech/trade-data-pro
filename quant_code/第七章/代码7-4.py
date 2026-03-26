def process(code_list,num):
    browser = webdriver.Chrome()
    for code in code_list:

        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
    browser.quit()
def process2(code_list,num):
    browser = webdriver. Firefox()
    for code in code_list:

        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
browser.quit()
def process3(code_list,num):
    browser = webdriver. Edge()
    for code in code_list:

        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
browser.quit()
