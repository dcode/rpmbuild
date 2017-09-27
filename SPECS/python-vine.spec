%global pypi_name vine
%if 0%{?fedora}
%global with_python3 1
%endif

# docs depend on package sphinx_celery
# https://github.com/celery/sphinx_celery
%global with_docs 0

# tests depend on python-case
# https://bugzilla.redhat.com/show_bug.cgi?id=1408868
%global with_tests 0

Name:           python-%{pypi_name}
Version:        1.1.3
Release:        2%{?dist}
Summary:        Promises, promises, promises

License:        BSD
URL:            http://github.com/celery/vine
Source0:        https://files.pythonhosted.org/packages/source/v/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  pytest
BuildRequires:  python2-pytest-cov

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
%endif

%description
%{summary}


%package -n     python2-%{pypi_name}
Summary:        Promises, promises, promises
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{summary}

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Promises, promises, promises
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{summary}
%endif

%if 0%{?with_docs} > 0
%package -n python-%{pypi_name}-doc
Summary:        vine documentation
%description -n python-%{pypi_name}-doc
Documentation for vine
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

# docs depend on sphinx-celery
%if 0%{?with_docs} > 0
# generate html docs

sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif

%py2_install

%if 0%{?with_tests}
%check
py.test -xv --cov=vine --cov-report=xml --no-cov-on-fail

%if 0%{?with_python3}
py.test-3 -xv --cov=vine --cov-report=xml --no-cov-on-fail
%endif
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc docs/templates/readme.txt README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc docs/templates/readme.txt README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%if 0%{?with_docs} > 0
%files -n python-%{pypi_name}-doc
%doc html
%endif

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 27 2016 Matthias Runge <mrunge@redhat.com> - 1.1.3-1
- Initial package. (rhbz#1408869)
