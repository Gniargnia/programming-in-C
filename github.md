# 🧠 Git — Guide CLI Essentiel (Codespaces & Local)

## 📌 Configuration initiale

git config --global user.name "Ton Nom"
git config --global user.email "ton@email.com"

Vérifier :
git config --list

---

## 📁 Créer ou cloner un dépôt

Initialiser un dépôt :
git init

Cloner un dépôt existant :
git clone https://github.com/user/repo.git

---

## 📊 État du dépôt

git status

Afficher les différences :
git diff

---

## ➕ Ajouter des fichiers

Ajouter un fichier précis :
git add fichier.c

Ajouter tout :
git add .

---

## 💾 Commit

git commit -m "Message clair et précis"

Ajouter + commit en une fois (fichiers déjà suivis) :
git commit -am "Message"

---

## 🔄 Synchronisation avec GitHub

Envoyer les commits :
git push

Récupérer les changements :
git pull

---

## 🌿 Branches

Lister les branches :
git branch

Créer une branche :
git branch nouvelle-branche

Changer de branche :
git checkout nouvelle-branche

Créer + changer :
git checkout -b nouvelle-branche

---

## 🔀 Fusion (merge)

git checkout main
git merge nouvelle-branche

---

## 🧹 Annuler / corriger

Annuler un fichier modifié (non ajouté) :
git restore fichier.c

Retirer un fichier du staging :
git restore --staged fichier.c

Modifier le dernier commit :
git commit --amend

---

## 🗑️ Supprimer des fichiers

Supprimer du dépôt :
git rm fichier.c

Supprimer sans effacer localement :
git rm --cached fichier.c

---

## 📜 Historique

git log

Version compacte :
git log --oneline --graph --all

---

## 🧪 Travailler avec Docker / devcontainer

Modifier l’environnement :
- Modifier Dockerfile
- Modifier .devcontainer/

Puis :
git add Dockerfile .devcontainer
git commit -m "Update dev environment"
git push

Rebuild séparément :
- Codespaces → Rebuild Container
- Local → Reopen in Container

---

## 🚫 .gitignore recommandé

# Build
*.o
*.out
build/

# VS Code local
.vscode/

# OS
.DS_Store

Ne jamais ignorer :
- Dockerfile
- .devcontainer/

---

## 🔍 Vérifications utiles

Voir les fichiers suivis :
git ls-files

Voir les remotes :
git remote -v

---

## 🧠 Règles d’or

- Git synchronise le code
- Docker reconstruit l’environnement
- Codespaces et local sont indépendants
- Le dépôt est la source de vérité

---

## ✅ Workflow recommandé

git pull
# travailler
git add .
git commit -m "Feature / fix"
git push
