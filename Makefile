CC = clang
CFLAGS = -Wall -Wextra -std=c11

SRC = src/main.c
OBJ = $(SRC:.c=.o)

all: programme

programme: $(OBJ)
		$(CC) $(CFLAGS) -o $@ $^

clean:
		rm -f $(OBJ) programme