%global desc An open source asynchronous task queue/job queue based on\
distributed message passing. It is focused on real-time\
operation, but supports scheduling as well.\
\
The execution units, called tasks, are executed concurrently\
on one or more worker nodes using multiprocessing, Eventlet\
or gevent. Tasks can execute asynchronously (in the background)\
or synchronously (wait until ready).\
\
Celery is used in production systems to process millions of\
tasks a day.\
\
Celery is written in Python, but the protocol can be implemented\
in any language. It can also operate with other languages using\
web hooks.\
\
The recommended message broker is RabbitMQ, but limited support\
for Redis, Beanstalk, MongoDB, CouchDB and databases\
(using SQLAlchemy or the Django ORM) is also available.\

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif


Name:           python-celery
Version:        4.0.2
Release:        2%{?dist}
BuildArch:      noarch

License:        BSD
URL:            http://celeryproject.org
Source0:        https://github.com/celery/celery/archive/v%{version}/%{name}-%{version}.tar.gz
Summary:        Distributed Task Queue


%description
%desc


%package doc
Summary: Documentation for python-celery

%description doc
Documentation for python-celery.


%package -n python2-celery
Summary:        Distributed Task Queue

%{?python_provide:%python_provide python2-celery}

Requires:       pyparsing
Requires:       python-amqp
Requires:       python-anyjson
Requires:       python-billiard >= 1:3.3.0.22
Requires:       python-kombu >= 1:3.0.33
Requires:       python2-setuptools
Requires:       pytz

BuildRequires:  python2-billiard
BuildRequires:  python2-kombu
BuildRequires:  python-sqlalchemy
BuildRequires:  python2-devel
BuildRequires:  python2-rpm-macros
BuildRequires:  python2-setuptools
BuildRequires:  python-sphinx



%description -n python2-celery
%{desc}


%if %{?with_python3:1}%{!?with_python3:0}
%package -n python3-celery
Summary:        Distributed Task Queue

%{?python_provide:%python_provide python3-celery}

Requires:       python3-amqp
Requires:       python3-billiard >= 1:3.3.0.22
Requires:       python3-kombu >= 1:3.0.33
Requires:       python3-pytz
Requires:       python3-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-setuptools


%description -n python3-celery
%{desc}
%endif # with_python3

%prep
%autosetup -n celery-%{version}


%build
%py2_build
%if %{?with_python3:1}%{!?with_python3:0}
%py3_build
%endif # with_python3

pushd docs
# missing python-sphinx_celery (for the moment)
#make %{?_smp_mflags} html
popd


%install
%if %{?with_python3:1}%{!?with_python3:0}
%py3_install
pushd %{buildroot}%{_bindir}
mv celery celery-3
ln -s celery-3 celery-%{python3_version}
popd
%endif # with_python3

%py2_install
pushd %{buildroot}%{_bindir}
ln -s celery celery-2
ln -s celery-2 celery-%{python2_version}
popd


%files doc
%license LICENSE
#%doc docs/.build/html/*


%files -n python2-celery
%license LICENSE
%doc README.rst TODO CONTRIBUTORS.txt examples
%{_bindir}/celery
%{_bindir}/celery-2*
#%{_bindir}/celerybeat
#%{_bindir}/celerybeat-2*
#%{_bindir}/celeryd
#%{_bindir}/celeryd-2*
#%{_bindir}/celeryd-multi
#%{_bindir}/celeryd-multi-2*
%{python2_sitelib}/celery-*.egg-info
%{python2_sitelib}/celery

%if %{?with_python3:1}%{!?with_python3:0}
%files -n python3-celery
%license LICENSE
%doc README.rst TODO CONTRIBUTORS.txt examples
%{_bindir}/celery-3*
#%{_bindir}/celerybeat-3*
#%{_bindir}/celeryd-3*
#%{_bindir}/celeryd-multi-3*
%{python3_sitelib}/celery-*.egg-info
%{python3_sitelib}/celery
%endif # with_python3

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Matthias Runge <mrunge@redhat.com> - 4.0.2-1
- upgrade to 4.0.x (rhbz#1400270, rhbz#1410864)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.1.20-5
- Rebuild for Python 3.6

* Mon Nov 28 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.1.20-4
- Remove obsolete Requires for python-uuid

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.20-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Randy Barlow <rbarlow@redhat.com> - 3.1.20-1
- update to 3.1.20 (#1080882).

* Sat Jan 23 2016 Randy Barlow <rbarlow@redhat.com> - 3.1.19-1
- update to 3.1.19 (#1080882).
- Remove conditionals on Python 3 - always build for Python 3.
- Remove tests as they were disabled and don't pass anyway.
- Update to use the python2/3 naming conventions.
- Use the fancy new Python macros (#1300083).
- Add a -doc subpackage (#1223099).
- Use the license macro (#1223099).
- Remove dependency on importlib, since it is present in 2.7 and 3.5.

* Tue Dec 01 2015 Brian Bouterse <bbouters@redhat.com> - 3.1.11-1
- update to 3.1.11

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> - 3.1.9-1
- update to 3.1.9 (rhbz#1055304)

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> - 3.1.7-4
- add runtime requirement pyzu (rhbz#1069774)
- remove runtime req. python-dateutil

* Fri Jan 10 2014 Matthias Runge <mrunge@redhat.com> - 3.1.7-3
- add runtime requirement python-setuptools (rhbz#1051176)

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.1.7-2
- require correct python-kombu-version

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.1.7-1
- update to 3.1.7 (rhbz#1034115)
- add more explicit requirement to python-billiard (rhbz#1028626)

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 3.0.24-1
- update to 3.0.24 (rhbz#1018596)

* Fri Sep 27 2013 Matthias Runge <mrunge@redhat.com> - 3.0.23-1
- update to 3.0.23 (rhbz#979595)

* Fri Sep 27 2013 Matthias Runge <mrunge@redhat.com> - 3.0.19-4
- add python-amqp to deps
- add requirement python-amqp
- fix requirements: python3-kombu, python3-pytz, python3-dateutil and billiard
- separate binaries for py3 and py (fixes rhbz#1000750)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Matthias Runge <mrunge@redhat.com> - 3.0.19-1
- update to celery-3.0.19 (rhbz#919560)

* Fri Feb 15 2013 Matthias Runge <mrunge@redhat.com> - 3.0.15-1
- update to celery-3.0.15 (rhbz#909919)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Matthias Runge <mrunge@redhat.com> - 3.0.13-1
- update to upstream version 3.0.13 (rhbz#892923)

* Wed Nov 14 2012 Matthias Runge <mrunge@redhat.com> - 3.0.12-1
- update to upstream version 3.0.12

* Tue Oct 16 2012 Matthias Runge <mrunge@redhat.com> - 3.0.11-1
- update to upstream version 3.0.11

* Sun Aug 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 3.0.7-1
- update to upstream version 3.0.7

* Thu Aug 23 2012 Matthias Runge <mrunge@matthias-runge.de> - 3.0.6-1
- update to upstream version 3.0.6

* Fri Aug 03 2012 Matthias Runge <mrunge@matthias-runge.de> - 3.0.5-1
- update to version 3.0.5
- enable python3 support

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 2.2.8-1
- Security FIX CELERYSA-0001

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 2.2.7-3
- Fix rpmlint errors
- Fix dependencies

* Sat Jun 25 2011 Andrew Colin Kissa <andrew@topdog.za.net> 2.2.7-2
- Update for RHEL6

* Tue Jun 21 2011 Andrew Colin Kissa <andrew@topdog.za.net> 2.2.7-1
- Initial package
