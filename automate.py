import copy as cp
import os
from graphviz import Digraph

class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """

    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
        réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """

        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 


    def __str__(self):
        """affichage de l'automate par fonction print"""
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"
        for k,v in self.transition.items():    
            res += str(k) + ": " + str(v) + "\n"
        res += "*********************************"
        return res


    def ajoute_transition(self, q0, a, qlist):
        """ ajoute la liste de transitions (q0, a, q1) pour tout q1 
            dans qlist à l'automate
            qlist est une liste d'états
        """
        if not isinstance(qlist, list):
            raise TypeError("Erreur de type: ajoute_transition requiert une liste à ajouter")
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            self.transition.update({(q0, a): qlist})

def generer_graphique(a, nom_fichier):
    """Génère un fichier PDF représentant l'automate a (Exigence Section 8)"""
    dot = Digraph(comment=a.name)
    dot.attr(rankdir='LR')

    # Création des états
    for i in range(a.n):
        if i in a.final:
            dot.node(str(i), str(i), shape='doublecircle')
        else:
            dot.node(str(i), str(i), shape='circle')

    # État initial
    dot.node('', '', shape='none')
    dot.edge('', '0')

    # Transitions
    for (etat_origine, char), etats_dest in a.transition.items():
        for etat_dest in etats_dest:
            label_char = 'ε' if char == 'E' else char
            dot.edge(str(etat_origine), str(etat_dest), label=label_char)

    dot.render(nom_fichier, format='pdf', cleanup=True)

def concatenation(a1, a2): 
    """Retourne l'automate qui reconnaît la concaténation des
    langages reconnus par les automates a1 et a2"""
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)

    res = automate()
    res.n = a1.n + a2.n
    res.name = f"({a1.name}.{a2.name})"

    res.transition = cp.deepcopy(a1.transition)

    offset = a1.n
    for (etat, char), destinations in a2.transition.items():
        res.transition[(etat + offset, char)] = [d + offset for d in destinations]

    for f in a1.final:
        res.ajoute_transition(f, "E", [0 + offset])

    res.final = [f + offset for f in a2.final]

    return res


def union(a1, a2):
    """Retourne l'automate qui reconnaît l'union des
    langages reconnus par les automates a1 et a2"""
    a1 = cp.deepcopy(a1)
    a2 = cp.deepcopy(a2)

    res = automate()
    res.n = 1 + a1.n + a2.n
    res.name = f"({a1.name}|{a2.name})"

    offset1 = 1
    offset2 = 1 + a1.n

    for (etat, char), destinations in a1.transition.items():
        res.transition[(etat + offset1, char)] = [d + offset1 for d in destinations]

    for (etat, char), destinations in a2.transition.items():
        res.transition[(etat + offset2, char)] = [d + offset2 for d in destinations]

    res.ajoute_transition(0, "E", [0 + offset1, 0 + offset2])

    res.final = [f + offset1 for f in a1.final] + [f + offset2 for f in a2.final]

    return res


def etoile(a):
    """Retourne l'automate qui reconnaît l'étoile de Kleene du
    langage reconnu par l'automate a"""
    a = cp.deepcopy(a)

    res = automate()
    res.n = 1 + a.n
    res.name = f"({a.name})*"

    offset = 1

    for (etat, char), destinations in a.transition.items():
        res.transition[(etat + offset, char)] = [d + offset for d in destinations]

    res.ajoute_transition(0, "E", [0 + offset])

    for f in a.final:
        res.ajoute_transition(f + offset, "E", [0 + offset])

    res.final = [0] + [f + offset for f in a.final]

    return res


def acces_epsilon(a):
    """ retourne la liste pour chaque état des états accessibles par epsilon
        transitions pour l'automate a
        res[i] est la liste des états accessible pour l'état i
    """
    # on initialise la liste résultat qui contient au moins l'état i pour chaque état i
    res = [[i] for i in range(a.n)]
    for i in range(a.n):
        candidats = list(range(i)) + list(range(i+1, a.n))
        new = [i]
        while True:
            # liste des epsilon voisins des états ajoutés en dernier:
            voisins_epsilon = []
            for e in new:
                if (e, "E") in a.transition.keys():
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]
            # on calcule la liste des nouveaux états:
            new = list(set(voisins_epsilon) & set(candidats))
            # si la nouvelle liste est vide on arrête:
            if new == []:
                break
            # sinon on retire les nouveaux états ajoutés aux états candidats
            candidats = list(set(candidats) - set(new))
            res[i] += new 
    return res


