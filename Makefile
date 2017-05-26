ARCH:=x86_64
DIST:=.el7.centos

SPECS := $(wildcard SPECS/*.spec)
SRPM_TARGETS=$(foreach spec,$(SPECS),$(shell cat $(spec) | awk '/^Name:/{name=$$2}; /^Version:/{version=$$2}; /^Release:/{release=gensub(/([0-9]+).*/, "\\1", "g", $$2)}; END { print name"-"version"-"release"$(DIST).src.rpm"}'))

PWD:=$(shell pwd)

all: rpm

.PHONY: rpm srpm setup all clean

rpm:   RPMS/$(NAME)-$(VERSION)-$(RELEASE)$(SNAPSHOT)$(DIST).$(ARCH).rpm
srpm:  $(addprefix SRPMS/,$(SRPM_TARGETS))
#$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm

.SECONDEXPANSION:
SRPMS/%.src.rpm: SPECS/$$(firstword $$(subst -, ,%)).spec
	spectool -g -C SOURCES $<
	rpmbuild -bs --nodeps $<

RPMS/%.x86_64.rpm: SRPMS/%.src.rpm 
	@mock --offline -r ./rock-7-x86_64.cfg --resultdir=$(PWD)/RPMS $<

%:	SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm

copr_submit:
	curl -XPOST \
	    -F metadata='{"project_id": 10395, "chroots": ["fedora-26-x86_64", "centos-7-x86_64"], "enable_net": false}' \
            -F "srpm=@$(srpm);type=application/x-rpm" \
            https://copr.fedorainfracloud.org/api_2/builds

clean:
	rm -rf SOURCES/$(SOURCE) ./tmp/ RPMS 
