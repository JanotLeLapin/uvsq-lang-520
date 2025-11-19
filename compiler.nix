{ gcc
, flex
, stdenv

, name
, parser
, lexer
}: stdenv.mkDerivation {
  name = "${name}-compiler";

  src = ./.;
  dontUnpack = true;

  buildInputs = [
    gcc
    flex
  ];
  buildPhase = ''
    cp ${parser}/lib/* .
    cp ${lexer}/lib/* .
    gcc -o out *.tab.c *.yy.c -L${flex}/lib/lib -lfl
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp out $out/bin/${name}-compiler
  '';
}
