/*
The `select/3` clause: select(L,X,R), selects element X from list L and gives the rest of the list on R.
*/

select([X],X,[]):-!.
select([X|Y],X,Y).
select([X|Y],Z,W):-select(Y,Z,K),append([X],K,W).

/*
The `reduce/4` clause: reduce(OLD,L,NL,NEW) where OLD is the old element of L, L is a list, NL is a new list created from L, and NEW is the new value for OLD.
OLD >= 1
NEW is either 0 or 1, if OLD is 1 then NEW is 0.
This predicate tries to assign OLD a new value NEW. In case of being 0 NL is the same as L. In the case of beign 1 NL is [1 | L].
This represents the play as follows:
*/
reduce(_,L,L,0).
reduce(X,L,[1|L],1) :- X > 1.

%Every element on the list must be greater than zero
/*
The `nim/1` clause: nim(L) where L is a list returns true if playing optimally is possible to win an instance of the nim game, or false if it isnt.
The variation of nim used consider as the winner the player who cannot reduce any number, in this case all values are 0s.
The `nim/3` clause: nim(L,OLD,NEW) is a convience clause for extracting the element to be modified and its new value. 
*/
nim([X]):- X>1,!.
nim(L):-length(L,LEN), LEN > 1, select(L,X,R), reduce(X,R,S,_), not(nim(S)),!.

nim([X],X,1):- X>1, !.
nim(L,O,N):- length(L,LEN), LEN > 1, select(L,O,R), reduce(O,R,S,N), not(nim(S)),!.
