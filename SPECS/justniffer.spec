Name:           justniffer
Version:        0.5.15
Release:        1%{?dist}
Summary:        TCP sniffer that displays flows in a customizable way

License:        GPLv3
URL:            http://justniffer.sourceforge.net/
Source0:        https://github.com/onotelli/justniffer/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  libpcap-devel
BuildRequires:  boost-devel
BuildRequires:  boost-iostreams
BuildRequires:  boost-program-options
BuildRequires:  boost-regex
BuildRequires:  python
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  bash
BuildRequires:  tar
BuildRequires:  patch
Requires:       boost-iostreams
Requires:       boost-program-options
Requires:       boost-regex
Requires:       python

%description
justniffer is a TCP sniffer. It reassembles and reorders packets and displays the tcp flow in a customizable way. It can log network traffic in web server log format. It can also log network services performances (e.g. web server response times) and extract http content (images, html, scripts, etc)


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
mkdir -p %{buildroot}%{_docdir}/%{name}
gzip -c ChangeLog > %{buildroot}%{_docdir}/%{name}/changelog.gz
gzip -c debian/copyright > %{buildroot}%{_docdir}/%{name}/copyright.gz
install README %{buildroot}%{_docdir}/%{name}/README

mkdir -p %{buildroot}%{_datadir}/%{name}
(cd python; make install DESTDIR=%{buildroot})

%files
%dir %{_docdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%doc %{_mandir}/man8/justniffer.8.gz
%doc %{_docdir}/%{name}/*
%{_bindir}/justniffer
%{_bindir}/justniffer-grab-http-traffic
%{_datadir}/%{name}/scripts/*

%changelog
