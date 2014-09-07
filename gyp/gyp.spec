%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global		revision	1967
%{expand:	%%global	archivename	gyp-%{version}%{?revision:-svn%{revision}}}
%if !(0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:		gyp
Version:	0.1
Release:	0.11%{?revision:.%{revision}svn}%{?dist}
Summary:	Generate Your Projects

Group:		Development/Tools
License:	BSD
URL:		http://code.google.com/p/gyp/
# No released tarball avaiable. so the tarball was generated
# from svn as following:
#
# 1. svn co http://gyp.googlecode.com/svn/trunk gyp
# 2. cd gyp
# 3. version=$(grep version= setup.py|cut -d\' -f2)
# 4. revision=$(svn info|grep -E "^Revision:"|cut -d' ' -f2)
# 5. tar -a --exclude-vcs -cf /tmp/gyp-$version-svn$revision.tar.bz2 *
Source0:	%{archivename}.tar.bz2
Source1:        generate-tarball.sh
Patch0:		    gyp-rpmoptflags.patch

BuildRequires:	python2-devel
BuildRequires:  python-setuptools
BuildArch:	    noarch

%description
GYP is a tool to generates native Visual Studio, Xcode and SCons
and/or make build files from a platform-independent input format.

Its syntax is a universal cross-platform build representation
that still allows sufficient per-platform flexibility to accommodate
irreconcilable differences.


%prep
%setup -q -c -n %{archivename}
%patch0 -p1 -b .0-rpmoptflags
for i in $(find pylib -name '*.py'); do
	sed -e '\,#![ \t]*/.*python,{d}' $i > $i.new && touch -r $i $i.new && mv $i.new $i
done

%build
%{__python} setup.py build


%install
%{__python} setup.py install --root $RPM_BUILD_ROOT --skip-build


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{_bindir}/gyp
%{python_sitelib}/*


%changelog
* Mon Aug 25 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.1-0.11.1967svn
- Fix build on copr and mock

* Tue May 22 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.1-0.11.1922svn
- Rebase to r1922

* Wed May 07 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.1-0.11.1917svn
- Fix github atom editor build, and some another nodejs build using node-gyp.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.11.1617svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Akira TAGOH <tagoh@redhat.com> - 0.1-0.10.1617svn
- Rebase to r1617

* Tue Feb 12 2013 Akira TAGOH <tagoh@redhat.com> - 0.1-0.9.1569svn
- Rebase to r1569 (#908983)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.8.1010svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.7.1010svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Akira TAGOH <tagoh@redhat.com> - 0.1-0.6.1010svn
- Rebase to r1010.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.5.840svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.4.840svn
- Rebase to r840.
- generate Makefile with RPM_OPT_FLAGS in CCFLAGS.

* Fri Aug  6 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.3.839svn
- Drop the unnecessary macro.

* Thu Aug  5 2010 Akira TAGOH <tagoh@redhat.com. - 0.1-0.2.839svn
- Update the spec file according to the suggestion in rhbz#621242.

* Wed Aug  4 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.1.839svn
- Initial packaging.

