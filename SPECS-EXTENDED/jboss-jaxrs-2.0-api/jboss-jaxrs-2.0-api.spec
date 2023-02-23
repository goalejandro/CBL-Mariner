Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}
%global oname jboss-jaxrs-api_2.0_spec

Name:          jboss-jaxrs-2.0-api
Version:       1.0.0
Release:       18%{?dist}
Summary:       JAX-RS 2.0: The Java API for RESTful Web Services
# ASL 2.0 src/main/java/javax/ws/rs/core/GenericEntity.java
License:       (CDDL or GPLv2 with exceptions) and ASL 2.0
URL:           https://github.com/jboss/jboss-jaxrs-api_spec
Source0:       https://github.com/jboss/jboss-jaxrs-api_spec/archive/%{oname}-%{namedversion}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.jboss:jboss-parent:pom:)
BuildRequires: mvn(javax.xml.bind:jaxb-api)

BuildArch:     noarch

%description
JSR 339: JAX-RS 2.0: The Java API for RESTful Web Services.

%prep
%setup -q -n jboss-jaxrs-api_spec-%{oname}-%{namedversion}

# Unneeded plugin
%pom_remove_plugin :maven-source-plugin

# Fix JDK11 build, add missing javax.xml.bind
%pom_add_dep javax.xml.bind:jaxb-api

%mvn_file :%{oname} %{name}

# remove after upgrading narayana
%mvn_alias ":jboss-jaxrs-api_2.0_spec" "org.jboss.resteasy:jaxrs-api"

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%changelog
* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.0.0-18
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Dogtag PKI Team <pki-devel@redhat.com> - 1.0.0-15
- Drop jboss-jaxrs-2.0-api-javadoc

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Markku Korkeala <markku.korkeala@iki.fi> - 1.0.0-12
- Fix JDK11 build by adding dependency for javax.xml.bind.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.0.0-11
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 24 2016 gil cattaneo <puntogil@libero.it> 1.0.0-3
- temporarily add org.jboss.resteasy:jaxrs-api alias

* Tue Jun 07 2016 gil cattaneo <puntogil@libero.it> 1.0.0-2
- review fixes

* Mon Jun 06 2016 gil cattaneo <puntogil@libero.it> 1.0.0-1
- initial rpm