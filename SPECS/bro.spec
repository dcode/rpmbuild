#
# spec file for package Bro
#
# Copyright (c) 1995-2014 The Regents of the University of California
# through the Lawrence Berkeley National Laboratory and the
# International Computer Science Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
# (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# (3) Neither the name of the University of California, Lawrence Berkeley
#     National Laboratory, U.S. Dept. of Energy, International Computer
#     Science Institute, nor the names of contributors may be used to endorse
#     or promote products derived from this software without specific prior
#     written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Note that some files in the distribution may carry their own copyright
# notices.

# Conditionals
%bcond_without afpacket
%bcond_without kafka
%bcond_with myricom

Name:           bro
Version:        2.5
Release:        1%{dist}
Summary:        Bro is a powerful framework for network analysis and security monitoring
Group:          Productivity/Networking/Diagnostic

License:        BSD-3-Clause
URL:            http://bro.org
Source0:        https://www.bro.org/downloads/%{name}-%{version}.tar.gz
Patch0:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/eaa0424012bcce69ce2efcaaa03066596b9d9664/install-symlink-old-cmake.patch
Patch1:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/bc14d4ffa8c445abc8eedfd68053bee9fa9a08c1/cmake-2.6.patch
Patch2:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/6e20e150aaef566a4ff8cb543146cbaf52dee8cb/bro-kafka-configurable-timestamps.patch

Requires:       bro-core = %{version}
Requires:       broctl = %{version}
Requires:       libbroccoli = %{version}
Requires(pre):  /usr/sbin/groupadd, /usr/bin/getent