def supression_epsilon_transitions(a):
    """ retourne l'automate équivalent sans epsilon transitions
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name
    res.n = a.n
    res.final = a.final
    # pour chaque état on calcule les états auxquels il accède
    # par epsilon transitions.
    acces = acces_epsilon(a)
    # on retire toutes les epsilon transitions
    res.transition = {c: j for c, j in a.transition.items() if c[1] != "E"}
    for i in range(a.n):
        # on ajoute i dans les états finals si accès à un état final:
        if (set(acces[i]) & set(a.final)):
            if i not in res.final:
                res.final.append(i)
        # on ajoute les nouvelles transitions en parcourant toutes les transitions
        for c, v in a.transition.items():
            if c[1] != "E" and c[0] in acces[i]:
                res.ajoute_transition(i, c[1], v)
    return res


def determinisation(a):
    """ retourne l'automate équivalent déterministe
        la construction garantit que tous les états sont accessibles
        automate d'entrée sans epsilon-transitions
    """
    res = automate()
    res.name = "Det(" + a.name + ")"

    start_set = frozenset([0])

    mapping = {start_set: 0}

    queue = [start_set]

    compteur = 1

    new_transitions = {}
    new_finals = []

    if any(s in a.final for s in start_set):
        new_finals.append(0)

    while queue:
        current_set = queue.pop(0)
        u = mapping[current_set]

        for char in a.alphabet:
            next_states = set()
            for s in current_set:
                if (s, char) in a.transition:
                    next_states.update(a.transition[(s, char)])

            if not next_states:
                continue

            next_frozenset = frozenset(next_states)

            if next_frozenset not in mapping:
                mapping[next_frozenset] = compteur
                queue.append(next_frozenset)
                if any(s in a.final for s in next_states):
                    new_finals.append(compteur)
                compteur += 1

            v = mapping[next_frozenset]
            new_transitions[(u, char)] = [v]

    res.n = compteur
    res.final = new_finals
    res.transition = new_transitions
    return res


def completion(a):
    """ retourne l'automate a complété
        l'automate en entrée doit être déterministe
    """
    a = cp.deepcopy(a)
    poubelle_needed = False

    for i in range(a.n):
        for char in a.alphabet:
            if (i, char) not in a.transition:
                poubelle_needed = True
                break
        if poubelle_needed:
            break

    if not poubelle_needed:
        return a

    res = a
    poubelle_state = res.n
    res.n += 1

    for i in range(poubelle_state):
        for char in res.alphabet:
            if (i, char) not in res.transition:
                res.transition[(i, char)] = [poubelle_state]

    for char in res.alphabet:
        res.transition[(poubelle_state, char)] = [poubelle_state]

    return res


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # on copie pour éviter les effets de bord     
    a = cp.deepcopy(a)
    res = automate()
    res.name = a.name

    # Étape 1 : partition initiale = finaux / non finaux
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    # on retire les ensembles vides
    part = [e for e in part if e != set()]  

    # Étape 2 : raffinement jusqu’à stabilité
    modif = True
    while modif:
        modif = False
        new_part = []
        for e in part:
            # sous-ensembles à essayer de séparer
            classes = {}
            for q in e:
                # signature = tuple des indices des blocs atteints pour chaque lettre
                signature = []
                for c in a.alphabet:
                    for i, e2 in enumerate(part):
                        if a.transition[(q, c)][0] in e2:
                            signature.append(i)
                # on ajoute l'état q à la clef signature calculée
                classes.setdefault(tuple(signature), set()).add(q)
            if len(classes) > 1:
                # s'il y a >2 signatures différentes on a séparé des états dans e
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)
        part = new_part
    # on réordonne la partition pour que le premier sous-ensemble soit celui qui contient l'état initial
    for i, e in enumerate(part):
        if 0 in e:
            part[0], part[i] = part[i], part[0]
            break

    # Étape 3 : on construit le nouvel automate minimal
    mapping = {}
    # on associe à chaque état q le nouvel état i
    # obtenu comme étant l'indice du sous-ensemble de part
    for i, e in enumerate(part):
        for q in e:
            mapping[q] = i

    res.n = len(part)
    res.final = list({mapping[q] for q in a.final if q in mapping})
    for i, e in enumerate(part):
        # on récupère un élément de e:
        representant = next(iter(e))
        for c in a.alphabet:
            q = a.transition[(representant, c)][0]
            res.transition[(i, c)] = [mapping[q]]
    return res


def tout_faire(a):
    a1 = supression_epsilon_transitions(a)
    a2 = determinisation(a1)
    a3 = completion(a2)
    a4 = minimisation(a3)
    return a4


def egal(a1, a2):
    """ retourne True si a1 et a2 sont isomorphes
        a1 et a2 doivent être minimaux
    """
    if len(a1.alphabet) != len(a2.alphabet):
        return False
    if a1.n != a2.n:
        return False
    if len(a1.final) != len(a2.final):
        return False

    mapping = {0: 0}
    queue = [0]
    visited = {0}

    while queue:
        u1 = queue.pop(0)
        u2 = mapping[u1]

        if (u1 in a1.final) != (u2 in a2.final):
            return False

        for char in a1.alphabet:
            dest1 = a1.transition.get((u1, char), [])
            dest2 = a2.transition.get((u2, char), [])

            if bool(dest1) != bool(dest2):
                return False

            if not dest1:
                continue

            v1 = dest1[0]
            v2 = dest2[0]

            if v1 in mapping:
                if mapping[v1] != v2:
                    return False
            else:
                mapping[v1] = v2
                if v1 not in visited:
                    visited.add(v1)
                    queue.append(v1)

    return True



# Tests utilitaires pour chaque fonction

def test_union():
    """Tests avec plusieurs exemples pour la fonction union"""
    print("\n--- 1. TESTS DE LA FONCTION 'UNION' ---")
    
    # Exemple 1 : Union simple a + b
    print("Exemple 1 : a + b...", end=" ", flush=True)
    u1 = union(automate("a"), automate("b"))
    generer_graphique(u1, "tests_pdf/01_union_simple")
    print("[OK]")

    # Exemple 2 : Union avec Epsilon a + E
    print("Exemple 2 : a + E (epsilon)...", end=" ", flush=True)
    u2 = union(automate("a"), automate("E"))
    generer_graphique(u2, "tests_pdf/02_union_epsilon")
    print("[OK]")

    # Exemple 3 : Union complexe (a + b) + c
    print("Exemple 3 : (a + b) + c...", end=" ", flush=True)
    u3 = union(u1, automate("c"))
    generer_graphique(u3, "tests_pdf/03_union_complexe")
    print("[OK]")


def test_concatenation():
    """Tests avec plusieurs exemples pour la fonction concatenation"""
    print("\n--- 2. TESTS DE LA FONCTION 'CONCATENATION' ---")
    
    # Exemple 1 : Concaténation simple a.b
    print("Exemple 1 : a . b...", end=" ", flush=True)
    c1 = concatenation(automate("a"), automate("b"))
    generer_graphique(c1, "tests_pdf/04_concat_base")
    print("[OK]")

    # Exemple 2 : Concaténation avec Epsilon a.E
    print("Exemple 2 : a . E (epsilon)...", end=" ", flush=True)
    c2 = concatenation(automate("a"), automate("E"))
    generer_graphique(c2, "tests_pdf/05_concat_epsilon")
    print("[OK]")

    # Exemple 3 : Concaténation triple a.b.c
    print("Exemple 3 : a . b . c...", end=" ", flush=True)
    c3 = concatenation(c1, automate("c"))
    generer_graphique(c3, "tests_pdf/06_concat_triple")
    print("[OK]")


def test_etoile():
    """Tests avec plusieurs exemples pour la fonction etoile"""
    print("\n--- 3. TESTS DE LA FONCTION 'ETOILE' ---")
    
    # Exemple 1 : Étoile simple a*
    print("Exemple 1 : a*...", end=" ", flush=True)
    e1 = etoile(automate("a"))
    generer_graphique(e1, "tests_pdf/07_etoile_kleene")
    print("[OK]")

    # Exemple 2 : Étoile d'une union (a + b)*
    print("Exemple 2 : (a + b)*...", end=" ", flush=True)
    u1 = union(automate("a"), automate("b"))
    e2 = etoile(u1)
    generer_graphique(e2, "tests_pdf/08_etoile_union_ab")
    print("[OK]")


def test_determinisation():
    """Tests avec plusieurs exemples pour la fonction determinisation"""
    print("\n--- 4. TESTS DE LA FONCTION 'DETERMINISATION' ---")

    # Exemple 1 : AFN non-déterministe vers AFD (a + a)
    print("Exemple 1 : AFN vers AFD (a + a)...", end=" ", flush=True)
    nfa_a = automate("a")
    nfa_a.ajoute_transition(0, "a", [1]) # Forcer le non-déterminisme
    det1 = determinisation(nfa_a)
    generer_graphique(det1, "tests_pdf/09_AFN-AFD_a+a")
    print("[OK]")

    # Exemple 2 : Déterminisation de (a + b)*
    print("Exemple 2 : Déterminisation de (a + b)*...", end=" ", flush=True)
    u1 = union(automate("a"), automate("b"))
    e1 = etoile(u1)
    det2 = determinisation(supression_epsilon_transitions(e1))
    generer_graphique(det2, "tests_pdf/10_determinisation_ab*")
    print("[OK]")


def test_completion():
    """Tests avec plusieurs exemples pour la fonction completion"""
    print("\n--- 5. TESTS DE LA FONCTION 'COMPLETION' ---")

    # Exemple 1 : Compléter un automate simple 'a' pour l'alphabet {a, b, c}
    print("Exemple 1 : Compléter l'automate 'a'...", end=" ", flush=True)
    a_det = determinisation(supression_epsilon_transitions(automate("a")))
    comp1 = completion(a_det)
    generer_graphique(comp1, "tests_pdf/11_completion_a")
    print("[OK]")

    # Exemple 2 : Compléter l'automate vide 'O'
    print("Exemple 2 : Compléter l'automate vide 'O'...", end=" ", flush=True)
    o_det = determinisation(supression_epsilon_transitions(automate("O")))
    comp2 = completion(o_det)
    generer_graphique(comp2, "tests_pdf/12_completion_2_vide")
    print("[OK]")


def test_minimisation():
    """Tests avec plusieurs exemples pour la fonction minimisation"""
    print("\n--- 6. TESTS DE LA FONCTION 'MINIMISATION' (Moore) ---")

    # Exemple 1 : Automate déjà minimal 'a'
    print("Exemple 1 : Automate déjà minimal 'a'...", end=" ", flush=True)
    a_comp = completion(determinisation(supression_epsilon_transitions(automate("a"))))
    mini1 = minimisation(a_comp)
    generer_graphique(mini1, "tests_pdf/13_min_deja_minimal")
    print("[OK]")

    # Exemple 2 : Automate avec redondance (a + a)*
    print("Exemple 2 : Automate redondant (a + a)*...", end=" ", flush=True)
    aa_star = etoile(union(automate("a"), automate("a")))
    mini2 = minimisation(completion(determinisation(supression_epsilon_transitions(aa_star))))
    generer_graphique(mini2, "tests_pdf/14_min_redondance")
    print("[OK]")

    # Exemple 3 : Cas "Textbook" (a|b)*abb
    print("Exemple 3 : Complexe (a|b)*abb ...", end=" ", flush=True)
    a_ou_b_star = etoile(union(automate("a"), automate("b")))
    abb = concatenation(automate("a"), concatenation(automate("b"), automate("b")))
    exp3 = concatenation(a_ou_b_star, abb)
    mini3 = tout_faire(exp3)
    generer_graphique(mini3, "tests_pdf/15_min_complexe")
    print("[OK]")


def test_egalite():
    """Tests avec plusieurs exemples pour la fonction egal (Isomorphisme)"""
    print("\n--- 7. TESTS DE LA FONCTION 'EGAL' ---")

    # Exemple 1 : (a+b)* == (a*+b*)* (Identité algébrique)
    print("Exemple 1 : (a+b)* == (a*+b*)*...", end=" ", flush=True)
    exp1 = tout_faire(etoile(union(automate("a"), automate("b"))))
    exp2 = tout_faire(etoile(union(etoile(automate("a")), etoile(automate("b")))))
    print(f"[{egal(exp1, exp2)}]")

    # Exemple 2 : Distributivité a(b+c) == ab + ac
    print("Exemple 2 : a(b+c) == ab + ac...", end=" ", flush=True)
    dist1 = tout_faire(concatenation(automate("a"), union(automate("b"), automate("c"))))
    dist2 = tout_faire(union(concatenation(automate("a"), automate("b")), 
                             concatenation(automate("a"), automate("c"))))
    print(f"[{egal(dist1, dist2)}]")

    # Exemple 3 : Différence simple a* vs b*
    print("Exemple 3 : a* == b*...", end=" ", flush=True)
    print(f"[{egal(tout_faire(etoile(automate('a'))), tout_faire(etoile(automate('b'))))}]")




if __name__ == "__main__":
    print("\n=== DÉBUT DE LA SUITE DE TESTS ===")
    
    # Création du dossier pour les schémas si absent
    if not os.path.exists("tests_pdf"):
        os.makedirs("tests_pdf")

    # Appel des fonctions de test
    test_union()
    test_concatenation()
    test_etoile()
    test_determinisation()
    test_completion()
    test_minimisation()
    test_egalite()
    
    print("\n==============================================")
    print("Tests terminés. Résultats disponibles dans 'tests_pdf/'.")
