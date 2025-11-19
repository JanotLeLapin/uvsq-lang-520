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

struct expr_node *make_expr_node(enum expr_node_type type);
struct expr_node *make_expr_val_node(char val);
struct expr_node *make_expr_binary_node(enum expr_node_type type, struct expr_node *left, struct expr_node *right);
struct expr_node *make_expr_unary_node(enum expr_node_type type, struct expr_node *n);

void print_expr_node(struct expr_node *node, int depth);
void free_expr_node(struct expr_node *node);
