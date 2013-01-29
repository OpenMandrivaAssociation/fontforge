%define ffversion	20120731
%define docversion	20120731

%define major 1
%define gdraw_major 4
%define gunicode_major 3
%define libname %mklibname %{name} %{major}
%define libgdraw %mklibname gdraw %{gdraw_major}
%define libgioftp %mklibname gioftp %{major}
%define libgunicode %mklibname gunicode %{gunicode_major}
%define libgutils %mklibname gutils %{major}
%define develname %mklibname %{name} -d

#define		_disable_ld_no_undefined	1
#define		_disable_ld_as_needed		1

Name:		fontforge
Version:	1.0
Release:	0.%{ffversion}.4
Summary:	Font Editor for PostScript, TrueType, OpenType and various fonts
License:	BSD-like
Group:		Publishing
URL:		http://fontforge.sourceforge.net/
Source0:	http://fontforge.sourceforge.net/fontforge_full-%{ffversion}.tar.bz2
Source2:	http://fontforge.sourceforge.net/fontforge_htdocs-%{docversion}.tar.bz2
Source3:	http://fontforge.sourceforge.net/cidmaps.tar.bz2
Source4:	http://fontforge.sourceforge.net/fontforge-tutorial.pdf
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		fontforge-20110222-link.patch
Patch1:		fontforge-20090224-pythondl.patch
Patch4:		libpng15-dynamic.diff
Patch5:		fontforge-20110222-libz.so-linkage.patch

BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	jpeg-devel
BuildRequires:	ungif-devel
BuildRequires:	libuninameslist-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libpng15)
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

%package -n %{develname}
Group:		Development/C
Summary:	Development files for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgdraw} = %{version}-%{release}
Requires:	%{libgioftp} = %{version}-%{release}
Requires:	%{libgunicode} = %{version}-%{release}
Requires:	%{libgutils} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the development files for %{name}.

%package python
Group:		Development/Python
Summary:	Library bindings for python
Conflicts:	%{name} < 1.0-0.20110222.4
%py_requires -d

%description python
This package contains the python library for python applications that
use %{name}.

%prep
%setup -qn fontforge-%{ffversion}
%patch0 -p0
%patch1 -p1
#patch4 -p0
%patch5 -p1

mkdir -p htdocs cidmap
tar xjf %{SOURCE2} -C htdocs
tar xjf %{SOURCE3} -C cidmap

cp %{SOURCE4} .

# Fix bad line terminators
%{__sed} -i 's/\r//' htdocs/Big5.txt
%{__sed} -i 's/\r//' htdocs/corpchar.txt

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
  --dir %{buildroot}%{_datadir}/applications            \
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

%files -n %{develname}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig
%{_includedir}/%{name}


%changelog
* Thu Dec 22 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.0-0.20110222.4
+ Revision: 744478
- fixed files list
- converted BRs to pkgconfig provides
- properly split up subpkgs
- split out libs and python pkgs
- added back devel pkg files
- cleaned up spec a bit

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix deps
    - rebuilt against libtiff.so.5

* Wed Nov 23 2011 Paulo Andrade <pcpa@mandriva.com.br> 1.0-0.20110222.2
+ Revision: 732809
- Rebuild with png1.5.

  + Oden Eriksson <oeriksson@mandriva.com>
    - attempt to relink against libpng15.so.15

* Sat Apr 09 2011 Funda Wang <fwang@mandriva.org> 1.0-0.20110222.1
+ Revision: 652027
- BR desktop-file-utils
- new version 20110222

* Sat Apr 09 2011 Funda Wang <fwang@mandriva.org> 1.0-0.20090923.5
+ Revision: 652016
- req potrace instead

* Wed Mar 16 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 1.0-0.20090923.4
+ Revision: 645696
- drop ancient scriptlets
- fix dependency problems related to texlive upgrade

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20090923.3mdv2011.0
+ Revision: 605181
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20090923.2mdv2010.1
+ Revision: 522653
- rebuilt for 2010.1

* Sun Sep 27 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0-0.20090923.1mdv2010.0
+ Revision: 449729
- Update to new version 20090923

* Wed Sep 16 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0-0.20090914.1mdv2010.0
+ Revision: 443643
- Update to new version 20090914
- Remove string format patch and segfault patch: fixed upstream

* Thu May 14 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0-0.20090408.1mdv2010.0
+ Revision: 375761
- Update to new version 20090408
- Add some Debian patches:
  * Use grey background
  * Link with libgif
  * Segmentation fault fix

