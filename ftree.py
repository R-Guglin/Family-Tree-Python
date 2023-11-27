from person import *

class FTree:
    def __init__(self, root = Person()):
        self.root = root
        while root.generation != 0:
            root = root.parent
        self.people = self.addPeople(root)

    @classmethod
    def fromFile(cls, filename):
        return FTree(Person.fromFile(filename))

    def addPeople(self, root, people = {}):
        gen = root.generation
        if gen not in people.keys():
            people[gen] = [root]
        else:
            people[gen].append(root)
        for child in root.children:
            people = self.addPeople(child, people)
        return people
    
    def save(self, filename = None):
        return self.root.save(filename)
    
    def isInTree(self, person):
        for g in self.people.values():
            for p in g:
                if p == person:
                    return True
        return False

    def add(self, person, parent):
        if self.isInTree(parent):
            parent.setChild(person)
            self.addPeople(person, self.people)
        else:
            print("Parent not found.")
    
    def findByName(self, first, middle = None, last = None, suffix = None):
        for g in self.people.values():
            for p in g:
                if p.name.equals(first, middle, last, suffix):
                    return p
        return False
    
    # Takes a person and string which must match one of the possible relations (ex: "grandmother", "great-granduncle")
    # Returns a list of people who are the person's relatives of that type
    def relatives(self, person, type):
        rels = []
        for g in self.people.values():
            for p in g:
                if getRelation(person, p) == type:
                    rels.append(g)
    
# Family tree toolkit

def getLCA(A, B): 
    # Climbs up the tree until we find an ancestor shared by both people. A's generation must be younger than or equal to B's.
    if A.isDescendant(B):
        return B
    else:
        if B.parent:
            return getLCA(A, B.parent)
        else:
            return None
            
def getRelation(A, B):
    # Uses least common ancestor (LCA) to find out how two people are related.
    if B.generation <= A.generation:
        lca = getLCA(A, B)
    elif B.generation > A.generation:
        lca = getLCA(B, A)

    degree = min(A.distanceFrom(lca), B.distanceFrom(lca)) - 1
    removed = A.generation - B.generation

    return parseRelation(degree, removed, A, B)

def parseRelation(deg, rem, pA, pB):
    terms = parseGender(pB.gender)
    if deg == -1:
        if rem < 0: # descendant
            return ((abs(2 + min(rem, -2)) * "great-") + (min(1, abs(rem + 1)) * "grand") + terms[4])
        elif rem == 0:
            # you are your own "-1 cousin 0 times removed"
            return "self"
        elif rem > 0: # ancestor
            return ((abs(2 - max(rem, 2)) * "great-") + (min(1, abs(1 - rem)) * "grand") + terms[3])
        
    elif deg == 0:
        if rem < 0: # niece/nephew
            if terms[7] == "niece" or terms[7] == "nephew":
                return ((abs(2 + min(rem, -2)) * "great-") + (min(1, abs(rem + 1)) * "grand") + terms[7])
            else:
                return "sibling's " + parseRelation(-1, rem, Person(), pB)
        elif rem == 0: # sibling
            return (pA.birthdate == pB.birthdate) * "twin " + terms[5]
        elif rem > 0:
            return ((abs(2 - max(rem, 2)) * "great-") + (min(1, abs(1 - rem)) * "grand") + terms[6])
        
    elif deg > 0:
        nth = str(deg) + "th "
        times = " " + str(abs(rem)) + " times removed"

        if nth[-3] == "1":
            nth = str(deg) + "st "
        elif nth[-3] == "2":
            nth = str(deg) + "nd "
        elif nth[-3] == "3":
            nth == str(deg) + "rd "

        if rem == 0:
            times = ""
        if abs(rem) == 1:
            times = " once removed"
        elif abs(rem) == 2:
            times = " twice removed"
        elif abs(rem) == 3:
            times == " thrice removed"
        
        return nth + "cousin" + times

def parseGender(gender):
    # will accept properly-formatted custom pronoun lists
    if type(gender) == list and len(gender) == 8:
        return gender
    elif gender in ['M', 'm']:
        return ['he', 'him', 'his', 'father', 'son', 'brother', 'uncle', 'nephew']
    elif gender in ['F','f']:
        return ['she', 'her', 'hers', 'mother', 'daughter', 'sister', 'aunt', 'niece']
    else: 
        #default gender-neutral pronouns
        return ['they', 'them', 'theirs', 'parent', 'child', 'sibling', "parent's sibling", "sibling's child"]
