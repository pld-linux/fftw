# RPM spec file for FFTW.
# This file is used to build Redhat Package Manager packages for the
# FFTW library.  Such packages make it easy to install and uninstall
# the library and related files from binaries or source.
#
# This spec file is for version 2.1.2 of FFTW, and will need to be
# modified for future releases.  First, the string "2.1.2" should
# be replaced everywhere in this file with the new version number.
# Second, the shared library version numbers (in the %files list)
# will need to be updated.  Any other changes in the installed files
# list, build commands, etcetera will of course also require changes.
#
# The icon associated with this package can be downloaded from:
#     http://theory.lcs.mit.edu/~fftw/fftw-logo-thumb.gif
# and will need to be placed in the SOURCES directory to build the RPM.
#
Name: fftw
Summary: fast fourier transform library
Version: 2.1.2
Release: 3
Copyright: GPL
Icon: fftw-logo-thumb.gif
Group: Libraries
Prefix: /usr
Source: ftp://theory.lcs.mit.edu/pub/fftw/fftw-2.1.2.tar.gz
URL: http://theory.lcs.mit.edu/~fftw
BuildRoot: /var/tmp/fftw-%{PACKAGE_VERSION}-root

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.
This RPM package includes both the double- and single-precision FFTW
uniprocessor and threads libraries.
%package devel
Summary: headers, libraries, & docs for FFTW fast fourier transform library
Group: Development/Libraries
Prefix: /usr
Requires: fftw = 2.1.2
%description devel
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%prep
%setup

%ifarch i386
./configure --enable-shared --enable-type-prefix --enable-i386-hacks --enable-threads --prefix=%prefix
%else
./configure --enable-shared --enable-type-prefix --enable-threads --prefix=%prefix
%endif

%build

make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

# hack to also compile/install single-precision version:
make distclean
%ifarch i386
./configure --enable-shared --enable-type-prefix --enable-threads --enable-float --prefix=%prefix --enable-i386-hacks
%else
./configure --enable-shared --enable-type-prefix --enable-threads --enable-float --prefix=%prefix
%endif
make prefix=$RPM_BUILD_ROOT%{prefix} install

%files
/usr/lib/libdfftw.so.2.0.4
/usr/lib/libdfftw_threads.so.2.0.4
/usr/lib/libdrfftw.so.2.0.4
/usr/lib/libdrfftw_threads.so.2.0.4
/usr/lib/libsfftw.so.2.0.4
/usr/lib/libsfftw_threads.so.2.0.4
/usr/lib/libsrfftw.so.2.0.4
/usr/lib/libsrfftw_threads.so.2.0.4
/usr/lib/libdfftw.so.2
/usr/lib/libdfftw_threads.so.2
/usr/lib/libdrfftw.so.2
/usr/lib/libdrfftw_threads.so.2
/usr/lib/libsfftw.so.2
/usr/lib/libsfftw_threads.so.2
/usr/lib/libsrfftw.so.2
/usr/lib/libsrfftw_threads.so.2
%files devel
/usr/info/fftw.info
/usr/info/fftw.info-1
/usr/info/fftw.info-2
/usr/info/fftw.info-3
/usr/info/fftw.info-4
/usr/info/fftw.info-5
/usr/include/dfftw.h
/usr/include/dfftw_threads.h
/usr/include/drfftw.h
/usr/include/drfftw_threads.h
/usr/include/sfftw.h
/usr/include/sfftw_threads.h
/usr/include/srfftw.h
/usr/include/srfftw_threads.h
/usr/lib/libdfftw.a
/usr/lib/libdfftw.la
/usr/lib/libdfftw.so
/usr/lib/libdfftw_threads.a
/usr/lib/libdfftw_threads.la
/usr/lib/libdfftw_threads.so
/usr/lib/libdrfftw.a
/usr/lib/libdrfftw.la
/usr/lib/libdrfftw.so
/usr/lib/libdrfftw_threads.a
/usr/lib/libdrfftw_threads.la
/usr/lib/libdrfftw_threads.so
/usr/lib/libsfftw.a
/usr/lib/libsfftw.la
/usr/lib/libsfftw.so
/usr/lib/libsfftw_threads.a
/usr/lib/libsfftw_threads.la
/usr/lib/libsfftw_threads.so
/usr/lib/libsrfftw.a
/usr/lib/libsrfftw.la
/usr/lib/libsrfftw.so
/usr/lib/libsrfftw_threads.a
/usr/lib/libsrfftw_threads.la
/usr/lib/libsrfftw_threads.so

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug 03  1999 Dax Kelson <dax@gurulabs.com>
- Set prefix to /usr so there is no need to futz with ldconfig
