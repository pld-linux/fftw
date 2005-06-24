#
# Conditional build
%bcond_without  single            # without single precision library

Summary:	Fast Fourier transform library
Summary(pl):	Biblioteka z funkcjami szybkiej transformaty Fouriera
Summary(pt_BR):	Biblioteca fast Fourier transform
Name:		fftw
Version:	2.1.5
Release:	2
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
# Source0-md5:	8d16a84f3ca02a785ef9eb36249ba433
Patch0:		%{name}-info.patch
Icon:		fftw-logo-thumb.gif
URL:		http://www.fftw.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FFTW is a collection of fast C routines for computing the Discrete
Fourier Transform in one or more dimensions. It includes complex,
real, and parallel transforms, and can handle arbitrary array sizes
efficiently. This RPM package includes the double precision FFTW
uniprocessor and threads libraries.

%description -l pl
FFTW jest zbiorem szybkich funkcji C do obliczania dyskretnych
transformat Fouriera w jednym lub wiêcej wymiarach. Zawiera równie¿
zespolone, rzeczywiste oraz równoleg³e transformaty i potrafi wydajnie
radziæ sobie z tablicami o dowolnych rozmiarach. Ten pakiet RPM
zawiera wersje FFTW o podwójnej precyzji dla architektur
jednoprocesorowych oraz z obs³ug± w±tków.

%description -l pt_BR
FFTW é uma coleção de rotinas rápidas em C para computar a Discrete
Fourier Transform em uma ou mais dimensões. Incluindo transformações
complexas, reais e paralelas, também pode manipular vetores de tamanho
arbitrário eficientemente. Esse pacote RPM inclui bibliotecas FFTW com
suporte a threads, normal e dupla precisão (Os arquivos de precisão
normal tem um prefixo "s").

%package devel
Summary:	Headers, libraries & docs for fftw
Summary(pl):	Nag³ówki, biblioteki oraz dokumentacja do fftw
Summary(pt_BR):	headers, bibliotecas e documentação do pacote FFTW
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains the additional header files, documentation and
Libraries you need to develop programs using the FFTW (fast Fourier
transform library).

%description devel -l pl
Ten pakiet zawiera dodatkowe pliki nag³ówkowe, dokumentacjê oraz
biblioteki niezbêdne do tworzenia programów u¿ywaj±cych biblioteki
FFTW (fast Fourier transform library).

%description devel -l pt_BR
Este pacote contém documentação, headers e bibliotecas adicionais para
desenvolver programas usando a FFTW.

%package static
Summary:	Static fftw libraries
Summary(pl):	Statyczne biblioteki fftw
Summary(pt_BR):	bibliotecas estáticas do pacote FFTW
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static fftw libraries.

%description static -l pl
Statyczne biblioteki fftw.

%description static -l pt_BR
Este pacote contém as bibliotecas estáticas do pacote FFTW.

%prep
%setup -q
%patch -p1

%build
# This is important to do sfftw (Single precision library)
%if %{with single}
cp -r ../%{name}-%{version} ../single
cd ../single

%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%ifarch %{ix86}
        --enable-i386-hacks \
%endif
        --enable-shared \
        --enable-threads \
        --enable-float \
	--enable-type-prefix \
        --%{!?debug:dis}%{?debug:en}able-debug

%{__make}

cd -
%endif

%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%ifarch %{ix86}
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-threads \
	--%{!?debug:dis}%{?debug:en}able-debug
#        --enable-type-prefix \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with single}
cd ../single
%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT
cd -
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_infodir}/fftw.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
