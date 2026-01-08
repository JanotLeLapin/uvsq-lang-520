{ gcc
, flex
, python3
, python3Packages
, clang-tools
, valgrind
, mkShell
}: mkShell {
  buildInputs = [
    gcc flex python3
    python3Packages.python-lsp-server clang-tools
    valgrind
  ];
}
