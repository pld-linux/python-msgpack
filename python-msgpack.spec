#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		msgpack
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny, efektywny format wymiany danych
Name:		python-%{module}
# keep 1.0.5 here for python2 support
Version:	1.0.5
Release:	3
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/msgpack/
Source0:	https://files.pythonhosted.org/packages/source/m/msgpack/%{module}-%{version}.tar.gz
# Source0-md5:	da12a9f0a65a803ec005219f6095d0a3
URL:		https://msgpack.org/
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-Cython >= 0.29.30
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:35.0.2
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.29.30
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:35.0.2
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%description -l pl.UTF-8
MessagePack to biblioteka do binarnej, efektywnej serializacji
obiektów. Pozwala wymieniać strukturalne obiekty pomiędzy wieloma
językami, podobnie jak JSON. W odróżnieniu od JSON-a jest bardzo
szybka i mała.

%package -n python3-%{module}
Summary:	Binary-based efficient data interchange format
Summary(pl.UTF-8):	Binarny, efektywny format wymiany danych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
MessagePack is a binary-based efficient object serialization library.
It enables to exchange structured objects between many languages like
JSON. But unlike JSON, it is very fast and small.

%description -n python3-%{module} -l pl.UTF-8
MessagePack to biblioteka do binarnej, efektywnej serializacji
obiektów. Pozwala wymieniać strukturalne obiekty pomiędzy wieloma
językami, podobnie jak JSON. W odróżnieniu od JSON-a jest bardzo
szybka i mała.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest test
%endif
%endif

%if %{with python3}
/usr/bin/cython3 --cplus msgpack/_cmsgpack.pyx
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest test
%endif
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
