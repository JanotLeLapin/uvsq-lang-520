%{
#include "y.tab.h"
%}

const [abcE]
op [+.*]

%%

{const} {
  yylval.c = yytext[0];
  return CONST;
}
"+" { return '+'; }
"." { return '.'; }
"*" { return '*'; }
"(" { return '('; }
")" { return ')'; }

.|\n {}

%%
