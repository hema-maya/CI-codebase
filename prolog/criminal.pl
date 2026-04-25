`% Facts
american(west).
enemy(nono, america).
missile(m1).
owns(nono, m1).

% Rules
weapon(X) :- missile(X).
hostile(X) :- enemy(X, america).

% Main Rule: West is a criminal if he sells weapons to a hostile nation

sells(west, X, nono) :- missile(X), owns(nono, X).
criminal(X) :- american(X), weapon(Y), sells(X, Y, Z), hostile(Z).