Summary:	fast fourier transform library
Name:		fftw
Version:	2.1.2
Release:	3
Copyright:	GPL
Icon:		fftw-logo-thumb.gif
Group:		Libraries
Source:		ftp://theory.lcs.mit.edu/pub/fftw/%{name}-%{version}.tar.gz
Patch:		fftw-info.patch
Prereq:		/sbin/install-info
URL:		http://theory.lcs.mit.edu/~fftw/
BuildRoot:	/tmp/%{name}-%{version}-root

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions. It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently. This
RPM package includes both the double- and single-precision FFTW uniprocessor
and threads libraries.

%package devel
Summary:	headers, libraries, & docs for fftw
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier transform
library.

%package static
Summary:	Static fftw libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static fftw libraries.

%prep
%setup -q
%patch -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
%ifarch i386 i486 i586 i686
	--enable-i386-hacks \
%endif
	--enable-shared \
	--enable-type-prefix \
	--enable-threads

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/fftw.info*

%post
/sbin/install-info %{_infodir}/%{name}.info.gz /etc/info-dir >&2

%preun
if [ "$1" = "0" ]; then
        /sbin/install-info --delete %{_infodir}/%{name}.info.gz \
                /etc/info-dir >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
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
