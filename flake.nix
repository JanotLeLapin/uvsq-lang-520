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
    packages = eachSystem ({ pkgs, ... }: rec {
      regexp-parser = pkgs.callPackage ./parser.nix {};
      regexp-lexer = pkgs.callPackage ./lexer.nix {};
      regexp-compiler = pkgs.callPackage ./compiler.nix {
        inherit regexp-parser regexp-lexer;
      };
    });
  };
}
