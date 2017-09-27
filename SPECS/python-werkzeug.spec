# Created by pyp2rpm-3.2.2
%global pypi_name Werkzeug
%global pkg_name werkzeug
%if 0%{?fedora} || 0%{?epel} > 6
# keeping python3 subpackage as stdlib mock lives in a different namespace
# Some people may have not fixed their imports
%bcond_without with_python3
%else
%bcond_with with_python3
%endif


Name:           python-%{pkg_name}
Version:        0.12.2
Release:        1%{?dist}
Summary:        The Swiss Army knife of Python web development

License:        BSD
URL:            http://werkzeug.pocoo.org/
Source0:        https://github.com/pallets/%{pkg_name}/archive/%{version}.tar.gz#/%{pkg_name}-%{version}.tar.gz
Patch0:         https://github.com/pallets/werkzeug/commit/fe37756adc77e46f7753eeeaf8dc0b34394951e2.patch#/werkzeug-0.12.2-versionfix.patch
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-sphinx

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with_python3

%description
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility modules. It
includes a powerful debugger, full featured request and response objects, HTTP
utilities to handle entity tags, cache control headers, HTTP dates, cookie
handling, file uploads, a powerful URL routing system and a bunch of community
contributed addon...

%package -n     python2-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkg_name}}
 
Requires:       python2-watchdog
Requires:       python2-termcolor
%description -n python2-%{pkg_name}
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility modules. It
includes a powerful debugger, full featured request and response objects, HTTP
utilities to handle entity tags, cache control headers, HTTP dates, cookie
handling, file uploads, a powerful URL routing system and a bunch of community
contributed addon...

%if 0%{?with_python3}
%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}
 
Requires:       python3-watchdog
Requires:       python3-termcolor
%description -n python3-%{pkg_name}
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility modules. It
includes a powerful debugger, full featured request and response objects, HTTP
utilities to handle entity tags, cache control headers, HTTP dates, cookie
handling, file uploads, a powerful URL routing system and a bunch of community
contributed addon...
%endif # with_python3

%package -n python-%{pkg_name}-doc
Summary:        Werkzeug documentation
%description -n python-%{pkg_name}-doc
Documentation for Werkzeug

%prep
%autosetup -n %{pkg_name}-%{version} -p1
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x

# generate html docs 
sphinx-build -b html docs/ docs/_build/html/
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif # with_python3

%py2_install


%files -n python2-%{pkg_name}
%license werkzeug/debug/shared/FONT_LICENSE LICENSE
%doc README.rst
%{python2_sitelib}/werkzeug
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%license werkzeug/debug/shared/FONT_LICENSE LICENSE
%doc README.rst
%{python3_sitelib}/werkzeug
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%files -n python-%{pkg_name}-doc
%doc docs/_build/html examples
%license werkzeug/debug/shared/FONT_LICENSE LICENSE

%changelog
* Thu Jul 20 2017 dcode - 0.12.2-1
- Initial package.
