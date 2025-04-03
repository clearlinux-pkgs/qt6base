#!/bin/bash

set -eu -o pipefail

pkgs=('qt6base' 'qt6shadertools' 'qt6svg' 'qt6tools' 'qt6base' 'qt6declarative')
for i in "${pkgs[@]}"; do
    pushd "../${i}"
    git fetch origin
    git reset --hard origin/main
    make update-versions || if [ "$i" != 'qt6base' ]; then exit 1; fi
    make autospec
    make koji
    make koji-waitrepo
    sleep 60
    popd
done

python3 update.py
