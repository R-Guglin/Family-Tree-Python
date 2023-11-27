import json
from datetime import datetime
import os

class Name:
    def __init__(self, first = "", middle = "", last = "", suffix = ""):
        self.first = first
        self.middle = middle
        self.last = last
        self.suffix = suffix

    @classmethod
    def fromData(cls, data):
        return Name(data[0], data[1], data[2], data[3])
    
    def __repr__(self) -> str:

        if self.first == self.middle == self.last == self.suffix:
            return "No Name"        
        out = ""
        if self.first != "":
            out += self.first        
        if self.middle != "":
            out += " " + self.middle       
        if self.last != "":
            out += " " + self.last
        if self.suffix != "":
            out += " " + self.suffix
        return out
    
    def asList(self):
        return [self.first, self.middle, self.last, self.suffix]
    
    def asFileName(self):
        if self.first == self.middle == self.last == self.suffix:
            return "No_Name.json"
        else:
            return self.first[0] + "_" + self.last + ".json"
        
    def equals(self, first, middle = None, last = None, suffix = None):
        if first == self.first:
            if middle:
                if middle != self.middle:
                    return False 
                if last:
                    if last != self.last:
                        return False
                    if suffix:
                        if suffix != self.suffix:
                            return False 
            return True
     
class Date:
    def __init__(self, day = 1, month = 1, year = 1):
        self.day = self.month = self.year = 1

        if day == "" and int(day) in range(1,32):
            self.day = int(day)

        if month != "" and int(month) in range(1,13):
            self.month = int(month)

        if year != "" and int(year) > 0:
            self.year = int(year)

    @classmethod
    def fromData(cls, data):
        return Date(data[0], data[1], data[2])

    def __repr__(self) -> str:
        months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
        return (months[self.month - 1] + " " + str(self.day) + ", " + str(self.year))
    
    def asList(self):
        return [self.day, self.month, self.year]

class Person:
    def __init__(self, 
                 name = Name(), 
                 gender = "",
                 bday = Date(),
                 parent = None):
        self.name = name
        self.gender = gender
        self.bday = bday
        self.spouse = None
        self.parent = parent
        self.children = []
        self.generation = 0
        self.file = ""

        if parent:
            parent.setChild(self)

    def setChild(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parent = self
            child.updateGen(self.generation)
    
    def updateGen(self, gen):
        self.generation = gen + 1
        for i in range(len(self.children)):
            self.children[i].updateGen(self.generation)

    @classmethod
    def fromData(cls, data):
        name = Name.fromData(data["name"])
        gender = data["gender"]
        bday = Date.fromData(data["bday"])

        newP = Person(name, gender, bday)
        newP.spouse = data["spouse"]

        children = data["children"]
        if len(children) != 0:
            for i in range(len(children)):
                if type(children[i]) == dict:
                    newP.setChild(Person.fromData(children[i]))
                elif type(children[i]) == str:
                    newP.setChild(Person.fromFile(children[i]))
        
        return newP

    @classmethod
    def fromFile(cls, filename):
        with open(filename, "r") as rf:
            data = json.load(rf)
        newP = Person.fromData(data)
        newP.file = filename
        return newP
    
    @classmethod
    def fromUser(cls):
        first = input("Name:\n\tFirst: ")
        middle = input("\tMiddle: ")
        last = input("\tLast: ")
        suffix = input("\tSuffix: ")
        name = Name(first, middle, last, suffix)

        day = input("Birthday:\n\tDay: ")
        month = input("\tMonth: ")
        year = input("\tYear: ")
        bday = Date(day, month, year)

        gender = input("Gender (M/F/custom list): ")
        newP = Person(name, gender, bday)

        spouse = None
        if input("Does " + first + " have a spouse? (Y/N) ") in ["y","Y"]:
            spouse = input("\tSpouse's name: ")
        newP.spouse = spouse

        ccount = int(input("How many children does " + first + " have? "))
        if ccount > 0:
            for i in range(ccount):
                print(first + ": Child " + str(i+1))
                newChild = Person.fromUser()
                newP.setChild(newChild)
        
        return newP
    
    def save(self, filename = None):
        if not filename:
            #figure out how to get the current directory, because this is not it
            path = ""
            filename = path + self.name.asFileName()
        data = self.getData()
        self.file = filename
        with open(filename, "w") as wf:
            json.dump(data, wf, indent=4)
        return filename

    def getData(self):
        data = {"name": self.name.asList(),
                "gender": self.gender,
                "bday": self.bday.asList(),
                "spouse": self.spouse}
        data["children"] = []
        for i in range(len(self.children)):
            child = self.children[i]
            if child.file != "":
                data["children"].append(child.file)
            else:
                data["children"].append(child.getData())
        return data
    
    def getAge(self):
        today = datetime.now()
        dif = today.year - self.bday.year
        if today.month < self.bday.month or (today.month == self.bday.month and today.day < self.bday.day):
            dif -= 1
        return dif
    
    def isDescendant(self, personB):
        if self == personB:
            return True
        else:
            if self.parent:
                return self.parent.isDescendant(personB)
        return False
    
    def distanceFrom(self, personB, count = 0):
        if self.isDescendant(personB):
            if self == personB:
                return count
            else:
                count += 1
                if self.parent:
                    return self.parent.distanceFrom(personB, count)
        return -99
    
    def __repr__(self):
        return str(self.name) + " (Age " + str(self.getAge()) + ")"
