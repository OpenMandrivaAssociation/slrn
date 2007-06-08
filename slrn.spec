%define name	slrn
%define version 0.9.8.2
%define cvs	20070607
%if %cvs
%define release %mkrel 0.%cvs.1
%else
%define release %mkrel 1
%endif

Name:		%{name}
Summary:	A powerful, easy to use, threaded Internet news reader
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/News
URL:		http://www.slrn.org/
%if %cvs
Source0:	%{name}-%{cvs}.tar.bz2
%else
Source0:	ftp://slrn.sourceforge.net/pub/slrn/%{name}-%{version}.tar.bz2
%endif
Source1:	slrnpull-expire
Source2:	slrnpull.log
Source3:	README.rpm-slrnpull
#Patch0:		slrn-0.9.8.0-utf8.patch
Requires:	slang >= 2.0.0, inews
BuildRoot:	%{_tmppath}/%{name}-build
BuildRequires:  slang-devel >= 2.0.0
BuildRequires:  sendmail-command

%description
SLRN is a powerful, easy to use, threaded Internet news reader.  SLRN is
highly customizable and allows you to design complex filters to sort or kill
news articles.  SLRN works well over slow network connections, and includes
a utility for reading news off-line.

Install slrn if you need a full-featured news reader, if you have a slow
network connection, or if you'D like to save on-line time by reading your
news off-line.

%package pull
Summary:	Offline news reading support for slrn
Group:		Networking/News
Requires:	%{name} = %{version}

%description pull
This package provides slrnpull, which allows set up of a small news
spool for offline news reading.

%prep
%if %cvs
%setup -q -n %{name}
%else
%setup  -q
%endif
#%patch0 -p0 -b .utf8

%build
%if %cvs
./autogen.sh
%endif
# FHS compliant install
%configure --sysconfdir=%{_sysconfdir}/news --with-slrnpull
%make

%install
%makeinstall
%find_lang %{name}

mkdir -p $RPM_BUILD_ROOT/etc/{cron.daily,logrotate.d,news}
install doc/slrn.rc $RPM_BUILD_ROOT/etc/news/
chmod 644 $RPM_BUILD_ROOT/etc/news/slrn.rc
#install -d $RPM_BUILD_ROOT/var/spool/slrnpull/out.going
#install doc/slrnpull/slrnpull.conf $RPM_BUILD_ROOT/var/spool/slrnpull
#install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily
#install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/slrnpull
#cp      %{SOURCE3} doc/slrnpull/README.rpm
#chmod 644 doc/slrnpull/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=SLRN
Comment=Newsreader
Exec=%{_bindir}/%{name} 
Icon=news_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Network;News;X-MandrivaLinux-Internet-News;
EOF

#(peroyvind) remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf %buildroot

%post
%update_menus
%postun
%update_menus

%files -f %{name}.lang 
%defattr(-,root,root)
%doc COPYING    doc/FIRST_STEPS doc/README.SSL doc/help.txt doc/score.txt doc/slrnfuns.txt
%doc COPYRIGHT  README            doc/README.macros     doc/THANKS       doc/manual.txt  doc/slrn-doc.html
%doc doc/FAQ doc/README.GroupLens  doc/README.multiuser changes.txt  doc/score.sl    doc/slrn.rc
%attr(755,root,root) %{_bindir}/slrn
%{_mandir}/man1/slrn.1*
%config(noreplace) %{_sysconfdir}/news/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%_datadir/applications/mandriva-%{name}.desktop

%files pull
%defattr(-,root,root)
%doc doc/slrnpull/*
%{_mandir}/man1/slrnpull*
#%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/slrnpull-expire
#%config(noreplace) %{_sysconfdir}/logrotate.d/slrnpull
%{_bindir}/slrnpull
#%attr(775,news,news) %dir /var/spool/slrnpull
#%attr(3777,news,news) %dir /var/spool/slrnpull/out.going
#%attr(644,news,news) %config(noreplace) /var/spool/slrnpull/slrnpull.conf

