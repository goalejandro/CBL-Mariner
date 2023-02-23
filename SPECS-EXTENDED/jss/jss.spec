Vendor:         Microsoft Corporation
Distribution:   Mariner
################################################################################
Name:           jss
################################################################################

Summary:        Java Security Services (JSS)
URL:            http://www.dogtagpki.org/wiki/JSS
License:        MPLv1.1 or GPLv2+ or LGPLv2+

# For development (i.e. unsupported) releases, use x.y.z-0.n.<phase>.
# For official (i.e. supported) releases, use x.y.z-r where r >=1.
Version:        5.1.0
Release:        1%{?_timestamp}%{?_commit_id}%{?dist}
#global         _phase -alpha2

# To generate the source tarball:
# $ git clone https://github.com/dogtagpki/jss.git
# $ cd jss
# $ git tag v4.5.<z>
# $ git push origin v4.5.<z>
# Then go to https://github.com/dogtagpki/jss/releases and download the source
# tarball.
Source:         https://github.com/dogtagpki/%{name}/archive/v%{version}%{?_phase}/%{name}-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > jss-VERSION-RELEASE.patch
# Patch: jss-VERSION-RELEASE.patch

################################################################################
# Java
################################################################################

%define java_devel java-17-openjdk-devel
%define java_headless java-17-openjdk-headless
%define java_home %{_jvmdir}/jre-17-openjdk

################################################################################
# Build Options
################################################################################

# By default the javadoc package will be built unless --without javadoc
# option is specified.

%bcond_without javadoc

# By default the build will not execute unit tests unless --with tests
# option is specified.

%bcond_with tests

################################################################################
# Build Dependencies
################################################################################

BuildRequires:  make
BuildRequires:  cmake >= 3.14
BuildRequires:  zip
BuildRequires:  unzip

BuildRequires:  gcc-c++
BuildRequires:  nss-devel >= 3.66
BuildRequires:  nss-tools >= 3.66
BuildRequires:  %{java_devel}
BuildRequires:  jpackage-utils
BuildRequires:  slf4j
BuildRequires:  slf4j-jdk14
BuildRequires:  apache-commons-lang3

BuildRequires:  junit

Requires:       nss >= 3.66
Requires:       %{java_headless}
Requires:       jpackage-utils
Requires:       slf4j
Requires:       slf4j-jdk14
Requires:       apache-commons-lang3

Conflicts:      ldapjdk < 4.20
Conflicts:      idm-console-framework < 1.2
Conflicts:      tomcatjss < 7.6.0
Conflicts:      pki-base < 10.10.0

%description
Java Security Services (JSS) is a java native interface which provides a bridge
for java-based applications to use native Network Security Services (NSS).
This only works with gcj. Other JREs require that JCE providers be signed.

%if %{with javadoc}
################################################################################
%package javadoc
################################################################################

Summary:        Java Security Services (JSS) Javadocs
Requires:       jss = %{version}-%{release}

%description javadoc
This package contains the API documentation for JSS.
%endif

################################################################################
%prep

%autosetup -n %{name}-%{version}%{?_phase} -p 1

################################################################################
%build

%set_build_flags

export JAVA_HOME=%{java_home}

# Enable compiler optimizations
export BUILD_OPT=1

# Generate symbolic info for debuggers
CFLAGS="-g $RPM_OPT_FLAGS"
export CFLAGS

# Check if we're in FIPS mode
modutil -dbdir /etc/pki/nssdb -chkfips true | grep -q enabled && export FIPS_ENABLED=1

./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --jni-dir=%{_jnidir} \
    --lib-dir=%{_libdir} \
    --version=%{version} \
    %{!?with_javadoc:--without-javadoc} \
    %{?with_tests:--with-tests} \
    dist

################################################################################
%install

./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --install-dir=%{buildroot} \
    install

################################################################################
%files

%defattr(-,root,root,-)
%doc jss.html
%license MPL-1.1.txt gpl.txt lgpl.txt symkey/LICENSE
%{_libdir}/*
%{_jnidir}/*

%if %{with javadoc}
################################################################################
%files javadoc

%defattr(-,root,root,-)
%{_javadocdir}/%{name}/
%endif

################################################################################
%changelog
* Mon Feb 14 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.1.0-1
- Rebase to JSS 5.1.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.1.0-0.3.alpha2
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-0.2.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.1.0-0.1.alpha2
- Rebase to JSS 5.1.0-alpha2

* Thu Sep 30 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-1
- Rebase to JSS 5.0.0

* Wed Sep 29 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.5.beta1
- Drop BuildRequires and Requires on glassfish-jaxb-api

* Fri Sep 03 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.4.beta1
- Rebase to JSS 5.0.0-beta1

* Thu Aug 12 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.3.alpha2
- Rebase to JSS 5.0.0-alpha2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-0.2.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 5.0.0-0.1.alpha1
- Rebase to JSS 5.0.0-alpha1