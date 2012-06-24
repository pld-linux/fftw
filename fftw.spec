#
# Conditional build
%bcond_without	single		# without single precision library
#
Summary:	Fast Fourier Transform library
Summary(pl):	Biblioteka z funkcjami szybkiej transformaty Fouriera
Summary(pt_BR):	Biblioteca fast Fourier transform
Name:		fftw
Version:	2.1.5
Release:	4
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
# Source0-md5:	8d16a84f3ca02a785ef9eb36249ba433
Patch0:		%{name}-info.patch
Patch1:		%{name}-link.patch
URL:		http://www.fftw.org/
BuildRequires:	autoconf
BuildRequires:	automake
# to detect proper F77 name mangling for fortran binding functions
BuildRequires:	gcc-g77
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FFTW is a collection of fast C routines for computing the Discrete
Fourier Transform in one or more dimensions. It includes complex,
real, and parallel transforms, and can handle arbitrary array sizes
efficiently. This RPM package includes the single and double precision
FFTW uniprocessor and threads libraries.

%description -l pl
FFTW jest zbiorem szybkich funkcji C do obliczania dyskretnych
transformat Fouriera w jednym lub wi�cej wymiarach. Zawiera r�wnie�
zespolone, rzeczywiste oraz r�wnoleg�e transformaty i potrafi wydajnie
radzi� sobie z tablicami o dowolnych rozmiarach. Ten pakiet RPM
zawiera wersje FFTW o pojedy�czej i podw�jnej precyzji dla architektur
jednoprocesorowych oraz z obs�ug� w�tk�w.

%description -l pt_BR
FFTW � uma cole��o de rotinas r�pidas em C para computar a Discrete
Fourier Transform em uma ou mais dimens�es. Incluindo transforma��es
complexas, reais e paralelas, tamb�m pode manipular vetores de tamanho
arbitr�rio eficientemente. Esse pacote RPM inclui bibliotecas FFTW com
suporte a threads, normal e dupla precis�o (Os arquivos de precis�o
normal tem um prefixo "s").

%package devel
Summary:	Header files and development documentation for FFTW library
Summary(pl):	Pliki nag��wkowe i dokumentacja programisty do biblioteki FFTW
Summary(pt_BR):	Headers e documenta��o do pacote FFTW
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the additional header files and documentation
you need to develop programs using the FFTW (fast Fourier transform
library).

%description devel -l pl
Ten pakiet zawiera dodatkowe pliki nag��wkowe oraz dokumentacj� do
tworzenia program�w u�ywaj�cych biblioteki FFTW (fast Fourier
transform library).

%description devel -l pt_BR
Este pacote cont�m documenta��o e headers adicionais para desenvolver
programas usando a FFTW.

%package static
Summary:	Static FFTW libraries
Summary(pl):	Statyczne biblioteki FFTW
Summary(pt_BR):	bibliotecas est�ticas do pacote FFTW
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FFTW libraries.

%description static -l pl
Statyczne biblioteki FFTW.

%description static -l pt_BR
Este pacote cont�m as bibliotecas est�ticas do pacote FFTW.

%package single
Summary:	Single-precision Fast Fourier Transform libraries
Summary(pl):	Biblioteki szybkiej transformaty Fouriera pojedynczej precyzji
Group:		Libraries
Conflicts:	fftw < 2.1.5-4

%description single
Single-precision Fast Fourier Transform libraries.

%description single -l pl
Biblioteki szybkiej transformaty Fouriera pojedynczej precyzji.

%package single-devel
Summary:	Header files for single-precision FFTW libraries
Summary(pl):	Pliki nag��wkowe bibliotek FFTW pojedynczej precyzji
Group:		Development/Libraries
Requires:	%{name}-single = %{version}-%{release}

%description single-devel
Header files for single-precision FFTW libraries.

%description single-devel -l pl
Pliki nag��wkowe bibliotek FFTW pojedynczej precyzji.

%package single-static
Summary:	Static single-precision FFTW libraries
Summary(pl):	Statyczne biblioteki FFTW pojedynczej precyzji
Group:		Development/Libraries
Requires:	%{name}-single-devel = %{version}-%{release}

%description single-static
Static single-precision FFTW libraries.

%description single-static -l pl
Statyczne biblioteki FFTW pojedynczej precyzji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# don't use pregenerated file
rm -f fftw/config.h

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%if %{with single}
install -d build-single
cd build-single
../%configure \
%ifarch %{ix86}
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-threads \
	--enable-float \
	--enable-type-prefix \
	--%{!?debug:dis}%{?debug:en}able-debug

%{__make}
cd ..
%endif

install -d build-double
cd build-double
../%configure \
%ifarch %{ix86}
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-threads \
	--%{!?debug:dis}%{?debug:en}able-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-single install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build-double install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post	single -p /sbin/ldconfig
%postun	single -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfftw.so.*.*.*
%attr(755,root,root) %{_libdir}/libfftw_threads.so.*.*.*
%attr(755,root,root) %{_libdir}/librfftw.so.*.*.*
%attr(755,root,root) %{_libdir}/librfftw_threads.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfftw.so
%attr(755,root,root) %{_libdir}/libfftw_threads.so
%attr(755,root,root) %{_libdir}/librfftw.so
%attr(755,root,root) %{_libdir}/librfftw_threads.so
%{_libdir}/libfftw.la
%{_libdir}/libfftw_threads.la
%{_libdir}/librfftw.la
%{_libdir}/librfftw_threads.la
%{_includedir}/fftw*.h
%{_includedir}/rfftw*.h
%{_infodir}/fftw.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfftw.a
%{_libdir}/libfftw_threads.a
%{_libdir}/librfftw.a
%{_libdir}/librfftw_threads.a

%files single
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsfftw.so.*.*.*
%attr(755,root,root) %{_libdir}/libsfftw_threads.so.*.*.*
%attr(755,root,root) %{_libdir}/libsrfftw.so.*.*.*
%attr(755,root,root) %{_libdir}/libsrfftw_threads.so.*.*.*

%files single-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsfftw.so
%attr(755,root,root) %{_libdir}/libsfftw_threads.so
%attr(755,root,root) %{_libdir}/libsrfftw.so
%attr(755,root,root) %{_libdir}/libsrfftw_threads.so
%{_libdir}/libsfftw.la
%{_libdir}/libsfftw_threads.la
%{_libdir}/libsrfftw.la
%{_libdir}/libsrfftw_threads.la
%{_includedir}/sfftw*.h
%{_includedir}/srfftw*.h

%files single-static
%defattr(644,root,root,755)
%{_libdir}/libsfftw.a
%{_libdir}/libsfftw_threads.a
%{_libdir}/libsrfftw.a
%{_libdir}/libsrfftw_threads.a
