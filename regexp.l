%{
  #define CONST 0x10 /* constant */
  #define OP    0x20 /* operator */
  #define PAR_O 0x30 /* left paren */
  #define PAR_C 0x31 /* right paren */
%}

const [abce]
op [+.*]

%%

{const} { return CONST; }
{op} { return OP; }
\( { return PAR_O; }
\) { return PAR_C; }

.|\n {}

%%

int main() {
  int res = yylex();
  return 0;
}
