from person import *

def isValid(date):
    if date[0] in range(1, 32) and date[1] in range(1,13) and date[2] >= 0:
        return True
    return False

def getNameTag(person, members):
    fname = person.name[0]
    if fname in members.keys():
        return input("This tree already contains a person with the first name "
                        + fname
                        + "--please enter an alternative nametag for your new person, so"+
                        "I can find them in the tree later. This won't change any information about the person."
                        + "(\nExamples: 'Jake2', 'JoshK') ")
    else:
        return fname

members = {}

def addPerson(person):
    members[getNameTag(person, members)] = person
    for c in person.children:
        addPerson(c)

def buildPerson(parent = None):
    if input("Is this person already in the tree? (Y/N) ") in ["Y", "y"]:
        if parent:
            nametag = input("Enter their first name or nametag: ")
            parent.setChild(members[nametag])
        else:
            print("Done")
        
    elif input("Is this person already stored in a JSON file? (Y/N) ") in ["Y", "y"]:
        newP = Person.fromFile(input("Enter the exact filename, including capitalization and the '.json': "))
        addPerson(newP)
        if parent:
            parent.setChild(newP)
        else:
            print("Done")

    else:
        name = ["","",""]
        gender = None
        bday = [1,1,1000]

        namestring = input("Enter name in this format: First Middle Last \n(if any part is unknown, type a single space instead): ")
        name = namestring.split(" ")

        gender = input("Enter gender (M/F) or custom list (see README): ")

        datestring = input("Enter birthdate in this format: DD/MM/YYYY\n(if any part is unknown, type a single space instead): ")
        bday = datestring.split("/")
        for i in range(len(bday)):
            if bday[i] == ' ':
                bday[i] = 1
            else:
                bday[i] = int(bday[i])
        while not isValid(bday):
            datestring = input("Invalid date. Enter the date in this format: DD/MM/YYYY\n(if any part is unknown, type a single space instead): ")
            bday = datestring.split("/")
            for i in range(len(bday)):
                if bday[i] == ' ':
                    bday[i] = 1
                else:
                    bday[i] = int(bday[i])

        person = Person(name, gender, bday)

        addPerson(person)
        if parent:
            parent.setChild(person)
