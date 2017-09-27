%global pypi_name termcolor
%global sum ANSI Color formatting for output in terminal

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        12%{?dist}
Summary:        %{sum}

License:        MIT
URL:            http://pypi.python.org/pypi/termcolor/1.1.0
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif

%description
ANSI Color formatting for output in terminal.


%package -n python2-%{pypi_name}
Summary:  %{sum}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
A Python 2 version of ANSI Color formatting for output in terminal.

%if %{with python3}
%package -n python3-%{pypi_name}
Summary:  %{sum}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
A Python 3 version of ANSI Color formatting for output in terminal.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}


%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%files -n python2-%{pypi_name}
%doc README.rst
%license COPYING.txt
%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info


%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license COPYING.txt
%{python3_sitelib}/%{pypi_name}.py*
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

# there is an asterisk in the name of the file,
# because sometimes the suffix of the architecture is added
%{python3_sitelib}/__pycache__/%{pypi_name}.cpython-%{python3_version_nodots}*.py?
%endif

%changelog
* Sun Jul 23 2017 Derek Ditch <derek@rocknsm.io> - 1.1.0-12
- Backported for CentOS 7
- Added conditionals for Python 3 support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 24 2016 Matthias Runge <mrunge@redhat.com> - 1.1.0-8
- fix typo in summary (rhbz#1263051)
- source location updated

* Fri May 06 2016 Dominika Krejci <dkrejci@redhat.com> - 1.1.0-7
- added support for Python 3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Matthias Runge <mrunge@matthias-runge.de> - 1.1.0-1
- Initial package.
