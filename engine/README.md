# Engine
The script NimAI.hs is the engine that plays the nim game. It plays the standard version of the nim game.
It expects as command line arguments an array of integers which represents the instance of the nim game.
It outputs the new instance of the nim game after making a move.

# Installation :
The NimAI.hs script can be compiled with GHC(Glasgow Haskell Compiler) to produce a binary executable.
On CLI use, after proper setup of Glasgow Haskell Compiler:
`ghc NimAI.hs -o engine.exe` on Windows

# Usage :
Assumning you named the binary `engine.exe`.
Suppose your nim instance is `[12 0 1 4 29]`
Do:
`engine.exe 12 0 1 4 29`
The result should be the following:
`12 0 1 4 9`

To use the binary from other processes pass the nim instance as arguments to the binary as in the
example above.