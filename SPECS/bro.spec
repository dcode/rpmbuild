# Conditionals
%bcond_without afpacket
%bcond_without kafka

Name:           bro
Version:        2.5.1
Release:        1%{dist}
Summary:        Bro is a powerful framework for network analysis and security monitoring

License:        BSD-3-Clause
URL:            http://bro.org
Source0:        https://www.bro.org/downloads/%{name}-%{version}.tar.gz
Patch0:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/eaa0424012bcce69ce2efcaaa03066596b9d9664/install-symlink-old-cmake.patch
Patch1:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/bc14d4ffa8c445abc8eedfd68053bee9fa9a08c1/cmake-2.6.patch
Patch2:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/6e20e150aaef566a4ff8cb543146cbaf52dee8cb/bro-kafka-configurable-timestamps.patch
Patch3:         https://gist.githubusercontent.com/dcode/5e58fed4df358983738244ade4d100e3/raw/a435afbcc1b71182e826358c32f9205cab71a8d2/bro-findkernelheaders-hack.patch
Source1:        https://github.com/J-Gras/bro-af_packet-plugin/archive/master.tar.gz#/bro-plugin-afpacket-%{version}.tar.gz
Source2:        https://github.com/JonZeolla/metron-bro-plugin-kafka/archive/master.tar.gz#/bro-plugin-kafka-%{version}.tar.gz
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
Requires:       bind-libs
Requires:       GeoIP
%ifnarch s390 s390x
Requires:       gperftools
%endif
Requires:       jemalloc
Requires:       libpcap
%if 0%{?fedora} >= 26
Requires:       compat-openssl10
%else
Requires:       openssl
%endif
Requires:       zlib

BuildRequires:  bind-devel
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  GeoIP-devel
BuildRequires:  gcc-c++
%ifnarch s390 s390x
BuildRequires:  gperftools-devel
%endif
BuildRequires:  jemalloc-devel
BuildRequires:  libpcap-devel
%if 0%{?fedora} >= 26
BuildRequires:  compat-openssl10-devel
%else
BuildRequires:  openssl-devel
%endif
BuildRequires:  python2-devel
BuildRequires:  python-tools
BuildRequires:  swig
BuildRequires:  zlib-devel

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

%description -n libbroccoli
The broccoli library

%package -n libbroccoli-devel
Summary:        Development files for broccoli
Requires:       libbroccoli = %{version}-%{release}
Requires:       pkgconfig

%description -n libbroccoli-devel
Eat more Broccoli!

%package -n python2-broccoli
Summary:        Python bindings for libbroccoli
BuildRequires:  python2-devel
Requires:       libbroccoli = %{version}-%{release}
Provides:       python-broccoli


%description -n python2-broccoli
Provides Python bindings for libbroccoli

%package -n broctl
Summary:        Bro Control
BuildRequires:  python-devel
BuildRequires:  systemd
Requires:       python2
Requires:       bash
Requires:       libbroccoli = %{version}-%{release}
Requires:       python2-broccoli = %{version}-%{release}
Requires:       bro-core = %{version}-%{release}
#Requires:      pysubnettree
#Requires:      trace-summary
#Requires:      capstats
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n broctl
This is Bro Control

#%package doc
#Summary:          Documentation for bro
#
#BuildRequires:    python-sphinx
#BuildRequires:    doxygen
#BuildRequires:    rsync
#
#%description doc
#This package contains the documentation for bro.

###################### Begin Bro Plugins ##############################
%if %{with afpacket}
%package -n bro-plugin-af_packet
Summary:	AF_PACKET input plugin for Bro
Requires:	bro-core = %{version}
BuildRequires:	kernel-devel 
BuildRequires:  kernel-headers

%description -n bro-plugin-af_packet
This plugin provides native AF_Packet support for Bro.
%endif

%if %{with kafka}
%package -n bro-plugin-kafka
Summary:	Kafka logging plugin for Bro
Requires:	bro-core = %{version} librdkafka1 
BuildRequires:	librdkafka-devel

%description -n bro-plugin-kafka
This plugin provides native Kafka logging support for Bro.
%endif

###################### End Bro Plugins ################################

%prep
%setup -n bro-%{version} -q
# some platforms do in-source builds when using cmake. I don't really care, so just patch the error out.
find ./ -name "ProhibitInSourceBuild.cmake" | xargs -I file sh -c 'cat /dev/null > "file"'
%patch0 -p0
%if 0%{?centos_version} == 600 || 0%{?scientificlinux_version} == 600 || 0%{?rhel_version} == 505
%patch1 -p0
%endif

%if %{with afpacket}
rm -rf aux/plugins/af_packet
mkdir -p aux/plugins/af_packet
pushd aux/plugins/af_packet
gzip -dc %{_sourcedir}/bro-plugin-afpacket-%{version}.tar.gz | tar -xvvf - --strip-components=1
popd
%endif

%if %{with kafka}
rm -rf aux/plugins/kafka
mkdir -p aux/plugins/kafka
pushd aux/plugins/kafka
gzip -dc %{_sourcedir}/bro-plugin-kafka-%{version}.tar.gz | tar -xvvf - --strip-components=1
popd
%endif

