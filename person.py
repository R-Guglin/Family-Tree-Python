import json
from datetime import datetime

class Person:
    def __init__(self, 
                 name = ["","",""], 
                 gender = None,
                 birthdate = [1,1,1],
                 parent = None):
        self.gen = 0
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        self.parent = parent
        self.children = []
        self.file = ""

        if parent != None:
            parent.setChild(self)

    @classmethod
    def fromData(cls, data):
        assert isinstance(data, dict)
        name = data["name"]
        gender = data["gender"]
        birthdate = data["birthdate"]

        newP = Person(name, gender, birthdate, None)

        children = data["children"]
        if children != 0:
            for i in range(0, len(children)):
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
        newP.setFile(filename)
        return newP

    def saveToFile(self, filename = None):
        data = self.getData()
        if not filename:
            filename = self.name[0] + "_" + self.name[2] + ".json" #ex: Rebecca_Guglin.json
        with open(filename, "w") as wf:
            json.dump(data, wf, indent=4)
        self.setFile(filename)

    def getData(self):
        data = {"name" : self.name,
                "gender": self.gender,
                "birthdate": self.birthdate}
        if len(self.children) > 0:
            data["children"] = [] #[child1 data or child1.json, child2 data or child2.json...]
            for c in self.children:
                if c.file == "":  
                    data["children"].append(c.getData())
                else: 
                    data["children"].append(c.file)
        else:
            data["children"] = 0
        return data

    def setName(self, n):
        self.name = n

    def setGender(self, g):
        self.gender = parseGender(g)

    def setBday(self, b):
        self.birthdate = b

    def setChild(self, c):
        if c not in self.children:
            self.children.append(c)
            c.parent = self
            c.updateGen(self.gen)
        
    def setFile(self, filename):
        self.file = filename

    def updateGen(self, gen):
        assert gen >= 0 
        self.gen = gen + 1
        if len(self.children) > 0:
            for child in self.children:
                child.updateGen(self.gen)
    
    def getAge(self):
        today = datetime.now()
        bday = self.birthdate 
        dif = today.year - bday[2] 
        if today.month < bday[1] or (today.month == bday and today.day_ < bday[0]):
            dif -= 1
        return dif   

    def __repr__(self):
        out = ""
        if self.name == ["","",""]:
            out += "No Name"
        else:
            for i in range(0,3):
                if self.name[i] == "":
                    pass
                else:
                    out += self.name[i] + " "
        out += ("(Age " + str(self.getAge()) + ")\n")
        return out

# Family tree toolkit

def isDescendant(A, B):
    # for debugging... take this shit out before publishing
    assert isinstance(A, Person) and isinstance(B, Person) 

    if A == B:
        return True
    else: 
        if A.parent:
            return isDescendant(A.parent, B)
    return False 
    
def distanceFrom(A, B, count=0):
    assert isinstance(A, Person) and isinstance(B, Person)

    # Returns the number of generations between a person and their ancestor.
    if not isDescendant(A, B):
        return -99 
    elif A == B:
            return count 
    else:
        count += 1
        if A.parent:
            return distanceFrom(A.parent, B, count)

def getLCA(A, B): 
    assert isinstance(A, Person) and isinstance(B, Person)

    # Climbs up the tree until we find an ancestor shared by both people. A's generation must be younger than or equal to B's.
    if isDescendant(B, A):
        return A 
    else:
        if A.parent:
            return getLCA(A.parent, B)
        else:
            return None
            
def getRelation(A, B):
    assert isinstance(A, Person) and isinstance(B, Person)

    # Uses least common ancestor (LCA) to find out how two people are related.
    if B.gen <= A.gen:
        lca = getLCA(A, B)
    elif B.gen > A.gen:
        lca = getLCA(B, A)

    degree = min(distanceFrom(A, lca), distanceFrom(B, lca)) - 1
    removed = A.gen - B.gen

    return parseRelation(degree, removed, A, B)

def parseRelation(deg, rem, pA, pB):
    gender = parseGender(pB.gender)
    if deg == -1:
        if rem < 0: # descendant
            return ((abs(2 + min(rem, -2)) * "great-") + (min(1, abs(rem + 1)) * "grand") + gender[4])
        elif rem == 0:
            # you are your own "-1 cousin 0 times removed"
            return "self"
        elif rem > 0: # ancestor
            return ((abs(2 - max(rem, 2)) * "great-") + (min(1, abs(1 - rem)) * "grand") + gender[3])
        
    elif deg == 0:
        if rem < 0: # niece/nephew
            if gender[7] == "niece" or gender[7] == "nephew":
                return ((abs(2 + min(rem, -2)) * "great-") + (min(1, abs(rem + 1)) * "grand") + gender[7])
            else:
                return "sibling's " + parseRelation(-1, rem, Person(), pB)
        elif rem == 0: # sibling
            return (pA.birthdate == pB.birthdate) * "twin " + gender[5]
        elif rem > 0:
            return ((abs(2 - max(rem, 2)) * "great-") + (min(1, abs(1 - rem)) * "grand") + gender[6])
        
    elif deg > 0:
        nth = str(deg) + "th"
        times = str(abs(rem)) + " times removed"

        if nth[-3] == "1":
            nth = "1st"
        elif nth[-3] == "2":
            nth = "2nd"
        elif nth[-3] == "3":
            nth == "3rd"

        if rem == 0:
            times = ""
        if rem == 1:
            times = " once removed"
        elif rem == 2:
            times = " twice removed"
        elif rem == 3:
            times == " thrice removed"
        

        return nth + " cousin " + times

def parseGender(gender):
    if isinstance(gender, tuple) and len(gender) == 8:
        return gender
    elif gender == 'M':
        return ['he', 'him', 'his', 'father', 'son', 'brother', 'uncle', 'nephew']
    elif gender == 'F':
        return ['she', 'her', 'hers', 'mother', 'daughter', 'sister', 'aunt', 'niece']
    else: 
        #default gender-neutral pronouns
        return ['they', 'them', 'theirs', 'parent', 'child', 'sibling', "parent's sibling", "sibling's child"]
    

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
    
def parseDate(date):
    day = date[0]
    month = date[1]
    year = date[2]
    assert day in range(1,32) and month in range(1,13) and year >= 1000
    return (months[month - 1] + " " + str(day) + ", " + str(year))

