from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from itertools import chain
from collections import OrderedDict
from defs import *
import time
import datetime
import re


ROWS = 5
COLUMNS = 7



def extract_info(inp):
    result = []
    for member in inp:
        pattern = re.compile(r'行事曆： \s*(?P<course>.*?)\s*標題：\s*(?P<assignment>.*)')
        match = pattern.search(member)
        if match:
            course = match.group('course')
            assignment = match.group('assignment')
            result.append((course, assignment))
        else:
            pass
    return result


def process_data(soup):
    all_data = [[[] for _ in range(7)] for _ in range(5)]
    for i, div in enumerate(soup):
        available_blocks = [1] * COLUMNS
        trs = div.find('tbody').findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            _index = 0
            for j, block in enumerate(available_blocks):
                if block:
                    td = tds[_index]
                    if td.getText():
                        all_data[i][j].append(td.getText())
                    if td.get('rowspan', 0):
                        available_blocks[j] = 0 
                    _index += 1
    return all_data


def get_date(soup):
    iso_date = soup[0].find('td')['data-date']
    start_date = datetime.datetime(*(int(i) for i in iso_date.split('-')))
    return start_date


def main() -> "OrderedDict[str, list[tuple[str, str]]]":
    options = Options()
    options.add_argument("--disable-notifications")
    
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get('https://adfs.ntu.edu.tw/adfs/ls/?SAMLRequest=fVJNj9owEL33V0S%2B53OBJRYgUVBVpG0bQdpDL5VxJruWHDv1TAr993UCbHPY5WR55r15M29mgaLRLV939GL28LsDpODcaIN8SCxZ5wy3AhVyIxpATpIf1l%2BeeBYlvHWWrLSajSj3GQIRHClrWLDbLtkvmEH6ME1mYT0Rs3AijiIU2XEaZtM6n0%2Fmj3mSP7LgBzj0nCXzJTwRsYOdQRKGfCjJHsI0DZO8TGd8kvNk%2FpMFWz%2BHMoIG1gtRizyORVVjZKiLoOoiOg3%2FWGPMgvWtrY012DXgDuD%2BKAnf90%2F%2F6dJaPaZr%2B6xM3M%2FMguLqxEdlKmWe75twvICQfy7LIiy%2BHUq2WvR1%2BDCaW%2FWKbwj2kGwRj5GLy%2Fq%2Beo3dtrBayb%2FBJ%2BsaQe%2B3kEbpEFFVWA9Q3hlsQapaQeW90NqeNg4EwZKR64DFN5nrgUA1nIv3iuBMwcY2rXAKe6vhLCTdphmjNtqvfg%2F16u51SC57nA8X%2FjlZV%2FXGgvSSpRO%2BS%2BvoasCbxS%2B5dxp9zY6PffXhHw%3D%3D&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=L%2FLD4Z%2F6i%2FwOV6KvgHDtugZeM7%2FyGhplaLFKsvG9Mfvmq5icNJTtMAnEV3GRlnv5F2WFrtk3kKWNqTPBN37IgRwX075HfY2gSdrQOd1fXo8JWV7AA0ValWG3V%2BHfwt%2BtatNSqWQjM8PmpkzckA1SKxIR8Mui80IljxpYdydmwBhaESla%2FrqfPcdMaa7x7w0NUHfqOTl0acxIMGTfYRYbQ4WjyCyQoFZs13LWpG8By2AXOoMRTsM4xQ3UCIrQ%2Fv98i9IuaXpD%2BF7Exnh%2B%2FstsgiP6YoF7onUHBtjMySS3BvSLvk8y45PV5r2U1c8HbtBxS4egJNRKIJMI4kUQRe%2FHWA%3D%3D')

    username = chrome.find_element(By.ID, "ContentPlaceHolder1_UsernameTextBox")
    password = chrome.find_element(By.ID, "ContentPlaceHolder1_PasswordTextBox")
    button   = chrome.find_element(By.ID, "ContentPlaceHolder1_SubmitButton")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    button.click()

    chrome.get(f'https://cool.ntu.edu.tw/calendar#view_name=month&view_start={datetime.date.today()}')
    time.sleep(1)


    # --- Crawling Starts --- #
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    soup = soup.find('div', class_='fc-view fc-month-view fc-basic-view')
    soup = soup.findAll('div', class_='fc-content-skeleton') # type: ignore
    
    all_data, start_date = process_data(soup), get_date(soup)
    
    output = OrderedDict()
    for i, data in enumerate(list(chain(*all_data))):
        if data:
            new_date = str(start_date + datetime.timedelta(days=i)).split(' ')[0]
            output.update({new_date: extract_info(data)})
    return output


if __name__ == '__main__':
    print(main())


