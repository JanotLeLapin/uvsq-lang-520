{ flex
, stdenv
}: stdenv.mkDerivation {
  name = "regexp-lexer";

  src = ./regexp.l;
  dontUnpack = true;

  buildInputs = [
    flex
  ];
  buildPhase = ''
    flex $src
  '';

  installPhase = ''
    mkdir -p $out/lib
    cp *.yy.c $out/lib
  '';
}
