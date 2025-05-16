Jeu des 7 Familles – Édition Emoji

Bienvenue dans Seven_Families – Jeu des 7 Familles Emoji !
Un jeu de mémoire amusant développé en Python avec Tkinter pour l'interface graphique et Pygame pour la musique et les effets sonores.

Présentation du projet :

Ce projet est une adaptation numérique du classique jeu des 7 familles, utilisant des emojis pour représenter les membres des familles.
L'objectif est de former des familles complètes en demandant des cartes aux adversaires.

Le projet propose :

    7 familles différentes représentées par des emojis.

    Un système de tours alternés entre deux joueurs.

    Une ambiance sonore dynamique avec musique et effets sonores.

    Une interface graphique simple, intuitive et interactive.

    Une gestion du volume pour personnaliser l'expérience.

Technologies utilisées :

    Python 3

    Tkinter (interface graphique)

    Pygame (musique et sons)

    Playsound (version initiale pour certains sons simples)

Installation :

    Cloner le projet :
    git clone https://github.com/HxHadam/Repo-Hub-Priv-.git


Installer les dépendances : (Assurez-vous d'avoir pip installé.)

    pip install pygame

    Tkinter est intégré à Python sur la plupart des distributions standard (sinon installer python3-tk).

Lancer le jeu :

Dans le terminal, placez-vous dans le dossier du projet puis lancez :

python3 matchmojis.py

    Assurez-vous que les fichiers audio (bg_music.mp3, click.wav, correct.wav, fail.wav) soient bien présents dans le dossier ou sous un dossier assets/ si vous avez organisé les fichiers.

 Fonctionnalités principales :

    7 familles de 6 membres chacune avec des emojis uniques.

    Mémoire et stratégie : demandez les bons membres pour compléter vos familles.

    Système de tours : alternez pour demander des cartes.

    Effets sonores : clics, réussite, échec, musique de fond.

    Contrôle du volume intégré dans l'interface.

    Écran de victoire ou défaite avec possibilité de rejouer.

Organisation du projet : 

/sounds
    ├── bg_music.mp3
    ├── correct.wav
    └── fail.wav
Seven_Families.py
README.md
requirements.txt

User Stories (Résumé)

    Démarrer une partie via un bouton Start.

    Voir sa main de cartes sous forme d'emojis.

    Demander une carte à l'adversaire.

    Entendre un son lors de la réussite ou de l'échec.

    Ajuster le volume de la musique et des sons.

    Recevoir une notification en complétant une famille.

    Pouvoir recommencer une nouvelle partie après une victoire ou défaite.

(Voir le GitHub Project pour le détail complet des tâches)

Auteur:
HxHadam

Licence :
Projet open-source à but éducatif.

Notes importantes :

    Ce jeu est monojoueur pour l’instant (pas de multijoueur en réseau).

    Le projet est compatible avec Windows, Linux et Mac OS (avec Python3 et Tkinter).