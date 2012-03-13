Name:		gzip
Summary:	The GNU data compression program
Version:	1.4
Release:	%mkrel 4
Source0:	ftp://alpha.gnu.org/pub/gnu/gzip/gzip-%{version}.tar.gz
Source1:	ftp://alpha.gnu.org/pub/gnu/gzip/gzip-%{version}.tar.gz.sig
Patch0:		gzip-1.3.12-openbsd-owl-tmp.patch
Patch1:		gzip-1.3.5-zforce.patch
Patch3:		gzip-1.3.9-stderr.patch
Patch4:		gzip-1.3.10-zgreppipe.patch
Patch5:		gzip-1.3.13-rsync.patch
Patch6:		gzip-1.3.3-window-size.patch
Patch7:		gzip-1.3.9-addsuffix.patch
Patch12:	gzip-1.3.5-cve-2006-4335.patch
Patch13:	gzip-1.3.5-cve-2006-4336.patch
Patch14:	gzip-1.3.5-cve-2006-4338.patch
Patch15:	gzip-1.3.9-cve-2006-4337.patch
Patch16:	gzip-1.3.5-cve-2006-4337_len.patch
Patch17:	gzip-1.3.14-CVE-2009-2624-1.diff
URL:		http://www.gzip.org
License:	GPLv3+
Group:		Archiving/Compression
Requires(pre):	info-install
Requires(preun): info-install
Requires:	mktemp less
BuildRequires:	texinfo
Suggests:	%{name}-utils

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your Mandriva Linux system, because it is a
very commonly used data compression program.

%package utils
Summary:	Utilities dealing with gzip compressed files
Requires:	gzip = %{version}

%description utils
The gzip-utils package contains programs for manipulating gzip-compressed
archives: zcat, zcmp, zdiff, zgrep.

%prep
%setup -q
%patch0 -p1 -b .owl-tmp
%patch1 -p0 -b .zforce
%patch3 -p1 -b .stderr
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
rm -rf %{buildroot}

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


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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
