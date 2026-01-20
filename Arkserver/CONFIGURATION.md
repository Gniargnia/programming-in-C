# Configuration ARK - Clarifications importantes

## Comment ARK charge la carte et les mods

### 🗺️ **Carte (Map)**

**Méthode utilisée :** Argument de ligne de commande

```bash
# ark-core.sh lit current_map
MAP_NAME=$(cat /home/arkserver/arkserver/config/current_map)

# Lance le serveur avec la carte
./ShooterGameServer TheIsland?SessionName=... -server -log
```

**Ce qui ne fonctionne PAS :**
- ❌ `ServerMap=TheIsland` dans GameUserSettings.ini (n'existe pas)
- ❌ Fichier `map.txt` quelque part

**Ce qui fonctionne :**
- ✅ `current_map` lu par ark-core.sh
- ✅ Passé comme premier argument au binaire

---

### 🔧 **Mods**

**Méthode utilisée :** Option `-mods=` en ligne de commande

```bash
# ark-core.sh génère automatiquement depuis mods.list
MOD_IDS="731604991,1404697612"  # Extrait de mods.list
./ShooterGameServer TheIsland?... -server -log -mods=731604991,1404697612
```

**Fichier mods.list (format) :**
```
731604991|Structures Plus
1404697612|Awesome Spyglass
```

**Ce qui ne fonctionne PAS :**
- ❌ `GameModIds=731604991,1404697612` dans GameUserSettings.ini
- ❌ `ActiveMods=` dans GameUserSettings.ini

**Ce qui fonctionne :**
- ✅ `mods.list` (ID|NAME format)
- ✅ Converti automatiquement en `-mods=` par ark-core.sh au démarrage
- ✅ Les mods doivent être téléchargés dans `/home/arkserver/Steam/steamapps/workshop/content/346110/`

---

## Flux de démarrage ARK

```
1. systemctl start ark-core.service
   ↓
2. ark-core.sh s'exécute
   ↓
3. Lit current_map → MAP_NAME="TheIsland"
   ↓
4. Lit mods.list → génère MODS_FLAG="-mods=731604991,1404697612"
   ↓
5. Lit settings.conf → SESSION_NAME, ports, EXTRA_FLAGS, etc.
   ↓
6. Lance : ShooterGameServer TheIsland?SessionName=...&MaxPlayers=20 -server -log -mods=... -NoBattlEye
   ↓
7. ARK démarre et lit GameUserSettings.ini pour les paramètres de gameplay
```

---

## GameUserSettings.ini - À quoi sert-il vraiment ?

**Ce fichier configure :**
- ✅ Paramètres de jeu (multiplicateurs XP, récolte, apprivoisement)
- ✅ Paramètres graphiques serveur
- ✅ Configuration avancée (loot drops, spawns, etc.)
- ✅ Mots de passe (mais aussi passés en ligne de commande pour override)

**Ce fichier ne configure PAS :**
- ❌ La carte à charger
- ❌ Les mods à activer
- ❌ Les ports réseau (bien que certains paramètres puissent s'y trouver)

---

## Architecture complète

```
Démarrage serveur
├── current_map          → Quelle carte charger
├── mods.list            → Quels mods activer (converti en -mods=)
├── settings.conf        → Ports, session name, passwords (ligne de commande)
└── GameUserSettings.ini → Paramètres de gameplay (lu par ARK au runtime)
```

---

## Conséquences pour le menu Python

### ✅ **Changement de carte**
```python
# Écrire dans current_map
with open("/home/arkserver/arkserver/config/current_map", "w") as f:
    f.write("Ragnarok")

# Redémarrer le serveur pour appliquer
```

### ✅ **Gestion des mods**
```python
# Modifier mods.list (format ID|NAME)
with open("/home/arkserver/arkserver/config/mods.list", "w") as f:
    f.write("731604991|Structures Plus\n")
    f.write("1404697612|Awesome Spyglass\n")

# Télécharger les mods
subprocess.run(["bash", "/home/arkserver/arkserver/core/ark-mods.sh", "update"])

# Redémarrer le serveur pour activer
```

### ✅ **Modification des paramètres**
```python
# Utiliser le parser INI pour GameUserSettings.ini
parser = ArkINIParser("/path/to/GameUserSettings.ini")
parser.set_value("ServerSettings", "XPMultiplier", "2.0")
parser.write()

# Redémarrer le serveur pour appliquer
```

---

## Résumé

| Élément | Fichier | Comment c'est chargé |
|---------|---------|---------------------|
| **Carte** | `current_map` | Argument CLI (TheIsland?...) |
| **Mods** | `mods.list` | Converti en `-mods=ID,ID` |
| **Session/Ports** | `settings.conf` | Arguments CLI (?SessionName=...&Port=...) |
| **Gameplay** | `GameUserSettings.ini` | Lu par ARK au runtime |
| **Avancé** | `Game.ini` | Lu par ARK au runtime |
