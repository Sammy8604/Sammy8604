import requests
from bs4 import BeautifulSoup
import random
import customtkinter

letter_count = 1
link = "https://www.thesaurus.com/browse/"

def word_split(text):
    words = []
    temp = ""
    letter_count = 1
    for i in range(0, len(text)):
        if text[i] == " " or text[i] == "-":
            words.append(temp)
            temp = ""
        else:
            temp = temp + str(text[i])

        if letter_count == len(text):
            words.append(temp)
            temp = ""

        letter_count += 1
    return words

def get_words(list):
    global link
    synonyms = []
    for i in list:
        synonyms_each = []
        main = requests.get(link+i).text
        soup = BeautifulSoup(main, "lxml")
        red_tag = soup.find_all("button", class_="Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC fQdXDP6Pfndr85gESLI_")
        for x in red_tag:
            synonyms_each.append(x.text)

        if len(synonyms_each)>0:
            synonyms.append(synonyms_each)
        else:
            orange_tag = soup.find_all("button", class_="Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC DL3p3OH7u8i4dIoN1agF")
            for x in orange_tag:
                synonyms_each.append(x.text)
            if len(synonyms_each)>0:
                synonyms.append(synonyms_each)
            else:
                yellow_tag = soup.find_all("button", class_="Cil3vPqnHSU3LLCTZ62n Ip2xyQSEjrh_jZExawdC MjZsFvWY0uOO_JJhtba_")
                for x in orange_tag:
                    synonyms_each.append(x.text)
                if len(synonyms_each)>0:
                    synonyms.append(synonyms_each)
                else:
                    synonyms.append([str(i)+" "])
    return synonyms

def add_random():
    global label2
    text = text_box.get()
    seperated = word_split(text)
    synonyms = get_words(seperated)
    final = ""
    for i in synonyms:
        length = len(i)
        index = random.randint(0, length - 1)
        final = final + i[index] +" "
    print(final)
    label2.configure(text="Result: "+final)
    label2.update_idletasks()

customtkinter.set_appearance_mode("dark")
main = customtkinter.CTk()
main.geometry("500x300")
window = customtkinter.CTkFrame(master=main)
window.pack(padx=5,pady=10)
label = customtkinter.CTkLabel(master=window, text="Word Randomizer", font=("Times",55))
label.pack(pady=10)
text_box = customtkinter.CTkEntry(master=window, placeholder_text="Enter Words", width=150, height=40)
text_box.pack(pady=20)
button = customtkinter.CTkButton(master=window, text="Enter", command=add_random)
button.pack(pady=5)
label2 = customtkinter.CTkLabel(master = window, text="Result:")
label2.pack(pady=10)
main.mainloop()