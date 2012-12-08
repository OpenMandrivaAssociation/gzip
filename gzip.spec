Name:		gzip
Summary:	The GNU data compression program
Version:	1.5
Release:	1
License:	GPLv3+
Group:		Archiving/Compression
URL:		http://www.gzip.org
Source0:	ftp://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.gz.sig
Patch0:		gzip-1.3.12-openbsd-owl-tmp.patch
Patch1:		gzip-1.3.5-zforce.patch
Patch4:		gzip-1.3.10-zgreppipe.patch
Patch5:		gzip-1.5-rsync.diff
Patch6:		gzip-1.3.3-window-size.patch
Patch7:		gzip-1.3.9-addsuffix.patch
Patch12:	gzip-1.3.5-cve-2006-4335.patch
Patch13:	gzip-1.3.5-cve-2006-4336.patch
Patch14:	gzip-1.3.5-cve-2006-4338.patch
Patch15:	gzip-1.3.9-cve-2006-4337.patch
Patch16:	gzip-1.3.5-cve-2006-4337_len.patch
Patch17:	gzip-1.3.14-CVE-2009-2624-1.diff
BuildRequires:	texinfo
Requires:	mktemp
Requires:	less

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your Mandriva Linux system, because it is a
very commonly used data compression program.

%package	utils
Summary:	Utilities dealing with gzip compressed files
Requires:	gzip = %{version}

%description	utils
The gzip-utils package contains programs for manipulating gzip-compressed
archives: zcat, zcmp, zdiff, zgrep.

%prep
%setup -q
%patch0 -p1 -b .owl-tmp
%patch1 -p0 -b .zforce
%patch4 -p1 -b .nixi
%patch5 -p1 -b .rsync
%patch6 -p1 -b .window-size
%patch7 -p1 -b .addsuffix
%patch12 -p1 -b .4335
%patch13 -p1 -b .4336
%patch14 -p1 -b .4338
%patch15 -p1 -b .4337
%patch16 -p1 -b .4337l
%patch17 -p0 -b .CVE-2009-2624-1

%build
export DEFS="-DNO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
%configure2_5x
%make

%check
make check

%install
%makeinstall_std

install -d %{buildroot}/bin

for i in gzip gunzip zcat; do
    mv -f %{buildroot}%{_bindir}/$i %{buildroot}/bin/$i
    ln -sf ../../bin/$i %{buildroot}%{_bindir}/$i
done

for i in zcmp zdiff zforce zgrep zmore znew ; do
	sed -e "s|%{buildroot}||g" < %{buildroot}%{_bindir}/$i > %{buildroot}%{_bindir}/.$i
	rm -f %{buildroot}%{_bindir}/$i
	mv %{buildroot}%{_bindir}/.$i %{buildroot}%{_bindir}/$i
	chmod 755 %{buildroot}%{_bindir}/$i
done

# uncompress is a part of ncompress package
rm -f %{buildroot}%{_bindir}/uncompress

cat > %{buildroot}%{_bindir}/zless <<EOF
#!/bin/sh
export LESSOPEN="|lesspipe.sh %s"
less "\$@"
EOF
chmod 755 %{buildroot}%{_bindir}/zless

