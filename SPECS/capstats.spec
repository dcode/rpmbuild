Name:           capstats
Version:        0.25
Release:        1%{?dist}
Summary:        A command-line tool collecting packet statistics

License:        BSD
URL:            https://www.bro.org/sphinx/components/capstats/README.html
Source0:        http://www.bro.org/downloads/%{name}-%{version}.tar.gz
Patch0:         capstats-0.21-configure.patch

BuildRequires:  cmake
BuildRequires:  libpcap-devel

%description
capstats is a small tool to collect statistics on the current load of a
network interface, using either libpcap or the native interface for Endace's.
It reports statistics per time interval and/or for the tool’s total run-time.

%prep
%setup -q
%patch0 -p1 -b .configure

%build
%configure --disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

%files
%doc CHANGES COPYING README
%{_bindir}/%{name}

%changelog
* Mon Sep 25 2017 Derek Ditch <derek@rocknsm.io> - 0.25-1
- Update to new upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.22-1
- Update to new upstream release 0.22

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.21-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.21-1
- Update to new upstream release 0.21

* Mon Feb 17 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.20-1
- Initial package
