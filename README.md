# Family-Tree-Python
Python implementation of a single-parent family tree.
 **person.py:**
- An object of the class Person is initialized as the root of an empty tree.
- name is a list [First, Middle, Last]; birthdate is [Day, Month, Year] because that's how most of the world does it.
- gender is either "M" or "F" OR a list [Subject, Object, Possessive, [terms for relations]] if the person uses different pronouns. It is used to determine not only pronouns, but terms like "mother/father/parent", "sister/brother/sibling", etc. -- if no sufficient parameter is provided, the constructor defaults to:
  ["they", "them", "theirs", "parent", "child", "sibling", "parent's sibling", "sibling's child"].
- bio is an optional JSON with cool stuff like a biography and photo(s). There are several functions for adding bio stuff to a Person, all stored in bio.py (not included as of Nov 17, 2023) so that their heinous bulk doesn't clutter up and desecrate the class module.
- gen is the number of generations between this object and the root of the tree it's in; initialized to 0.
- If initialized with a parent and/or children, the constructor changes generations as needed, using updateGen().
- The Person may also be initialized from a source JSON file, which is described in more detail below.

Since all the parameters of __init__ are technically optional, we have the following default Person:
- Name: Empty string
- Pronouns: they/them/theirs
- Age: 2023 years old
- No parent
- No children
- No bio
- No source file

There is another constructor, class method fromFile(), which takes in a JSON file and creates one or many People as instructed... which is helpful when we want to store a family tree over time--there's also a saveToFile() method. This creates a JSON file describing THE TREE ROOTED AT THIS PERSON, not the whole family tree! The user is responsible for saving trees properly.
However, you can put JSONs in JSONs (in JSONs, in JSONs...) -- so I can save Mom.json and then include it later on in Grandma.json. Grandma's fromFile() constructor will then consider that Mom is now trapped in that awful JSON file, and it will build a nice Mom Person out of Mom.json, and add Mom to Grandma's children.

**The Family Tree Toolkit**
- person.py includes implementations of several functions that are used to navigate a family tree and provide information about individual members' relationships to each other. In particular, it has a function getRelation(person A, person B) which tells us _who person B is to person A_, not the other way around.
For example:
    - getRelation(me, Mom) = mother
    - getRelation(me, my grandma's daughter) = aunt
    - getRelation(my sister, my grandma's cousin's daughter) = second cousin once removed
    - getRelation(me, my brother's granddaughter's son) = great-grandnephew
 
**interface.py**
This contains some functions that can help build a user interface in order to make it easier to make and store family trees. Right now that's up to you--eventually I plan to add more functionality that will turn all of this into a single program in which the user can Click On Cool Buttons, instead of Typing Tedious Words.

