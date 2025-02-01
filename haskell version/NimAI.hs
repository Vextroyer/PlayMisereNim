module Main where
import System.Environment (getArgs)

-- Función que convierte un número entero en una representación binaria como lista de Booleanos.
bin :: Int -> [Bool]
bin x   
    | x == 0 = [False] -- La representación binaria de 0 es una lista con un único valor 'False'
    | even x = bin (div x 2) ++ [False] -- Si x es par, se divide entre 2 y se añade 'False'
    | otherwise = bin (div x 2) ++ [True] -- Si x es impar, se divide entre 2 y se añade 'True'

-- Convierte una lista de enteros en una lista de representaciones binarias (en forma de listas de Booleanos).
bins :: [Int] -> [[Bool]]        
bins xs = map (reverse . bin) xs -- Se utiliza 'map' para aplicar 'bin' a cada elemento y luego se revierte la lista.

-- Función que realiza la operación XOR entre dos listas de Booleanos.
xor :: [Bool] -> [Bool] -> [Bool]
xor [] xs = xs -- Si la primera lista está vacía, devuelve la segunda.
xor xs [] = xs -- Si la segunda lista está vacía, devuelve la primera.
xor (x:xs) (y:ys) 
    | (x && y) || (not x && not y) = False : (xor xs ys) -- Si ambos son iguales, se añade 'False'.
    | otherwise = True : xor xs ys -- Si son diferentes, se añade 'True' y se sigue recursivamente.

-- Función que aplica XOR sobre todas las listas de Booleanos en una lista de listas.
xorList :: [[Bool]] -> [Bool]   
xorList xs = reverse (foldr xor [] xs) -- Se usa 'foldr' para acumular el resultado y se invierte el resultado final.

-- Función que convierte una lista de Booleanos en un número entero.
toInt :: [Bool] -> Int
toInt [] = 0 -- Si la lista está vacía, el resultado es 0.
toInt (x:xs) 
    | x = 2 ^ (length xs) + toInt xs -- Si el primer elemento es 'True', suma 2 elevado a la longitud restante.
    | otherwise = toInt xs -- Si es 'False', continúa con la conversión de la cola.

-- Función principal que calcula el XOR de una lista de enteros.
calculate_xor :: [Int] -> Int
calculate_xor [] = 0 -- Si la lista está vacía, el resultado es 0.
calculate_xor xs = toInt . xorList . bins $ xs -- Aplica las funciones para obtener el resultado.

-- Función que determina si hay un movimiento válido posible dando una cantidad.
canMove :: [Int] -> Int -> Bool
canMove [] _ = False -- Si la lista está vacía, no hay movimientos posibles.
canMove (x:xs) n 
    | x >= n = True -- Si hay una pila que es lo suficientemente grande, se puede mover.
    | otherwise = canMove xs n -- Continúa verificando las siguientes pilas.

-- Función que realiza un movimiento válido de las pilas, retornando las nuevas pilas.
goodMove :: [Int] -> Int -> [Int]   
goodMove (x:xs) n 
    | x < n = x : goodMove xs n -- Si la pilas son menores que n, se mantienen sin cambios.
    | otherwise = (x - n) : xs -- Si es lo suficientemente grande, se reduce.

-- Función que realiza un movimiento no válido de las pilas (puede llevar a una pérdida).
badMove :: [Int] -> Int -> [Int]   
badMove (x:xs) n 
    | x < n = x : badMove xs n -- Similar a goodMove, pero mantiene las pilas que son menores que n.
    | otherwise = (x - n) : xs -- Si se puede mover, aplica la reducción.

-- Función que simula un movimiento de la máquina.
maquinaMove :: [Int] -> [Int]
maquinaMove [] = [] -- Si no hay pilas, no hay movimiento.
maquinaMove xs = let y = max (calculate_xor xs) 1 in move xs y -- Calcula el XOR y luego intenta el movimiento correspondiente.
    where 
        move xs y 
            | canMove xs y = goodMove xs y -- Si se puede mover, espacio de buenas jugadas.
            | otherwise = badMove xs (2 ^ ((length . bin) y - 2)) -- Si no, realiza un movimiento malo.


-- Función principal del programa que procesa la entrada del usuario y muestra el resultado.
main :: IO ()
main = do
  args <- getArgs
  let piles = map read args :: [Int]
  let newPiles = maquinaMove piles
  putStrLn $ unwords $ map show newPiles
