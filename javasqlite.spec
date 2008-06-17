Name:           javasqlite
Version:        20080420
Release:        %mkrel 0.1.1
Summary:        SQLite Java Wrapper/JDBC Driver

Group:          Development/Java
License:        BSD
URL:            http://www.ch-werner.de/javasqlite/
Source0:        http://www.ch-werner.de/javasqlite/%{name}-%{version}.tar.gz
# jnipath: Fedora specific, no need to send upstream
Patch0:         %{name}-20080315-jnipath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  sqlite-devel
BuildRequires:  java-rpmbuild
BuildRequires:  java-javadoc
BuildRequires:  libtool

%description
javasqlite is a Java wrapper including a basic JDBC driver for the
SQLite 2/3 database engine. It is designed using JNI to interface to
the SQLite API.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       java-javadoc

%description    javadoc
API documentation for %{name}.

%prep
%setup -q
%{__sed} -e 's|\@JNIPATH\@|%{_libdir}/%{name}|' %{PATCH0} | patch -p1
%{__sed} -i -e 's/\r$//g' doc/ajhowto.txt

%build
%{configure2_5x} \
    --with-jdk=%{java_home} \
    --with-jardir=%{_jnidir} \
    --libdir=%{_libdir}/%{name}
%{__make} JAVAC_FLAGS="-source 5" LIBTOOL=%{_bindir}/libtool
%{__make} javadoc JAVADOCLINK=%{_javadocdir}/java

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std} LIBTOOL=%{_bindir}/libtool
%{__rm} %{buildroot}%{_libdir}/%{name}/libsqlite_jni.*a
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{__mv} %{buildroot}%{_jnidir}/sqlite.jar %{buildroot}%{_jnidir}/sqlite-%{version}.jar
%{__ln_s} sqlite-%{version}.jar %{buildroot}%{_jnidir}/sqlite.jar

%clean
%{__rm} -rf %{buildroot}

%check
%{make} test

%files
%defattr(0644,root,root,0755)
%doc ChangeLog license.terms
%defattr(-,root,root,0755)
%{_jnidir}/sqlite-%{version}.jar
%{_jnidir}/sqlite.jar
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libsqlite_jni.so

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}

