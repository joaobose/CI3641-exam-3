import Prelude hiding (foldr, takeWhile)

--- Parte a)

foldr :: (a -> b -> b) -> b -> [a] -> b
foldr _ e [] = e
foldr f e (x : xs) = f x $ foldr f e xs

takeWhile :: (a -> Bool) -> [a] -> [a]
takeWhile p = foldr (\a r -> if p a then a : r else []) []

gen :: Int -> [Int]
gen n = n : gen (n + 1)

{-

----------------------- Evaluacion normal parte a)

  takeWhile (<= 3) (gen 1)

-- Evaluamos takeWhile
= foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 1)

-- Evaluamos gen 1
= foldr (\a r -> if (<= 3) a then a : r else []) [] (1 : gen 2)

-- Evaluamos foldr
= (\a r -> if (<= 3) a then a : r else []) 1 $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 2)

-- Evaluamos (\a r -> if (<= 3) a then a : r else []) 1
= (\r -> if (<= 3) 1 then 1 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 2)

-- Evaluamos (<= 3) 1
= (\r -> if true then 1 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 2)

-- Evaluamos if true
= (\r -> 1 : r) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 2)

-- Evaluamos (\r -> 1 : r) lo que esta a la derecha del $
= 1 : foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 2)

-- Evaluamos gen 2
= 1 : foldr (\a r -> if (<= 3) a then a : r else []) [] (2 : gen 3)

-- Evaluamos foldr
= 1 : (\a r -> if (<= 3) a then a : r else []) 2 $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 3)

-- Evaluamos (\a r -> if (<= 3) a then a : r else []) 2
= 1 : (\r -> if (<= 3) 2 then 2 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 3)

-- Evealuamos (<= 3) 2
= 1 : (\r -> if true then 2 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 3)

-- Evaluamos if true
= 1 : (\r -> 2 : r) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 3)

-- Evaluamos (\r -> 2 : r) lo que esta a la izquierda del $
= 1 : 2 : foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 3)

-- Evaluamos gen 3
= 1 : 2 : foldr (\a r -> if (<= 3) a then a : r else []) [] (3 : gen 4)

-- Evaluamos foldr
= 1 : 2 : (\a r -> if (<= 3) a then a : r else []) 3 $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 4)

-- Evaluamos (\a r -> if (<= 3) a then a : r else []) 3
= 1 : 2 : (\r -> if (<= 3) 3 then 3 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 4)

-- Evaluamos (<= 3) 3
= 1 : 2 : (\r -> if true 3 then 3 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 4)

-- Evaluamos if true
= 1 : 2 : (\r -> 3 : r) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 4)

-- Evaluamos (\r -> 3 : r) lo que esta a la izquierda del $
= 1 : 2 : 3 : foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 4)

-- Evaluamos gen 4
= 1 : 2 : 3 : foldr (\a r -> if (<= 3) a then a : r else []) [] (4 : gen 5)

-- Evaluamos foldr
= 1 : 2 : 3 : (\a r -> if (<= 3) a then a : r else []) 4 $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 5)

-- Evaluamos (\a r -> if (<= 3) a then a : r else []) 4
= 1 : 2 : 3 : (\r -> if (<= 3) 4 then 4 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 5)

-- Evaluamos (<= 3) 4
= 1 : 2 : 3 : (\r -> if false then 4 : r else []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 5)

-- Evaluamos if false
= 1 : 2 : 3 : (\r -> []) $ foldr (\a r -> if (<= 3) a then a : r else []) [] (gen 5)

-- Evaluamos (\r -> []) lo que esta a la izquierda del $
= 1 : 2 : 3 : []

-- Evaluamos el resto
= 1 : 2 : [3]
= 1 : [2, 3]
= [1, 2, 3]

-}

-----------------------------------------------------------------------

{-

----------------------- Evaluacion aplicativa parte a)

  takeWhile (<= 3) (gen 1)

-- Evaluamos gen 1

= takeWhile (<= 3) (1 : gen 2)

= takeWhile (<= 3) (1 : 2 : gen 3)

= takeWhile (<= 3) (1 : 2 : 3 : gen 4)

= takeWhile (<= 3) (1 : 2 : 3 : 4 : gen 5)

= takeWhile (<= 3) (1 : 2 : 3 : 4 : 5 : gen 6)

= takeWhile (<= 3) (1 : 2 : 3 : 4 : 5 : 6 : gen 7)

. . .

Esta evaluacion nunca termina de ejecutarse. Pues gen continuara expandiendose indefinidamente

-}

--- Parte b)

data Arbol a = Hoja | Rama a (Arbol a) (Arbol a)

foldA :: (a -> b -> b -> b) -> b -> Arbol a -> b
foldA _ e Hoja = e
foldA f e (Rama elem izq der) = f elem (foldA f e izq) (foldA f e der)

--- Parte c)

takeWhileA :: (a -> Bool) -> Arbol a -> Arbol a
takeWhileA p = foldA (\a i d -> if p a then Rama a i d else Hoja) Hoja

genA :: Int -> Arbol Int
genA n = Rama n (genA (n + 1)) (genA (n * 2))

{-

----------------------- Evaluacion normal parte c)
[EVALUACION PRINCIPAL]

  takeWhileA (<= 3) (genA 1)

-- Evaluamos takeWhileA
= foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 1)

-- Evaluamos genA 1
= foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (Rama 1 (genA 2) (genA 2))

-- Evaluamos foldA
= (\a i d -> if (<= 3) a then Rama a i d else Hoja) 1 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2))

