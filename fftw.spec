#
# Conditional build
%bcond_without	single		# without single precision library
#
Summary:	Fast Fourier Transform library
Summary(pl.UTF-8):	Biblioteka z funkcjami szybkiej transformaty Fouriera
Summary(pt_BR.UTF-8):	Biblioteca fast Fourier transform
Name:		fftw
Version:	2.1.5
Release:	5
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

%description -l pl.UTF-8
FFTW jest zbiorem szybkich funkcji C do obliczania dyskretnych
transformat Fouriera w jednym lub więcej wymiarach. Zawiera również
zespolone, rzeczywiste oraz równoległe transformaty i potrafi wydajnie
radzić sobie z tablicami o dowolnych rozmiarach. Ten pakiet RPM
zawiera wersje FFTW o pojedyńczej i podwójnej precyzji dla architektur
jednoprocesorowych oraz z obsługą wątków.

%description -l pt_BR.UTF-8
FFTW é uma coleção de rotinas rápidas em C para computar a Discrete
Fourier Transform em uma ou mais dimensões. Incluindo transformações
complexas, reais e paralelas, também pode manipular vetores de tamanho
arbitrário eficientemente. Esse pacote RPM inclui bibliotecas FFTW com
suporte a threads, normal e dupla precisão (Os arquivos de precisão
normal tem um prefixo "s").

%package devel
Summary:	Header files and development documentation for FFTW library
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty do biblioteki FFTW
Summary(pt_BR.UTF-8):	Headers e documentação do pacote FFTW
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the additional header files and documentation
you need to develop programs using the FFTW (fast Fourier transform
library).

%description devel -l pl.UTF-8
Ten pakiet zawiera dodatkowe pliki nagłówkowe oraz dokumentację do
tworzenia programów używających biblioteki FFTW (fast Fourier
transform library).

%description devel -l pt_BR.UTF-8
Este pacote contém documentação e headers adicionais para desenvolver
programas usando a FFTW.

%package static
Summary:	Static FFTW libraries
Summary(pl.UTF-8):	Statyczne biblioteki FFTW
Summary(pt_BR.UTF-8):	bibliotecas estáticas do pacote FFTW
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FFTW libraries.

%description static -l pl.UTF-8
Statyczne biblioteki FFTW.

%description static -l pt_BR.UTF-8
Este pacote contém as bibliotecas estáticas do pacote FFTW.

%package single
Summary:	Single-precision Fast Fourier Transform libraries
Summary(pl.UTF-8):	Biblioteki szybkiej transformaty Fouriera pojedynczej precyzji
Group:		Libraries
Conflicts:	fftw < 2.1.5-4

%description single
Single-precision Fast Fourier Transform libraries.

%description single -l pl.UTF-8
Biblioteki szybkiej transformaty Fouriera pojedynczej precyzji.

%package single-devel
Summary:	Header files for single-precision FFTW libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek FFTW pojedynczej precyzji
Group:		Development/Libraries
Requires:	%{name}-single = %{version}-%{release}

%description single-devel
Header files for single-precision FFTW libraries.

%description single-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek FFTW pojedynczej precyzji.

%package single-static
Summary:	Static single-precision FFTW libraries
Summary(pl.UTF-8):	Statyczne biblioteki FFTW pojedynczej precyzji
Group:		Development/Libraries
Requires:	%{name}-single-devel = %{version}-%{release}

%description single-static
Static single-precision FFTW libraries.

%description single-static -l pl.UTF-8
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

%post devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

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
