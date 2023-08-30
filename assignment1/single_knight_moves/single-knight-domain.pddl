;Header and description

(define (domain knight)

    ;remove requirements that are not needed
    (:requirements :strips)

    (:predicates
        (at ?p ?x ?y) ;Indicates that piece ?p is at the square ?x, ?y
        (occupied ?x ?y)    ;Indicates that the square ?x, ?y is occupied by another (untitled) piece
        (delta1 ?y1 ?y2);Indicates that the x- or y- coordinates ?y1, ?y2 are adjacent
        (delta2 ?y1 ?y2);Indicates that the x- or y- coordinates ?y1, ?y2 are separated by one square
    )


    (:action move
        :parameters (?p ?x1 ?y1 ?x2 ?y2)
        :precondition (and 
            (at ?p ?x1 ?y1) 
            (not (occupied ?x2 ?y2))
            (or
                (and (delta1 ?x1 ?x2) (delta2 ?y1 ?y2)) ; x vals are adjacent, y are sep by 1
                (and (delta1 ?x1 ?x2) (delta2 ?y2 ?y1)) ; x vals are adjacent, y are sep by 1
                (and (delta1 ?x2 ?x1) (delta2 ?y1 ?y2)) ; x vals are adjacent, y are sep by 1
                (and (delta1 ?x2 ?x1) (delta2 ?y2 ?y1)) ; x vals are adjacent, y are sep by 1


                (and (delta1 ?y1 ?y2) (delta2 ?x1 ?x2)) ; y vals are adjacent, x are sep by 1
                (and (delta1 ?y1 ?y2) (delta2 ?x2 ?x1)) ; y vals are adjacent, x are sep by 1
                (and (delta1 ?y2 ?y1) (delta2 ?x1 ?x2)) ; y vals are adjacent, x are sep by 1
                (and (delta1 ?y2 ?y1) (delta2 ?x2 ?x1)) ; y vals are adjacent, x are sep by 1
            )
        )  
        :effect (and
            (not (at ?p ?x1 ?y1))
            (at ?p ?x2 ?y2)
            (occupied ?x2 ?y2)
            (not (occupied ?x1 ?y1))
        )
    )    
)