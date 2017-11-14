# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

%global srcname xkcdpass
%global sum     Generate secure multiword passwords/passphrases, inspired by XKCD

Name:           python-%{srcname}
Version:        1.14.1
Release:        1%{?dist}
Summary:        %{sum}
License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}/
Source0:        https://files.pythonhosted.org/packages/source/x/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with python3

%description
A flexible and scriptable password generator which generates strong passphrases, inspired by XKCD 936.

%if %{with python3}
%package     -n python3-%{srcname}
Summary:        %{sum}

%description -n python3-%{srcname}
A flexible and scriptable password generator which generates strong passphrases, inspired by XKCD 936.

%endif # with python3

%package     -n python2-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A flexible and scriptable password generator which generates strong passphrases, inspired by XKCD 936.


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%if %{with python3}
%py3_build
%endif # with python3

%install
rm -rf $RPM_BUILD_ROOT
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python3 version
# to be the default for now on Fedora).
%py2_install

%if %{with python3}
%py3_install
%endif # with python3


%check
%{__python2} setup.py test

%if %{with python3}
%{__python3} setup.py test
%endif

%files -n python2-%{srcname}
%license LICENSE.BSD
%doc README.rst examples/ xkcdpass.1

%{python2_sitelib}/*

%if ! %{with python3}
/usr/bin/%{srcname}
%endif

%if %{with python3}
%files -n python3-%{srcname}
%license LICENSE.BSD
%doc README.rst examples/ xkcdpass.1

%{python3_sitelib}/*
/usr/bin/%{srcname}

%endif # with python3


%changelog
* Tue Nov  7 2017 Derek Ditch <derek@rocknsm.io>
- Initial packaging
