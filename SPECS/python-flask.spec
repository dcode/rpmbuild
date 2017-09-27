# Created by pyp2rpm-3.2.2
%global pypi_name Flask
%global pkg_name flask
%if 0%{?fedora} || 0%{?epel} > 6
# keeping python3 subpackage as stdlib mock lives in a different namespace
# Some people may have not fixed their imports
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{pkg_name}
Version:        0.12.2
Epoch:          1
Release:        1%{?dist}
Summary:        A microframework based on Werkzeug, Jinja2 and good intentions

License:        BSD
URL:            http://github.com/pallets/flask/
Source0:        https://files.pythonhosted.org/packages/source/F/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-sphinx

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with_python3

%description
--Flask is a microframework for Python based on Werkzeug, Jinja 2 and good
intentions. And before you ask: It's BSD licensed!Flask is Fun Save in a
hello.py:.. code:: python from flask import Flask app Flask(__name__)
@app.route("/") def hello(): return "Hello World!" if __name__ "__main__":
app.run()And Easy to Setup And run it:.. code:: bash $ pip install Flask $
python hello.py * Running on...

%package -n     python2-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pkg_name}}
 
Requires:       python2-werkzeug >= 0.7
Requires:       python2-jinja2 >= 2.4
Requires:       python2-itsdangerous >= 0.21
Requires:       python2-click >= 2.0
%description -n python2-%{pkg_name}
--Flask is a microframework for Python based on Werkzeug, Jinja 2 and good
intentions. And before you ask: It's BSD licensed!Flask is Fun Save in a
hello.py:.. code:: python from flask import Flask app Flask(__name__)
@app.route("/") def hello(): return "Hello World!" if __name__ "__main__":
app.run()And Easy to Setup And run it:.. code:: bash $ pip install Flask $
python hello.py * Running on...

%if 0%{?with_python3}
%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}
 
Requires:       python3-werkzeug >= 0.7
Requires:       python3-jinja2 >= 2.4
Requires:       python3-itsdangerous >= 0.21
Requires:       python3-click >= 2.0
%description -n python3-%{pkg_name}
--Flask is a microframework for Python based on Werkzeug, Jinja 2 and good
intentions. And before you ask: It's BSD licensed!Flask is Fun Save in a
hello.py:.. code:: python from flask import Flask app Flask(__name__)
@app.route("/") def hello(): return "Hello World!" if __name__ "__main__":
app.run()And Easy to Setup And run it:.. code:: bash $ pip install Flask $
python hello.py * Running on...
%endif # with_python3

%package -n python-%{pkg_name}-doc
Summary:        Flask documentation
%description -n python-%{pkg_name}-doc
Documentation for Flask

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3
# generate html docs 
PYTHONPATH=`pwd` sphinx-build -b html docs/ docs/_build/html/
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
%license artwork/LICENSE docs/license.rst LICENSE
%doc 
%{python2_sitelib}/flask
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%if %{?with_python3:0}%{!?with_python3:1}
/usr/bin/flask
%endif # with_python3

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%license artwork/LICENSE docs/license.rst LICENSE
%doc 
%{python3_sitelib}/flask
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
/usr/bin/flask
%endif # with_python3

%files -n python-%{pkg_name}-doc
%doc docs/_build/html examples
%license artwork/LICENSE docs/license.rst LICENSE


%changelog
* Thu Jul 20 2017 dcode - 0.12.2-1
- Initial package.
