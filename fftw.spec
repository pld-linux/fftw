Summary:	Fast Fourier transform library
Summary(pl):	Biblioteka z funkacjami szybkiej transformaty Fouriera
Name:		fftw
Version:	2.1.3
Release:	8
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.fftw.org/pub/fftw/%{name}-%{version}.tar.gz
Patch0:		%{name}-info.patch
Icon:		fftw-logo-thumb.gif
URL:		http://www.fftw.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FFTW is a collection of fast C routines for computing the Discrete
Fourier Transform in one or more dimensions. It includes complex,
real, and parallel transforms, and can handle arbitrary array sizes
efficiently. This RPM package includes both the double- and
single-precision FFTW uniprocessor and threads libraries.

%description -l pl
FFTW jest zbiorem szybkich funkcji C do obliczania dyskretnych
transformacji Fouriera w jedym lub wiêcej wymiarach. Zawiera równie¿
z³o¿one, rzeczywiste oraz równoleg³e transformacje i potrafi wydajnie
radziæ sobie z tablicami o dowolnych rozmiarach. Ten pakiet RPM
zawiera zarówno uniprocesor FFTW o pojedynczej i podwójnej precyzji
jak i biblioteki w±tków.

%package devel
Summary:	Headers, libraries & docs for fftw
Summary(pl):	Nag³ówki, biblioteki oraz dokumentacja do fftw
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

%package static
Summary:	Static fftw libraries
Summary(pl):	Statyczne biblioteki fftw
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static fftw libraries.

%description static -l pl
Statyczne biblioteki fftw.

%prep
%setup -q
%patch -p1

%build
%configure2_13 \
%ifarch %{ix86}
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-threads \
	--%{!?debug:disable}%{?debug:enable}-debug

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
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*
%{_infodir}/fftw.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
