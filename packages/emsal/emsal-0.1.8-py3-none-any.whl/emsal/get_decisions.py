import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
from os import path


def get_decisions(driver_path, year, init_no=0, last_no=999999, keyword='içtihat'):
    try:
        # define driver
        driver = webdriver.Chrome(executable_path=driver_path)

        # get the website
        driver.get('https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/')
        get_decisions.last_no_static = str(last_no)
        # click to the search box
        search_form = driver.find_element(By.ID, 'aramaForm:aranan')

        # write down the search term
        search_form.send_keys(keyword)

        # click to the detailed search box
        detailed_search_form = driver.find_element(By.ID, 'aramaForm:detayliAramaLabel')
        detailed_search_form.click()

        time.sleep(1)
        # click to the year box
        year_input = driver.find_element(By.ID, 'aramaForm:karaYilInput')

        # write down the year
        year_input.send_keys(year)
        driver.find_element_by_xpath("//body").click()
        time.sleep(1)

        # write down year range
        year_input = driver.find_element(By.ID, 'aramaForm:ilkKararNoInput')
        year_input.send_keys(init_no)
        driver.find_element(By.XPATH, "//body").click()
        time.sleep(1)

        year_input = driver.find_element(By.ID, 'aramaForm:sonKararNoInput')
        year_input.send_keys(last_no)
        time.sleep(1)

        # click to sort by decision number
        driver.find_element(By.XPATH, '//*[@id="aramaForm:siralamaKriteri"]/tbody/tr/td[2]').click()

        # wait for user to enter captcha
        time.sleep(10)

        # click to the search button
        search_btn = driver.find_element(By.ID, 'aramaForm:aramaButonu')
        search_btn.click()

        # wait for website to fetch results
        time.sleep(3)

        # parse html code of the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # get number of text
        num = int(soup.get_text().split(" Adet Karardan")[0].split(" ")[-1])

        # click to details button
        show_btn = driver.find_element(By.ID, 'aramaForm:sonucTable:0:rowbtn')
        show_btn.click()

        # wait for website to fetch result
        time.sleep(3)

        for i in range(num):

            if i % 30 == 0 and i != 0:
                time.sleep(60)

            # parse html code of the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # add new line for every <br>
            for elem in soup.find_all(["br"]):
                elem.append('\n')

            # remove redundant text
            text = re.sub('[\n]+', '\n', soup.get_text())
            text = \
                re.sub(' +', ' ', text).split("PDF Olarak Kaydet...Karar İçeriği")[1].replace("\xa0", "").split(
                    ">>Sonraki>>")[
                    0].replace('Metni"', 'Metni"\n')

            # determine file name as decision number
            file_name = text.split("\n")[0].replace("/", "_")

            if path.exists(file_name):
                buff = 1
                while True:
                    file_name = "{0}_{2}{1}".format(*path.splitext(file_name) + (buff,))
                    if path.exists(file_name):
                        buff += 1
                    else:
                        break

            # create file and write text
            # print(file_name)
            # comma_split = file_name.split(",")

            get_decisions.last_no_static = file_name.split(",")[1].split("_")[1].split(" ")[0]
            # raise ValueError("some stuff");
            file = open(file_name + ".txt", "w")
            file.write(text)
            file.close()

            if i != num - 1:
                # go to next decision
                time.sleep(3)
                next_btn = driver.find_element(By.ID, 'aramaForm:sonrakiEvrakLabel')
                next_btn.click()

        print(file_name)
    except Exception as e:
        print(str(e))
        raise ValueError(get_decisions.last_no_static)