Summary:	Font Editor for PostScript, TrueType, OpenType and various fonts
Name:		fontforge
Version:	20220308
Release:	1
License:	BSD-like
Group:		Publishing
Url:		http://fontforge.sourceforge.net/
# For current version, check https://github.com/fontforge/fontforge/releases
Source0:	http://github.com/fontforge/fontforge/archive/%{version}/%{name}-%{version}.tar.gz
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png

BuildRequires:	chrpath
BuildRequires:	git
BuildRequires:	desktop-file-utils
BuildRequires:	jpeg-devel
BuildRequires:	ungif-devel
BuildRequires:	libtool-devel
BuildRequires:	libuninameslist-devel
BuildRequires:	tiff-devel
BuildRequires:	uthash-devel
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libwoff2enc)
BuildRequires:	pkgconfig(libwoff2dec)
BuildRequires:	pkgconfig(libspiro)
BuildRequires:	giflib-devel
# The various libraries were never used by anything outside of fontforge itself,
# and "ninja install" doesn't install their headers, so they're useless...
%define libgdraw %mklibname gdraw 6
%define libgunicode %mklibname gunicode 5
%define libexe %mklibname %{name}exe 3
%define libgutils %mklibname gutils 3
%define libfontforge %mklibname fontforge 3
%define devname %mklibname %{name} -d 
Obsoletes:	%{libexe} %{libgdraw} %{libgunicode} %{libgutils} %{libfontforge}
Obsoletes:	%{devname}

# (Abel) it wants either autotrace or potrace
Requires:	potrace

%description
FontForge is an outline font editor that lets you create your own 
postscript, truetype, opentype, cid-keyed, multi-master, cff, svg and 
bitmap (bdf) fonts, or edit existing ones. Also lets you convert one
format to another. FontForge has support for many macintosh font formats.

%package python
Group:		Development/Python
Summary:	Library bindings for python
Conflicts:	%{name} < 1.0-0.20110222.4
BuildRequires:	python-devel

%description python
This package contains the python library for python applications that
use %{name}.

%prep
%autosetup -p1

# FIXME switch to ENABLE_DOCS at some point, when
# they actually compile with current sphinx
%cmake -G Ninja \
	-DENABLE_DOCS:BOOL=OFF \
	-DENABLE_FONTFORGE_EXTRAS:BOOL=ON \
	-DENABLE_LIBSPIRO:BOOL=ON \
	-DENABLE_PYTHON_EXTENSION:BOOL=ON \
	-DENABLE_TILE_PATH:BOOL=ON \
	-DENABLE_WOFF2:BOOL=ON \
	-DENABLE_WRITE_PFM:BOOL=ON \
	-DENABLE_X11:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build

desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	desktop/org.fontforge.FontForge.desktop

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}/%{_datadir}/mime/packages

install -p desktop/fontforge.xml %{buildroot}/%{_datadir}/mime/packages/

chrpath -d %{buildroot}%{_bindir}/%{name} %{buildroot}%{_libdir}/*.so.*

%find_lang FontForge

%files -f FontForge.lang
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*.png
%optional %{_iconsdir}/hicolor/*/apps/*.svg
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/fontforge.xml
%{_datadir}/metainfo/org.fontforge.FontForge.*.xml
%{_datadir}/%{name}
%{_libdir}/libfontforge.so*

%files python
%{python_sitearch}/fontforge.so
%{python_sitearch}/psMat.so
