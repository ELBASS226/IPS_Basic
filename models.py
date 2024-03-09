import sqlite3
from datetime import date, datetime
import time
import os  
import msvcrt                                                 


def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


DATABASE = "IPS.db"


# ====================================================================================================================
# Cette classe gère uniquemnt la connexion à la base de données et fournie des méthodes
# d'accès à la base de données
class Connexion:
    # connexion = sqlite3.Connection(DATABASE)

    def __init__(self) -> None:
        pass

    def execut_sql(req):
        # Connexion à la base de données
        cnxion = sqlite3.Connection(DATABASE)
        curseur = cnxion.cursor()
        try:
            curseur.execute(req)
            cnxion.commit()
            res = True
        except:
            print("Erreur lors de la tentative de connexion à la base de données. Veuillez réessayer plus tard!")
            res = False
        return res
    
    def lister_donnees(req):
        data = []
        # Connexion à la base de données
        cnxion = sqlite3.Connection(DATABASE)
        curseur = cnxion.cursor()
        res = curseur.execute(req).fetchall()
        cnxion.close()
        return res

# ====================================================================================================================


# ====================================================================================================================
# Cette classe permet la gestion des barèmes dans la base de donnée
# Elle offre des méthodes permettant d'accéder à une performance donnée
class Bareme:
    def __init__(self, id_barem, p_course, p_saut, note_garcon_tranche1, note_garcon_tranche2,
                 note_garcon_tranche3, note_fille_tranche1, note_fille_tranche2, note_fille_tranche3):
        self.id = id_barem; self.P_Course = p_course; self.P_Saut = p_saut
        self.NoteG_T1 = note_garcon_tranche1; self.NoteG_T2 = note_garcon_tranche2; self.NoteG_T3 = note_garcon_tranche3
        self.NoteF_T1 = note_fille_tranche1; self.NoteF_T2 = note_fille_tranche2; self.NoteF_T3 = note_fille_tranche3
    
    # Méthode permettant d'ajouter une performance dans la table des barèmes
    def ajouter(self):
        req = f"INSERT INTO TBaremes (id,P_Course,P_Saut,NoteG_T1,NoteG_T2,NoteG_T3," +\
              f"NoteF_T1,NoteF_T2,NoteF_T3) Values({self.id},'{self.P_Course}', '{self.P_Course}',"+\
              f"{self.NoteG_T1}, {self.NoteG_T2}, {self.NoteG_T3}, {self.NoteF_T1}, {self.NoteF_T2}, {self.NoteF_T3})"
        if Connexion.execut_sql(req):
            pass
        else:
            print("Impossible!")

    # Cette méthode permet de modifier un barème dans la table des barèmes
    def modifier(self):
        req = f"UPDATE TBaremes SET P_Course = '{self.P_Course}', P_Saut = '{self.P_Course}',"+\
              f"NoteG_T1 = {self.NoteG_T1}, NoteG_T2 = {self.NoteG_T2}, NoteG_T3 = {self.NoteG_T3},"+\
              f"NoteF_T1 = {self.NoteF_T1}, NoteF_T2 = {self.NoteF_T2}, NoteF_T3 = {self.NoteF_T3}) WHERE id ={self.id}"
        if Connexion.execut_sql(req):
            print("Barème modifié avec succès!")
        else:
            print("Impossible de modifier le barème!")

    # Cette méthode permet de supprimer un barème dans la table des barèmes
    def supprimer(self):
        req = f"DELETE FROM TBaremes WHERE id = {self.id}"
        if Connexion.execut_sql(req):
            print("Barème supprimé avec succès!")
        else:
            print("Impossible de supprimer le barème!")
    
    # Cette méthode Affiche le barème de notation
    @staticmethod
    def afficher():
        req = "SELECT * FROM TBaremes"
        baremes = Connexion.lister_donnees(req)
        print("N°   Course      Saut        -12ans(G)       12,13ans(G)")
        for bareme in baremes:
            print(str(bareme[0]).zfill(2), "     ", str(bareme[1]).zfill(4), "    ", bareme[2], "      ", \
                  str(bareme[3]).zfill(2), "     ", str(bareme[4]).zfill(2), "    ", str(bareme[5]).zfill(2), \
                  "    ", str(bareme[6]).zfill(2), "       ", str(bareme[7]).zfill(2), "      ", str(bareme[8]).zfill(2))

    # Cette méthode permet d'obtenir une performance valide:
    # En effet, toutes les performances n'existant pas dans le tableau de barème ,
    # La règle dit que si une performance n'existe pas, se repporter à la performance inférieure:
    # Pour la vitesse, pour obtenir la performance inférieure, on ajoute des tiers.
    # Mais pour le saut , on enlève des centimètres.
    @staticmethod
    def get_performance_valid(discipline, performance):
        if discipline.lower() == "vitesse":
            req = "SELECT P_Course FROM TBaremes"
            performance_int = int(performance.replace("'", ""))
            performances_str = Connexion.lister_donnees(req)

            try:
                performances_int = [int(performances_str[i][0].replace("'", "")) for i in range(len(performances_str))]
            except:
                return -1  # La conversion a rencontré un problème

            while performance_int not in performances_int:
                performance_int += 1  # Permet de descendre vers la performance inférieure!
            return performance_int

        else:
            req = "SELECT P_Saut FROM TBaremes"
            performance_int = int(performance.replace(".", ""))
            performances_str = Connexion.lister_donnees(req)
            performances_int = [int(performances_str[i][0].replace(".", "")) for i in range(len(performances_str))]

            while performance_int not in performances_int:
                performance_int -= 1  # Permet de descendre vers la performance inférieure!
            return performance_int

    # Cette méthode recoit en entrée une discipline 'vitesse' ou saut , le sexe et l'âge d'un athlète et renvoie
    # la note correspondante à sa performance.
    # Elle fait appelle à la méthode get_performance_valid() pour obtenir une performance valide
    @staticmethod
    def interpreter_performance(discipline, sexe, age, performance):
        performance = Bareme.get_performance_valid(discipline, performance)  # Pour obtenir une performance valide
        if discipline.lower() == "vitesse":
            if sexe.lower() == "garçon":  # l'athlète est un garçon
                if int(age) < 12: 
                    # l'athlète est un garçon de moins de 12 ans
                    req = f"SELECT NoteG_T1 FROM TBaremes WHERE P_Course = {performance}"
                elif int(age) == 12 or int(age) == 13 or int(age) == 14: 
                    # l'athlète est un garçon de 12,13 ou 14 ans
                    req = f"SELECT NoteG_T2 FROM TBaremes WHERE P_Course = {performance}"               
                else: # l'athlète est un garçon de plus de 15 ans
                    req = f"SELECT NoteG_T3 FROM TBaremes WHERE P_Course = {performance}"

            else:  # l'athlète est une fille
                if int(age) < 12:  # l'athlète est une fille de moins de 12 ans
                    req = f"SELECT NoteF_T1 FROM TBaremes WHERE P_Course = {performance}"
                elif int(age) == 12 or int(age) == 13 or int(age) == 14: 
                    # l'athlète est une fille de  12,13 ans
                    req = f"SELECT NoteF_T2 FROM TBaremes WHERE P_Course = {performance}"
                else:  # l'athlète est une fille de plus de 14 ans
                    req = f"SELECT NoteF_T3 FROM TBaremes WHERE P_Course = {performance}"

        else:  # Pour le saut
            if sexe.lower() == "garçon":  # l'athlète est un garçon
                if int(age) < 12:  # l'athlète est un garçon de moins de 12 ans
                    req = f"SELECT NoteG_T1 FROM TBaremes WHERE P_Saut = {performance}"
                elif int(age) == 12 or int(age) == 13 or int(age) == 14:  # l'athlète est un garçon de 12,13 ou 14 ans
                    req = f"SELECT NoteG_T2 FROM TBaremes WHERE P_Saut = {performance}"
                else: # l'athlète est un garçon de plus de 15 ans
                    req = f"SELECT NoteG_T3 FROM TBaremes WHERE P_Saut = {performance}"

            else:  # l'athlète est une fille
                if int(age) < 12:
                    req = f"SELECT NoteF_T1 FROM TBaremes WHERE P_Saut = {performance}"
                elif int(age) == 12 or int(age) == 13 or int(age) == 14:
                    req = f"SELECT NoteF_T2 FROM TBaremes WHERE P_Saut = {performance}"
                else:
                    req = f"SELECT NoteF_T3 FROM TBaremes WHERE P_Saut = {performance}"

        list_note = Connexion.lister_donnees(req)
        note = list_note[0][0]
        return note


