ARCH:=x86_64
DIST:=.el7.centos

SPECS := $(wildcard SPECS/*.spec)
SPEC_TARGETS=$(foreach template,$(wildcard TEMPLATES/*.spec.in),$( echo $(template) | sed 's/\.in//'))
SRPM_TARGETS=$(foreach spec,$(SPECS),$(shell rpmspec -P $(spec) | awk '/^Name:/{name=$$2}; /^Version:/{version=$$2}; /^Release:/{release=$$2}; END { print name"-"version"-"release".src.rpm"}'))
RPM_TARGETS=$(foreach srpm,$(SRPM_TARGETS),$(shell echo $(srpm) | sed 's/src.rpm/$(ARCH).rpm/'))

PWD:=$(shell pwd)

all: rpm

.PHONY: rpm srpm setup all clean

rpm:   $(addprefix RPMS/,$(RPM_TARGETS))
srpm:  $(addprefix SRPMS/,$(SRPM_TARGETS))
specs: $(addprefix SPECS/,$(SPEC_TARGETS))

#$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm

.SECONDEXPANSION:
SRPMS/%.src.rpm: SPECS/$$(firstword $$(subst -, ,%)).spec
	spectool -g -C SOURCES $<
	rpmbuild -bs --nodeps $<

RPMS/%.x86_64.rpm: SRPMS/%.src.rpm 
	@mock -r ./rock-7-x86_64.cfg --resultdir=$(PWD)/RPMS $<

copr_submit:
	curl -XPOST \
	    -F metadata='{"project_id": 10395, "chroots": ["fedora-26-x86_64", "centos-7-x86_64"], "enable_net": false}' \
            -F "srpm=@$(srpm);type=application/x-rpm" \
            https://copr.fedorainfracloud.org/api_2/builds

clean:
	rm -rf SOURCES/$(SOURCE) ./tmp/ RPMS 
