#
# Conditional build:
## %bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	msgpack
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny efektywny format wymiany danych.
Name:		python-%{module}
Version:	0.4.5
Release:	1
License:	ASL
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/m/msgpack-python/msgpack-python-%{version}.tar.gz
# Source0-md5:	3b82bc542d5599896695512e7c32f42d
URL:		http://msgpack.org/
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
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
Summary:	-
Summary(pl.UTF-8):	-
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
%setup -q -n msgpack-python-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_packer.so
%attr(755,root,root) %{py_sitedir}/%{module}/_unpacker.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/msgpack_python-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.rst
%dir %{py3_sitedir}/%{module}
%attr(755,root,root) %{py3_sitedir}/%{module}/_packer.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/_unpacker.cpython-*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/msgpack_python-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
