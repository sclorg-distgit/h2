%{?scl:%scl_package h2}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:           %{?scl_prefix}h2
Version:        1.3.176
Release:        4.%{baserelease}%{?dist}
Summary:        Java SQL database

License:        EPL or MPLv1.1
URL:            http://www.h2database.com
Source0:        http://www.h2database.com/h2-2014-04-05.zip
Source1:        http://repo2.maven.org/maven2/com/h2database/h2/%{version}/h2-%{version}.pom
Patch0:         fix-build.patch
Patch1:         rm-osgi-jdbc-service.patch
Patch2:         fix-broken-tests.patch
Patch3:         lucene4.patch
Patch4:         remove-jts.patch
BuildArch: noarch

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}lucene
BuildRequires:  %{?scl_prefix_java_common}lucene-analysis
BuildRequires:  %{?scl_prefix_java_common}lucene-queryparser
BuildRequires:  %{?scl_prefix_java_common}slf4j >= 1.5
BuildRequires:  %{?scl_prefix_maven}felix-osgi-core >= 1.2
BuildRequires:  %{?scl_prefix}glassfish-servlet-api

%description
H2 is a the Java SQL database. The main features of H2 are:
* Very fast, open source, JDBC API
* Embedded and server modes; in-memory databases
* Browser based Console application
* Small footprint: around 1 MB jar file size 

%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}
pushd src/test/org/h2/test/unit
rm TestServlet.java
popd
%patch0
%patch2
%patch3 -p3
%patch4 -p3

# Because no Fedora package provides org.osgi.service.jdbc interfaces yet
%patch1
rm src/main/org/h2/util/OsgiDataSourceFactory.java
rm -fr src/test/org/h2/test/server/TestWeb.java src/test/org/h2/test/db/TestSpatial.java
sed -i -e "/TestWeb/d" -e "/TestSpatial/d" src/test/org/h2/test/TestAll.java
sed -i '/org.osgi.service.jdbc/d' src/main/META-INF/MANIFEST.MF

# Delete pre-built binaries
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

sed -i -e 's|authenticated|authenticate authenticated|' src/tools/org/h2/build/doc/dictionary.txt
echo "devtoolset classic queryparser" >> src/tools/org/h2/build/doc/dictionary.txt

# Remove bits that require jts
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
export JAVA_HOME=/usr/lib/jvm/java
chmod u+x build.sh
./build.sh jar docs
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p bin/h2-%{version}.jar   \
$RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
cp -rp docs/javadoc  \
$RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}

mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
cp -rp %SOURCE1 $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap JPP-%{pkg_name}.pom %{pkg_name}.jar
%{?scl:EOF}


%files -f .mfiles
%doc src/docsrc/html/license.html

%files javadoc
%{_javadocdir}/%{pkg_name}
%doc src/docsrc/html/license.html

%changelog
* Tue Feb 23 2016 Mat Booth <mat.booth@redhat.com> - 1.3.176-4.2
- License correction.

* Tue Jan 19 2016 Mat Booth <mat.booth@redhat.com> - 1.3.176-4.1
- Import latest from Fedora
- Patch out unneeded dep on jts
- Port to newer version of lucene

* Wed Jun 17 2015 Alexander Kurtakov <akurtako@redhat.com> 1.3.176-4
- Fix FTBFS - delete more tests.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.176-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 13 2014 Mat Booth <mat.booth@redhat.com> - 1.3.176-2
- Fix erroneous osgi dep on org.osgi.service.jdbc

* Wed Jun 11 2014 Mat Booth <mat.booth@redhat.com> - 1.3.176-1
- Update to latest upstream stable release
- Fix lucene BRs
- Patch to remove implementation of non-existant inferface
- Patch to fix tests broken by new servlet API

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.168-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Alexander Kurtakov <akurtako@redhat.com> 1.3.168-5
- Require java-headless.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.168-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.168-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Alexander Kurtakov <akurtako@redhat.com> 1.3.168-2
- Bring back real pom.

* Mon Jul 23 2012 Alexander Kurtakov <akurtako@redhat.com> 1.3.168-1
- Update to latest upstream.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.147-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar  8 2012 Andy Grimm <agrimm@gmail.com> - 1.2.147-6
- Add a POM file

* Tue Jan 24 2012 Deepak Bhole <dbhole@redhat.com> - 1.2.147-5
- Added patch for JDBC 4.1/Java 7 support (based on upstream patch)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.147-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 18 2011 Chris Aniszczyk <zx@redhat.com> 1.2.147-3
- Fix build to use the correct version of servlet APIs.

* Fri Feb 18 2011 Chris Aniszczyk <zx@redhat.com> 1.2.147-2
- Fix build to properly export JAVA_HOME.

* Fri Feb 18 2011 Chris Aniszczyk <zx@redhat.com> 1.2.147-1
- Update to the latest stable release.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.145-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 6 2010 Alexander Kurtakov <akurtako@redhat.com> 1.2.145-3
- Fix build to not screw osgi metadata.

* Mon Dec 6 2010 Alexander Kurtakov <akurtako@redhat.com> 1.2.145-2
- Install jar without version.

* Wed Nov 17 2010 Chris Aniszczyk <zx@redhat.com> 1.2.145-1
- Initial packaging
