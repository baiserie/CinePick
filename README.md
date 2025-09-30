# 🎬 CinePick

**CinePick** est un script Python pratique pour t'aider à décider **quel film regarder** dans ta watchlist Letterboxd.
Fini la paralysie du choix ! 🍿

---

## 🌟 Fonctionnalités

* 🎲 **Tirage aléatoire de film** depuis ta watchlist CSV.
* 🔒 **Film verrouillé** : tu ne peux pas tirer un nouveau film tant que tu n'as pas validé le précédent.
* ⭐ **Top 5 aléatoire** pour avoir une sélection rapide.
* 💖 **Favoris** : ajoute tes films préférés pour y revenir facilement.
* 📊 **Historique** : garde une trace des films déjà regardés.
* 🎯 **Gamification / Score** : chaque film validé augmente ton score.
* 🌐 **Letterboxd intégré** : ouvre directement la page du film.
* 🖌️ **Menu coloré et terminal nettoyé** pour une meilleure lisibilité.

---

## 📝 Prérequis

* Python 3.x
* Modules standards : `csv`, `os`, `random`, `time`, `datetime`, `platform`, `webbrowser`

---

## 📂 Structure du projet

```
CinePick/
├─ watchlist.csv             # Ta watchlist exportée depuis Letterboxd
├─ cinepick.py               # Script Python principal
├─ films_deja_vus.csv        # Historique généré automatiquement
├─ dernier_film.txt          # Film verrouillé en cours
├─ favoris.txt               # Tes favoris
├─ score.txt                 # Score des films validés
└─ README.md
```

---

## 📝 Format CSV attendu

Le CSV Letterboxd doit contenir **exactement ces colonnes** :

```
Date,Name,Year,Letterboxd URI
```

Exemple :

| Date       | Name       | Year | Letterboxd URI                                                                     |
| ---------- | ---------- | ---- | ---------------------------------------------------------------------------------- |
| 2025-01-01 | Inception  | 2010 | [https://letterboxd.com/film/inception/](https://letterboxd.com/film/inception/)   |
| 2025-02-15 | The Matrix | 1999 | [https://letterboxd.com/film/the-matrix/](https://letterboxd.com/film/the-matrix/) |

---

## 🚀 Comment exporter sa watchlist depuis Letterboxd

1. Connecte-toi sur [Letterboxd](https://letterboxd.com).
2. Va dans **Profile → Films → Watchlist**.
3. Clique sur le bouton **Export** (souvent en bas de la page).
4. Télécharge le fichier **CSV** et place-le dans le même dossier que `cinepick.py`.

💡 Assure-toi que le CSV contient bien les colonnes : `Date,Name,Year,Letterboxd URI`.

---

## 🚀 Utilisation

1. Place `watchlist.csv` dans le même dossier que `cinepick.py`.
2. Lance le script :

```bash
python cinepick.py
```

3. Utilise le menu pour :

   * Tirer un film aléatoire (et ajouter aux favoris ou voir sur Letterboxd)
   * Valider le film actuel pour débloquer un nouveau tirage
   * Relancer le dernier film
   * Tirer un Top 5 aléatoire
   * Ouvrir le film sur Letterboxd
   * Quitter le programme

---

## 🎯 Astuces

* **Valide toujours les films** pour débloquer le tirage suivant et augmenter ton score.
* **Favoris** : consulte rapidement tes films préférés.
* **Gamification** : essaye de battre ton record de films validés par semaine !
