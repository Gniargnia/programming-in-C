CC = clang
CFLAGS = -Wall -Wextra -std=c11 -Iinclude

SRC = src/main.c src/utils.c
OBJ = $(SRC:.c=.o)

all: programme

programme: $(OBJ)
		$(CC) $(CFLAGS) -o $@ $^

clean:
		rm -f $(OBJ) programme