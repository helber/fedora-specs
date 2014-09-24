%{?nodejs_find_provides_and_requires}
%global         npm_name atom
%global         atom_path %{_datadir}/atom
%global         _missing_build_ids_terminate_build 0

Name:           %{npm_name}
Version:        0.131.0
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
BuildRequires:  git
BuildRequires:  gyp >= 0.1-0.16.1970
BuildRequires:  python2-devel
Requires:       nodejs
Requires:       http-parser
Requires:       zsh
Requires:       %{name}-libs = %{version}

BuildRequires:  curl
BuildRequires:  make


%description
Atom is a hackable text editor for the 21st century, built on atom-shell, and based on everything we love about our favorite editors. We designed it to be deeply customizable, but still approachable using the default configuration.

Visit https://atom.io to learn more.

%package libs
Summary: Library to chromium
Group: Development/Libraries

%description libs
Libraries need for atom

%prep
%setup -q -n %{npm_name}-%{version}

%build
# https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md
CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CFLAGS
CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CXXFLAGS
INSTALL_PREFIX=%{buildroot}/usr ; export INSTALL_PREFIX
## Upgrade npm
mkdir -p %{buildroot}%{_bindir}
#curl -L https://npmjs.org/install.sh | sh
# install new npm to build package
# npm config set registry="http://registry.npmjs.org/"
npm config set ca ""
npm config set strict-ssl false
npm install -g --ca=null --prefix %{buildroot}/usr npm 
# Export PATH to new npm version
export PATH="%{buildroot}/usr/bin:$PATH"
# ./script/build 2>&1 >> /dev/null
./script/build --verbose 2>&1
npm config delete ca

%install
#rm -rf $RPM_BUILD_ROOT
CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CFLAGS
CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CXXFLAGS
INSTALL_PREFIX=%{buildroot}/usr ; export INSTALL_PREFIX
./script/grunt install 2>&1 >> /dev/null
rm -f %{buildroot}%{_datadir}/atom/resources/app/apm/node_modules/atom-package-manager/bin/node
cd %{buildroot}%{_datadir}/atom/resources/app/apm/node_modules/atom-package-manager/bin/
ln -sf /usr/bin/node node
br=`echo %{buildroot}| sed -r 's/\//\\\\\//g'`
sed -i "s/$br//g" %{buildroot}%{_datadir}/applications/Atom.desktop
mkdir -p %{buildroot}%{_libdir}/
install -pm755 %{buildroot}%{_datadir}/atom/libchromiumcontent.so %{buildroot}%{_libdir}
install -pm755 %{buildroot}%{_datadir}/atom/libudev.so.0 %{buildroot}%{_libdir}
rm -Rf /tmp/atom-build

%post

%post libs -p /sbin/ldconfig

%preun

%postun

%postun libs -p /sbin/ldconfig

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md docs/
%{_bindir}/atom
%{_bindir}/apm
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/applications/Atom.desktop

%files libs
%{_libdir}/libchromiumcontent.so
%{_libdir}/libudev.so.0

%changelog
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
