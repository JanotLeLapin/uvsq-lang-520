# Outils de compil, on utilise bison pour être tranquille sur WSL
CC = gcc
LEX = flex
YACC = yacc
CFLAGS = -Wall -g 
LDFLAGS = -lfl

# Options pour Bison pour qu'il nous sorte les bons fichiers .c et .h
YFLAGS = -d -y 

EXEC = regexp-compiler
OBJ = regexp.o y.tab.o lex.yy.o

# Cible principale pour tout compiler d'un coup
all: $(EXEC)

# On lie les fichiers objets pour faire l'exécutable
$(EXEC): $(OBJ)
	@echo "On relie tout pour créer le binaire final..."
	$(CC) $(CFLAGS) -o $(EXEC) $(OBJ) $(LDFLAGS)

# Compilation de l'AST (notre structure d'arbre)
regexp.o: regexp.c regexp.h
	$(CC) $(CFLAGS) -c regexp.c

# Compilation du parser généré par Bison
y.tab.o: y.tab.c regexp.h
	$(CC) $(CFLAGS) -c y.tab.c

# Compilation du lexer généré par Flex
lex.yy.o: lex.yy.c y.tab.h
	$(CC) $(CFLAGS) -c lex.yy.c

# Génération des sources C depuis la grammaire
y.tab.c y.tab.h: regexp.y
	$(YACC) $(YFLAGS) regexp.y -o y.tab.c

# Génération du code C depuis les tokens
lex.yy.c: regexp.l y.tab.h
	$(LEX) regexp.l

clean:
	rm -f *.o y.tab.c y.tab.h lex.yy.c $(EXEC) main.py

.PHONY: all clean
