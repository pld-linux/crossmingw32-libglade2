%define		realname libglade2
Summary:	libglade library - cross Mingw32 version
Summary(pl.UTF-8):	Biblioteka do ładowania definicji interfejsu generowanego programem glade - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	2.6.4
Release:	2
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libglade/2.6/libglade-%{version}.tar.bz2
# Source0-md5:	d1776b40f4e166b5e9c107f1c8fe4139
Patch0:		%{realname}-gmodule-link.patch
Patch1:		%{realname}-no-gnome-common.patch
URL:		https://developer.gnome.org/libglade/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	crossmingw32-atk >= 1.18.0
BuildRequires:	crossmingw32-gettext
BuildRequires:	crossmingw32-gtk+2 >= 2.10.13
BuildRequires:	crossmingw32-libxml2 >= 2.6.29
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	python >= 2.0
BuildRequires:	python-modules >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	crossmingw32-atk >= 1.18.0
Requires:	crossmingw32-gtk+2 >= 2.10.13
Requires:	crossmingw32-libxml2 >= 2.6.29
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%define		_ssp_cflags		%{nil}
%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
This library allows you to load user interfaces in your program, which
are stored externally. This allows alteration of the interface without
recompilation of the program. The interfaces can also be edited with
GLADE.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteka libglade umożliwia dynamiczne ładowanie definicji
interfejsu użytkownika generowanego za pomocą programu glade. Taka
separacja definicji interfejsu umożliwia pracę nad nim bez
konieczności rekompilacji programu.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libglade library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libglade (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libglade library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libglade (wersja skrośna mingw32).

%package dll
Summary:	DLL libglade library for Windows
Summary(pl.UTF-8):	Biblioteka DLL libglade dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-atk-dll >= 1.18.0
Requires:	crossmingw32-gtk+2-dll >= 2.10.13
Requires:	crossmingw32-libxml2-dll >= 2.6.29
Requires:	wine

%description dll
DLL libglade library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libglade dla Windows.

%prep
%setup -q -n libglade-%{version}
%patch0 -p1
%patch1 -p1

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__glib_gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	lt_cv_deplibs_check_method=pass_all \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk-doc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglade-*.la

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/libglade-convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{gtk-doc,xml}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libglade-2.0.dll.a
%{_pkgconfigdir}/libglade-2.0.pc
%{_includedir}/libglade-2.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libglade-2.0.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libglade-2.0-0.dll
