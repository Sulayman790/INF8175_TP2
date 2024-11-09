include "globals.mzn";


% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)


%-----------------------------------------------------------------------------%
% Données

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Décomposition du nombre en un ensemble de chiffres
array[1..4] of var 1..9: chiffres;

% nombre à 4 chiffres
var 1000..9999: nombre = 1000 * chiffres[1] + 100 * chiffres[2] + 10 * chiffres[3] + chiffres[4];

% produit des 3 derniers chiffres
var int: p = chiffres[2] * chiffres[3] * chiffres[4];

%-----------------------------------------------------------------------------%
% Contraintes
%-----------------------------------------------------------------------------%

% Le nombre doit être pair
constraint chiffres[4] mod 2 = 0;

% Les chiffres doivent être tous différents
constraint all_different(chiffres);

% aucun chiffre n'est ègale à 0
constraint forall(i in 1..4) (chiffres[i] != 0);

% le chiffre à la position des milliers doit être supérieur à celui des centaines
constraint chiffres[1] > chiffres[2];

% le chiffre à la position des dizaines doit être inférieur à celui des unités
constraint chiffres[3] < chiffres[4];

% le chiffre à la position des centaines doit être supérieur à celui des unités
constraint chiffres[2] > chiffres[4];

% la somme des 4 chiffres doit être supérieure à 15
constraint sum(chiffres) > 15;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% On veux minimizer le probléme
solve minimize p;

output [
  show(nombre)
];

