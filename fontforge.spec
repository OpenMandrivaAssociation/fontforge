%define major 2
%define gdraw_major 5
%define gunicode_major 4
%define libname %mklibname %{name} %{major}
%define libgdraw %mklibname gdraw %{gdraw_major}
%define libgioftp %mklibname gioftp %{major}
%define libgunicode %mklibname gunicode %{gunicode_major}
%define libgutils %mklibname gutils %{major}
%define libexe %mklibname %{name}exe %{major}
%define devname %mklibname %{name} -d
%define gnulib_githead 2bf7326

Summary:	Font Editor for PostScript, TrueType, OpenType and various fonts
Name:		fontforge
Version:	20141014
Release:	1
License:	BSD-like
Group:		Publishing
Url:		http://fontforge.sourceforge.net/
Source0:	http://github.com/fontforge/fontforge/archive/%{version}.tar.gz
# https://github.com/fontforge/fontforge/issues/1725
# http://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=snapshot;h=%{gnulib_githead};sf=tgz;name=gnulib-%{gnulib_githead}.tar.gz
Source1:	gnulib-%{gnulib_githead}.tar.gz
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch1:		fontforge-20140813-use-system-uthash.patch

BuildRequires:	chrpath
BuildRequires:	git
BuildRequires:	desktop-file-utils
BuildRequires:	jpeg-devel
BuildRequires:	ungif-devel
BuildRequires:	libuninameslist-devel
BuildRequires:	tiff-devel
BuildRequires:	uthash-devel
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

# (Abel) it wants either autotrace or potrace
Requires:	potrace

%description
FontForge is an outline font editor that lets you create your own 
postscript, truetype, opentype, cid-keyed, multi-master, cff, svg and 
bitmap (bdf) fonts, or edit existing ones. Also lets you convert one
format to another. FontForge has support for many macintosh font formats.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{name} < 1.0-0.20110222.4

%description -n %{libname}
This package contains the shared library libfontforge.

%package -n %{libexe}
Group:          System/Libraries
Summary:        Library for %{name}
Conflicts:      %{name} < 1.0-0.20110222.4

%description -n %{libexe}
This package contains the shared library libfontforgeexe.


%package -n %{libgdraw}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{name} < 1.0-0.20110222.4

%description -n %{libgdraw}
This package contains the shared library libgdraw.

%package -n %{libgioftp}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{name} < 1.0-0.20110222.4

%description -n %{libgioftp}
This package contains the shared library libgioftp.

%package -n %{libgunicode}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{name} < 1.0-0.20110222.4

%description -n %{libgunicode}
This package contains the shared library libgunicode.

%package -n %{libgutils}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{name} < 1.0-0.20110222.4

%description -n %{libgutils}
This package contains the shared library libgutils.

%package -n %{devname}
Group:		Development/C
Summary:	Development files for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libexe} = %{version}-%{release}
Requires:	%{libgdraw} = %{version}-%{release}
Requires:	%{libgioftp} = %{version}-%{release}
Requires:	%{libgunicode} = %{version}-%{release}
Requires:	%{libgutils} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%package python
Group:		Development/Python
Summary:	Library bindings for python
Conflicts:	%{name} < 1.0-0.20110222.4
BuildRequires:	python-devel

%description python
This package contains the python library for python applications that
use %{name}.

%prep
%setup -qn fontforge-%{version}
tar xzf %{SOURCE1}

%apply_patches

mkdir htdocs
cp -pr doc/html/* htdocs
chmod 644 htdocs/nonBMP/index.html
# Fix bad line terminators
sed -i 's/\r//' htdocs/Big5.txt
sed -i 's/\r//' htdocs/corpchar.txt


%build
./bootstrap --skip-git --gnulib-srcdir=gnulib-%{gnulib_githead}
%configure \
	--disable-static \
	--with-freetype-bytecode=no \
	--with-regular-link \
	--enable-pyextension \
	--enable-longdouble \
	--enable-type3 \
	--enable-libff

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make 

%install
%makeinstall_std

desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	desktop/fontforge.desktop

# The fontforge makefiles install htdocs as well, but we
# prefer to have them under the standard RPM location, so
# remove the extra copy
rm -rf %{buildroot}%{_datadir}/doc/fontforge

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}/%{_datadir}/mime/packages

install -p desktop/fontforge.xml %{buildroot}/%{_datadir}/mime/packages/

chrpath -d %{buildroot}%{_bindir}/%{name} %{buildroot}%{_libdir}/*.so.*

%find_lang FontForge

%files -f FontForge.lang
%doc LICENSE doc/README-unix doc/README-Unix.html doc/html/fontforge-tutorial.pdf
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/fontforge.xml
%{_datadir}/%{name}

%files python
%{python_sitearch}/fontforge.so
%{python_sitearch}/psMat.so

%files -n %{libname}
%{_libdir}/libfontforge.so.%{major}*

%files -n %{libexe}
%{_libdir}/libfontforgeexe.so.%{major}*

%files -n %{libgdraw}
%{_libdir}/libgdraw.so.%{gdraw_major}*

%files -n %{libgioftp}
%{_libdir}/libgioftp.so.%{major}*

%files -n %{libgunicode}
%{_libdir}/libgunicode.so.%{gunicode_major}*

%files -n %{libgutils}
%{_libdir}/libgutils.so.%{major}*

%files -n %{devname}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig
%{_includedir}/%{name}

