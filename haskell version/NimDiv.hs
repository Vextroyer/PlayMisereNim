import Data.Bits (xor)
import Data.List (find)
import Data.Maybe (fromMaybe)

-- Función auxiliar: devuelve los divisores de un número
divisors :: Int -> [Int]
divisors x = [d | d <- [1..x], x `mod` d == 0]

-- Función `get(x)`: asigna un valor de Grundy basado en la estrategia del juego
get :: Int -> Int
get 1 = 1
get x
    | x `mod` 2 == 0 = 0  -- Si el menor factor primo es 2, retorna 0
    | otherwise = x  -- En esta versión, usamos `x` directamente para simplificar

-- Calcula el Nim-Sum (XOR de todos los valores `get(x)`)
nimSum :: [Int] -> Int
nimSum xs = foldl xor 0 (map get xs)

-- Encuentra un movimiento óptimo si es posible
optimalMove :: [Int] -> Maybe [Int]
optimalMove xs =
    let currentNimSum = nimSum xs
    in findMove xs currentNimSum

-- Encuentra una pila donde quitar `d` piedras genera un Nim-Sum de 0
findMove :: [Int] -> Int -> Maybe [Int]
findMove [] _ = Nothing
findMove (x:xs) nim =
    let gx = get x  -- Grundy number de x
        target = gx `xor` nim  -- Queremos que gx ⊕ nim sea 0
        validMoves = [d | d <- divisors x, get (x - d) == target] -- Buscar `d` válido
    in case validMoves of
        (d:_) -> Just ((x - d) : xs)  -- Modificar la pila y devolver la nueva lista
        [] -> (x :) <$> findMove xs nim  -- Intentar en la siguiente pila

-- Si no hay movimiento óptimo, realizamos cualquier movimiento válido
randomMove :: [Int] -> [Int]
randomMove (x:xs) =
    let d = head (divisors x)  -- Tomamos el primer divisor posible
    in (x - d) : xs
randomMove [] = []  -- No debería pasar, pero por seguridad

-- Función principal que realiza un movimiento en el juego
makeMove :: [Int] -> [Int]
makeMove xs = fromMaybe (randomMove xs) (optimalMove xs)


