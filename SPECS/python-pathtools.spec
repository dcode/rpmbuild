%global upname pathtools

Name:		python-%{upname}
Version:	0.1.2
Release:	9%{?dist}
Summary:	Pattern matching and various utilities for file systems paths

License:	MIT
URL:		https://github.com/gorakhargosh/%{upname}
Source0:	https://pypi.python.org/packages/source/p/%{upname}/%{upname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-setuptools

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	python-sphinx-theme-flask

BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-sphinx-theme-flask
%endif

%description
%{name} is a Python API library for common path
and pattern functionality.


%if 0%{?fedora} || 0%{?rhel} >= 8
%package -n python3-%{upname}
Summary:	Pattern matching and various utilities for file systems paths

%description  -n python3-%{upname}
%{name} is a Python API library for common path
and pattern functionality.
%endif


%prep
%setup -qn %{upname}-%{version}

# remove hashbang from lib's files
sed -i -e '/#!\//d' pathtools/*.py

# Python3 for Fedora and EL7+,
# no autodocs for RHEL <= 6 , but a hint
%if 0%{?fedora} || 0%{?rhel} >= 8
rm -rf %{py3dir} py3_docs
cp -a . %{py3dir}
%else
cat > README.docs << EOF
The version of python-sphinx in RHEL <= 6 is much too dated for building
this packages documentation.  Even python-sphinx 1.0.8 fails to build them.
If you need some good documentation and API reference, please visit:

http://pythonhosted.org/pathtools/
EOF
%endif


%build
%{__python} setup.py build

%if 0%{?fedora} || 0%{?rhel} >= 8
pushd docs
make html
rm -rf build/html/.build*
popd

pushd %{py3dir}
%{__python3} setup.py build
pushd docs
make html
rm -rf build/html/.build*
popd
%endif


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?fedora} || 0%{?rhel} >= 8
mv %{py3dir}/docs py3_docs
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif


%check
%{__python} setup.py test

%if 0%{?fedora} || 0%{?rhel} >= 8
pushd %{py3dir}
%{__python3} setup.py test
%endif


%files
%doc AUTHORS LICENSE README
%if 0%{?fedora} || 0%{?rhel} >= 8
%doc docs/build/html
%else
%doc README.docs
%endif
%{python_sitelib}/*

%if 0%{?fedora} || 0%{?rhel} >= 8
%files -n python3-%{upname}
%doc AUTHORS LICENSE README py3_docs/build/html
%{python3_sitelib}/*
%endif


%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug 12 2013 Björn Esser <bjoern.esser@gmail.com> - 0.1.2-1
- Initial RPM release (#996088)
