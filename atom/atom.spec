%{?nodejs_find_provides_and_requires}
%global         npm_name atom
%global         atom_path %{_datadir}/atom
%global         _missing_build_ids_terminate_build 0
%global         npm_ver 2.7.6

Name:           %{npm_name}
Version:        1.2.3
Release:        1%{?dist}
Summary:        A hackable text editor for the 21st Century

Group:          Applications/Editors
License:        MIT
URL:            https://atom.io/
Source0:        https://github.com/%{npm_name}/%{npm_name}/archive/v%{version}.tar.gz

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires:  nodejs-packaging
BuildRequires:  npm
BuildRequires:  libgnome-keyring-devel
BuildRequires:  node-gyp
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  git-core
Requires:       nodejs
Requires:       http-parser
Requires:       zsh
Requires:       %{name}%{?_isa} = %{version}-%{release}

BuildRequires:  curl
BuildRequires:  make
BuildRequires:  svn


%description
Atom is a text editor that's modern, approachable, yet hackable to the core - a tool you can customize to do anything but also use productively without ever touching a config file.

Visit https://atom.io to learn more.

%package libs
Summary: Library to chromium
Group: System Environment/Libraries

%description libs
Libraries need for atom

%prep
%setup -q -n %{npm_name}-%{version}

%build
export INSTALL_PREFIX="%{buildroot}%{_prefix}"
## Upgrade npm
%{__mkdir_p} %{buildroot}%{_bindir}
# install new npm to build package
npm config set registry="http://registry.npmjs.org/"
npm config set ca ""
npm config set strict-ssl false
npm install -g --ca=null --prefix %{buildroot}%{_prefix} npm@%{npm_ver}
# Export PATH to new npm version
export PATH="%{buildroot}%{_bindir}:$PATH"
./script/build --verbose 2>&1
npm config delete ca

%install
INSTALL_PREFIX=%{buildroot}%{_prefix} ; export INSTALL_PREFIX
./script/grunt install 2>&1 >> /dev/null
%{__rm} -f %{buildroot}%{_datadir}/atom/resources/app/apm/bin/node
cd %{buildroot}%{_datadir}/atom/resources/app/apm/bin/
%{__ln_s}f %{_bindir}/node node
%{__sed} -i "s/=.*atom/=atom/g" %{buildroot}%{_datadir}/applications/atom.desktop
%{__sed} -i "s/atom.png/atom/g" %{buildroot}%{_datadir}/applications/atom.desktop

# copy over icons in sizes that most desktop environments like
for i in 1024 512 256 128 64 48 32 24 16;do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    cp /tmp/atom-build/icons/${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/atom.png
done

%{__mkdir_p} %{buildroot}%{_libdir}
%{__install} -pm755 %{buildroot}%{_datadir}/atom/libnode.so %{buildroot}%{_libdir}
%{__rm} -Rf /tmp/atom-build

%post

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md docs/
%{_bindir}/atom
%{_bindir}/apm
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/applications/atom.desktop
%{_datadir}/icons/hicolor/

%files libs
%{_libdir}/libnode.so

%changelog
* Thu Nov 19 2015 Florian Kaiser <florian.kaiser@fnkr.net> v1.2.3-1
- Release 1.2.3
* Thu Nov 12 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.2.0-1
- Release 1.2.0
* Thu Sep 17 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.13-1
- Change lib to libnode
* Tue Sep 01 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.10-1
- Release 1.0.10
* Thu Aug 27 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.8-1
- Clean and test spec for epel, centos and fedora
- Release 1.0.8
* Tue Aug 11 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.6-1
- Release 1.0.6
* Thu Aug 06 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.5-1
- Release 1.0.5
* Wed Jul 08 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.1-1
- Release 1.0.1
* Thu Jun 25 2015 Helber Maciel Guerra <helbermg@gmail.com> v1.0.0-1
- Release 1.0.0
* Wed Jun 10 2015 Helber Maciel Guerra <helbermg@gmail.com> - v0.208.0-1
- Fix atom.desktop
* Tue Jun 09 2015 Helber Maciel Guerra <helbermg@gmail.com> - v0.207.0-1
- Fix desktop icons and some rpmlint.
* Fri Oct 31 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.141.0-1
- release 0.141.0
* Thu Oct 23 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.139.0-1
- release 0.139.0
* Wed Oct 15 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.137.0-2
- release 0.137.0
* Tue Oct 07 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.136.0-1
- release 0.136.0
* Tue Sep 30 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.133.0-2
- Build OK
* Fri Aug 22 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.123.0-2
- Change package name to atom.
* Thu Aug 21 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.123.0-1
- RPM package is just working.
* Sat Jul 26 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.119.0-1
- Try without nodejs.
* Tue Jul 01 2014 Helber Maciel Guerra <helbermg@gmail.com> - v0.106.0-1
- Try new version
* Sun May 25 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.99.0
- Initial package
