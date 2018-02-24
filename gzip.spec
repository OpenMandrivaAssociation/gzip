# (tpg) optimize it a bit
%global optflags %optflags -Ofast

Summary:	The GNU data compression program
Name:		gzip
Version:	1.9
Release:	2
License:	GPLv3+
Group:		Archiving/Compression
Url:		http://www.gzip.org
Source0:	ftp://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.gz
Patch18:	gzip-1.9-clang.patch
BuildRequires:	texinfo
# (tpg) this is a part of basesystem package
# (itchka) Needed it for the test package
BuildRequires:	less

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your Mandriva Linux system, because it is a
very commonly used data compression program.

%package utils
Summary:	Utilities dealing with gzip compressed files
Requires:	%{name} = %{version}

%description utils
The gzip-utils package contains programs for manipulating gzip-compressed
archives: zcat, zcmp, zdiff, zgrep.

%prep
%setup -q
%apply_patches

%build
export DEFS="-DNO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"

%configure
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
