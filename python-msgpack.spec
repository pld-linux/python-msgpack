#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	msgpack
%define		pypi_name	msgpack-python
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny efektywny format wymiany danych.
Name:		python-%{module}
Version:	1.0.0
Release:	1
License:	ASL
Group:		Development/Languages/Python
Source0:	https://pypi.debian.net/msgpack/%{module}-%{version}.tar.gz
# Source0-md5:	c35ee8f991dad3969884e9585e56ebba
URL:		http://msgpack.org/
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
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

%package -n python3-%{module}
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny efektywny format wymiany danych.
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%description -n python3-%{module} -l pl.UTF-8
MessagePack jest binarną, efektywną biblioteką serializacji obiektów.
Pozwala wymieniać strukturalne obiekty pomiędzy wieloma językami
podobnie jak JSON. W odróżnieniu jest bardzo szybka i mała.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING README.md
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/msgpack-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.md
%dir %{py3_sitedir}/%{module}
%attr(755,root,root) %{py3_sitedir}/%{module}/_cmsgpack.cpython-*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/msgpack-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
