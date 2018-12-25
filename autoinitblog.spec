%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%else
%global __python2 /usr/bin/python
%endif

%define name blogrobot
%define version 1.0
%define unmangled_version 1.0
%define unmangled_version 1.0
%define release 1
Summary: auto install scripts for blog
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: UNKNOWN <UNKNOWN>
Provides: provide-files

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}/var/lib/blogrobot
mkdir -p %{buildroot}/var/log/blogrobot
mv %{name}/initconfig.yaml %{buildroot}%{_sysconfdir}/%{name}/
touch %{buildroot}/var/log/blogrobot/blog_robot.log
touch %{buildroot}%{_sysconfdir}/%{name}/exec.txt

install -p -D -m 755 %{_builddir}/%{name}-%{version}/bin/* %{buildroot}%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/blogrobot*
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/%{name}/
%{_bindir}/*
/var/log/blogrobot
/var/lib/blogrobot
