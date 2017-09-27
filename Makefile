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

%: srpm/%
	make RPMS/$(shell rpmspec -P --define='dist $(DIST)' SPECS/$(<F).spec | awk '/^Name:/{name=$$2}; /^Version:/{version=$$2}; /^Release:/{release=$$2}; END { print name"-"version"-"release".$(ARCH).rpm"}')

srpm/%:	SPECS/%.spec 
	make SRPMS/$(shell rpmspec -P --define='dist $(DIST)' $< | awk '/^Name:/{name=$$2}; /^Version:/{version=$$2}; /^Release:/{release=$$2}; END { print name"-"version"-"release".src.rpm"}')

#$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm

.SECONDEXPANSION:
SRPMS/%.src.rpm:
	make SPECS/$(shell echo $@ | sed -E 's/^SRPMS\///; s/\-[0-9]+(\.[0-9]*)?(\.[0-9]*)?-[0-9]+.*\.centos\.src\.rpm//').spec
	@spectool -g -C SOURCES SPECS/$(shell echo $@ | sed -E 's/^SRPMS\///; s/\-[0-9]+(\.[0-9]*)?(\.[0-9]*)?-[0-9]+.*\.centos\.src\.rpm//').spec
	@mock -r ./rock-7-x86_64.cfg --buildsrpm --resultdir=$(PWD)/SRPMS  --source=$(PWD)/SOURCES --spec=SPECS/$(shell echo $@ | sed -E 's/^SRPMS\///; s/\-[0-9]+(\.[0-9]*)?(\.[0-9]*)?-[0-9]+.*\.centos\.src\.rpm//').spec

RPMS/%.x86_64.rpm: SRPMS/%.src.rpm 
	@mock -r ./rock-7-x86_64.cfg --no-clean --no-cleanup-after --resultdir=$(PWD)/RPMS $<
	rm RPMS/$(<F)

copr_submit:
	curl -XPOST \
	    -F metadata='{"project_id": 10395, "chroots": ["fedora-26-x86_64", "centos-7-x86_64"], "enable_net": false}' \
            -F "srpm=@$(srpm);type=application/x-rpm" \
            https://copr.fedorainfracloud.org/api_2/builds

clean:
	rm -rf SOURCES/$(SOURCE) ./tmp/ RPMS 
	@mock -r ./rock-7-x86_64.cfg clean
