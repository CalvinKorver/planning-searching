(define (problem single-king-problem) 

    (:domain king)
    (:objects
        king
        x1 x2 x3 x4 x5 x6 x7
        y1 y2 y3 y4 y5 y6 y7 y8
    )

    (:init
        (at king x1 y1)
        (adjacent x1 x2)
        (adjacent x2 x1)
        (adjacent x3 x2)
        (adjacent x4 x3)
        (adjacent x5 x4)
        (adjacent x6 x5)
        (adjacent x7 x6)
        (adjacent x6 x7)
        (adjacent x5 x6)
        (adjacent x4 x5)
        (adjacent x3 x4)
        (adjacent x2 x3)
        (adjacent y1 y2)
        (adjacent y2 y3)
        (adjacent y3 y4)
        (adjacent y5 y6)
        (adjacent y6 y7)
        (adjacent y7 y8)
        (adjacent y8 y7)
        (adjacent y7 y6)
        (adjacent y6 y5)
        (adjacent y5 y4)
        (adjacent y4 y3)
        (adjacent y3 y2)
        (adjacent y2 y1)
        (occupied x7 y7)
        (occupied x6 y7)
    )

    (:goal (and
        (at king x7 y8) 
    ))

)