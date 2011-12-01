%define ffversion	20110222
%define docversion	20110221
%define	Summary		Font Editor for PostScript, TrueType, OpenType and various fonts

%define		_disable_ld_no_undefined	1
%define		_disable_ld_as_needed		1

Name:		fontforge
Version:	1.0
Release:	%mkrel 0.%{ffversion}.2
Summary:	%{Summary}
License:	BSD-like
Group:		Publishing
Source0:	http://fontforge.sourceforge.net/fontforge_full-%{ffversion}.tar.bz2
Source2:	http://fontforge.sourceforge.net/fontforge_htdocs-%{docversion}.tar.bz2
Source3:	http://fontforge.sourceforge.net/cidmaps.tar.bz2
Source4:	http://fontforge.sourceforge.net/fontforge-tutorial.pdf
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		fontforge-20110222-link.patch
Patch1:         fontforge-20090224-pythondl.patch
Patch2:         fontforge-20100501-select-points-crash.patch
Patch3:	        fontforge-20110222-multilib.patch
Patch4:		fontforge-20110222-png1.5.patch
URL:		http://fontforge.sourceforge.net/
# (Abel) it wants either autotrace or potrace
Requires:	potrace
BuildRequires:	freetype2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	libungif-devel
BuildRequires:	libxml2-devel
BuildRequires:	libuninameslist-devel
BuildRequires:	python-devel
BuildRequires:	libx11-devel
BuildRequires:	libxi-devel
BuildRequires:	libxft-devel
BuildRequires:	pango-devel
BuildRequires:	cairo-devel
BuildRequires:	desktop-file-utils
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
FontForge is an outline font editor that lets you create your own 
postscript, truetype, opentype, cid-keyed, multi-master, cff, svg and 
bitmap (bdf) fonts, or edit existing ones. Also lets you convert one
format to another. FontForge has support for many macintosh font formats.

%prep
%setup -qn fontforge-%{ffversion}
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1

mkdir -p htdocs cidmap
tar xjf %{SOURCE2} -C htdocs
tar xjf %{SOURCE3} -C cidmap

cp %{SOURCE4} .

%build
%configure2_5x \
	--disable-static --with-freetype-bytecode=no \
	--with-regular-link --enable-pyextension \
	--enable-longdouble --enable-type3 --enable-libff
%make

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications            \
  Packaging/fontforge.desktop

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}/%{_datadir}/mime/packages

install -p Packaging/fontforge.xml %{buildroot}/%{_datadir}/mime/packages/

rm -rf %{buildroot}%{_includedir} %{buildroot}%{_libdir}/{*.la,*.so,pkgconfig}

chrpath -d %{buildroot}%{_bindir}/%{name} %{buildroot}%{_libdir}/*.so.*

%find_lang FontForge

%clean
rm -rf %{buildroot}

%files -f FontForge.lang
%defattr(-,root,root)
%doc LICENSE README-unix README-Unix.html fontforge-tutorial.pdf
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/fontforge.xml
%{python_sitearch}/fontforge*.egg-info
%{python_sitearch}/fontforge.so
%{python_sitearch}/psMat.so
%{_libdir}/*.so.*
%{_datadir}/fontforge