%if %{defined rhel_version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%define _prefix     /opt/bro
%define _sysconfdir %{_prefix}/etc
%define _libdir     %{_prefix}/lib
%define _mandir     %{_prefix}/share/man

%if %{with myricom}
%define with_snf /opt/snf
%endif

%if 0%{?suse_version}
%define __cmake /usr/bin/cmake
%endif

%description
Bro is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Bro
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Bro has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Bro's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.

%package -n bro-core
Summary:        The core bro installation without broctl
Group:          Productivity/Networking/Diagnostic
BuildRequires:  flex bison cmake openssl-devel zlib-devel python-devel swig gcc-c++
BuildRequires:  libpcap-devel

%description -n bro-core
Bro is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Bro
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Bro has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Bro's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.

%package -n libbroccoli
Summary:        Broccoli library
Group:          System/Libraries

%description -n libbroccoli
The broccoli library

%package -n libbroccoli-devel
Summary:        Development files for broccoli
Group:          Development/Libraries/C and C++
Requires:       libbroccoli = %{version}

%description -n libbroccoli-devel
Eat more Broccoli!

%package -n python-broccoli
Summary:        Python bindings for libbroccoli
Group:          System/Libraries

BuildRequires:  python2-devel
Requires:       libbroccoli = %{version}

%description -n python-broccoli
Provides Python bindings for libbroccoli

%package -n broctl
Summary:        Bro Control
Group:          Productivity/Networking/Diagnostic
Requires:       python
Requires:       libbroccoli = %{version}
Requires:       python-broccoli = %{version}
Requires:       bro-core = %{version}
%if 0%{?suse_version}
Requires:       python-curses
%endif

%description -n broctl
This is Bro Control

%if %{with afpacket}
%package -n bro-plugin-af_packet
Summary:	AF_PACKET input plugin for Bro
Group:		Productivity/Networking/Diagnostic
Requires:	bro-core = %{version}
BuildRequires:	kernel-devel kernel-headers

%description -n bro-plugin-af_packet
This plugin provides native AF_Packet support for Bro.
%endif

%if %{with kafka}
%package -n bro-plugin-kafka
Summary:	Kafka logging plugin for Bro
Group:		Productivity/Networking/Diagnostic
Requires:	bro-core = %{version} librdkafka1 
BuildRequires:	librdkafka-devel

%description -n bro-plugin-kafka
This plugin provides native Kafka logging support for Bro.
%endif

%if %{with myricom}
%package -n bro-plugin-myricom
Summary:	Myricom input plugin for Bro
Group:		Productivity/Networking/Diagnostic
Requires:	bro-core = %{version} myri_snf
BuildRequires:	kernel-devel kernel-headers myri_snf

%description -n bro-plugin-myricom
This plugin provides native Myricom support for Bro.
%endif

%pre
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro

%pre -n bro-core
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro

%pre -n broctl
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro

%pre -n libbroccoli
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro

%pre -n libbroccoli-devel
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro

%prep
%setup -n bro-%{version} -q
# some platforms do in-source builds when using cmake. I don't really care, so just patch the error out.
find ./ -name "ProhibitInSourceBuild.cmake" | xargs -I file sh -c 'cat /dev/null > "file"'
%patch0 -p0
%if 0%{?centos_version} == 600 || 0%{?scientificlinux_version} == 600 || 0%{?rhel_version} == 505
%patch1 -p0
%endif

# Apply plugins patches
%patch2 -p1

%build
./configure --prefix=%{_prefix} --binary-package --disable-broker
make %{?_smp_mflags}

%if %{with afpacket}
# Build af_packet plugin
pushd aux/plugins/af_packet
./configure  --install-root=%{buildroot}%{_libdir}/bro/plugins
make %{?_smp_mflags}
popd
%endif

%if %{with kafka}
## Build kafka plugin
pushd aux/plugins/kafka
./configure --install-root=%{buildroot}%{_libdir}/bro/plugins
make %{?_smp_mflags}
popd
%endif

%if %{with myricom}
# Build myricom plugin
pushd aux/plugins/myricom
./configure --install-root=%{buildroot}%{_libdir}/bro/plugins --with-myricom=%{with_snf}
make %{?_smp_mflags}
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{defined rhel_version}
make install DESTDIR=$RPM_BUILD_ROOT

%else
%make_install

%endif

%if %{with afpacket}
# af_packet
pushd aux/plugins/af_packet
make install 
popd
%endif

%if %{with kafka}
# kafka plugin
pushd aux/plugins/kafka
make install
popd
%endif

%if %{with myricom}
## myricom plugin
pushd aux/plugins/myricom
make install
popd
%endif

mkdir -p %{?buildroot}/%{_prefix}/spool/tmp
mkdir -p %{?buildroot}/%{_prefix}/logs
touch %{?buildroot}/%{_prefix}/spool/broctl-config.sh

%post -n libbroccoli -p /sbin/ldconfig

%postun -n libbroccoli -p /sbin/ldconfig

%files

%files -n bro-core
%defattr(-,root,bro,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_datadir}
%dir %{_datadir}/bro
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man8
%{_bindir}/bro
%{_bindir}/bro-cut
%{_bindir}/bro-config
%{_bindir}/adtrace
%{_bindir}/rst
%{_datadir}/bro/base
%{_datadir}/bro/policy
%{_datadir}/bro/broxygen
%{_mandir}/man1/bro-cut.1
%{_mandir}/man8/bro.8
%defattr(0664,root,bro,2775)
%dir %{_datadir}/bro/site
%config %{_datadir}/bro/site/local-logger.bro
%config %{_datadir}/bro/site/local-manager.bro
%config %{_datadir}/bro/site/local-proxy.bro
%config %{_datadir}/bro/site/local-worker.bro
%config %{_datadir}/bro/site/local.bro

%files -n broctl
%defattr(-,root,bro,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_datadir}
%dir %{_datadir}/bro
%dir %{_libdir}
%dir %{_libdir}/broctl
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man8
%{_bindir}/broctl
%{_bindir}/capstats
%{_bindir}/trace-summary
%{_datadir}/broctl
%{_datadir}/bro/broctl
%{_libdir}/broctl/*.so
%{_libdir}/broctl/*.p*
%{_libdir}/broctl/plugins
%{_libdir}/broctl/BroControl
%{_mandir}/man8/broctl.8
%{_mandir}/man1/trace-summary.1
%defattr(0664,root,bro,2775)
%dir %{_sysconfdir}
%config %{_sysconfdir}/broctl.cfg
%config %{_sysconfdir}/networks.cfg
%config %{_sysconfdir}/node.cfg
%defattr(0664,root,bro,2770)
%{_prefix}/spool
%{_prefix}/logs

%files -n libbroccoli
%defattr(-,root,bro,0755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_libdir}
%{_bindir}/broccoli-config
%{_libdir}/libbroccoli.so.*
%defattr(0664,root,bro,2775)
%dir %{_sysconfdir}
%config %{_sysconfdir}/broccoli.conf

%files -n libbroccoli-devel
%defattr(-,root,bro,0755)
%dir %{_prefix}
%dir %{_includedir}
%dir %{_libdir}
%{_includedir}/broccoli.h
%{_libdir}/libbroccoli.so
%{_libdir}/libbroccoli.a

%if %{with afpacket}
%files -n bro-plugin-af_packet
%defattr(-,root,bro,0755)
%dir %{_libdir}/bro/plugins/Bro_AF_Packet
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/scripts
%{_libdir}/bro/plugins/Bro_AF_Packet/__bro_plugin__
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/*.so
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_AF_Packet/scripts/*.bro
%endif

%if %{with kafka}
%files -n bro-plugin-kafka
%defattr(-,root,bro,0755)
%dir %{_libdir}/bro/plugins/Bro_Kafka
%dir %{_libdir}/bro/plugins/Bro_Kafka/lib
%dir %{_libdir}/bro/plugins/Bro_Kafka/lib/bif
%dir %{_libdir}/bro/plugins/Bro_Kafka/scripts
%dir %{_libdir}/bro/plugins/Bro_Kafka/scripts/Bro
%dir %{_libdir}/bro/plugins/Bro_Kafka/scripts/Bro/Kafka
# TODO: These should be %doc
%{_libdir}/bro/plugins/Bro_Kafka/CHANGES
%{_libdir}/bro/plugins/Bro_Kafka/COPYING
%{_libdir}/bro/plugins/Bro_Kafka/README
%{_libdir}/bro/plugins/Bro_Kafka/VERSION
%{_libdir}/bro/plugins/Bro_Kafka/__bro_plugin__
%{_libdir}/bro/plugins/Bro_Kafka/lib/*.so
%{_libdir}/bro/plugins/Bro_Kafka/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_Kafka/scripts/*.bro
%{_libdir}/bro/plugins/Bro_Kafka/scripts/Bro/Kafka/*.bro

%endif

%if %{with myricom}
%files -n bro-plugin-myricom
%defattr(-,root,bro,0755)
%dir %{_libdir}/bro/plugins/Bro_Myricom
%dir %{_libdir}/bro/plugins/Bro_Myricom/lib
%dir %{_libdir}/bro/plugins/Bro_Myricom/lib/bif
%dir %{_libdir}/bro/plugins/Bro_Myricom/scripts
%{_libdir}/bro/plugins/Bro_Myricom/__bro_plugin__
%{_libdir}/bro/plugins/Bro_Myricom/lib/*.so
%{_libdir}/bro/plugins/Bro_Myricom/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_Myricom/scripts/*.bro
%{_libdir}/bro/plugins/Bro_Myricom/broctl/myricom.py
%{_libdir}/bro/plugins/Bro_Myricom/broctl/myricom.pyc
%{_libdir}/bro/plugins/Bro_Myricom/broctl/myricom.pyo
%endif

%doc CHANGES COPYING NEWS README VERSION

%changelog
* Mon Feb 09 2015 Johanna Amann <build@xxon.net> 2.4-680
Nightly build version specification
* Wed Jan 28 2015 Johanna Amann <build@xxon.net> 2.3.2
Update to Bro 2.3.2
* Wed Oct 29 2014 Johanna Amann <build@xxon.net> 2.3.1
Initial version
-
