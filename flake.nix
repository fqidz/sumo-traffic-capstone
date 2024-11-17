{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
    ultralytics = (pkgs.python311.pkgs.buildPythonPackage rec {
      pname = "ultralytics";
      version = "8.3.32";

      src = pkgs.fetchPypi {
        inherit pname version;
        sha256 = "sha256-iaMTPzzWwJu8dmCcp7Yqv5ISEua2/xOgzITHACaxJVY=";
      };

      buildInputs = with pkgs.python311.pkgs; [
        numpy
        matplotlib
        opencv-python
        pillow
        pyyaml
        requests
        scipy
        torch
        torchvision
        tqdm
        psutil
        py-cpuinfo
        pandas
        seaborn
        ultralytics-thop
      ];
    });

    ultralytics-thop = (pkgs.python311.pkgs.buildPythonPackage {
      pname = "ultralytics-thop";
      version = "2.0.11";

      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/1f/87/372e7a1beea2ed84b05a7b096f86ca67cb9a945337923ca6be6f80d4a200/ultralytics_thop-2.0.11.tar.gz";
        sha256 = "sha256-G+O2F2IxR51Hi0WR7gmDaO4EJJATEj75y9BDudOhXd0=";
      };

      buildInputs = with pkgs.python311.pkgs; [
        numpy
        torch
      ];
    });

    stable-baselines3 = (pkgs.python311.pkgs.buildPythonPackage {
      pname = "stable-baselines3";
      version = "2.3.2";

      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ea/bd/8b6fd663cca67793c7a651b7929f987cee021e72a8d910e8851ea0b4d9c2/stable_baselines3-2.3.2.tar.gz";
        sha256 = "sha256-L4GIkW5gdXHEwk+Iqf9vhO2vss8i1dJPnBmVY8Ev8Wg=";
      };
    });

    sumo-rl = (pkgs.python311.pkgs.buildPythonPackage {
      pname = "sumo-rl";
      version = "1.4.5";

      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e9/76/892e7b2e314887f21958a9c5b215c689a2e50cc134e49ec6654efef66751/sumo_rl-1.4.5.tar.gz";
        sha256 = "sha256-Iwl5+3eWmnaDnNNgJ9sqwa6g4qQdmzgAD1kih8PRLBE=";
      };

      buildInputs = with pkgs.python311.pkgs; [
        gymnasium
        pettingzoo
        numpy
        pandas
        pillow
        sumolib
        traci
      ];
    });

    sumolib = (pkgs.python311.pkgs.buildPythonPackage rec {
      pname = "sumolib";
      version = "1.21.0";

      src = pkgs.fetchPypi {
        inherit pname version;
        sha256 = "sha256-p+TM+ICibuJTaysg2qomtGY3aQncsRPiPGXQnUpt56o=";
      };
    });

    traci = (pkgs.python311.pkgs.buildPythonPackage rec {
      pname = "traci";
      version = "1.21.0";

      src = pkgs.fetchPypi {
        inherit pname version;
        sha256 = "sha256-iwdl0I/IvH5/oWR8fLCs6ZZLFdiYDel5peEKIGxBcxE=";
      };

      buildInputs = [
        sumolib
      ];
    });
  in
  {
    devShells."x86_64-linux".default = pkgs.mkShell {
      packages = [
        pkgs.python311
        pkgs.sumo

        (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
          matplotlib
          tensorboard
          pathvalidate
          ultralytics
          stable-baselines3
          sumo-rl
        ]))
      ];
    };
  };
}
