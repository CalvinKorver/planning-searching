;Header and description

(define (domain king)

    ;remove requirements that are not needed
    (:requirements :strips)

    (:predicates
        (at ?p ?x ?y) ;Indicates that piece ?p is at the square ?x, ?y
        (adjacent ?y1 ?y2);Indicates that the x- or y- coordinates ?y1, ?y2 are adjacent
        (occupied ?x ?y)    ;Indicates that the square ?x, ?y is occupied by another (untitled) piece
    )


    (:action move
        :parameters (?p ?x1 ?y1 ?x2 ?y2)
        :precondition (and 
            (at ?p ?x1 ?y1) 
            (not (occupied ?x2 ?y2))
            (or
                (and (= ?x1 ?x2) (adjacent ?y1 ?y2)) ; up and down
                (and (= ?x1 ?x2) (adjacent ?y2 ?y1)) ; up and down
                (and (= ?y1 ?y2) (adjacent ?x1 ?x2)) ; left and right
                (and (= ?y1 ?y2) (adjacent ?x2 ?x1)) ; left and right
                (and (adjacent ?x1 ?x2) (adjacent ?y1 ?y2)) ; diagonal
                (and (adjacent ?x2 ?x1) (adjacent ?y1 ?y2)) ; diagonal
                (and (adjacent ?x1 ?x2) (adjacent ?y2 ?y1)) ; diagonal
                (and (adjacent ?x2 ?x1) (adjacent ?y2 ?y1)) ; diagonal
            )
        )  
        :effect (and
            (not (at ?p ?x1 ?y1))
            (not (occupied ?x1 ?y1))
            (at ?p ?x2 ?y2)
            (occupied ?x2 ?y2)
        )
    )    
)