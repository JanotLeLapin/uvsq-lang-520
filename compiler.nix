{ gcc
, flex
, stdenv

, regexp-parser
, regexp-lexer
}: stdenv.mkDerivation {
  name = "regexp-compiler";

  src = ./.;
  dontUnpack = true;

  buildInputs = [
    gcc
    flex
  ];
  buildPhase = ''
    cp ${regexp-parser}/lib/y.tab.c .
    cp ${regexp-parser}/lib/y.tab.h .
    cp ${regexp-lexer}/lib/lex.yy.c .
    gcc -o out y.tab.c lex.yy.c -L${flex}/lib/lib -lfl
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp out $out/bin/regexp-compiler
  '';
}
