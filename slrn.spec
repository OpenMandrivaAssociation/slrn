%define name	slrn
%define version 0.9.9
%define svn	254
%if %svn
%define release %mkrel 0.%svn.1
%else
%define release %mkrel 1
%endif

Name:		%{name}
Summary:	A powerful, easy to use, threaded Internet news reader
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Networking/News
URL:		http://www.slrn.org/
%if %svn
Source0:	%{name}-%{svn}.tar.lzma
%else
Source0:	ftp://slrn.sourceforge.net/pub/slrn/%{name}-%{version}.tar.bz2
%endif
Source1:	slrnpull-expire
Source2:	slrnpull.log
Source3:	README.rpm-slrnpull
Requires:	slang >= 2.0.0
Requires:	inews
BuildRequires:  slang-devel >= 2.0.0
BuildRequires:  sendmail-command
BuildRequires:	gettext-devel

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
%if %svn
%setup -q -n %{name}
%else
%setup  -q
%endif

%build
# FHS compliant install
%configure2_5x --sysconfdir=%{_sysconfdir}/news --with-slang-library=%_libdir --with-slrnpull
%make

%install
%makeinstall_std
%find_lang %{name}

mkdir -p %{buildroot}/etc/{cron.daily,logrotate.d,news}
install doc/slrn.rc %{buildroot}/etc/news/
chmod 644 %{buildroot}/etc/news/slrn.rc

#(peroyvind) remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %buildroot

%post
%update_menus
%postun
%update_menus

%files -f %{name}.lang 
%defattr(-,root,root)
%doc doc/{FIRST_STEPS,README.SSL,help.txt,score.txt,slrnfuns.txt,README.macros,THANKS,manual.txt,slrn-doc.html,FAQ,README.GroupLens,README.multiuser,score.sl,slrn.rc} COPYRIGHT README changes.txt
%attr(755,root,root) %{_bindir}/slrn
%{_mandir}/man1/slrn.1*
%config(noreplace) %{_sysconfdir}/news/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files pull
%defattr(-,root,root)
%doc doc/slrnpull/*
%{_mandir}/man1/slrnpull*
%{_bindir}/slrnpull

