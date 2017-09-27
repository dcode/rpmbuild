%global pypi_name case
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif


# docs depend on package sphinx_celery
# https://github.com/celery/sphinx_celery
%global with_docs 0

Name:           python-%{pypi_name}
Version:        1.5.2
Release:        3%{?dist}
Summary:        Python unittest Utilities

License:        BSD
URL:            http://github.com/celery/case
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-coverage >= 3.0
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python2-mock

%description
%{summary}

%package -n     python2-%{pypi_name}
Summary:        Python unittest Utilities
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-six
Requires:       python-setuptools >= 0.7
Requires:       python-nose >= 1.3.7
Requires:       python-setuptools
BuildRequires:  python-unittest2
BuildRequires:  python-nose
%description -n python2-%{pypi_name}
%{summary}

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Python unittest Utilities
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-six
Requires:       python3-setuptools >= 0.7
Requires:       python3-nose >= 1.3.7
Requires:       python3-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-coverage >= 3.0
BuildRequires:  python3-setuptools
BuildRequires:  python3-unittest2
BuildRequires:  python3-nose

%description -n python3-%{pypi_name}
%{summary}
%endif

%if 0%{?with_docs} > 0
%package -n python-%{pypi_name}-doc
Summary:        case documentation
%description -n python-%{pypi_name}-doc
Documentation for case
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


%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
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
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Matthias Runge <mrunge@redhat.com> - 1.5.2-2
- add missing builddeps: python[23]-unittest2, python[23]-nose

* Tue Dec 27 2016 Matthias Runge <mrunge@redhat.com> - 1.5.2-1
- Initial package. (rhbz#1408868)