-- Evaluamos (\a i d -> if (<= 3) a then Rama a i d else Hoja) 1
= (\i d -> if (<= 3) 1 then Rama 1 i d else Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2))

-- Evaluamos (<= 3) 1
= (\i d -> if true then Rama 1 i d else Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2))

-- Evaluamos if true
= (\i d -> Rama 1 i d) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2))

-- Evaluamos (\i d -> Rama 1 i d) ...
= Rama 1 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2))

------ Por temas de legibilidad, evaluaremos una sola vez foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2) y luego sustuiremos el resultado
    [EVALUACION 2]

      foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)

    -- Evaluamos genA 2
    = foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (Rama 2 (genA 3) (genA 4))

    -- Evaluamos foldA
    = (\a i d -> if (<= 3) a then Rama a i d else Hoja) 2 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 3)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))

    -- Evaluamos (\a i d -> if (<= 3) a then Rama a i d else Hoja) 2
    -- Nos saltaremos algunos pasos que ya se evidenciaron en lo que llevamos evaluado
    -- . . .
    = Rama 2 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 3)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))

------ Por temas de legibilidad, evaluaremos (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 3)) y luego sustuiremos el resultado
    [EVALUACION 3]

      foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 3)

    -- Evaluamos genA 3
    = foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (Rama 3 (genA 4) (genA 6))

    -- Evaluamos foldA
    = (\a i d -> if (<= 3) a then Rama a i d else Hoja) 3 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 6))

    -- Evaluamos (\a i d -> if (<= 3) a then Rama a i d else Hoja) 3
    -- Nos saltaremos algunos pasos que ya se evidenciaron en lo que llevamos evaluado
    -- . . .
    = Rama 3 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 6))

------ Por temas de legibilidad, evaluaremos (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4)) y luego sustuiremos el resultado
    [EVALUACION 4]

      foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4)

    -- Evaluamos genA 4
    = foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (Rama 4 (genA 5) (genA 8))

    -- Evaluamos foldA
    = (\a i d -> if (<= 3) a then Rama a i d else Hoja) 4 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 5)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 8))

    -- Evaluamos (\a i d -> if (<= 3) a then Rama a i d else Hoja) 4
    = (\i d -> if (<= 3) 4 then Rama 4 i d else Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 5)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 8))

    -- Evaluamos (<= 3) 4
    = (\i d -> if false then Rama 4 i d else Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 5)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 8))

    -- Evaluamos if false
    = (\i d -> Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 5)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 8))

    -- Evaluamos (\i d -> Hoja)
    = Hoja

    FIN DE [EVALUACION 4]

------ CONTINUANDO CON [EVALUACION 3]

    -- Sustituimos el valor de (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))
    = Rama 3 Hoja (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 6))

    -- Evaluamos genA 6
    = Rama 3 Hoja (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (Rama 6 (genA 7) (genA 12)))

    -- Evaluamos foldA
    = Rama 3 Hoja ((\a i d -> if (<= 3) a then Rama a i d else Hoja) 6 (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 7)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 12)))

    -- Evaluamos (\a i d -> if (<= 3) a then Rama a i d else Hoja) 6
    -- Evaluamos (<= 3) 6
    -- Evaluamos if false
    = Rama 3 Hoja ((\i d -> Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 7)) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 12)))

    -- Evaluamos (\i d -> Hoja)
    = Rama 3 Hoja Hoja

    FIN DE [EVALUACION 3]

------ CONTINUANDO CON [EVALUACION 2]

    -- Sustituimos el valor de foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 3)
    = Rama 2 (Rama 3 Hoja Hoja) (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))

    -- Evaluamos (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))
    -- De [EVALUACION 4], sistituimos el valor de (foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 4))
    = Rama 2 (Rama 3 Hoja Hoja) Hoja

    FIN DE [EVALUACION 2]

-- CONTINUANDO CON [EVALUACION PRINCIPAL]

-- Sustituimos el valor de foldA (\a i d -> if (<= 3) a then Rama a i d else Hoja) Hoja (genA 2)
= Rama 1 (Rama 2 (Rama 3 Hoja Hoja) Hoja) (Rama 2 (Rama 3 Hoja Hoja) Hoja)

FIN DE [EVALUACION PRINCIPAL]

-}

-----------------------------------------------------------------------

{-

----------------------- Evaluacion aplicativa parte c)

  takeWhileA (<= 3) (genA 1)

-- Evaluamos genA 1
= takeWhileA (<= 3) (Rama 1 (genA 2) (genA 2))

-- Evaluamos el primer genA 2
= takeWhileA (<= 3) (Rama 1 (Rama 2 (genA 3) (genA 4)) (genA 2))

-- Evaluamos genA 3
= takeWhileA (<= 3) (Rama 1 (Rama 2 (Rama 3 (genA 4) (genA 6)) (genA 4)) (genA 2))

-- Evaluamos el primer genA 4
= takeWhileA (<= 3) (Rama 1 (Rama 2 (Rama 3 (Rama 4 (genA 5) (genA 8)) (genA 6)) (genA 4)) (genA 2))

-- Evaluamos genA 5
= takeWhileA (<= 3) (Rama 1 (Rama 2 (Rama 3 (Rama 4 (Rama 5 (genA 6) (genA 10)) (genA 8)) (genA 6)) (genA 4)) (genA 2))

. . .

Esta evaluacion nunca termina de ejecutarse. Pues genA continuara indefinidamente expandiendo la profundidad del arbol que genera.

-}