# Apply plugins patches
#%patch2 -p1
%patch3 -p1

%build
./configure \
   --prefix=%{_prefix} \
   --enable-debug \
   --enable-mobile-ipv6 \
   --disable-broker
#   --libdir=%{_libdir} \
#   --conf-files-dir=%{_sysconfdir}/bro \
#   --python-install-dir=%{python2_sitelib} 
 
make %{?_smp_mflags}

%if %{with afpacket}
# Build af_packet plugin
pushd aux/plugins/af_packet
./configure  --install-root=%{buildroot}/%{_libdir}/bro/plugins
make %{?_smp_mflags}
popd
%endif

%if %{with kafka}
## Build kafka plugin
pushd aux/plugins/kafka
./configure --install-root=%{buildroot}/%{_libdir}/bro/plugins
make %{?_smp_mflags}
popd
%endif

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Install some aux tools
%{__install} -m 755 ./build/aux/bro-aux/adtrace/adtrace %{buildroot}/%{_prefix}/bin/
%{__install} -m 755 ./build/aux/bro-aux/rst/rst %{buildroot}/%{_prefix}/bin/

############# Install plugins #################
%if %{with afpacket}
# af_packet
pushd aux/plugins/af_packet
make install INSTALL="install -p" #DESTDIR=%{buildroot} 
popd
%endif

%if %{with kafka}
# kafka plugin
pushd aux/plugins/kafka
make install INSTALL="install -p" #DESTDIR=%{buildroot} 
popd
%endif

# Create spool dir
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/tmp
touch %{?buildroot}/%{_prefix}/spool/broctl-config.sh


# Create logs dir
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/logs

touch %{?buildroot}/%{_prefix}/spool/broctl-config.sh

# Remove devel, junk, and zero length files
find "%{buildroot}%{_prefix}" -iname "*.la" -delete;
find "%{buildroot}" -iname "*.log" -delete;
rm -rf %{buildroot}%{_includedir}/binpac.h.in

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

%post
/sbin/ldconfig
%systemd_post bro.service

%preun
%systemd_preun bro.service

%postun
%systemd_postun bro.service

%postin -n libbroccoli
/sbin/ldconfig

%postin -n libbroccoli-devel
/sbin/ldconfig

%postun -n libbroccoli
/sbin/ldconfig

%postun -n libbroccoli-devel
/sbin/ldconfig


%files
%doc CHANGES COPYING NEWS README VERSION

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
%config(noreplace) %{_sysconfdir}/broctl.cfg
%config(noreplace) %{_sysconfdir}/networks.cfg
%config(noreplace) %{_sysconfdir}/node.cfg
%defattr(0664,root,bro,2770)
%dir %{_prefix}/spool
%{_prefix}/spool/broctl-config.sh
%dir %{_prefix}/logs

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

%files -n python2-broccoli
%{_libdir}/broctl/broccoli_intern.py*
%{_libdir}/broctl/_broccoli_intern.so
%{_libdir}/broctl/broccoli.py*


%if %{with afpacket}
%files -n bro-plugin-af_packet
%defattr(-,root,bro,0755)
%dir %{_libdir}/bro/plugins/Bro_AF_Packet
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/broctl
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/scripts

%{_libdir}/bro/plugins/Bro_AF_Packet/__bro_plugin__
%{_libdir}/bro/plugins/Bro_AF_Packet/broctl/*
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/*.so
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_AF_Packet/scripts/*.bro
%endif

%if %{with kafka}
%files -n bro-plugin-kafka
%defattr(-,root,bro,0755)
%dir %{_libdir}/bro/plugins/APACHE_KAFKA
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/lib
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/lib/bif
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache/Kafka
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Bro
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Bro/Kafka

%{_libdir}/bro/plugins/APACHE_KAFKA/CHANGES
%{_libdir}/bro/plugins/APACHE_KAFKA/COPYING
%{_libdir}/bro/plugins/APACHE_KAFKA/VERSION
%{_libdir}/bro/plugins/APACHE_KAFKA/__bro_plugin__
%{_libdir}/bro/plugins/APACHE_KAFKA/lib/*.so
%{_libdir}/bro/plugins/APACHE_KAFKA/lib/bif/*.bro
%{_libdir}/bro/plugins/APACHE_KAFKA/scripts/*.bro
%{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache/Kafka/*.bro
%{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Bro/Kafka/*.bro

%endif


%changelog
* Mon Sep 25 2017 Derek Ditch <derek@rocknsm.io> 2.5.1-1
- Updated to upstream 2.5.1
- Updated to upstream plugin packages for Kafka and AF_Packet
- Fixed issue where building AF_Packet plugin couldn't find kernel headers
- Fixed compilation on Fedora 26 w/ openssl compat libs

* Mon Feb 09 2015 Johanna Amann <build@xxon.net> 2.4-680
- Nightly build version specification

* Wed Jan 28 2015 Johanna Amann <build@xxon.net> 2.3.2
- Update to Bro 2.3.2

* Wed Oct 29 2014 Johanna Amann <build@xxon.net> 2.3.1
- Initial version
