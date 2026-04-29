1)Factorial
-----------
(defun fact2(n)
    (if (= n 0)1
       (* n (fact2(- n 1)))
    )
)



2)Fibonacci
-----------
(defun fib2(n)
  (cond
     ((= n 0) 0)
     ((= n 1) 1)
     ((> n 1)(+ (fib2(- n 1))(fib2 (- n 2))))
)
)





3)Palindrome
------------
(defun pali (str)
  (equal str (reverse str)))



4)Area of circle
----------------
(defun AreaOfCircle()
  (terpri)
  (princ "Enter Radius:")
  (setq radius (read))
  (setq area (* 3.1416 radius radius))
  (format t "Radius: = ~F~% Area = ~F" radius area)
)

