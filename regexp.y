%{
#include <stdio.h>

extern int yylex(void);
int yyerror(const char *s) {
    fprintf(stderr, "parser error: %s\n", s);
    return 0;
}
%}

%token CONST

%left '+'
%left '.'
%left '*'

%%
expr: '(' expr ')'
    | expr '+' expr
	| expr '.' expr
	| expr '*'
	| CONST
	;

%%

int main() {
    if (0 == yyparse()) {
        printf("successfully parsed\n");
    } else {
        printf("something went wrong\n");
    }
    return 0;
}
