Summary:	Fast Fourier transform library
Summary(pl):	Biblioteka z funkacjami szybkiej transformaty Fouriera
Summary(pt_BR):	biblioteca fast fourier transform
Name:		fftw
Version:	2.1.3
Release:	10
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
Icon:		fftw-logo-thumb.gif
URL:		http://www.fftw.org/
BuildRequires:	automake
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
libraries you need to develop programs using the FFTW (fast fourier
transform library).

%description devel -l pl
Ten pakiet zawiera dodatkowe pliki nag³ówkowe, dokumetacjê oraz
biblioteki niezbêdne do tworzenia programów u¿ywaj±cych biblioteki
FFTW (fast fourier transform library).

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
install %{_datadir}/automake/install-sh .
install %{_datadir}/automake/config.* .
%configure2_13 \
%ifarch %{ix86}
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-threads \
	--%{!?debug:dis}%{?debug:en}able-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
