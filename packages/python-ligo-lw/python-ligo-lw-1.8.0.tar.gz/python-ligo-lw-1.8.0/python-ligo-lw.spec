%global shortname ligo-lw

Name: 		python-%{shortname}
Summary:	LIGO Light-Weight XML I/O Library
Version:	1.8.0
Release:	1%{?dist}
License:	GPL-3.0-or-later
Source:		http://software.ligo.org/lscsoft/source/%{name}-%{version}.tar.gz
Url:		https://git.ligo.org/kipp.cannon/python-ligo-lw
Prefix:		%{_prefix}

BuildRequires:	epel-rpm-macros
BuildRequires:	python-devel
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python-rpm-macros
BuildRequires:	python-srpm-macros
BuildRequires:	python2-rpm-macros
BuildRequires:	python3-rpm-macros
# for xmllint tool used by test suite
BuildRequires:	libxml2

%description
The LIGO Light-Weight XML format is widely used within gravitational-wave
data analysis pipelines.  This package provides Python libraries
to read, write, and interact with documents in this format, as well as
several programs to perform common, basic, manipulations of files in this format.

%package -n python2-%{shortname}
Summary:	LIGO Light-Weight XML I/O Library (python%{python2_version})
Requires:	python >= 2.7
Requires:	python2-dateutil
# temporarily commented out to break cyclic dependency.  The following are
# optional dependencies, but the rpm version at CIT is too old for that
# feature
#Requires:	python2-glue
#Requires:	python2-lal
#Requires:	python2-lalburst
Requires:	python2-ligo-common
Requires:	python2-ligo-segments
Requires:	python2-numpy >= 1.6
Requires:	python2-pyyaml
Requires:	python2-six
Requires:	python2-tqdm
# temporary dependency to ensure -bin package is installed.  remove when
# other things, like gstlal, depend on -bin themselves
Requires:	python%{python3_pkgversion}-%{shortname}-bin
%{?python_provide:%python_provide python2-%{shortname}}
%description -n python2-%{shortname}
The LIGO Light-Weight XML format is widely used within gravitational-wave
data analysis pipelines.  This package provides a Python %{python2_version}
library to read, write, and interact with documents in this format.

%package -n python%{python3_pkgversion}-%{shortname}
Summary:	LIGO Light-Weight XML I/O Library (python%{python3_version})
Requires:	python%{python3_pkgversion}
Requires:	python%{python3_pkgversion}-dateutil
# temporarily commented out to break cyclic dependency.  The following are
# optional dependencies, but the rpm version at CIT is too old for that
# feature
#Requires:	python%{python3_pkgversion}-glue
#Requires:	python%{python3_pkgversion}-lal
#Requires:	python%{python3_pkgversion}-lalburst
Requires:	python%{python3_pkgversion}-ligo-segments
Requires:	python%{python3_pkgversion}-numpy >= 1.6
Requires:	python%{python3_pkgversion}-six
Requires:	python%{python3_pkgversion}-tqdm
Requires:	python%{python3_pkgversion}-PyYAML
%{?python_provide:%python_provide python%{python3_pkgversion}-%{shortname}}
%description -n python%{python3_pkgversion}-%{shortname}
The LIGO Light-Weight XML format is widely used within gravitational-wave
data analysis pipelines.  This package provides a Python %{python3_version}
library to read, write, and interact with documents in this format.

%package -n python%{python3_pkgversion}-%{shortname}-bin
Summary:	Programs for manipulating LIGO Light-Weight XML files
Requires:	python%{python3_pkgversion}-%{shortname} = %{version}
Requires:	python%{python3_pkgversion}
# temporarily commented out to break cyclic dependency.  The following are
# optional dependencies, but the rpm version at CIT is too old for that
# feature
#Requires:	python%{python3_pkgversion}-glue
#Requires:	python%{python3_pkgversion}-lal
Requires:	python%{python3_pkgversion}-ligo-segments
Conflicts:	glue-ligolw-tools
Obsoletes:	glue-ligolw-tools
Provides:	glue-ligolw-tools
Conflicts:	glue < 2.0 python-pylal
%description -n python%{python3_pkgversion}-%{shortname}-bin
The LIGO Light-Weight XML format is widely used within gravitational-wave
data analysis pipelines.  This package provides several programs to
performe common, basic, manipulations of files in this format.

%prep
%setup

%build
%py2_build
%py3_build

%install
# install python2 first so that /bin/ is populated by python3
%py2_install
%py3_install

%clean
rm -rf %{buildroot}

%files -n python2-%{shortname}
%license LICENSE
%{python2_sitearch}/ligo/lw
%{python2_sitearch}/python_ligo_lw-*.egg-info
%exclude %{python2_sitearch}/ligo/__init__.py*

%files -n python%{python3_pkgversion}-%{shortname}
%license LICENSE
%{python3_sitearch}/ligo/lw
%{python3_sitearch}/python_ligo_lw-*.egg-info
%exclude %{python3_sitearch}/ligo/__init__.py*
%exclude %{python3_sitearch}/ligo/__pycache__/__init__.*

%files -n python%{python3_pkgversion}-%{shortname}-bin
%license LICENSE
%{_bindir}/*

%changelog
* Thu Dec 5 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.6.0-3
- Fix bug in files to not bundle ligo/__init__.py

* Thu Dec 5 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.6.0-2
- Rebuild with python3 packages

* Tue May 8 2018 Kipp Cannon <kipp.cannon@ligo.org>
- Initial release.