# ====================================================================================================================


# ====================================================================================================================
class Athlete:
    def __init__(self, id_athlete, num_pv, nom, prenom, sexe, date_naissance) -> None:
        self.id = id_athlete
        self.num_pv = num_pv
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.date_naissance = date_naissance

    def ajouter(self):
        req = f"INSERT INTO TAthletes (id, num_pv, nom, prenom, sexe, date_naissance) " + \
              f"values({self.id},'{self.num_pv}','{self.nom}','{self.prenom}','{self.sexe}','{self.date_naissance}')"
        if Connexion.execut_sql(req):
            print("Athlète ajouté avec succès!")
        else:
            print("Impossible d'ajouter cet athlète!")

    # Cette méthode permet de modifier un athlète dans la table des athlètes
    def modifier(self):
        req = f"UPDATE TAthletes SET num_pv = '{self.num_pv}', nom = '{self.nom}'," + \
              f"prenom = {self.prenom}, sexe = {self.sexe}, date_naissance = {self.date_naissance},WHERE id ={self.id}"
        if Connexion.execut_sql(req):
            print("Athlète modifié avec succès!")
        else:
            print("Impossible de modifier ce athlète!")

    # Cette méthode permet de supprimer un athlète dans la table des TAthletes
    def supprimer(self):
        req = f"DELETE FROM TAthletes WHERE id = {self.id}"
        if Connexion.execut_sql(req):
            print("Athlète supprimé avec succès!")
        else:
            print("Impossible de supprimer cet athlète!")

    # Cette méthode permet de lister les athlètes
    @staticmethod
    def lister():
        req = "SELECT * FROM TAthletes"
        athletes = Connexion.lister_donnees(req)
        for a in athletes:
            params =[a[i] for i in range(len(a))]
            print(*params)

    def afficher_infos(self):
        print(f"Numéro PV: {self.num_pv}")
        print(f"Nom: {self.nom}")
        print(f"Prénom: {self.prenom}")
        print(f"Sexe: {self.sexe}")
        print(f"Date de Naissance: {self.date_naissance}")

    def retourner_infos_eleve(self):
        return {
            "num_pv": self.num_pv,
            "nom": self.nom,
            "prenom": self.prenom,
            "sexe": self.sexe,
            "date_naissance": self.date_naissance,
        }

    # Fonction permettant de vérifier si un élève a l'age scolaire
    # On considère ici que l'age scolaire est de 6 ans le cas du Burkina Faso
    def get_date_naissance_valide(self):
        date_valide = ""
        # vérifions si la date de naissance est sous format date
        if len(self.date_naissance) == 0:
            date_valide = date.today()
        elif len(self.date_naissance) < 10:
            date_valide = self.date_naissance.replace("En ", "") + '-12-31'
        else:
            date_valide = self.date_naissance
        return datetime.strptime(date_valide.replace("/", "-"), "%d-%m-%Y").date()

    # Cette fonction permet de calculer l'age d'un élève connaissant
    # Sa date de naissance.
    def calculer_age(self):
        annee_actuel = date.today()
        annee_naissance= self.get_date_naissance_valide()
        # calcul de l'age de l'élève
        age = annee_actuel - annee_naissance
        age = divmod(age.days, 365)[0]
        """ La division entière du nombre total de jour donne le nombre d'année
        et le nombre de jours restants. [0] permet de recupperer l'année et [1]
        Permet de recuperer le reste des jours."""
        return age
    

