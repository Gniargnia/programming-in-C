# Notes — Bash & C (CS50)

Objectif : avoir un mémo clair et réutilisable pendant les exercices.

---

## Bash (commandes utiles)

| Commande | Rôle |
|---|---|
| `cd` | changer de dossier |
| `ls` | lister le contenu |
| `mkdir` | créer un dossier |
| `touch` | créer un fichier vide |
| `cp` | copier |
| `mv` | déplacer / renommer |
| `rm` | supprimer un fichier |
| `rmdir` | supprimer un dossier vide |
| `code` | ouvrir un fichier dans VS Code |

### Code de sortie d’un programme

- `echo $?` : affiche le code de sortie du dernier programme.
  - `0` : succès.
  - autre valeur : erreur (souvent `1`).

---

## C — mémo rapide

### `printf` : formats courants

| Format | Type |
|---|---|
| `%c` | `char` |
| `%i` | `int` |
| `%li` | `long` |
| `%lld` | `long long` |
| `%f` | `float` / `double` |
| `%s` | chaîne C (`char *`) / `string` CS50 |

### Opérateurs logiques

- `&&` : ET
- `||` : OU

Exemple :
```c
if (c == 'y' || c == 'Y')
{
    // ...
}
```

### Boucles

- Boucle infinie (volontaire) :
```c
while (true)
{
    // ...
}
```

---

## Comparaisons (très important)

### Nombres / caractères

- `==` marche pour comparer `int`, `char`, `double`, etc.

### Chaînes de caractères

- On ne compare pas des chaînes avec `==` (ça compare des adresses, pas le contenu).
- Utiliser `strcmp(a, b)` (dans `<string.h>`).

Rappel `strcmp` :
- retourne `0` si les deux chaînes sont égales
- retourne `< 0` si `a` est “avant” `b`
- retourne `> 0` si `a` est “après” `b`

Exemple :
```c
if (strcmp(nom, "stop") == 0)
{
    // égal
}
```

---

## Constantes

- `const` : empêche la modification.
- Convention : constantes en MAJUSCULES.

```c
const int N = 3;
```

---

## Tableaux

### Taille d’un tableau (cas “simple”)

Quand tu as **un vrai tableau** (pas un pointeur) :

```c
int a[10];
int n = sizeof(a) / sizeof(a[0]);
```

- `sizeof(a)` = taille totale en octets.
- `sizeof(a[0])` = taille d’un élément.
- Donc $n$ = nombre d’éléments.

### Attention : tableau vs pointeur

- Dans une fonction, un paramètre `int a[]` se comporte comme un `int *`.
- Donc `sizeof(a)` dans la fonction donnera la taille du **pointeur**, pas du tableau.

### Remarque sur `int numbers[N];`

- En C, `int numbers[N];` avec `N` lu à l’exécution est un **VLA** (Variable Length Array) : c’est un tableau “sur la pile” dont la taille dépend de `N`.
- Ce n’est pas une allocation dynamique `malloc`.

---

## Chaînes de caractères (strings)

### C “pur”

- Une chaîne est un tableau de `char` terminé par `\0` (NUL).
- Exemple : `"HI!"` correspond à : `72 73 33 0`.

```c
char s[] = "HI!";      // taille 4 : 'H' 'I' '!' '\0'
int len = strlen(s);   // 3 (ne compte pas le '\0')
```

### CS50 `string`

- En CS50, `string` est un alias de `char *`.
- `get_string(...)` te renvoie un pointeur vers une zone mémoire contenant la chaîne.

### Longueur vs capacité

- `strlen(s)` : longueur “utile” (nombre de caractères avant `\0`).
- `sizeof(...)` : taille en octets (utile seulement si tu as un tableau **statique** et accessible dans le même scope).

---

## Fonctions (rappel)

- Prototype (déclaration) avant `main`.
- Définition ensuite.

```c
int add(int a, int b);

int main(void)
{
    printf("%i\n", add(2, 3));
}

int add(int a, int b)
{
    return a + b;
}
```

---

## Pointeurs & mémoire (mini-mémo)

- Un pointeur contient une **adresse**.
- Les chaînes (`char *`) sont des pointeurs.

Deux pièges fréquents :
- `sizeof(ptr)` donne la taille du pointeur (souvent 8), pas la taille des données.
- Comparer des chaînes avec `==` compare des adresses, pas le texte.

---

## Bibliothèques courantes

- `<cs50.h>` : `get_int`, `get_string`, etc.
- `<stdio.h>` : `printf`, `scanf` (si utilisé)
- `<string.h>` : `strlen`, `strcmp`, `strcpy`, etc.
- `<ctype.h>` : `toupper`, `tolower`, etc.
- `<math.h>` : `sqrt`, etc.

---

## Complexité (Big-O)

- $O(f(n))$ : borne supérieure (au plus)
- $\Omega(f(n))$ : borne inférieure (au moins)
- $\Theta(f(n))$ : ordre serré (au plus et au moins pareil)

---

## Types (catégories)

- Types primitifs : `int`, `bool`, `char`, `float`, ...
- Types composés / dérivés : construits à partir d’autres types (tableaux, `struct`, chaînes `char *`)
- Types abstraits : souvent modélisés via `struct` (et en C++ on parlerait aussi de `class`)

## Opérateurs 

- Adresse de l'opérateur : `&`
- Opérateur de déréférencement : `*`

- Permet d'utiliser les pointeurs: `%p`

Un pointeur c'est simplement une variable qui contient l'adresse de quelque chose : `int *p = &n` --> se traduit par la variable p sera un pointeur qui contiendra l'adresse d'un integer. À droite se traduit par prend l'adresse de n. Au final, c'est l'adresse de n qui sera assignée dans la variable p. Cette adresse est hexadécimal de forme 0x.


