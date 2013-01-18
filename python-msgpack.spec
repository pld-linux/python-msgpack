# %bcond_without	tests	# do not perform "make test"

%define 	module	msgpack
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny efektywny format wymiany danych.
Name:		python-%{module}
Version:	0.2.4
Release:	1
License:	ASL
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/m/msgpack-python/msgpack-python-%{version}.tar.gz
# Source0-md5:	c4bb313cd35b57319f588491b1614289
URL:		http://msgpack.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%description -l pl.UTF-8
MessagePack jest binarną, efektywną biblioteką serializacji obiektów.
Pozwala wymieniać strukturalne obiekty pomiędzy wieloma językami
podobnie jak JSON. W odróżnieniu jest bardzo szybka i mała.

%prep
%setup -q -n msgpack-python-%{version}

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_msgpack.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}*.egg-info
%endif
