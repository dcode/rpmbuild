# Created by pyp2rpm-3.2.2
%global pypi_name tonyg-rfc3339
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pypi_name}
Version:        0.1
Release:        1%{?dist}
Summary:        Python implementation of RFC 3339

License:        None
URL:            https://github.com/cardforcoin/python-rfc3339
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with python3

%description
%{summary}

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{summary}

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{summary}
%endif # with python3

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif # with python3

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if %{with python3}
%py3_install
%endif # with python3

%py2_install


%files -n python2-%{pypi_name}
%doc 

%{python2_sitelib}/rfc3339.py*
%{python2_sitelib}/tonyg_rfc3339-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc 

%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/rfc3339.py
%{python3_sitelib}/tonyg_rfc3339-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Sun Jul 23 2017 dcode - 0.1-1
- Initial package.
