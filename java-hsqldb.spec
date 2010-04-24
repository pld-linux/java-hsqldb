# TODO
# - make build with java 1.6
# - init script for webserver
# - pldized init script
# - set value for Xmx in sysconfig. Default is too low to run hsqldb server.

# does not build with java >= 1.6
%define	use_jdk	java5-sun

%define		ver	%(echo %{version} | tr . _)
%define		srcname	hsqldb
%include	/usr/lib/rpm/macros.java
Summary:	SQL relational database engine written in Java
Summary(pl.UTF-8):	Silnik relacyjnych baz danych SQL napisany w Javie
Name:		java-hsqldb
Version:	1.8.1.1
Release:	2
License:	BSD-like
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/hsqldb/%{srcname}_%{ver}.zip
# Source0-md5:	4114ba2e6aba58e6bfd3fa283d7dbc37
Source1:	%{name}-standard.cfg
Source2:	%{name}-standard-server.properties
Source3:	%{name}-standard-webserver.properties
Source4:	%{name}-standard-sqltool.rc
Patch0:		%{name}-scripts.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}-javadoc.patch
URL:		http://www.hsqldb.org/
BuildRequires:	ant
BuildRequires:	sed >= 4.0
BuildRequires:	java(servlet)
BuildRequires:	java-junit
%{buildrequires_jdk}
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	rpmbuild(macros) >= 1.556
BuildRequires:	unzip
Obsoletes:	hsqldb <= 1.8.1.1-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HSQLDB is the leading SQL relational database engine written in Java.
It has a JDBC driver and supports a rich subset of ANSI-92 SQL (BNF
tree format) plus SQL 99 and 2003 enhancements. It offers a small
(less than 100k in one version for applets), fast database engine
which offers both in-memory and disk-based tables and supports
embedded and server modes.

Additionally, it includes tools such as a minimal web server,
in-memory query and management tools (can be run as applets) and a
number of demonstration examples.

%description -l pl.UTF-8
HSQLDB to wiodący silnik relacyjnych baz danych SQL napisany w Javie.
Ma sterownik JDBC i obsługuje znaczny podzbiór ANSI-92 SQL (w formacie
drzew BNF) oraz rozszerzenia SQL 99 i 2003. Oferuje mały (poniżej 100k
w jednej wersji dla apletów), szybki silnik obsługujący tabele zarówno
w pamięci, jak i na dysku; obsługuje tryb wbudowany oraz serwerowy.

Ponadto zawiera narzędzia takie jak minimalny serwer WWW, zapytania w
pamięci i narzędzia zarządzające (mogące działać jako aplety) oraz
wiele przykładów demonstracyjnych.

%package manual
Summary:	Manual for HSQLDB
Summary(pl.UTF-8):	Podręcznik do HSQLDB
Group:		Documentation
Obsoletes:	hsqldb-manual

%description manual
Documentation for HSQLDB.

%description manual -l pl.UTF-8
Podręcznik do HSQLDB.

%package javadoc
Summary:	Javadoc for HSQLDB
Summary(pl.UTF-8):	Dokumentacja javadoc do HSQLDB
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	hsqldb-javadoc

%description javadoc
Javadoc for HSQLDB.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc do HSQLDB.

%package demo
Summary:	Demo for HSQLDB
Summary(pl.UTF-8):	Pliki demonstracyjne dla HSQLDB
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Obsoletes:	hsqldb-demo

%description demo
Demonstrations and samples for HSQLDB.

%description demo -l pl.UTF-8
Programy demonstracyjne i przykładowe dla HSQLDB.

%package -n hsqldb
Summary:	HSQLDB server
Summary(pl.UTF-8):	Serwer HSQLDB
Group:		Applications/Databases
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{version}-%{release}
Requires:	java(servlet)
Requires:	rc-scripts
Provides:	group(hsqldb)
Provides:	user(hsqldb)
Obsoletes:	hsqldb-server <= 1.8.1.1-1

%description -n hsqldb
HSQLDB server.

%description -n hsqldb -l pl.UTF-8
Serwer HSQLDB.

%prep
%setup -q -n %{srcname}
%undos build/build.xml
%patch0 -p0
%patch1 -p1
%patch2 -p1

# remove all binary libs
rm -f lib/hsqldb.jar
rm -f lib/servlet.jar

# create manual dir without apidocs
cp -a doc manual
rm -rf manual/src
cp -a index.html manual

%build
required_jars="\
	jsse/jsse \
	jsse/jnet \
	jsse/jcert \
	jdbc-stdext \
	junit \
	servlet-api \
"
export JAVA_HOME=%{java_home}
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant -f build/build.xml hsqldb javadoc

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d $RPM_BUILD_ROOT%{_javadir}
install lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s  %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# bin
install -d $RPM_BUILD_ROOT%{_bindir}
install bin/runUtil.sh $RPM_BUILD_ROOT%{_bindir}/%{srcname}RunUtil

# sysv init
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install bin/%{srcname} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{srcname}

# config
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{srcname}

# serverconfig
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}
install %{SOURCE2} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/server.properties
install %{SOURCE3} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/webserver.properties
install %{SOURCE4} $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/sqltool.rc
# lib
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/lib
install lib/functions $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/lib
ln -sf %{_javadir}/servlet-api.jar $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/lib/servlet.jar
# data
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{srcname}/data
# demo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install demo/*.sh 	$RPM_BUILD_ROOT%{_datadir}/%{name}/demo
install demo/*.html 	$RPM_BUILD_ROOT%{_datadir}/%{name}/demo

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a doc/src/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n hsqldb
%groupadd -g 169 %{srcname}
%useradd -u 169 -g %{srcname} -s /bin/sh -d %{_localstatedir}/lib/%{srcname} %{srcname}

%post -n hsqldb
/sbin/chkconfig --add %{srcname}
%service %{srcname} restart

%preun -n hsqldb
if [ "$1" = "0" ]; then
	%service -q %{srcname} stop
	/sbin/chkconfig --del %{srcname}
fi

%postun -n hsqldb
if [ "$1" = "0" ]; then
	%userremove %{srcname}
	%groupremove %{srcname}
fi

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc doc/hsqldb_lic.txt
%{_javadir}/*.jar

%files manual
%defattr(644,root,root,755)
%doc manual/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}

%files -n hsqldb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{srcname}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{srcname}
%dir %{_localstatedir}/lib/%{srcname}
%attr(755,hsqldb,hsqldb) %{_localstatedir}/lib/%{srcname}/data
%{_localstatedir}/lib/%{srcname}/lib
%{_localstatedir}/lib/%{srcname}/server.properties
%{_localstatedir}/lib/%{srcname}/webserver.properties
%attr(600,hsqldb,hsqldb) %{_localstatedir}/lib/%{srcname}/sqltool.rc
