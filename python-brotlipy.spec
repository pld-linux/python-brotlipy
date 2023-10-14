#
# Conditional build:
%bcond_with	tests	# unit tests (fixture files missing in sdist)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 binding to the Brotli library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki Brotli
Name:		python-brotlipy
Version:	0.7.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/brotlipy/
Source0:	https://files.pythonhosted.org/packages/source/b/brotlipy/brotlipy-%{version}.tar.gz
# Source0-md5:	300a63158cec5b74082625dd9a2ae4d2
URL:		https://pypi.org/project/brotlipy/
%if %{with python2}
BuildRequires:	python-cffi >= 1.0.0
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-enum34 >= 1.0.4
BuildRequires:	python-enum34 < 2
BuildRequires:	python-hypothesis
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.0.0
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
%if "%{py3_ver}" == "3.3"
BuildRequires:	python3-enum34 >= 1.0.4
BuildRequires:	python3-enum34 < 2
%endif
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
Conflicts:	python-brotli
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library contains Python bindings for the reference Brotli
encoder/decoder. This allows Python software to use the Brotli
compression algorithm directly from Python code.

%description -l pl.UTF-8
Ta biblioteka zawiera wiązania Pythona do wzorcowego kodera/dekodera
Brotli. Pozwala na korzystanie z algorytmu kompresji Brotli
bezpośrednio z kodu w Pythonie.

%package -n python3-brotlipy
Summary:	Python 3 binding to the Brotli library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki Brotli
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3
Conflicts:	python3-brotli

%description -n python3-brotlipy
This library contains Python bindings for the reference Brotli
encoder/decoder. This allows Python software to use the Brotli
compression algorithm directly from Python code.

%description -n python3-brotlipy -l pl.UTF-8
Ta biblioteka zawiera wiązania Pythona do wzorcowego kodera/dekodera
Brotli. Pozwala na korzystanie z algorytmu kompresji Brotli
bezpośrednio z kodu w Pythonie.

%prep
%setup -q -n brotlipy-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} -m pytest test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
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
%doc HISTORY.rst LICENSE README.rst
%dir %{py_sitedir}/brotli
%{py_sitedir}/brotli/*.py[co]
%attr(755,root,root) %{py_sitedir}/brotli/_brotli.so
%{py_sitedir}/brotlipy-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-brotlipy
%defattr(644,root,root,755)
%doc HISTORY.rst LICENSE README.rst
%dir %{py3_sitedir}/brotli
%{py3_sitedir}/brotli/*.py
%attr(755,root,root) %{py3_sitedir}/brotli/_brotli.abi3.so
%{py3_sitedir}/brotli/__pycache__
%{py3_sitedir}/brotlipy-%{version}-py*.egg-info
%endif
