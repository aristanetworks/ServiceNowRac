%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: ServiceNowRac
Version: Replaced_by_make
Release: 1%{?dist}
Summary: REST API client for communicating with a ServiceNow instance.

Group: Development/Libraries
License: BSD (3-clause)
URL: http://www.arista.com
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The ServiceNowRac package is part of the devops library for EOS developed by Arista. The ServiceNowRac provides a python REST API client for communicating with a ServiceNow instance.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%postun

%files
%defattr(-,root,root,-)
%{python_sitelib}/ServiceNowRac*

%changelog
* Thu Oct 1 2015 John Corbin
-- Initial Build.
