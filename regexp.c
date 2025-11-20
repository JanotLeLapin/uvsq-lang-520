#include <stdio.h>
#include <stdlib.h>

#include "regexp.h"

inline static struct expr_node *make_expr_node(enum expr_node_type type) {
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
        printf("binary expr (+):\n");
        print_expr_node(node->value.binary.left, depth + 1);
        print_expr_node(node->value.binary.right, depth + 1);
        break;
    case EXPR_NODE_CAT:
        printf("binary expr (.):\n");
        print_expr_node(node->value.binary.left, depth + 1);
        print_expr_node(node->value.binary.right, depth + 1);
        break;
    case EXPR_NODE_ALL:
        printf("unary expr (*):\n");
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

inline void stack_push(struct expr_node **stack, int *top, struct expr_node *node) {
    if (63 > *top) {
        stack[++(*top)] = node;
    }
}

inline struct expr_node *stack_pop(struct expr_node **stack, int *top) {
    if (-1 != *top) {
        return stack[(*top)--];
    }
    return 0;
}

int compile_expr(struct expr_node *node, FILE *f) {
    struct expr_node *stack_pre[64], *stack_post[64], *tmp;
    int top_pre = -1, top_post = -1, max, len;
    char buf[1024], *p;

    stack_push(stack_pre, &top_pre, node);

    while (-1 != top_pre) {
        tmp = stack_pop(stack_pre, &top_pre);
        stack_push(stack_post, &top_post, tmp);

        switch (tmp->type) {
        case EXPR_NODE_VAL:
            break;
        case EXPR_NODE_ADD:
        case EXPR_NODE_CAT:
            stack_push(stack_pre, &top_pre, tmp->value.binary.left);
            stack_push(stack_pre, &top_pre, tmp->value.binary.right);
            break;
        case EXPR_NODE_ALL:
            stack_push(stack_pre, &top_pre, tmp->value.unary);
            break;
        }
    }

    max = top_post;
    while (-1 != top_post) {
        tmp = stack_pop(stack_post, &top_post);

        len = snprintf(buf, sizeof(buf), "a%d = ", max - top_post);

        switch (tmp->type) {
        case EXPR_NODE_VAL:
            len += snprintf(buf + len, sizeof(buf) - len, "automate(\"%c\")\n", tmp->value.val);
            break;
        case EXPR_NODE_ADD:
            len += snprintf(buf + len, sizeof(buf) - len, "union(a%d, a%d)\n", max - top_post - 1, max - top_post - 2);
            break;
        case EXPR_NODE_CAT:
            len += snprintf(buf + len, sizeof(buf) - len, "concatenation(a%d, a%d)\n", max - top_post - 1, max - top_post - 2);
            break;
        case EXPR_NODE_ALL:
            len += snprintf(buf + len, sizeof(buf) - len, "etoile(a%d)\n", max - top_post - 1);
            break;
        }
        fwrite(buf, 1, len, f);
    }

    len = snprintf(buf, sizeof(buf), "a%d = tout_faire(a%d)\n", max + 2, max + 1);
    fwrite(buf, 1, len, f);

    return 0;
}
