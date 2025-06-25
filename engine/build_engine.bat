@echo off
set haskellCompiler=ghc
mkdir build
%haskellCompiler% -odir build -hidir build -o build\engine.exe NimAi.hs