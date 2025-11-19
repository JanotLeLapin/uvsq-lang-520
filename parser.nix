{ bison
, stdenv
}: stdenv.mkDerivation {
  name = "regexp-parser";

  src = ./regexp.y;
  dontUnpack = true;

  buildInputs = [
    bison
  ];
  buildPhase = ''
    yacc -d $src
  '';
  installPhase = ''
    mkdir -p $out/lib
    cp *.tab.* $out/lib
  '';
}