* Sat Mar 14 2009 Emmanuel Andry <eandry@mandriva.org> 1.0-0.20090224.1mdv2009.1
+ Revision: 355093
- New version 20090224
- update docs
- diff P2 to fix string format not literal

* Fri Sep 05 2008 Emmanuel Andry <eandry@mandriva.org> 1.0-0.20080828.1mdv2009.0
+ Revision: 281388
- New version

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.0-0.20071210.1mdv2009.0
+ Revision: 222751
- fix 'Installed (but unpackaged) file(s) found'
- parallel build is broken
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Giuseppe GhibÃ² <ghibo@mandriva.com>
    - Release 20071210.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Oct 13 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.0-0.20071002.1mdv2008.1
+ Revision: 97895
- Release: 20071002.

* Tue Sep 04 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-0.20070831.1mdv2008.0
+ Revision: 79024
- fd.o icons
- drop old menu file and X-Mandriva XDG category
- use draft license policy (-like, not Style)
- new snapshot 20070831


* Sat Feb 24 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.0-0.20061220.2mdv2007.0
+ Revision: 125431
- Added Patch0 so to avoid libuninameslist-devel into Requires.
- Added Patch1 for local helpdir.
- Added libxml2-devel to BuildRequires.

* Sun Jan 21 2007 David Walluck <walluck@mandriva.org> 1.0-0.20061220.1mdv2007.1
+ Revision: 111228
- 20061220

* Thu Aug 24 2006 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 1.0-0.20060715.2mdv2007.0
+ Revision: 57538
- fix xdg menu (categories, name, comment)
- use %%find_lang for translations
- remove rpath
- don't bzip2 icons
- drop redundant doc dir

* Fri Aug 11 2006 Bruno Cornec <Bruno.Cornec@mandriva.org> 1.0-0.20060715.1mdv2007.0
+ Revision: 55478
- THanks to F. Crozat for the remark anbout the forgotten \
- desktop file was not in %%files
- XDG compliance added following http://qa.mandriva.com/twiki/bin/view/Main/MenuMigrationToXDG
- Updated to 20060715
  Patches not used anymore but stil in SVN for now in case I missed something.
- import fontforge-1.0-0.20060125.2mdk

* Mon May 15 2006 Stefan van der Eijk <stefan@eijk.nu> 1.0-0.20060125.2mdk
- rebuild for sparc

* Sat Feb 04 2006 Giuseppe Ghibò <ghibo@mandriva.com> 1.0-0.20060125.1mdk
- Release: 20060125.
- Added PDF tutorial.

* Wed Dec 28 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.0-0.20051205.1mdk
- Release: 20051202.
- Rebuilt Patch1.

* Sat Nov 26 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.0-0.20051023.2mdk
- fix menu entry (#14732)

* Thu Oct 27 2005 Abel Cheung <deaddog@mandriva.org> 1.0-0.20051023.1mdk
- Release: 20051023.
- Adapted Patch1 (partially merged upstream).

* Thu Aug 25 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.0-0.20050809.1mdk
- Release: 20050809.

* Sat Aug 06 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.0-0.20050803.1mdk
- Release: 20050803.

* Tue Jun 28 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.0-0.20050624.1mdk
- Release: 20050624.
- Removed Patch0 (merged upstream).
- Adapted Patch1.

* Mon Feb 14 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0-0.20050209.1mdk
- Release: 20050209.
- Fixed helpdir (Patch2).

* Tue Jan 18 2005 Abel Cheung <deaddog@mandrake.org> 1.0-0.20041231.2mdk
- Don't obsolete/provide pfaedit, pfaedit should still stay (ghibo)
- UTF-8 spec

* Sun Jan 16 2005 Abel Cheung <deaddog@mandrake.org> 1.0-0.20041231.1mdk
- New release
- Updated cidmaps to 2004-12-22
- Obsoletes pfaedit
- Parallel build broken
- P0: fix detection of libxkbui
- P1: Adds DESTDIR support and --mode=* option to libtool calls
- (Seems not working very well, is urw-fonts broken?)

* Thu Aug 26 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0-0.20040824.1mdk
- Release: 20040824.
- Removed Patch0, merged upstream.

* Sun Aug 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0-0.20040703.2mdk
- Added Patch0 to get global variables like $fontversion working correctly.

* Fri Jul 30 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0-0.20040703.1mdk
- Initial release.

