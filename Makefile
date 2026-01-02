# ==========================================
# CONFIGURATION
# ==========================================
NAME         := programme_exe
CC           := clang
LDLIBS       := -lcs50

SRCS_DIR     := src
TESTS_DIR    := test
INCS_DIR     := include
BUILD_DIR    := build
BUILD_TEST   := build_test

# CFLAGS avec génération des dépendances (.d) au bon endroit
CFLAGS       := -Wall -Wextra -Werror -g -std=c11 -I$(INCS_DIR) -MMD -MP
MAKEFLAGS    += --silent

# ==========================================
# GESTION DES FICHIERS
# ==========================================
# --- Programme Principal ---
SRC          := $(wildcard $(SRCS_DIR)/*.c)
OBJ          := $(SRC:$(SRCS_DIR)/%.c=$(BUILD_DIR)/%.o)
DEPS         := $(OBJ:.o=.d)

# --- Exercices (Tests) ---
TEST_SRCS    := $(wildcard $(TESTS_DIR)/*.c)
TEST_OBJS    := $(TEST_SRCS:$(TESTS_DIR)/%.c=$(BUILD_TEST)/%.o)
TEST_BINS    := $(TEST_SRCS:$(TESTS_DIR)/%.c=$(TESTS_DIR)/run_%)
TEST_DEPS    := $(TEST_OBJS:.o=.d)

# ==========================================
# RÈGLES DE COMPILATION
# ==========================================
.PHONY: all test clean fclean re

# Empêche Make de supprimer les fichiers .o après la compilation
.SECONDARY: $(TEST_OBJS) $(OBJ)

# Règle par défaut (c'est celle-ci qui manquait)
all: $(NAME)

# Création des dossiers de build
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_TEST):
	mkdir -p $(BUILD_TEST)

# --- CONSTRUCTION DU PROGRAMME PRINCIPAL ---
$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $^ $(LDLIBS) -o $@

$(BUILD_DIR)/%.o: $(SRCS_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -MF $(@:.o=.d) -c $< -o $@

# --- CONSTRUCTION DES EXERCICES ---
test: $(TEST_BINS)

$(TESTS_DIR)/run_%: $(BUILD_TEST)/%.o
	$(CC) $(CFLAGS) $< $(LDLIBS) -o $@

$(BUILD_TEST)/%.o: $(TESTS_DIR)/%.c | $(BUILD_TEST)
	$(CC) $(CFLAGS) -MF $(@:.o=.d) -c $< -o $@

# Inclusion des fichiers de dépendances
-include $(DEPS) $(TEST_DEPS)

# ==========================================
# NETTOYAGE
# ==========================================
clean:
	rm -rf $(BUILD_DIR) $(BUILD_TEST)

fclean: clean
	rm -f $(NAME) $(TEST_BINS)

re: fclean all