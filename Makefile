PKG_NAME := qt6base
URL = https://download.qt.io/official_releases/qt/6.8/6.8.0/submodules/qtbase-everywhere-src-6.8.0.tar.xz
ARCHIVES = 

include ../common/Makefile.common

updateqt:
	python3 update.py http://$(KOJI_HOST)
