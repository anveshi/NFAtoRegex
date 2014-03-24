Ethan Clevenger

This program reads an NFA from a text file, formatted properly, and eliminates
states to form a regex representing the entire thing.

I was using Python 3.X. As of 3.0, print became a function (so print("My string")) 
and raw_input() became input(). If you're running Python 2.X, it won't compile. Edit
those functions accordingly.

Two test cases are included in this repo.

Any instance of the letter 'p' stands for "phi", the empty set (no transition exists)
'e' is an epsilon transition.

0s in the input files correspond to epsilon transitions.