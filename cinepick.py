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
    with open(DERNIER_FILM_FILE, "w", encoding="utf-8") as f:
        f.write(film["Name"])


def choisir_film(films, deja_vus):
    clear_terminal()
    films_restants = [f for f in films if f["Name"] not in deja_vus]
    if not films_restants:
        print(f"{GREEN}🎉 Tu as épuisé toute ta watchlist !{RESET}")
        return None, films_restants

    print(f"{YELLOW}🎲 Tirage en cours...{RESET}")
    for _ in range(5):
        print("➡️", random.choice(films_restants)["Name"])
        time.sleep(0.3)

    film = random.choice(films_restants)
    print(f"\n{CYAN}🎬 Film choisi : {film['Name']} ({film.get('Year','?')}){RESET}")
    print(f"{MAGENTA}📌 Films restants : {len(films_restants)-1}{RESET}")
    sauvegarder_historique(film)
    return film, films_restants


def relancer_dernier():
    clear_terminal()
    if not os.path.exists(DERNIER_FILM_FILE):
        print(f"{YELLOW}ℹ️ Aucun film n’a encore été tiré.{RESET}")
        return
    with open(DERNIER_FILM_FILE, "r", encoding="utf-8") as f:
        dernier = f.read().strip()
    print(f"{CYAN}🔁 Dernier film tiré : {dernier}{RESET}")


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


def ajouter_favori(film):
    with open(FAVORIS_FILE, "a", encoding="utf-8") as f:
        f.write(film["Name"] + "\n")
    print(f"{GREEN}💖 {film['Name']} ajouté aux favoris.{RESET}")


def voir_favoris():
    clear_terminal()
    if not os.path.exists(FAVORIS_FILE):
        print(f"{YELLOW}ℹ️ Aucun favori enregistré.{RESET}")
        return
    with open(FAVORIS_FILE, "r", encoding="utf-8") as f:
        favoris = f.readlines()
    print(f"\n{MAGENTA}💖 Tes favoris :{RESET}")
    for fav in favoris:
        print(" -", fav.strip())


def voir_sur_letterboxd(film):
    url = film.get("Letterboxd URI") 
    if url:
        print(f"🌐 Ouverture de {film['Name']} sur Letterboxd...")
        webbrowser.open(url)
    else:
        print("⚠️ Aucun lien Letterboxd disponible pour ce film.")


def reinitialiser_historique():
    clear_terminal()
    if os.path.exists(HISTORIQUE_FILE):
        os.remove(HISTORIQUE_FILE)
    if os.path.exists(DERNIER_FILM_FILE):
        os.remove(DERNIER_FILM_FILE)
    print(f"{GREEN}✅ Historique réinitialisé.{RESET}")


def afficher_menu():
    clear_terminal()
    print(f"""
{BOLD}{CYAN}=========== 🎬 MENU PRINCIPAL 🎬 ==========={RESET}
{YELLOW}1){RESET} Tirer un film aléatoire
{YELLOW}2){RESET} Relancer le dernier film tiré
{YELLOW}3){RESET} Tirer un Top 5 aléatoire
{YELLOW}4){RESET} Voir mes favoris
{YELLOW}5){RESET} Réinitialiser l’historique
{YELLOW}6){RESET} Quitter
{BOLD}{CYAN}============================================{RESET}
""")


def main():
    films = charger_watchlist()
    if not films:
        return

    while True:
        afficher_menu()
        choix = input("👉 Ton choix : ").strip()
        deja_vus = charger_historique()

        if choix == "1":
            film, restants = choisir_film(films, deja_vus)
            if film:
                print("\n💡 Options :")
                print("f = Ajouter aux favoris")
                print("l = Voir sur Letterboxd")
                choix_option = input("Que veux-tu faire ? ").strip().lower()
                if choix_option == "f":
                    ajouter_favori(film)
                elif choix_option == "l":
                    voir_sur_letterboxd(film)
            input(f"\n{YELLOW}Appuie sur Entrée pour revenir au menu...{RESET}")
        elif choix == "2":
            relancer_dernier()
            input(f"\n{YELLOW}Appuie sur Entrée pour revenir au menu...{RESET}")
        elif choix == "3":
            top5(films, deja_vus)
            input(f"\n{YELLOW}Appuie sur Entrée pour revenir au menu...{RESET}")
        elif choix == "4":
            voir_favoris()
            input(f"\n{YELLOW}Appuie sur Entrée pour revenir au menu...{RESET}")
        elif choix == "5":
            reinitialiser_historique()
            input(f"\n{YELLOW}Appuie sur Entrée pour revenir au menu...{RESET}")
        elif choix == "6":
            print(f"{GREEN}👋 À bientôt !{RESET}")
            break
        else:
            print(f"{RED}❌ Choix invalide. Tape 1-6.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
