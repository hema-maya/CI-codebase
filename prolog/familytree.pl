% ---------- Male ----------
male(carol). male(john). male(bob). male(tom). male(fred). male(scott).
male(steve). male(jack). male(rich). male(jim). male(mike). male(harry).

% ---------- Female ----------
female(patty). female(mary). female(alice). female(valerie). female(barbara).
female(linda). female(donna). female(rachel). female(jane). female(cindy).

% ---------- Parents ----------
% Fixed: Tom and Carol now share a Father (John) but different Mothers
father(john, tom).
father(john, carol).
father(john, linda).
father(bob, jim).

father(tom, valerie). father(tom, barbara).
father(fred, jane).
father(scott, cindy).
father(steve, jack). father(steve, rich).
father(jack, mike).
father(rich, harry).

mother(mary, tom).
mother(patty, carol). % Carol has a different mother than Tom
mother(mary, linda).
mother(mary, jim).

mother(alice, valerie). mother(alice, barbara).
mother(valerie, jane).
mother(barbara, cindy).
mother(linda, jack). mother(linda, rich).
mother(donna, mike).
mother(rachel, harry).

% ---------- Rules ----------
parent(X,Y) :- father(X,Y); mother(X,Y).

% STRICT Sibling Rule: Must share BOTH parents
sibling(X,Y) :-
    father(F,X), father(F,Y),
    mother(M,X), mother(M,Y),
    X \= Y.

brother(X,Y) :- male(X), sibling(X,Y).
sister(X,Y) :- female(X), sibling(X,Y).

% Grandparents
grandparent(X,Y) :- parent(X,Z), parent(Z,Y).
grandfather(X,Y) :- male(X), grandparent(X,Y).
grandmother(X,Y) :- female(X), grandparent(X,Y).

% Grandchildren
grandchild(X,Y) :- grandparent(Y,X).
grandson(X,Y) :- male(X), grandchild(X,Y).
granddaughter(X,Y) :- female(X), grandchild(X,Y).

% Aunts/Uncles (Strictly through full siblings)
aunt(X,Y) :- female(X), sibling(X,Z), parent(Z,Y).
uncle(X,Y) :- male(X), sibling(X,Z), parent(Z,Y).

% Cousins (Strictly through full siblings)
cousin(X,Y) :- parent(A,X), parent(B,Y), sibling(A,B), X \= Y.

% ---------- Relation Wrapper ----------

has_relation(X,Y) :-
    parent(X,Y); sibling(X,Y); grandparent(X,Y); grandchild(X,Y);
    uncle(X,Y); aunt(X,Y); cousin(X,Y).

relation(X,Y, father)       :- father(X,Y).
relation(X,Y, mother)       :- mother(X,Y).
relation(X,Y, brother)      :- brother(X,Y).
relation(X,Y, sister)       :- sister(X,Y).
relation(X,Y, grandfather)  :- grandfather(X,Y).
relation(X,Y, grandmother)  :- grandmother(X,Y).
relation(X,Y, grandson)     :- grandson(X,Y).
relation(X,Y, granddaughter) :- granddaughter(X,Y).
relation(X,Y, uncle)         :- uncle(X,Y).
relation(X,Y, aunt)          :- aunt(X,Y).
relation(X,Y, cousin)        :- cousin(X,Y).

% Catch-all: Step-relations now return 'no relation'
relation(X,Y, 'no relation') :- \+ has_relation(X,Y).
