%{?nodejs_find_provides_and_requires}
%global         npm_name atom
%global         atom_path %{_datadir}/atom
%global         _missing_build_ids_terminate_build 0

Name:           %{npm_name}
Version:        0.208.0
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
Requires:       %{name}-libs = %{version}

BuildRequires:  curl
BuildRequires:  make
BuildRequires:  svn


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
# Install gyp
git clone https://chromium.googlesource.com/external/gyp
cd gyp
%{__python} setup.py install --root $RPM_BUILD_ROOT

%build
# https://github.com/atom/atom/blob/master/docs/build-instructions/linux.md
CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CFLAGS
CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CXXFLAGS
export INSTALL_PREFIX=%{buildroot}/usr
## Upgrade npm
mkdir -p %{buildroot}%{_bindir}
# install new npm to build package
npm config set registry="http://registry.npmjs.org/"
npm config set ca ""
npm config set strict-ssl false
npm install -g --ca=null --prefix %{buildroot}/usr npm@2.7.6
# Export PATH to new npm version
export PATH="%{buildroot}/usr/bin:$PATH"
# Python to gyp
export PYTHONPATH=%{buildroot}%{python2_sitelib}
# ./script/build 2>&1 >> /dev/null
ls -l script
./script/build --verbose 2>&1
npm config delete ca

%install
#rm -rf $RPM_BUILD_ROOT
CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CFLAGS
CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64' ; export CXXFLAGS
INSTALL_PREFIX=%{buildroot}/usr ; export INSTALL_PREFIX
./script/grunt install 2>&1 >> /dev/null
rm -f %{buildroot}%{_datadir}/atom/resources/app/apm/bin/node
cd %{buildroot}%{_datadir}/atom/resources/app/apm/bin/
ln -sf /usr/bin/node node
sed -i "s/=.*atom/=atom/g" %{buildroot}%{_datadir}/applications/atom.desktop
sed -i "s/atom.png/atom/g" %{buildroot}%{_datadir}/applications/atom.desktop

# copy over icons in sizes that most desktop environments like
for i in 1024 512 256 128 64 48 32 24 16;do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    cp /tmp/atom-build/icons/${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/atom.png
done

mkdir -p %{buildroot}%{_libdir}/
install -pm755 %{buildroot}%{_datadir}/atom/libchromiumcontent.so %{buildroot}%{_libdir}
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
%{_datadir}/applications/atom.desktop
%{_datadir}/icons/hicolor/

%files libs
%{_libdir}/libchromiumcontent.so

%changelog
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
