(define (problem have-cake-eat-cake)
  (:domain cake)
  (:objects 
    cake
    cookies
    pie
  )
  (:init  )
  (:goal (and 
    (eaten cake)
    (eaten pie)
    (eaten cookies)
  ))
)