{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }: let
    eachSystem = fn: nixpkgs.lib.genAttrs [
      "x86_64-linux"
      "aarch64-linux"
    ] (system: (fn {
      inherit system;
      pkgs = (import nixpkgs { inherit system; });
    }));
  in {
    devShells = eachSystem ({ pkgs, ... }: {
      default = pkgs.callPackage ./shell.nix {};
    });
    packages = eachSystem ({ pkgs, ... }: let
      lexer = name: lexer-file: pkgs.callPackage ./lexer.nix { inherit name lexer-file; };
      parser = name: parser-file: pkgs.callPackage ./parser.nix { inherit name parser-file; };
      compiler = name: lexer: parser: pkgs.callPackage ./compiler.nix { inherit name lexer parser; };
    in rec {
      regexp-lexer = lexer "regexp" ./regexp.l;
      regexp-parser = parser "regexp" ./regexp.y;
      regexp-compiler = compiler "regexp" regexp-lexer regexp-parser;
    });
  };
}
