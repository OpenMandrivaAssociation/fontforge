%define ffversion	20120731-b
%define docversion	20120731-b

%define major 1
%define gdraw_major 4
%define gunicode_major 3
%define libname %mklibname %{name} %{major}
%define libgdraw %mklibname gdraw %{gdraw_major}
%define libgioftp %mklibname gioftp %{major}
%define libgunicode %mklibname gunicode %{gunicode_major}
%define libgutils %mklibname gutils %{major}
%define devname %mklibname %{name} -d

Name:		fontforge
Version:	1.0
Release:	0.20120731b.6
Summary:	Font Editor for PostScript, TrueType, OpenType and various fonts
License:	BSD-like
Group:		Publishing
Url:		http://fontforge.sourceforge.net/
Source0:	http://fontforge.sourceforge.net/fontforge_full-%{ffversion}.tar.bz2
Source2:	http://fontforge.sourceforge.net/fontforge_htdocs-%{docversion}.tar.bz2
Source3:	http://fontforge.sourceforge.net/cidmaps.tar.bz2
Source4:	http://fontforge.sourceforge.net/fontforge-tutorial.pdf
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		fontforge-20110222-link.patch
Patch1:		fontforge-20090224-pythondl.patch
Patch5:		fontforge-20110222-libz.so-linkage.patch

BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	jpeg-devel
BuildRequires:	ungif-devel
BuildRequires:	libuninameslist-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	python-devel
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
%setup -qn fontforge-%{ffversion}
%apply_patches

mkdir -p htdocs cidmap
tar xjf %{SOURCE2} -C htdocs
tar xjf %{SOURCE3} -C cidmap

cp %{SOURCE4} .

# Fix bad line terminators
sed -i 's/\r//' htdocs/Big5.txt
sed -i 's/\r//' htdocs/corpchar.txt

find . -name "Make*" -o -name "config*" |xargs sed -i -e 's,png15,png16,g;s,PNG15,PNG16,g'

%build
%configure2_5x \
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
	Packaging/fontforge.desktop

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}/%{_datadir}/mime/packages

install -p Packaging/fontforge.xml %{buildroot}/%{_datadir}/mime/packages/

chrpath -d %{buildroot}%{_bindir}/%{name} %{buildroot}%{_libdir}/*.so.*

%find_lang FontForge

%files -f FontForge.lang
%doc LICENSE README-unix README-Unix.html fontforge-tutorial.pdf
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/fontforge.xml
%{_datadir}/%{name}

%files python
%{python_sitearch}/fontforge*.egg-info
%{python_sitearch}/fontforge.so
%{python_sitearch}/psMat.so

%files -n %{libname}
%{_libdir}/libfontforge.so.%{major}*

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

