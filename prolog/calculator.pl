% Arithmetic Operations
calculate(+, A, B, R) :- R is A + B.
calculate(-, A, B, R) :- R is A - B.
calculate(*, A, B, R) :- R is A * B.
% Division handling
calculate(/, A, B, R) :- B =\= 0, !, R is A / B.
calculate(/, _, 0, 'Error: Division by zero').
% Modulo handling
calculate(mod, A, B, R) :- B =\= 0, !, R is A mod B.
calculate(mod, _, 0, 'Error: Division by zero').

% Main Entry Point
menu :-
    nl, write('1. ADD'), nl,
    write('2. SUB'), nl,
    write('3. MUL'), nl,
    write('4. DIV'), nl,
    write('5. MOD'), nl,
    write('6. EXIT'), nl,
    write('Enter your choice: '), read(Ch),
    (   Ch == 6 -> write('Exiting...'), nl
    ;   member(Ch, [1,2,3,4,5]) ->
        write('Enter the first number: '), read(A),
        write('Enter the second number: '), read(B),
        process(Ch, A, B),
        menu
    ;   write('Invalid choice'), nl, menu
    ).

% Process Choices
process(1, A, B) :- calculate(+, A, B, R), write('Result = '), write(R), nl.
process(2, A, B) :- calculate(-, A, B, R), write('Result = '), write(R), nl.
process(3, A, B) :- calculate(*, A, B, R), write('Result = '), write(R), nl.
process(4, A, B) :- calculate(/, A, B, R), write('Result = '), write(R), nl.
process(5, A, B) :- calculate(mod, A, B, R), write('Result = '), write(R), nl.