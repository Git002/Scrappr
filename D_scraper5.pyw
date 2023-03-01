from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
from bs4 import BeautifulSoup as Soup


def to_do():
    # vars...
    conn = sqlite3.connect(r'test.db')
    csv_file_location = r"data_file.csv"

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/80.0.3987.132 Safari/537.36'

    driver_exe = 'chromedriver'
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-cross-origin-auth-prompt")

    cur = conn.cursor()
    cur.execute("SELECT id FROM urls")

    for my_url in cur.fetchall():
        pass

    unwanted_chars = "()''"
    url_to_str = str(my_url)

    for wanted_char in unwanted_chars:
        result = url_to_str.replace(wanted_char, "")

    # changing tupled string by removing "(", ")", ","
    step_1 = result.replace("(", "")
    step_2 = step_1.replace(")", "")
    step_3 = step_2.replace(",", "")
    print(step_3)

    driver = webdriver.Chrome(
        executable_path=r"chromedriver", options=options)
    driver.get(step_3)

    cur.execute("SELECT class FROM classes")
    all_values = tuple()
    for class_Names in cur.fetchall():
        all_values += class_Names

    print(all_values)
    # changing tupled string by removing "(", ")", ","
    one, two, three, four, five = all_values

    one = one.replace(' ', '.')
    print(one)

    two = two.replace(' ', '.')
    print(two)

    three = three.replace(' ', '.')
    print(three)

    four = four.replace(' ', '.')
    print(four)

    five = five.replace(' ', '.')
    print(five)

    cur.execute("SELECT tag FROM classes;")
    all_values1 = tuple()
    for tags in cur.fetchall():
        all_values1 += tags

    print(all_values1)
    one1_, two2_, three3_, four4_, five5_ = all_values1

    x = one1_ + one
    print(x)

    y = two2_ + two
    print(y)

    z = three3_ + three
    print(z)

    z1 = four4_ + four
    print(z1)

    z2 = five5_ + five
    print(z2)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, x))
    )
    page = Soup(driver.page_source, features='html.parser')
    elements = page.select(x)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, y))
    )
    page = Soup(driver.page_source, features='html.parser')
    elements2 = page.select(y)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, z))
    )
    page = Soup(driver.page_source, features='html.parser')
    elements3 = page.select(z)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, z1))
    )
    page = Soup(driver.page_source, features='html.parser')
    elements4 = page.select(z1)

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, z2))
    )
    page = Soup(driver.page_source, features='html.parser')
    elements5 = page.select(z2)

    df = pd.DataFrame({
        "Title1": pd.Series([ele.text.strip() for ele in elements]),
        "Title2": pd.Series([ele2.text.strip() for ele2 in elements2]),
        "Title3": pd.Series([ele3.text.strip() for ele3 in elements3]),
        "Title4": pd.Series([ele4.text.strip() for ele4 in elements4]),
        "Title5": pd.Series([ele5.text.strip() for ele5 in elements5]),
    })

    df = df.dropna()
    df.to_csv(csv_file_location,
              index=False, mode='a', encoding='utf-8')
    try:
        f = open(csv_file_location)
        print("Done !!!\n"*3)
        # Do something with the file
    except IOError:
        print("File not accessible")
    finally:
        f.close()
    driver.quit()
    #print("Unable to scrape...")

    cur.execute("""DROP TABLE Classes;""")
    cur.execute("""DROP TABLE urls;""")
    print("start")
