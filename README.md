# Nim Game
NimGame is a prolog script that plays the misere variant of the nim game.

# The Game
The usual game of Nim consists of two players and some heaps of rocks. On each turn a player removes at least a rock from a heap.
On the normal nim game the player that removes the last rock wins. On the misere nim game the player that removes the last rock loses.

An instance of the nim game is considered a list $[x_1, x_2 ... , x_n]$. The players take alternate turns to play.
On each turn a player must reduce some $x_i$ by at least 1; if $x_i = 0$ then it cant be reduced. The player
that cant reduce any $x_i$ on its turn win, that is, the player that reaches $[0, 0 ... , 0]$ wins.

More about the nim game on wikipedia: https://en.wikipedia.org/wiki/Nim

# Usage
The nim.pl script provides a predicate `nim/3`: `nim(L,OLD,NEW)` to play the misere nim game.

L is intended to be a list representing the state of the game. It must not containt any 0.
OLD and NEW are values that the predicate uses to inform the move a player should take, that means
on current state L the element with value OLD should be changed to value NEW.

The predicate should be called with a list L and it will found the values of OLD and NEW if its possible
to win, or return false if its not.

Some examples:

        nim([1,14],O,N)       O = 14, N = 0
        nim([1],O,N)          false
        nim([1,1],O,N)        O = 1, N = 0

# Requirements
To execute the script you need to install a prolog interpreter, for example SWI-Prolog.

The latest stable version of SWI-Prolog can be found at https://www.swi-prolog.org/download/stable .
The script was tested using SWI-Prolog version 9.2.8 for x64-win64.

# Calling the script from the CLI
The script can be executed from the command line and called by external programs.

To call the script from the command line using SWI-Prolog use the following script:
    `swipl -s nim.pl -g nim([1,14],O,N),write(O),nl,write(N) -t halt`

You should substitute `[1,14]` for the instance you want to resolve. More on Usage.
