class Business:
    def __init__(self, name, number, address, cityNameLocation, rating, price, latitude, longitude):
        self.name = name
        self.number = number
        self.address = address
        self.cityNameLocation = cityNameLocation
        self.rating = rating
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.cleanInformation()

    def coordinates(self):
        return (self.latitude, self.longitude)

    def reverseCoordinates(self):
        return (self.longitude, self.latitude)

    def geoInformation(self):
        return (self.name, self.coordinates)

    def cleanInformation(self):
        self.name = str(self.name.replace(u"\u2019", "'").replace("&amp;", "&").replace(u"\u2018", "'").replace("\n", "")).strip()
        self.address = str(self.address.replace(u"\u2019", "'").replace(u"\u2018", "'").replace("\n", "")).strip()
        self.number = str(self.number.replace(u"\u2019", "'").replace(u"\u2018", "'").replace("\n", "")).strip()

    def toString(self):
        address = self.address[:self.cityNameLocation] + "\n\t\t\t\t " + self.address[self.cityNameLocation:]
        return ("Name: " + self.name + "\n\t\t\tAddress: " + address + "\n\t\t\tPhone Number: " + self.number + "\n")
