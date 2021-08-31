pai(adao,cain).
pai(adao,abel).
pai(adao,seth).
pai(seth,enos).

avo(X, Y) :- pai(X, Z), pai(Z, Y).
irmao(X, Y) :- pai(Z, X), pai(Z, Y), X\=Y.