%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex(void);
int yyerror(const char *s) {
    fprintf(stderr, "parser error: %s\n", s);
    return 0;
}

enum expr_node_type {
    EXPR_NODE_VAL = 0x00,
    EXPR_NODE_ADD = 0x10,
    EXPR_NODE_CAT = 0x11,
    EXPR_NODE_ALL = 0x12,
};

struct expr_node {
    enum expr_node_type type;
    union {
        char val;
        struct expr_node *unary;
        struct {
            struct expr_node *left;
            struct expr_node *right;
        } binary;
    } value;
};

inline struct expr_node *make_expr_node(enum expr_node_type type) {
    struct expr_node *node = malloc(sizeof(struct expr_node));
    if (0 == node) {
        return 0;
    }
    node->type = type;
    return node;
}

struct expr_node *make_expr_val_node(char val) {
    struct expr_node *node = make_expr_node(EXPR_NODE_VAL);
    if (0 == node) {
        return 0;
    }
    node->value.val = val;
    return node;
}

struct expr_node *make_expr_binary_node(enum expr_node_type type, struct expr_node *left, struct expr_node *right) {
    struct expr_node *node = make_expr_node(type);
    if (0 == node) {
        return 0;
    }
    node->value.binary.left = left;
    node->value.binary.right = right;
    return node;
}

struct expr_node *make_expr_unary_node(enum expr_node_type type, struct expr_node *n) {
    struct expr_node *node = make_expr_node(type);
    if (0 == node) {
        return 0;
    }
    node->value.unary = n;
    return node;
}

void print_expr_node(struct expr_node *node, int depth) {
    int i;

    for (i = 0; i < depth; i++) {
        printf(" ");
    }

    switch (node->type) {
    case EXPR_NODE_VAL:
        printf("val: '%c'\n", node->value.val);
        break;
    case EXPR_NODE_ADD:
    case EXPR_NODE_CAT:
        printf("binary expr:\n");
        print_expr_node(node->value.binary.left, depth + 1);
        print_expr_node(node->value.binary.right, depth + 1);
        break;
    case EXPR_NODE_ALL:
        printf("unary expr:\n");
        print_expr_node(node->value.unary, depth + 1);
        break;
    }
}

void free_expr_node(struct expr_node *node) {
    switch (node->type) {
    case EXPR_NODE_VAL:
        break;
    case EXPR_NODE_ADD:
    case EXPR_NODE_CAT:
        free_expr_node(node->value.binary.left);
        free_expr_node(node->value.binary.right);
        break;
    case EXPR_NODE_ALL:
        free_expr_node(node->value.unary);
        break;
    }
    free(node);
}

struct expr_node *root = 0;
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
    expr { root = $1; }
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
    if (0 == yyparse()) {
        printf("successfully parsed\n");
        if (0 != root) {
            print_expr_node(root, 0);
            free_expr_node(root);
        }
    } else {
        printf("something went wrong\n");
    }
    return 0;
}
