#
# TODO: register glade-2.0.dtd
# TODO: consider moving libglade-convert to main package - it is used to converting old
# 	1.2.x version *.glade files to current structure.
%define		_realname   libglade2
Summary:	libglade library - cross Mingw32 version
Summary(es.UTF-8):El libglade permite que usted cargue archivos del interfaz del glade
Summary(pl.UTF-8):Biblioteka do ładowania definicji interfejsu generowanego programem glade - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Esta biblioteca permite carregar arquivos da interface glade
Name:		crossmingw32-%{_realname}
Version:	2.6.0
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libglade/2.6/libglade-%{version}.tar.bz2
# Source0-md5:	81d7b2b64871ce23a5fae1e5da0b1f6e
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossmingw32-atk >= 1.12.1
BuildRequires:	crossmingw32-gettext
BuildRequires:	crossmingw32-gtk+2 >= 2.10.0
BuildRequires:	crossmingw32-libxml2 >= 2.6.26
BuildRequires:	crossmingw32-pkgconfig
BuildRequires:	libtool
BuildRequires:	python >= 2.0
BuildRequires:	python-modules >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	FHS >= 2.3-16
Requires:	crossmingw32-atk >= 1.12.1
Requires:	python-modules >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
This library allows you to load user interfaces in your program, which
are stored externally. This allows alteration of the interface without
recompilation of the program. The interfaces can also be edited with
GLADE.

%description -l es.UTF-8
El libglade permite que usted cargue archivos del interfaz del glade
en tiempo de ejecución.

%description -l pl.UTF-8
Biblioteka libglade umożliwia dynamiczne ładowanie definicji
interfejsu użytkownika generowanego za pomocą programu glade. Taka
separacja definicji interfejsu umożliwia pracę nad nim bez
konieczności rekompilacji programu.

%description -l pt_BR.UTF-8
O libglade permite carregar, em tempo de execução, arquivos da
interface glade. Não é necessário ter o glade instalado, mas esta
é a melhor maneira de criar os arquivos de interface.

%prep
%setup -q -n libglade-%{version}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__glib_gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk-doc

%{__sed} -i -e 's/^deplibs_check_method=.*/deplibs_check_method="pass_all"/' libtool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/libglade/2.0

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_libdir}/libglade
%dir %{_datadir}/xml/libglade
%{_datadir}/xml/libglade/*.dtd
%attr(755,root,root) %{_bindir}/*
%{_pkgconfigdir}/*
%{_includedir}/libglade-*
