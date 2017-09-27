%if 0%{?fedora}
%global with_python3 1
%endif

Name:           pysubnettree
Version:        0.27
Release:        1%{?dist}
Summary:        A Python Module for CIDR Lookups

License:        BSD
URL:            http://bro.org/sphinx/components/pysubnettree/README.html
Source0:        https://www.bro.org/downloads/%{name}-%{version}.tar.gz



BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  gcc-c++

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # with_python3

%description
The PySubnetTree package provides a Python data structure SubnetTree which
maps subnets given in CIDR notation (incl. corresponding IPv6 versions) to
Python objects. Lookups are performed by longest-prefix matching.

%prep
%autosetup

%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
chmod 0755 %{buildroot}%{python2_sitearch}/_SubnetTree.so

%files
%doc CHANGES README
%license COPYING
%{python2_sitearch}/*

%changelog
* Mon Sep 25 2017 Derek Ditch <derek@rocknsm.io> - 0.27-1
- Update to latest upstream release 0.27

* Wed May 13 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.24-1
- Update to lastest upstream release 0.24

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.23-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-3
- Fix macro

* Sun Jun 22 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-2
- Use PyPI as SOURCE0 for now
- Fix permission

* Fri Jun 20 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.23-1
- Initial package

