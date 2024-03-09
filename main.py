
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import models
from kivy.app import App
from kivy.config import Config
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics', 'width', '380')
Config.set('graphics', 'height', '750')


class Header(BoxLayout):
    logo = StringProperty("images/groupe_blanc.png")
    title = StringProperty(" I.PS")


class Footer(BoxLayout):
    copy = StringProperty("Copyright 2024 @ Tous droits resevés!")


class MenuPrincipal(BoxLayout):

    description = StringProperty("IPS, Interpréteur de Performance de Sport, Est une application mobile qui vous aide "
                                 "dans l'interprétation des performance en sport de vos élèves à l'école priamire.")
    copy = StringProperty("Copyright 2024 @ Tous droits resevés!")

    sexe_feminin_state = StringProperty("normal")
    sexe_masculin_state = StringProperty("normal")
    sexe = StringProperty(None)
    # tranche_age = StringProperty(None)
    sex_fille = BooleanProperty(True)
    tranche_age = NumericProperty()
    tranche1_state = StringProperty("normal")
    tranche2_state = StringProperty("normal")
    tranche3_state = StringProperty("normal")
    performance_vitesse_str = StringProperty("00:00")
    performance_vitesse_int = NumericProperty()
    performance_saut_str = StringProperty("0.0")
    performance_saut_int = NumericProperty()

    note_vitesse = StringProperty("0")
    note_longueur = StringProperty("0")
    total_note = StringProperty("0")
    moyenne_sur_10 = StringProperty("0")

    message_erreur = StringProperty("")

    age = NumericProperty()

    def auto_insert_apostroph(self, discipline):
        if discipline == "vitesse":
            if len(self.performance_vitesse_str) == 2:
                self.performance_vitesse_str = self.performance_vitesse_str + "'"
        elif discipline == "longueur":
            if len(self.performance_saut_str) == 1:
                self.performance_saut_str = self.performance_saut_str + '.'

    @staticmethod
    def message_box(titre, message):
        msg = Label(text=message)
        msgbox = Popup(title=titre, content=msg, size_hint=(None, None),
                       size=(360, 200), background='atlas://data/images/defaulttheme/button')
        msgbox.open()

    def get_athlete_sexe(self, widget):
        if not widget.state == "normal":
            self.sexe = widget.text
            if self.sexe == "Fille":
                self.sexe_feminin_state = "down"
                self.sexe_masculin_state = "normal"
                self.sex_fille = True
            else:
                self.sexe_masculin_state = "down"
                self.sexe_feminin_state = "normal"
                self.sex_fille = False

    # Cette méthode gère la selection de la tranche d'âge.
    def get_athlete_age_tranche(self, widget, tranche):
        if widget.state == "down":
            self.tranche_age = tranche
            if self.tranche_age == 1:
                self.tranche1_state = "down"
                self.tranche2_state = "normal"
                self.tranche3_state = "normal"
                self.age = 11
            elif self.tranche_age == 2:
                self.tranche1_state = "normal"
                self.tranche2_state = "down"
                self.tranche3_state = "normal"
                self.age = 13
            else:
                self.tranche1_state = "normal"
                self.tranche2_state = "normal"
                self.tranche3_state = "down"
                self.age = 15  # if self.sexe = "Fille" else 16

    # Récupération des performances saisies
    def get_performance_saisie(self, widget, discipline):
        if discipline == "vitesse":
            self.performance_vitesse_str = widget.text.strip()
        else:
            self.performance_saut_str = widget.text.strip()

    # Cette méthode permet de vérifier la validité de la saisie de l'utilisateur
    def verify_performance(self):
        if not self.sexe:
            self.message_erreur = "Vous devez choisir le sexe avant de continuer!"
            titre = "IPS || Erreur de choix de sexe!"
            self.message_box(titre, self.message_erreur)
            return False
        if not self.tranche_age:
            self.message_erreur = "Vous devez choisir la tranche d'âge \navant de continuer!"
            titre = "IPS || Erreur de saisie!"
            self.message_box(titre, self.message_erreur)
            return False
        if len(self.performance_vitesse_str) == 0 and len(self.performance_saut_str) == 0:
            self.message_erreur = "Vous devez saisir les performances \navant de continuer!"
            titre = "IPS || Erreur de saisie!"
            self.message_box(titre, self.message_erreur)
            return False

        performance_split = [c for c in self.performance_vitesse_str]
        is_valid_performance_vitesse = (5 <= len(performance_split) <= 6) and ("'" in performance_split)

        performance_split = [c for c in self.performance_saut_str]
        is_valid_performance_saut = len(performance_split) == 4 and ("." in performance_split)

        if is_valid_performance_vitesse is True and is_valid_performance_saut is True:
            return True
        elif self.performance_vitesse_str.split("'")[0] == 0 or self.performance_saut_str.split(".")[0] == 0:
            self.message_erreur = "La performance ne doit pas être 0!"
            titre = "IPS || Erreur de saisie!"
            self.message_box(titre, self.message_erreur)
            return False
        else:
            self.message_erreur = "Votre saisie est incorrecte. \n Veuillez la reverifier SVP!"
            titre = "IPS || Erreur de saisie!"
            self.message_box(titre, self.message_erreur)
            return False

    # Cette méthode permet d'arrondir la moyenne calculée en suivant les règle
    # de calcul des note de sport à l'école primaire
    @staticmethod
    def round_moyenne(moyenne):
        moyenne_arrondi = 0.0
        moyenne_str = str(moyenne)
        moyenne_split = moyenne_str.split(".")

        if len(moyenne_split) == 2:
            decimal = int(moyenne_split[1])
            if decimal < 50:
                moyenne_arrondi = moyenne_split[0]
            elif decimal > 50:
                moyenne_arrondi = int(moyenne_split[0])+1
            else:
                moyenne_arrondi = moyenne
            return moyenne_arrondi
        else:
            return moyenne

    # Cette méthode gère le click du boutton interpréter
    # Et permet d'appeler la méthode qui vérifie la saisie de l'utilisateur
    # Si la saisie est correcte, c'est à dire qu'il y a au moins 5 caractère dont un "'", alors,
    # On apelle la méthode interpréter_performance de la classe bareme qui rétourne la note
        
    def interpreter(self):
        res = self.verify_performance()
        if res is True:
            self.note_vitesse = str(models.Bareme.interpreter_performance("vitesse", self.sexe, self.age,
                                                                          self.performance_vitesse_str))
            self.note_longueur = str(models.Bareme.interpreter_performance("longeur", self.sexe, self.age,
                                                                           self.performance_saut_str))
            total = int(self.note_vitesse) + int(self.note_longueur)
            self.total_note = str(total)
            moyenne = total / 4
            self.moyenne_sur_10 = str(self.round_moyenne(str(moyenne)))


# Classe principal du programme.
class IPSApp(App):
    pass


#*********************************************************************************
#Lancement de l'application
if __name__== "__main__":
    IPSApp().run()

#*********************************************************************************