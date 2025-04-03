#!/bin/bash

set -eu -o pipefail

base_round=0
pkgs=('qt6base' 'qt6shadertools' 'qt6svg' 'qt6tools' 'qt6base' 'qt6declarative')
for i in "${pkgs[@]}"; do
    pushd "../${i}"
    git fetch origin
    git reset --hard origin/main
    if [ "$i" = 'qt6base' ]; then
        if [ $base_round -eq 0 ]; then
            base_round=1
            make update-versions
        fi
    else
        make update-versions
    fi
    make autospec
    make koji
    make koji-waitrepo
    sleep 60
    popd
done

python3 update.py
