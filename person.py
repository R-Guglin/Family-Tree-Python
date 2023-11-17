import json
from datetime import datetime

class Person:
    def __init__(self, 
                 name = ["","",""], 
                 gender = None,
                 birthdate = [1,1,1000],
                 parent = None):
        self.gen = 0
        self.name = name
        self.gender = parseGender(gender)
        self.birthdate = birthdate
        self.parent = parent
        self.children = []
        self.file = ""

        if parent != None:
            parent.setChild(self)

    def setChild(self, c):
        if c not in self.children:
            self.children.append(c)
            c.parent = self
            c.updateGen(self.gen)
            return True
        else:
            return False
        
    def setFile(self, filename):
        self.file = filename

    def updateGen(self, gen):
        assert gen >= 0 
        self.gen = gen + 1
        if len(self.children) > 0:
            for child in self.children:
                child.updateGen(self.gen)

    @classmethod
    def fromData(cls, data):
        # data must be a dict
        name = data["name"]
        gender = data["gender"]
        birthdate = data["birthdate"]

        newP = Person(name, gender, birthdate)

        children = data["children"]
        if children:
            for c in children.keys():
                if type(c) == str:
                    newChild = Person.fromData(json.loads(c))
                    newP.setChild(newChild)
                elif type(c) == dict:
                    newChild = Person.fromData(c)
                    newP.setChild(newChild)
    
        return newP


    @classmethod
    def fromFile(cls, filename):
        data = json.loads(filename)
        return Person.fromData(data)
    

    def saveToFile(self, filename = None):
        data = self.getData()
        if not filename:
            filename = self.name[0] + self.name[1][0] + self.name[2] + ".json"
        with open(filename, "w") as wf:
            json.dump(data, wf, indent=4)
        self.setFile(filename)

    def getData(self):
        data = {"name" : self.name,
                "gender": self.gender,
                "birthdate": self.birthdate}
        if len(self.children) > 0:
            data["children"] = {}
            for c in self.children:
                if c.file != "":
                    data["children"][c.name[0]] = c.file
                else:      
                    data["children"][c.name[0]] = c.getData()
        else:
            data["children"] = None
        return data
    
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
                out += self.name[i] + " "
        out += ("\nBorn " + parseDate(self.birthdate))
        out += (" (Aged " + str(self.getAge()) + ")")
        out += ("\nGeneration " + str(self.gen))
        if self.parent:
            out += "\nParent: " + self.parent.name[0] + " " + self.parent.name[2]
        if len(self.children) > 0:
            out += "\nChildren:\n"
            for child in self.children:
                out += "   " + child.name[0] + " " + child.name[2]+"\n"
        return out + "\n"

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

    if deg == -1:
        if rem < 0: # descendant
            return ((abs(2 + min(rem, -2)) * "great-") + (1 * "grand") + pB.gender[4])
        elif rem == 0:
            # you are your own "-1 cousin 0 times removed"
            return "self"
        elif rem > 0: # ancestor
            return ((abs(2 - max(rem, 2)) * "great-") + (1 * "grand") + pB.gender[3])
        
    elif deg == 0:
        if rem < 0: # niece/nephew
            return ((abs(2 + min(rem, -2)) * "great-") + (1 * "grand") + pB.gender[7])
        elif rem == 0: # sibling
            return (pA.birthdate == pB.birthdate) * "twin " + pB.gender[5]
        elif rem > 0:
            return ((abs(2 - max(rem, 2)) * "great-") + (1 * "grand") + pB.gender[6])
        
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



    
