# (tpg) optimize it a bit
%ifnarch %{riscv}
%global optflags %{optflags} -O3 --rtlib=compiler-rt
%endif

# (tpg) enable PGO build
%if %{cross_compiling}
%bcond_with pgo
%else
%bcond_without pgo
%endif

Summary:	The GNU data compression program
Name:		gzip
Version:	1.12
Release:	4
License:	GPLv3+
Group:		Archiving/Compression
Url:		http://www.gzip.org
Source0:	ftp://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.gz
Patch1:		gzip-1.11-clang.patch
BuildRequires:	texinfo
# (tpg) this is a part of basesystem package
# (itchka) Needed it for the test package
BuildRequires:	less
# (tpg) yes we are about to use multithreaded gzip
Requires:	pigz > 2.4-2

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
%autosetup -p1

%build
export DEFS="-DNO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"

%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)"

CFLAGS="%{optflags} -fprofile-generate" \
CXXFLAGS="%{optflags} -fprofile-generate" \
LDFLAGS="%{build_ldflags} -fprofile-generate" \
%configure

%make_build

make check

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f *.profraw
make clean

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
%configure

%make_build

%if ! %{cross_compiling}
%check
make check
%endif

%install
%make_install

# (tpg) we are using pigz, so move these
for i in gzip gunzip; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i-st
done

for i in zcmp zdiff zforce zgrep zmore znew ; do
    sed -e "s|%{buildroot}||g" < %{buildroot}%{_bindir}/"$i" > %{buildroot}%{_bindir}/."$i"
    rm -f %{buildroot}%{_bindir}/"$i"
    mv %{buildroot}%{_bindir}/."$i" %{buildroot}%{_bindir}/"$i"
    chmod 755 %{buildroot}%{_bindir}/"$i"
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
%doc %{_mandir}/man1/gunzip.1*
%doc %{_mandir}/man1/gzexe.1*
%doc %{_mandir}/man1/gzip.1*
%doc %{_mandir}/man1/zforce.1*
%doc %{_mandir}/man1/zless.1*
%doc %{_mandir}/man1/zmore.1*
%doc %{_mandir}/man1/znew.1*
%doc %{_infodir}/*
%{_bindir}/gzip-st
%{_bindir}/gunzip-st
%{_bindir}/gzexe
%{_bindir}/zforce
%{_bindir}/zless
%{_bindir}/zmore
%{_bindir}/znew

%files utils
%{_bindir}/zcat
%{_bindir}/zcmp
%{_bindir}/zdiff
%{_bindir}/zegrep
%{_bindir}/zfgrep
%{_bindir}/zgrep
%doc %{_mandir}/man1/zcat.1*
%doc %{_mandir}/man1/zcmp.1*
%doc %{_mandir}/man1/zdiff.1*
%doc %{_mandir}/man1/zgrep.1*
