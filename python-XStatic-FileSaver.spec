%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name XStatic-FileSaver

Name:           python-%{pypi_name}
Version:        1.3.2.0
Release:        1%{?dist}
Provides:       python2-%{pypi_name} = %{version}-%{release}
Summary:        FilseSaver (XStatic packaging standard)

License:        MIT
URL:            https://github.com/eligrey/FileSaver.js
Source0:        https://files.pythonhosted.org/packages/source/X/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%description
FilseSaver JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.


%package -n xstatic-filesaver-common
Summary:        %{summary}

BuildRequires:  web-assets-devel
Requires:       web-assets-filesystem

%description -n xstatic-filesaver-common
FilseSaver JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.

This package contains the JavaScript files.


%package -n python2-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

Requires:       python2-XStatic
Requires:       xstatic-filesaver-common

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
FilseSaver JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.

This package provides Python 2 build of %{pypi_name}.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-XStatic
Requires:       xstatic-filesaver-common

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
FilseSaver JavaScript library packaged for setup-tools (easy_install) / pip.

This package is intended to be used by any project that needs these files.

It intentionally does not provide any extra code except some metadata
nor has any extra requirements.

This package provides Python 3 build of %{pypi_name}.
%endif


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Patch to use webassets directory
sed -i "s|^BASE_DIR = .*|BASE_DIR = '%{_jsdir}/filesaver'|" xstatic/pkg/filesaver/__init__.py


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%py2_install
mkdir -p %{buildroot}/%{_jsdir}/filesaver
mv %{buildroot}/%{python2_sitelib}/xstatic/pkg/filesaver/data/FileSaver.js %{buildroot}/%{_jsdir}/filesaver
rmdir %{buildroot}%{python2_sitelib}/xstatic/pkg/filesaver/data/

%if 0%{?with_python3}
%py3_install
# Remove static files, already created by the python2 subpkg
rm -rf %{buildroot}%{python3_sitelib}/xstatic/pkg/filesaver/data/
%endif


%files -n python2-%{pypi_name}
%doc README.txt
%{python2_sitelib}/xstatic/pkg/filesaver
%{python2_sitelib}/XStatic_FileSaver-%{version}-py%{python_version}.egg-info
%{python2_sitelib}/XStatic_FileSaver-%{version}-py%{python_version}-nspkg.pth

%files -n xstatic-filesaver-common
%doc README.txt
%{_jsdir}/filesaver

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%{python3_sitelib}/xstatic/pkg/filesaver
%{python3_sitelib}/XStatic_FileSaver-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/XStatic_FileSaver-%{version}-py%{python3_version}-nspkg.pth
%endif


%changelog
* Fri Jul 13 2018 Radomir Dopieralski <rdopiera@redhat.com) - 1.3.2.0-1
- Initial package
