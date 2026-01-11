{ gcc
, flex
, bison
, python3
, python3Packages
, clang-tools
, valgrind
, mkShell
}: mkShell {
  buildInputs = [
    gcc flex bison python3 python3Packages.graphviz
    python3Packages.python-lsp-server clang-tools
    valgrind
  ];
}
