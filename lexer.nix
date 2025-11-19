{ flex
, gcc
, stdenv

, grammar-file
}: stdenv.mkDerivation {
  name = "lexer";

  src = grammar-file;
  dontUnpack = true;

  buildInputs = [
    gcc
    flex
  ];
  buildPhase = ''
    flex $src
    gcc lex.yy.c -o lexer -L${flex}/lib -lfl
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp lexer $out/bin
  '';
}
