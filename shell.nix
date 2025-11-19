{ gcc
, flex
, python3
, mkShell
}: mkShell {
  buildInputs = [ gcc flex python3 ];
}
