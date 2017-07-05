import requests
from BeautifulSoup import BeautifulSoup
import lxml.html
import urllib
import os
import Tkinter as tk

class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # create a textbox prompt that allows a user to enter in the type of business they
        #       want to search for
        self.searchPrompt = tk.Label(self, text = "Enter your Search Query: ", anchor = "center")
        self.searchEntry = tk.Entry(self)
        # create textbox prompt that allows a user to enter in the location they want to query
        #       in (city, city/state, country)
        self.locationPrompt = tk.Label(self, text = "Enter the Location for your Search: ", anchor = "center")
        self.locationEntry = tk.Entry(self)
        # create the button that a user clicks on to search for their result
        self.submitButton = tk.Button(self, text = "SEARCH", command = self.calculate)

        self.v = tk.StringVar()
        # creates the field to ouput the text of the search results to
        self.outputText = tk.Text(self)
        self.outputText.config(state='disabled')
        # creates a button to clear the entry fields
        self.clearButton = tk.Button(self, text = "CLEAR", command = self.clear)

        #self.scroller = tk.Scrollbar(self, command=self.outputText.yview)

        self.searchPrompt.pack(side="top", fill="x")
        self.searchEntry.pack(side="top", fill="x", padx=20)
        self.locationPrompt.pack(side="top", fill="x")
        self.locationEntry.pack(side="top", fill="x", padx=20)
        self.outputText.pack(side="top", fill="x", expand=True)
        self.submitButton.pack(side="top")
        self.clearButton.pack(side="top")
        #self.scroller.pack(side="right")


    def calculate(self):
        result = ""
        location = ""
        search = ""
        counter = 0
        if not self.searchEntry.get():
            result += "Please Enter a Search Query"
            self.setText(result)
        else:
            result += self.searchEntry.get()
            search = self.searchEntry.get()
        if not self.locationEntry.get():
            result += "\nPlease Enter a Location to Search"
            self.setText(result)
        else:
            result += self.locationEntry.get()
            location = self.locationEntry.get()
        if not location == "" and not search == "":
            self.setText("")
            self.search(search, location, counter)

    def setText(self, word):
        self.outputText.configure(state='normal')
        self.outputText.delete('1.0', tk.END)
        self.v.set("")
        self.v.set(word)
        self.outputText.insert('1.0', self.v.get())
        self.outputText.configure(state='disabled')

    def clear(self):
        self.locationEntry.delete(0, tk.END)
        self.searchEntry.delete(0, tk.END)
        self.setText("")

    def search(self, searchQuery, locationQuery, counter):
        search = searchQuery
        location = locationQuery

        query = 'https://www.yelp.com/search?find_desc='+search+'&find_loc='+location+'&start='+str(counter)

        response = requests.get(query)
        html = response.content
        # tree = lxml.html.fromstring(html)
        # results = tree.xpath("//span[@class='indexed-biz-name']/a[@class='biz-name']/@href")

        # for result in results:
        #     print url + result

        soup = BeautifulSoup(html)
        # list = soup.findAll('a', attrs={'class': 'biz-name js-analytics-click'})
        list = soup.findAll('li', attrs={'class': 'regular-search-result'})
        write_file = open('query_results.html', 'w')

        # for item in list:
        #     address = item.find('address')
        #     print address
        outString = ""
        for item in list:
            name = item.find('a', attrs={'class': 'biz-name js-analytics-click'}).text
            address = item.find('address').text
            number = item.find('span', attrs={'class': 'biz-phone'}).text
            outString += "Name: " + name + "\n\t\t\tAddress: " + address + "\n\t\t\tPhone Number: " + number + "\n"
            # print(outString)
            write_file.write("Name: " + name.replace(u"\u2019", "'").replace("amp;", "&").replace(u"\u2018", "'") + "</br>" + "Address: "
                + address.replace(u"\u2019", "'").replace(u"\u2018", "'") + "</br>" + "Phone Number: " + number.replace(u"\u2019", "'").replace(u"\u2018", "'") + "</br>")
        write_file.close()

        print(outString)

        self.setText(outString)
        # write th results to the output text location on the frame as well
        self.outputText.insert('end', self.v.get())


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Yelp Search")
    Window(root).pack(fill="both", expand = True)
    root.geometry('{}x{}'.format(800, 600))
    center(root)
    root.mainloop()
