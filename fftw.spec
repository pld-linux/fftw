Summary:	Fast Fourier transform library
Summary(pl):	biblioteka z funkacjami szybkiej transformaty Fouriera
Name:		fftw
Version:	2.1.3
Release:	8
License:	GPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	����������
Group(uk):	��̦�����
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
transformacji Fouriera w jedym lub wi�cej wymiarach. Zawiera r�wnie�
z�o�one, rzeczywiste oraz r�wnoleg�e transformacje i potrafi wydajnie
radzi� sobie z tablicami o dowolnych rozmiarach. Ten pakiet RPM
zawiera zar�wno uniprocesor FFTW o pojedynczej i podw�jnej precyzji
jak i biblioteki w�tk�w.

%package devel
Summary:	headers, libraries, & docs for fftw
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	%{name} = %{version}

%description devel
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%package static
Summary:	Static fftw libraries
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	%{name}-devel = %{version}

%description static
Static fftw libraries.

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
