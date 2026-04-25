% --- SET LOGIC ---

% 1. Member
is_member(X, [X|_]).
is_member(X, [_|T]) :- is_member(X, T).

% 2. Subset
is_subset([], _).
is_subset([H|T], Set2) :- is_member(H, Set2), is_subset(T, Set2).

% 3. Union
union([], Set2, Set2).
union([H|T], Set2, Res) :- is_member(H, Set2), !, union(T, Set2, Res).
union([H|T], Set2, [H|Res]) :- union(T, Set2, Res).

% 4. Intersection
intersection([], _, []).
intersection([H|T], Set2, [H|Res]) :- is_member(H, Set2), !, intersection(T, Set2, Res).
intersection([_|T], Set2, Res) :- intersection(T, Set2, Res).

% 5. Difference (Set1 - Set2)
difference([], _, []).
difference([H|T], Set2, Res) :- is_member(H, Set2), !, difference(T, Set2, Res).
difference([H|T], Set2, [H|Res]) :- difference(T, Set2, Res).

% 6. Cardinality (Length)
cardinality([], 0).
cardinality([_|T], Count) :- cardinality(T, C1), Count is C1 + 1.

% 7. Is Equivalent (Same elements, any order)
is_equivalent(Set1, Set2) :- is_subset(Set1, Set2), is_subset(Set2, Set1).

% --- MENU INTERFACE ---

main :-
    nl, write('--- SET OPERATIONS ---'), nl,
    write('1. Member Check'), nl,
    write('2. Subset Check'), nl,
    write('3. Union'), nl,
    write('4. Intersection'), nl,
    write('5. Difference (A-B)'), nl,
    write('6. Cardinality'), nl,
    write('7. Equality/Equivalence Check'), nl,
    write('8. Exit'), nl,
    write('Choice (1-8): '), read(Choice),
    process(Choice).

process(8) :- write('Goodbye!'), nl, !.

process(1) :-
    write('Element: '), read(X), write('Set: '), read(S),
    (is_member(X, S) -> write('Yes, is a member.'); write('No, not a member.')), nl, main.

process(2) :-
    write('Set A: '), read(A), write('Set B: '), read(B),
    (is_subset(A, B) -> write('A is a subset of B.'); write('A is NOT a subset.')), nl, main.

process(3) :-
    write('Set A: '), read(A), write('Set B: '), read(B),
    union(A, B, R), write('Union: '), write(R), nl, main.

process(4) :-
    write('Set A: '), read(A), write('Set B: '), read(B),
    intersection(A, B, R), write('Intersection: '), write(R), nl, main.

process(5) :-
    write('Set A: '), read(A), write('Set B: '), read(B),
    difference(A, B, R), write('Difference: '), write(R), nl, main.

process(6) :-
    write('Set: '), read(S), cardinality(S, C),
    write('Cardinality: '), write(C), nl, main.

process(7) :-
    write('Set A: '), read(A), write('Set B: '), read(B),
    (is_equivalent(A, B) -> write('Sets are equivalent.'); write('Sets are NOT equivalent.')), nl, main.

process(_) :- write('Invalid choice.'), nl, main.