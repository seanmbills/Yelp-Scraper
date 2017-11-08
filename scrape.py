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
        
        self.pricePrompt = tk.Label(self, text = "Choose a Maximum Price: ", anchor = "center")

        self.starPrompt = tk.Label(self, text = "Choose a Minimum Rating: ", anchor = "center")

        # create a stringvar to contain the text that gets put in the output text box
        self.v = tk.StringVar()

        # create a stringvar to hold the different price options
        self.priceVariable = tk.StringVar()
        # create a dropdown menu to allow a user to select the price range they want to limit their search to
        self.priceOption = tk.OptionMenu(self, self.priceVariable, "$", "$$", "$$$", "$$$$")
        self.priceOption.configure(width=10)

        # dropdown menu to allow user to select number of stars they want
        # to limit their search to
        self.starVariable = tk.StringVar()
        self.starOption = tk.OptionMenu(self, self.starVariable, u"\u2605", u"\u2605"u"\u2605", u"\u2605"u"\u2605"u"\u2605", u"\u2605"u"\u2605"u"\u2605"u"\u2605", u"\u2605"u"\u2605"u"\u2605"u"\u2605"u"\u2605")
        self.starOption.configure(width=10)
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
        self.pricePrompt.pack(side="top")
        self.priceOption.pack(side="top")
        self.starPrompt.pack(side="top")
        self.starOption.pack(side="top")
        self.outputText.pack(side="top", fill="x", expand=True)
        self.submitButton.pack(side="top")
        self.clearButton.pack(side="top")
        #self.scroller.pack(side="right")


    def calculate(self):
        result = ""
        location = ""
        search = ""
        price = ""
        rating = ""

        if not self.searchEntry.get():
            result += "Please Enter a Search Query"
            self.setText(result)
        else:
            # result += self.searchEntry.get()
            search = self.searchEntry.get()
        if not self.locationEntry.get():
            result += "\nPlease Enter a Location to Search"
            self.setText(result)
        else:
            if self.locationEntry.get().find(",") == -1:
                result += "\nPlease Enter a Valid City, State Location"
                self.setText(result)
            else:
                result += self.locationEntry.get()
                location = self.locationEntry.get()
        if self.priceVariable.get() == "":
            result += "\nPlease choose a maximum price range"
            self.setText(result)
        else:
            price = self.priceVariable.get()
        if self.starVariable.get() == "":
            result += "\nPlease choose a minimum rating"
            self.setText(result)
        else:
            rating = self.starVariable.get()
            # print(rating)
        if not location == "" and not search == "" and not price == "" and not rating == "":
            self.setText("")
            self.search(search, location, price, rating)

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
        self.priceVariable.set("")
        self.starVariable.set("")

    def search(self, searchQuery, locationQuery, price, rating):
        search = searchQuery
        location = locationQuery

        query = 'https://www.yelp.com/search?find_desc='+search+'&find_loc='+location+'&start='+str(0)

        response = requests.get(query)
        print(response)
        html = response.content
        print(html)
        
        updated_location = ", ".join(w.capitalize() for w in location.split(", "))
        print(updated_location)
        if updated_location.find(",") != -1:
            city_name = updated_location[:updated_location.find(",")]
            state_name = updated_location[updated_location.find(",") + 2:]
        else:
            city_name = updated_location #[:updated_location.find(",")]
            print(self.checkStates(city_name))

        ## convert price $$$ numbers into actual numbers for comparison below  
        # print(price)      
        price_comparator = self.calculatePrice(price)


        soup = BeautifulSoup(html)
        

        total_results = soup.find('span', attrs={'class': 'pagination-results-window'}).text
        index_results = total_results.find("of")
        num_results = int(total_results[index_results + 3:])

        pagination_pages = soup.find('div', attrs={'class': 'page-of-pages arrange_unit arrange_unit--fill'}).text
        index_of = pagination_pages.find("of")
        num_pages = int(pagination_pages[index_of + 3:])
        # print(num_pages)

        counter = num_pages

        outString = ""

        numResults = 0

        write_file = open('query_results.html', 'w')

        locationList = {}

        for i in range(counter):
            query = 'https://www.yelp.com/search?find_desc='+search+'&find_loc='+location+'&start='+str(i)

            response = requests.get(query)
            html = response.content

            soup = BeautifulSoup(html)

            list = soup.findAll('li', attrs={'class': 'regular-search-result'})
            
            if len(list) != 0 and list is not None:
                for item in list:
                    name = item.find('a', attrs={'class': 'biz-name js-analytics-click'})
                    if name is not None:
                        name = name.text
                    address = item.find('address')
                    if address is not None:
                        address = address.text
                    number = item.find('span', attrs={'class': 'biz-phone'})
                    if number is not None:
                        number = number.text
                    currPrice = item.find('span', attrs={'class': 'business-attribute price-range'})
                    if currPrice is not None:
                        currPrice = currPrice.text
                    
                    currRating = item.find('img', attrs={'class': 'offscreen'})

                    ratingNumber = 0
                    if currRating is not None:
                        currRating = currRating['alt']
                        currRating = currRating.encode('ascii')
                        index_decimal = currRating.find(".")
                        ratingNumber = float(currRating[index_decimal - 1 : index_decimal + 2])

                    rating_comparator = self.compareRatings(rating, ratingNumber)

                    currentIterationPrice = self.calculatePrice(currPrice)
                    
                    if name is not None and address is not None and number is not None and currPrice is not None and currentIterationPrice <= price_comparator and currRating is not None and rating_comparator is True:
                        city_name_location = address.find(city_name)

                        locationList[name].append([(address, number, currPrice, ratingNumber)])

                        address = address[:city_name_location] + "\n\t\t\t\t " + address[city_name_location:]
                        outString += "Name: " + name.replace("amp;", "") + "\n\t\t\tAddress: " + address + "\n\t\t\tPhone Number: " + number + "\n"
                        outString = outString.replace("&amp;", "&")
                        write_file.write("Name: " + name.replace(u"\u2019", "'").replace("amp;", "&").replace(u"\u2018", "'") + "</br>" + "Address: "
                            + address.replace(u"\u2019", "'").replace(u"\u2018", "'") + "</br>" + "Phone Number: "
                            + number.replace(u"\u2019", "'").replace(u"\u2018", "'") + "</br>")

                        numResults += 1
            


        write_file.close()
        totalPlace = 0
        for name in locationList:
            print(name)
            for locations in locationList[name]:
                print(locations)
                totalPlace += 1
        print("Location list size: " + str(totalPlace))
        # print("Output: " + outString)

        # print("Total Results: " + str(total_results))

        self.setText(outString)
        # write th results to the output text location on the frame as well
        self.outputText.insert('end', self.v.get())

    def compareRatings(self, baseRating, currentRating):
        minRating = 0.0
        if baseRating == u"\u2605":
            minRating = 1.0
        elif baseRating == u"\u2605"u"\u2605":
            minRating = 2.0
        elif baseRating == u"\u2605"u"\u2605"u"\u2605":
            minRating = 3.0
        elif baseRating == u"\u2605"u"\u2605"u"\u2605"u"\u2605":
            minRating = 4.0
        elif baseRating == u"\u2605"u"\u2605"u"\u2605"u"\u2605"u"\u2605":
            minRating = 5.0

        if currentRating >= minRating:
            return True
        else:
            return False

    def checkStates(self, location):
        state_names = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        if location in state_names:
            return True
        else:
            return False

    def calculatePrice(self, price):
        if price == "$":
            return 1
        elif price == "$$":
            return 2
        elif price == "$$$":
            return 3
        elif price == "$$$$":
            return 4


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, 0))



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Yelp Search")
    Window(root).pack(fill="both", expand = True)
    root.geometry('{}x{}'.format(800, 650))
    center(root)
    root.mainloop()
