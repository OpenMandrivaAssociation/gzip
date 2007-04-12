Name:		gzip
Summary:	The GNU data compression program
Version:	1.3.11
Release:	%mkrel 5
Source0:	ftp://alpha.gnu.org/pub/gnu/gzip/gzip-%{version}.tar.gz
Patch0:		gzip-1.3.9-openbsd-owl-tmp.patch
Patch1:		gzip-1.3.5-zforce.patch
Patch3:		gzip-1.3.9-stderr.patch
Patch4:		gzip-1.3.10-zgreppipe.patch
Patch5:		gzip-1.3.9-rsync.patch
Patch6:		gzip-1.3.3-window-size.patch
Patch7:		gzip-1.3.9-addsuffix.patch
Patch12:	gzip-1.3.5-cve-2006-4335.patch
Patch13:	gzip-1.3.5-cve-2006-4336.patch
Patch14:	gzip-1.3.5-cve-2006-4338.patch
Patch15:	gzip-1.3.9-cve-2006-4337.patch
Patch16:	gzip-1.3.5-cve-2006-4337_len.patch

URL:		http://www.gzip.org/
License:	GPL
Group:		Archiving/Compression
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(pre):	info-install
Requires(preun): info-install
Requires:	mktemp less
BuildRequires:	texinfo

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.  

Gzip should be installed on your Mandriva Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch0 -p1 -b .owl-tmp
%patch1 -p1 -b .zforce
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

%build
export DEFS="-DNO_ASM"
%{configure2_5x}
%{make}

%install
rm -rf %{buildroot}
install -d $RPM_BUILD_ROOT%{_mandir}

%{makeinstall} mandir=$RPM_BUILD_ROOT%{_mandir}

install -d $RPM_BUILD_ROOT/bin

for i in gzip gunzip zcat; do
    mv -f $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT/bin/$i
    ln -sf ../../bin/$i $RPM_BUILD_ROOT%{_bindir}/$i
done

for i in zcmp zdiff zforce zgrep zmore znew ; do
	sed -e "s|$RPM_BUILD_ROOT||g" < $RPM_BUILD_ROOT%{_bindir}/$i > $RPM_BUILD_ROOT%{_bindir}/.$i
	rm -f $RPM_BUILD_ROOT%{_bindir}/$i
	mv $RPM_BUILD_ROOT%{_bindir}/.$i $RPM_BUILD_ROOT%{_bindir}/$i
	chmod 755 $RPM_BUILD_ROOT%{_bindir}/$i
done

# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}%{_bindir}/uncompress

cat > $RPM_BUILD_ROOT%{_bindir}/zless <<EOF
#!/bin/sh
export LESSOPEN="|lesspipe.sh %s"
less "\$@"
EOF
chmod 755 $RPM_BUILD_ROOT%{_bindir}/zless

%check
%{make} check

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*


