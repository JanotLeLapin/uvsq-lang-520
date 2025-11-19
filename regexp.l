%{
#include "y.tab.h"
%}

const [abcE]
op [+.*]

%%

{const} { return CONST; }
"+" { return '+'; }
"." { return '.'; }
"*" { return '*'; }
"(" { return '('; }
")" { return ')'; }

.|\n {}

%%

int main() {
  return 0;
}
