/home/arkserver/arkserver/
│
├── core/                          ← Tous les scripts système (Bash)
│   ├── ark-core.sh                ← Start/verif (génère -mods= depuis mods.list)
│   ├── ark-backup.sh              ← Backups fast/daily/boot/prestop
│   ├── ark-mods.sh                ← Update mods via SteamCMD
│   ├── ark-stop.sh                ← Stop clean
│   └── ark-update-check.sh        ← Update ARK
│
├── manager/                       ← Le menu Python et ses modules
│   ├── menu.py                    ← Menu principal
│   ├── modules/
│   │   ├── server.py              ← Start/stop/status via Python
│   │   ├── backups.py             ← Gestion des backups
│   │   ├── updates.py             ← Update ARK + mods
│   │   ├── diagnostics.py         ← Logs, CPU, RAM, disque
│   │   └── config/
│   │       ├── maps.py            ← Gestion des cartes
│   │       ├── settings.py        ← GameUserSettings.ini
│   │       └── mods.py            ← Gestion des mods (ID + nom)
│   │
│   └── utils/
│       ├── ini_parser.py          ← Lecture/écriture INI propre
│       └── paths.py               ← Chemins centralisés
│
├── config/                        ← Fichiers de configuration ARK
│   ├── current_map                ← Carte active (lu par ark-core.sh)
│   ├── mods.list                  ← ID|Nom du mod (converti en -mods= au démarrage)
│   ├── settings.conf              ← Config serveur (ports, passwords, EXTRA_FLAGS)
│   ├── GameUserSettings.ini       ← Config ARK (paramètres de jeu)
│   └── Game.ini                   ← Config avancée ARK
│
├── backups/                       ← Tous les backups
│   ├── fast/                      ← 200 backups incrémentaux (fait)
│   ├── daily/                     ← 30 backups complets (fait)
│   ├── boot/                      ← 10 backups au démarrage (fait)
│   └── prestop/                   ← 10 backups avant arrêt (fait)
│
├── ShooterGame/                   ← Dossier ARK officiel
│   └── Saved/                     ← Sauvegardes du jeu
│
└── logs/                          ← (Optionnel) logs propres
    ├── core.log                   ← Logs du script core
    ├── backup.log                 ← Logs des backups
    └── mods.log                   ← Logs des updates mod