# ====================================================================================================================
class Evaluation(Athlete):
    def __init__(self, id_eval, id_athlete, p_vitesse, p_saut1, p_saut2, p_saut3, meilleur_saut,
                 note_course, note_saut, moyenne) -> None:
        self.id_eval = id_eval; self.p_vitesse = p_vitesse
        self.id_athlete = id_athlete
        self.p_saut1 = p_saut1; self.p_saut2 = p_saut2
        self.p_saut3 = p_saut3; self.meilleur_saut = meilleur_saut
        self.note_course = note_course; self.note_saut = note_saut
        self.moyenne = moyenne

    def ajouter(self):
        req = f"INSERT INTO TEvaluations (id_athlete, p_vitesse, p_saut1, p_saut2, p_saut3, meilleur_saut, " + \
              f"note_course, note_saut,moyenne) values({self.id_athlete}, '{self.p_vitesse }','{self.p_saut1}'," + \
              f"'{self.p_saut2}','{self.p_saut3}','{self.meilleur_saut}', {self.note_course},{self.note_saut}," + \
              f"{self.moyenne})"
        if Connexion.execut_sql(req):
            print("Evaluation ajoutée avec succès!")
        else:
            print("Impossible d'ajouter cette évaluation!" )

    @staticmethod
    def lister_athltes():
        Athlete.lister()
        athlete_choisi = input("Veuillez entrer l'ID de l'athlète")
        res = Connexion.lister_donnees(f"SELECT * FROM TAthletes WHERE id = {athlete_choisi}")
        a = res[0]
        athlete = Athlete(*a)
        print()
        athlete.afficher_infos()


def get_performance():
    performances = []
    temps_debut = time.time()
    while True:
        temps_actuel = time.time() - temps_debut
        minute, seconde = divmod(temps_actuel, 60)
        seconde, tiers = divmod(seconde, 1)
        tiers = int(tiers * 1e2)
        print(f"Temps total écoulé {int(minute)} : {int(seconde)} : {int(tiers)}", end='\r')
        if msvcrt.kbhit() and ord(msvcrt.getch()) == 13:
            performances.append(f"{int(minute)} : {int(seconde)} : {int(tiers)}")
            print(performances)
            return performances[0]


# ====================================================================================================================
# Utilisation de la classe
"""a = Athlete(2, "1286", "Ouedraogo", "Salamata", "F", "14/11/2011")
Evaluation.lister_athltes()

pv=get_performance()
e = Evaluation(1, a.id, pv, "340", "250", "365", "365", 10, 12, 11.0)

e.ajouter()"""
