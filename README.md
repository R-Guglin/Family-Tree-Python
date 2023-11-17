# Family-Tree-Python
Python implementation of a single-parent family tree.
An object of the class Person is initialized as the root of an empty tree.
- name is a list [First, Middle, Last]; birthdate is [Day, Month, Year] because that's how most of the world does it.
- gender is either "M" or "F" OR a list [Subject, Object, Possessive, [terms for relations]] if the person uses different pronouns. It is used to determine not only pronouns, but terms like "mother/father/parent", "sister/brother/sibling", etc. -- if no sufficient parameter is provided, the constructor defaults to:
  ["they", "them", "theirs", "parent", "child", "sibling", "parent's sibling", "sibling's child"]
since there is no standardized gender-neutral term for parent's sibling and sibling's child, this default gender can cause a few weird strings to occur. When it tries to describe someone like your great-great-grandma's nonbinary sibling (good on them for living their truth in 1910!); it'll say "great-great-grandparent's sibling" which is normal enough. However, if your sister has a nonbinary great-grandchild, the program will describe that person as your "great-sibling's child" which is an issue I plan to fix as soon as I do enough research to decide which is the most appropriate and respectful term for such a person. (I have seen "nibling" used but I'm not convinced that is right.)
- bio is an optional JSON with cool stuff like a biography and photo(s).
... there are several functions for adding bio stuff to a Person, all stored in bio.py (not included as of Nov 17, 2023) so that their heinous bulk doesn't clutter up and desecrate the class module.
- gen is the number of generations between this object and the root of the tree it's in; initialized to 0.
- If initialized with a parent and/or children, the constructor changes generations as needed, using updateGen().
- The Person may also be initialized from a source JSON file, which is described in more detail below, although this functionality is not working yet as of Nov 17, 2023 because it's also midterms week and this is a side project and I am learning all about JSONs and everything else from my own (impeccable) research skills, which means it will take some time for me to implement all that.

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
(As of Nov 17, 2023 the JSON implementation and bio.py are not complete.)

**The Family Tree Toolkit**
- person.py includes implementations of several functions that are used to navigate a family tree and provide information about individual members' relationships to each other. In particular, it has a function getRelation(person A, person B) which tells us _who person B is to person A_, not the other way around.
For example:
    getRelation(me, Mom) = mother
    getRelation(me, my grandma's daughter) = aunt
    getRelation(my sister, my grandma's cousin's daughter) = second cousin once removed

