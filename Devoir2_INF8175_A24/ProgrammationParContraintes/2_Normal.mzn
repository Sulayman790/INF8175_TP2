% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn"; 

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre de tâches
int: n;
% Durée maximal du projet
int: m;
% Limite de ressources pouvant être partagées entre les tâches en cours
int: limite;

% Durée des tâches
array[1..n] of 1..m: duree_tache;
% Ressources requises par les tâches
array[1..n] of 1..m: ressource_tache;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

array[1..n] of var 1..m: debut_tache; % Début des tâches
array[1..n] of var 1..m: fin_tache; % Fin des tâches

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Fin du projet
% on veux minimzer la fin du projet
var int: fin_projet;

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
%-----------------------------------------------------------------------------%

% contrainte pour definir la duree d'une tache
constraint forall(i in 1..n)(duree_tache[i] = fin_tache[i] - debut_tache[i]);

% pas plus de deux tâches ne démarrent en même temps
constraint forall(t in 1..m)(sum([1 | i in 1..n where debut_tache[i] = t]) <= 2);

% contrainte sur la consomation des ressources https://docs.minizinc.dev/en/stable/lib-globals-scheduling.html  cumulative(start,duration,ressource,bound);
constraint cumulative(debut_tache, duree_tache, ressource_tache, limite);

% la fin des taches ne peuvent pas depasser la fin du projet
constraint forall(i in 1..n)(fin_projet >= fin_tache[i]);

solve minimize fin_projet;
%-----------------------------------------------------------------------------%

output [
  "Envergure du projet  : ", show(fin_projet), "\n",
  "Début des tâches     : ", show(debut_tache), "\n",
  "Fin des tâches       : ", show(fin_tache), "\n",
];
