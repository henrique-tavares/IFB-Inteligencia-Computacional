% 1.2
pai(ivo, eva).
pai(gil, rai).
pai(gil, clo).
pai(gil, ary).
pai(rai, noe).
pai(ary, gal).

mae(ana, eva).
mae(bia, rai).
mae(bia, clo).
mae(bia, ary).
mae(eva, noe).
mae(lia, gal).

homem(ivo).
homem(gil).
homem(rai).
homem(ary).
homem(noe).

mulher(ana).
mulher(bia).
mulher(eva).
mulher(clo).
mulher(lia).
mulher(gal).

gerou(X, Y) :- pai(X, Y); mae(X, Y).

filho(X, Y) :- homem(X), gerou(Y, X).
filha(X, Y) :- mulher(X), gerou(Y, X).

tio(X, Y) :- homem(X), gerou(A, X), gerou(A, Z), X\=Z, gerou(Z, Y).
tia(X, Y) :- mulher(X), gerou(A, X), gerou(A, Z), X\=Z, gerou(Z, Y).

primo(X, Y) :- homem(X), gerou(Z, X), (tio(Z, Y); tia(Z, Y)).
prima(X, Y) :- mulher(X), gerou(Z, X), (tio(Z, Y); tia(Z, Y)).

avo_m(X, Y) :- gerou(Z, Y), pai(X, Z).
avo_f(X, Y) :- gerou(Z, Y), mae(X, Z).

% 1.3
feliz(X) :- gerou(X, _), !.

casal(X, Y) :- gerou(X, Z), gerou(Y, Z), X\=Y, !.