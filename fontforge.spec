%define ffversion	20071002
%define docversion	20071002
%define	Summary		Font Editor for PostScript, TrueType, OpenType and various fonts

Name:		fontforge
Version:	1.0
Release:	%mkrel 0.%{ffversion}.1
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
Patch0:		fontforge-%{version}-uni-nodevel.patch
Patch1:		fontforge-%{version}-local-helpdir.patch
URL:		http://fontforge.sourceforge.net/
# (Abel) it wants either autotrace or potrace
Requires:	fonttracer
Requires:	tetex-mfwin
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	libungif-devel
BuildRequires:	libxml2-devel
# (Abel) libuninameslist.so.0 is a runtime dependency via dlopen()
Requires:	%{mklibname uninameslist 0}
BuildRequires:	libuninameslist-devel
BuildRequires:	chrpath

%description
FontForge is an outline font editor that lets you create your own 
postscript, truetype, opentype, cid-keyed, multi-master, cff, svg and 
bitmap (bdf) fonts, or edit existing ones. Also lets you convert one
format to another. FontForge has support for many macintosh font formats.

%prep
%setup -q -n fontforge-%{ffversion}
%patch0 -p1 -b .uninames
%patch1 -p1 -b .helpdir
install -m 644 %{SOURCE4} .

# needed by patch
#autoconf

mkdir -p htdocs cidmap
tar xjf %{SOURCE2} -C htdocs
tar xjf %{SOURCE3} -C cidmap

%build
%configure2_5x \
	--with-multilayer \
	--with-devicetables \
	--disable-shared
%make

%install
rm -rf $RPM_BUILD_ROOT
#%makeinstall_std
%makeinstall

rm -rf $RPM_BUILD_ROOT%{_libdir}

# XDG compliance
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=FontForge
Comment=%{Summary}
Exec=%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Graphics;Scanning;OCR;Office;Viewer;
EOF

# icons
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# added with htdocs in %doc section
rm -rf %{buildroot}%{_datadir}/doc/fontforge

chrpath -d %{buildroot}%{_bindir}/%{name}

%find_lang FontForge

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f FontForge.lang
%defattr(-,root,root)
%doc LICENSE htdocs README-unix README-Unix.html fontforge-tutorial.pdf
%{_bindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/fontforge