%files
%doc NEWS README AUTHORS ChangeLog
/bin/gzip
/bin/gunzip
%{_mandir}/man1/gunzip.1*
%{_mandir}/man1/gzexe.1*
%{_mandir}/man1/gzip.1*
%{_mandir}/man1/zforce.1*
%{_mandir}/man1/zless.1*
%{_mandir}/man1/zmore.1*
%{_mandir}/man1/znew.1*
%{_infodir}/*
%{_bindir}/gunzip
%{_bindir}/gzexe
%{_bindir}/gzip
%{_bindir}/zforce
%{_bindir}/zless
%{_bindir}/zmore
%{_bindir}/znew

%files utils
/bin/zcat
%{_bindir}/zcat
%{_bindir}/zcmp
%{_bindir}/zdiff
%{_bindir}/zegrep
%{_bindir}/zfgrep
%{_bindir}/zgrep
%{_mandir}/man1/zcat.1*
%{_mandir}/man1/zcmp.1*
%{_mandir}/man1/zdiff.1*
%{_mandir}/man1/zgrep.1*


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.5-1
+ Revision: 806479
- 1.5
- rediff patches

* Fri Jun 08 2012 Andrey Bondrov <abondrov@mandriva.org> 1.4-7
+ Revision: 803273
- Drop some legacy junk

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - clean out old junk and adapt to comply with new policies

* Tue Mar 13 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.4-5
+ Revision: 784615
- remove cyclic dependencies

* Tue Mar 13 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.4-4
+ Revision: 784578
- move files that conflicts with zutils to separate gzip-utils package

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4-3
+ Revision: 664965
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdv2011.0
+ Revision: 605516
- rebuild

* Thu Jan 21 2010 Funda Wang <fwang@mandriva.org> 1.4-1mdv2010.1
+ Revision: 494602
- New version 1.4
- patch for CVE-2010-0001 merged

* Wed Jan 20 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.14-1mdv2010.1
+ Revision: 494077
- 1.3.14
- drop the zdiff-compressed patch, applied upstream
- P17: security fix for CVE-2009-2624 (redhat, corrects CVE-2006-4335)
- P18: security fix for CVE-2010-0001 (redhat/upstream)

* Sun Dec 27 2009 Funda Wang <fwang@mandriva.org> 1.3.13-1mdv2010.1
+ Revision: 482676
- new version 1.3.13

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.3.12-5mdv2010.0
+ Revision: 425085
- rebuild

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.12-4mdv2009.1
+ Revision: 316214
- rediffed some fuzzy patches

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.3.12-3mdv2009.0
+ Revision: 221123
- rebuild

* Thu Jan 10 2008 Olivier Blin <blino@mandriva.org> 1.3.12-2mdv2008.1
+ Revision: 147614
- fix zdiffing compressed files (patch from Ole Tange, on bug-gzip ML)
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jul 12 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.12-1mdv2008.0
+ Revision: 51587
- new version
- rediff patch 0
- provide patch 17
- export some flags
- some minor cleans


* Fri Mar 09 2007 David Walluck <walluck@mandriva.org> 1.3.11-5mdv2007.1
+ Revision: 140251
- run %%{make} check
- %%exclude %%{_bindir}/uncompress to prevent conflict with ncompress

  + Olivier Blin <oblin@mandriva.com>
    - remove uncompress, it is in the ncompress package (#29317)

* Fri Mar 09 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.3.11-2mdv2007.1
+ Revision: 138812
- add info-install ass requires(preun) too
- wipe out buildroot before installing
- remove variables defines on top as they get redefined
- cosmetics

  + Olivier Blin <oblin@mandriva.com>
    - gzip does do anything special anymore if called as gunzip or zcat, keep the real gunzip and zcat binaries

* Fri Mar 09 2007 David Walluck <walluck@mandriva.org> 1.3.11-1mdv2007.1
+ Revision: 138639
- 1.3.11 + patches (from Fedora)

  + Stew Benedict <sbenedict@mandriva.com>
    - try to add the sources again
    - 1.3.10
    - rediff, uncompress P9
    - drop P11 (CVE-2005-1228) - merged upstream
    - drop P12 (CVE-2005-0988) - merged upstream
    - drop P13 (CVE-2005-0758) - merged upstream
    - rediff P14

  + Emmanuel Andry <eandry@mandriva.org>
    - Import gzip

* Fri Sep 22 2006 Stew Benedict <sbenedict@mandriva.com> 1.3.5-3mdv2007.0
- P14: security fix for CVE-2006-4344,4345,4346,4347,4348

* Tue May 09 2006 Stew Benedict <sbenedict@mandriva.com> 1.3.5-2mdk
- still need P13 - used Fedora's

* Tue May 09 2006 Stew Benedict <sbenedict@mandriva.com> 1.3.5-1mdk
- 1.3.5, source URL
- drop P0-P8, redo P9, drop P10, redo P12, drop P13
- update Requires(pre)

* Tue Jan 31 2006 Olivier Blin <oblin@mandriva.com> 1.2.4a-19mdk
- from Vincent Danen: updated P13 for a more comprehensive fix for CVE-2005-0758

* Fri Jan 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.4a-18mdk
- rebuild

* Thu Jan 19 2006 Olivier Blin <oblin@mandriva.com> 1.2.4a-17mdk
- strip gzip before find-debuginfo.sh breaks the hard links
  (to be LSB compliant, though it makes the debug package useless)

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.2.4a-16mdk
- Rebuild

* Thu May 26 2005 Olivier Blin <oblin@mandriva.com> 1.2.4a-15mdk
- fix invalid word in description
- security update (from Stew Benedict) for:
  - CAN-2005-1228 (P11)
  - CAN-2005-0988 (P12)
  - CAN-2005-0758 (P13)

* Tue Dec 07 2004 Olivier Blin <blino@mandrake.org> 1.2.4a-14mdk
- fix some remaining temp file issues (CAN-2004-0970); only in zdiff, we 
  took care of the rest with an earlier update

* Thu Jul 01 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.2.4a-13mdk
- rebuild
- gc is no longer the packager
- desc: Mandrakelinux

