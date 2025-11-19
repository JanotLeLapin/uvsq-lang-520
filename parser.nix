{ bison
, stdenv

, name
, parser-file
}: stdenv.mkDerivation {
  name = "${name}-parser";

  src = parser-file;
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
