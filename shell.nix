{ gcc
, flex
, python3
, clang-tools
, valgrind
, mkShell
}: mkShell {
  buildInputs = [
    gcc flex python3
    clang-tools valgrind
  ];
}
