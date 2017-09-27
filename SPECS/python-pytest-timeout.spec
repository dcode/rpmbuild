%global pypi_name pytest-timeout
%global desc This is a plugin which will terminate tests after a certain timeout. When doing\
so it will show a stack dump of all threads running at the time. This is useful\
when running tests under a continuous integration server or simply if you don’t\
know why the test suite hangs.
%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        3%{?dist}
Summary:        py.test plugin to abort hanging tests

License:        MIT
URL:            https://bitbucket.org/pytest-dev/pytest-timeout/
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pytest
%if %{?with_python3:1}%{!?with_python3:0}
BuildRequires:  python3-devel
#BuildRequires:  python3-pytest
%endif # with_python3

%description
%{desc}

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-pytest
%description -n python2-%{pypi_name}
%{desc}

%if %{?with_python3:1}%{!?with_python3:0}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-pytest
%description -n python3-%{pypi_name}
%{desc}
%endif # with_python3

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build
%if %{?with_python3:1}%{!?with_python3:0}
%py3_build
%endif # with_python3

%install
%py2_install
%if %{?with_python3:1}%{!?with_python3:0}
%py3_install
%endif # with_python3


%files -n python2-%{pypi_name}
%doc README
%license LICENSE
%{python2_sitelib}/pytest_timeout*

%if %{?with_python3:1}%{!?with_python3:0}
%files -n python3-%{pypi_name}
%doc README
%license LICENSE
%{python3_sitelib}/pytest_timeout*
%{python3_sitelib}/__pycache__/pytest_timeout*
%endif # with_python3

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.0-2
- Rebuild for Python 3.6

* Thu Aug 11 2016 Scott Talbert <swt@techie.net> - 1.0.0-1
- Initial package.
