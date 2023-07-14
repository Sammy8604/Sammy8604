import requests
from bs4 import BeautifulSoup
import lxml
import os
import time

def sorter(list):
    sorted = False
    swaps = 0
    while sorted == False:
        swaps = 0
        for i in range(0, len(list) - 1):
            int1 = float((list[i][1][1:].replace(",", "")))
            int2 = float((list[i + 1][1][1:].replace(",", "")))
            if int1 > int2:
                temp = list[i]
                list[i] = list[i + 1]
                list[i + 1] = temp
                swaps += 1
        if swaps == 0:
            sorted = True
    return list


# deletes values which arent needed
def deleter(title, list):
    for i in range(0, len(list)):
        if list[i][0] == title:
            list.pop(i)
            return list
    return list


# returns the price
def getPrice(detail):
    price = ""
    num = 1
    for i in detail:
        if i != ".":
            num += 1
            price = price + str(i)
        else:
            price = price + "." + str(details[num:num + 2])
            break
    count = 0
    for i in range(0, len(price)):
        if price[i] != "£":
            count += 1
        else:
            price = price[count:]
            break
    return price


reset = '\033[0m'
magenta = "\033[0;35m"

list = []

logo = """⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣀⣀⣀⣀⠀⢸⣿⠀⣀⣀⣀⡀⠀⠀⠀⣀⣀⣀⣀⢀⣀⡀⠀⠀⠀⠀⣀⣀
⣰⡿⠋⠉⠉⠻⣷⣼⣿⡞⠉⠉⠉⢻⣦⡀⠿⠟⠉⠉⠻⣿⣿⣷⡀⠀⠀⣰⣿⠃
⣿⡷⠶⠶⠶⠶⠿⢿⣿⠀⠀⠀⠀⢨⣿⣧⣴⠶⠶⠶⠶⣿⡇⠹⣿⡀⣰⣿⠃⠀
⠹⣷⣄⣀⣀⣴⡶⢺⣿⣧⣀⣀⣠⣾⠟⠹⣷⣀⣀⣀⣴⣿⡇⠀⠹⣿⣿⠃⠀⠀
⠀⠀⠉⠉⠉⠁⠀⠈⠉⠀⠉⠉⠉⠁⠀⠀⠈⠉⠉⠉⠀⠉⠁⠀⣰⣿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀
"""

for i in logo:
    print(i, end="", flush=True)
    time.sleep(0.01)

item = str(input("Enter item to search for: "))
url = "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + item + "&_sacat=0"
next = True
page_number = 1

while next != False:
    list = []
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")

    divs = soup.find_all("div", class_="s-item__wrapper clearfix")
    for div in divs:
        title = div.find("div", class_="s-item__title").text
        if "New listing" in title:
            title = title[11:]
        details = div.find("div", class_="s-item__details clearfix").text
        price = getPrice(details)
        link = div.find("a", href=True)
        link = link["href"]
        list.append([title, price, link])

    list = sorter(list)
    list = deleter("Shop on eBay", list)
    for items in list:
        print(reset, "--------------------------------------")
        print("Title: " + items[0])
        print("Price: " + items[1])
        print("link:")
        print(magenta, items[2])

    print(reset, "")
    next_page = int(input("Enter 1 for next page or 2 to stop: "))
    if next_page == 1:
        next = True
        page_number += 1
        url = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=" + str(item) + "&_sacat=0&_pgn=" + str(page_number)
        os.system("cls")
    else:
        next = False

print("Thank you!")