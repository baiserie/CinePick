import csv
import os
import random
import time
import datetime
import platform
import webbrowser

WATCHLIST_FILE = "watchlist.csv"
HISTORIQUE_FILE = "films_deja_vus.csv"
FAVORIS_FILE = "favoris.txt"
DERNIER_FILM_FILE = "dernier_film.txt"
SCORE_FILE = "score.txt"

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def charger_watchlist():
    films = []
    if not os.path.exists(WATCHLIST_FILE):
        print(f"{RED}⚠️ Le fichier {WATCHLIST_FILE} est introuvable.{RESET}")
        return films
    with open(WATCHLIST_FILE, newline="", encoding="utf-8") as csvfile:
        lecteur = csv.DictReader(csvfile)
        for ligne in lecteur:
            films.append(ligne)
    return films


def charger_historique():
    if not os.path.exists(HISTORIQUE_FILE):
        return set()
    with open(HISTORIQUE_FILE, newline="", encoding="utf-8") as csvfile:
        lecteur = csv.DictReader(csvfile)
        return set(ligne["Name"] for ligne in lecteur)


def sauvegarder_historique(film):
    fichier_existe = os.path.exists(HISTORIQUE_FILE)
    with open(HISTORIQUE_FILE, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Year", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not fichier_existe:
            writer.writeheader()
        writer.writerow({
            "Name": film["Name"],
            "Year": film.get("Year", ""),
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


def charger_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    with open(SCORE_FILE, "r") as f:
        try:
            return int(f.read())
        except:
            return 0


def ajouter_score(points=1):
    score = charger_score() + points
    with open(SCORE_FILE, "w") as f:
        f.write(str(score))
    return score


def choisir_film(films, deja_vus):
    clear_terminal()
    films_restants = [f for f in films if f["Name"] not in deja_vus]
    if not films_restants:
        print(f"{GREEN}🎉 Tu as épuisé toute ta watchlist !{RESET}")
        return None

    print(f"{YELLOW}🎲 Tirage en cours...{RESET}")
    for _ in range(5):
        print("➡️", random.choice(films_restants)["Name"])
        time.sleep(0.3)

    film = random.choice(films_restants)
    print(f"\n{CYAN}🎬 Film choisi : {film['Name']} ({film.get('Year','?')}){RESET}")
    with open(DERNIER_FILM_FILE, "w", encoding="utf-8") as f:
        f.write(film["Name"])
    return film


def valider_film(films):
    if not os.path.exists(DERNIER_FILM_FILE):
        print(f"{YELLOW}ℹ️ Aucun film en attente.{RESET}")
        return
    with open(DERNIER_FILM_FILE, "r", encoding="utf-8") as f:
        nom_film = f.read().strip()
    film = next((f for f in films if f["Name"] == nom_film), None)
    if film:
        sauvegarder_historique(film)
        score = ajouter_score()
        print(f"{GREEN}✅ Film validé ! Score actuel : {score}{RESET}")
    else:
        print(f"{RED}⚠️ Film introuvable dans la watchlist.{RESET}")
    os.remove(DERNIER_FILM_FILE)


def voir_sur_letterboxd(film):
    url = film.get("Letterboxd URI")
    if url:
        print(f"🌐 Ouverture de {film['Name']} sur Letterboxd...")
        webbrowser.open(url)
    else:
        print("⚠️ Aucun lien Letterboxd disponible pour ce film.")


def top5(films, deja_vus):
    clear_terminal()
    films_restants = [f for f in films if f["Name"] not in deja_vus]
    if len(films_restants) < 5:
        print(f"{RED}⚠️ Moins de 5 films restants.{RESET}")
        return
    choix = random.sample(films_restants, 5)
    print(f"\n{GREEN}⭐ Voici 5 films au hasard :{RESET}")
    for i, film in enumerate(choix, 1):
        print(f"{i}. {film['Name']} ({film.get('Year','?')})")


def main():
    films = charger_watchlist()
    if not films:
        return

    while True:
        clear_terminal()
        film_verrouille = None
        if os.path.exists(DERNIER_FILM_FILE):
            with open(DERNIER_FILM_FILE, "r") as f:
                nom_film = f.read().strip()
            film_verrouille = next((f for f in films if f["Name"] == nom_film), None)

        deja_vus = charger_historique()
        score = charger_score()

        print(f"{BOLD}{CYAN}🎬 MENU PRINCIPAL (Score : {score}){RESET}")
        print("1) Tirer un film aléatoire")
        print("2) Valider le film actuel")
        print("3) Relancer le dernier film tiré")
        print("4) Tirer un Top 5 aléatoire")
        print("5) Voir un film sur Letterboxd")
        print("6) Quitter")
        print("====================================")

        choix = input("👉 Ton choix : ").strip()

        if choix == "1":
            if film_verrouille:
                print(f"{RED}❌ Tu dois d'abord regarder le film verrouillé : {film_verrouille['Name']}{RESET}")
            else:
                film = choisir_film(films, deja_vus)
                if film:
                    print("\n💡 Options :")
                    print("f = Ajouter aux favoris")
                    print("l = Voir sur Letterboxd")
                    choix_option = input("Que veux-tu faire ? ").strip().lower()
                    if choix_option == "f":
                        with open(FAVORIS_FILE, "a") as f:
                            f.write(film["Name"] + "\n")
                        print(f"{GREEN}💖 Film ajouté aux favoris.{RESET}")
                    elif choix_option == "l":
                        voir_sur_letterboxd(film)
            input("Appuie sur Entrée pour continuer...")
        elif choix == "2":
            valider_film(films)
            input("Appuie sur Entrée pour continuer...")
        elif choix == "3":
            if film_verrouille:
                print(f"{CYAN}🎬 Film verrouillé : {film_verrouille['Name']}{RESET}")
            else:
                print(f"{YELLOW}ℹ️ Aucun film verrouillé actuellement.{RESET}")
            input("Appuie sur Entrée pour continuer...")
        elif choix == "4":
            top5(films, deja_vus)
            input("Appuie sur Entrée pour continuer...")
        elif choix == "5":
            if film_verrouille:
                voir_sur_letterboxd(film_verrouille)
            else:
                print(f"{YELLOW}ℹ️ Aucun film à ouvrir.{RESET}")
            input("Appuie sur Entrée pour continuer...")
        elif choix == "6":
            print(f"{GREEN}👋 À bientôt !{RESET}")
            break
        else:
            print(f"{RED}❌ Choix invalide.{RESET}")
            time.sleep(1)

