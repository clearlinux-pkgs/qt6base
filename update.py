#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import time

from clr_artifact import ClearRepo


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('uri')
    return parser.parse_args()


def build(pkg):
    cwd = os.path.join("..", pkg)
    try:
        subprocess.run("git fetch origin".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run("git reset --hard origin/main".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run("make update-versions".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run("make autospec".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run("make koji".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run("make koji-waitrepo".split(), cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        time.sleep(60)
    except Exception as exptn:
        print(f"build failed for {pkg}: {exptn}")
        sys.exit(-1)


def qt6_update(uri):
    repo = ClearRepo(uri, 'mash', 'clr-repo-cache')
    repo.load_dbs()
    # these are handled specially by update.sh
    built = set(['qt6base', 'qt6shadertools', 'qt6svg', 'qt6tools', 'qt6declarative'])
    # The rest of the qt6 world
    qt6_pkgs = ['qt63d', 'qt6grpc', 'qt6quick3d', 'qt6serialport', 'qt6webchannel', 'qt6activeqt', 'qt6httpserver', 'qt6quick3dphysics', 'qt6webengine', 'qt6imageformats', 'qt6quickeffectmaker', 'qt6speech', 'qt6websockets', 'qt6charts', 'qt6languageserver', 'qt6quicktimeline', 'qt6webview', 'qt6connectivity', 'qt6lottie', 'qt6remoteobjects', 'qt6datavis3d', 'qt6multimedia', 'qt6scxml', 'qt6translations', 'qt6networkauth', 'qt6sensors', 'qt6virtualkeyboard', 'qt6doc', 'qt6positioning', 'qt6serialbus', 'qt6wayland']
    build_graph, dependency_graph = repo.create_graphs(qt6_pkgs)
    groups = 1
    while len(build_graph) > 0:
        print(f"Build group: {groups}")
        groups += 1
        repo.trim_graph(build_graph, dependency_graph, built)
        built = set()
        for pkg, pre_reqs in build_graph.items():
            if len(pre_reqs) == 0:
                print(f"building: {pkg}")
                build(pkg)
                built.add(pkg)
        if len(built) == 0:
            break


def main():
    args = get_args()
    qt6_update(args.uri)


if __name__ == '__main__':
    main()
