%{
#include <stdio.h>

#include "regexp.h"

extern int yylex(void);
int yyerror(const char *s) {
    fprintf(stderr, "parser error: %s\n", s);
    return 0;
}

struct expr_node *left = 0;
struct expr_node *right = 0;
%}

%start program

%union {
    char c;
    struct expr_node *node;
}

%token <c> CONST
%type <node> expr

%left '+'
%left '.'
%left '*'

%%
program:
    expr expr { left = $1; right = $2; }
    ;

expr:
    '(' expr ')'      { $$ = $2; }
    | expr '+' expr   { $$ = make_expr_binary_node(EXPR_NODE_ADD, $1, $3); }
	| expr '.' expr   { $$ = make_expr_binary_node(EXPR_NODE_CAT, $1, $3); }
	| expr '*'        { $$ = make_expr_unary_node(EXPR_NODE_ALL, $1); }
	| CONST           { $$ = make_expr_val_node($1); }
	;

%%

int main() {
    FILE *f;

    if (0 == yyparse()) {
        printf("successfully parsed\n");
        if (0 != left && 0 != right) {
            f = fopen("main.py", "a");
            if (0 == f) {
                free_expr_node(left);
                free_expr_node(right);
                return 1;
            }

            printf("left:\n");
            print_expr_node(left, 0);
            printf("right:\n");
            print_expr_node(right, 0);

            compile_expr(left, f);
            compile_expr(right, f);

            free_expr_node(left);
            free_expr_node(right);

            fclose(f);
        }
    } else {
        printf("something went wrong\n");
    }
    return 0;
}
