(define (problem single-knight-problem) 

    (:domain knight)
    (:objects
        knight1
        knight2
        x1 x2 x3 x4 x5 x6 x7
        y1 y2 y3 y4 y5 y6 y7 y8
    )

    (:init
        (at knight1 x1 y1)
        (at knight2 x7 y8)
        
        (delta1 x1 x2)
        (delta1 x2 x1)
        (delta1 x3 x2)
        (delta1 x4 x3)
        (delta1 x5 x4)
        (delta1 x6 x5)
        (delta1 x7 x6)
        (delta1 x6 x7)
        (delta1 x5 x6)
        (delta1 x4 x5)
        (delta1 x3 x4)
        (delta1 x2 x3)
        (delta1 y1 y2)
        (delta1 y2 y3)
        (delta1 y3 y4)
        (delta1 y5 y6)
        (delta1 y6 y7)
        (delta1 y7 y8)
        (delta1 y8 y7)
        (delta1 y7 y6)
        (delta1 y6 y5)
        (delta1 y5 y4)
        (delta1 y4 y3)
        (delta1 y3 y2)
        (delta1 y2 y1)
        
        (occupied x2 y3)
        (occupied x6 y6)

        (delta2 y1 y3)
        (delta2 y2 y4)
        (delta2 y3 y5)
        (delta2 y4 y6)
        (delta2 y5 y7)
        (delta2 y6 y8)
        (delta2 y8 y6)
        (delta2 y7 y5)
        (delta2 y6 y4)
        (delta2 y5 y3)
        (delta2 y4 y2)
        (delta2 y3 y1)

        (delta2 x1 x3)
        (delta2 x2 x4)
        (delta2 x3 x5)
        (delta2 x4 x6)
        (delta2 x5 x7)
        (delta2 x7 x5)
        (delta2 x6 x4)
        (delta2 x5 x3)
        (delta2 x4 x2)
        (delta2 x3 x1)

    )

    (:goal (and
        (at knight1 x7 y8) 
        (at knight2 x1 y1)
    ))

)