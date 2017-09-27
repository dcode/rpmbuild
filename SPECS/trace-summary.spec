Name:           trace-summary
Version:        0.87
Release:        1%{?dist}
Summary:        A script generating break-downs of network traffic

License:        BSD
URL:            http://bro.org/sphinx/components/trace-summary/README.html
Source0:        http://www.bro.org/downloads/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel

Requires:       pysubnettree

%description
trace-summary is a Python script that generates break-downs of network traffic,
including lists of the top hosts, protocols, ports, etc. Optionally, it can
generate output separately for incoming vs. outgoing traffic, per subnet, and
per time-interval.

%prep
%autosetup
sed -i 's|#! /usr/bin/env python|#!%{__python2}|g' trace-summary

%build
# nothing

%install
install -Dp -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc CHANGES README
%license COPYING
%{_bindir}/%{name}

%changelog
* Mon Sep 25 2017 Derek Ditch <derek@rocknsm.io> - 0.87-1
- Update to latest upstream release 0.87
- Revert to py2 for EL7

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.86-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.86-2
- Update shebang

* Sun Dec 25 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.86-1
- Update to latest upstream release 0.86

* Tue Aug 30 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.84-4
- Update for py3

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.84-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.84-1
- Update to latest upstream release 0.84

* Fri Jun 20 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.83-1
- Initial package
