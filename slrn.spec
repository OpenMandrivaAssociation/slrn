Name:		slrn
Summary:	A powerful, easy to use, threaded Internet news reader
Version:	0.9.9p1
Release:	6
License:	GPLv2+
Group:		Networking/News
URL:		http://www.slrn.org/
Source0:	ftp://slrn.sourceforge.net/pub/slrn/%{name}-%{version}.tar.bz2
Source1:	slrnpull-expire
Source2:	slrnpull.log
Source3:	README.rpm-slrnpull
Patch0:		slrn-0.9.9p1-dont-strip-binaries-on-install.patch
Requires:	inews
Suggests:	lynx
BuildRequires:  slang-devel >= 2.0.0
BuildRequires:  sendmail-command
BuildRequires:	gettext-devel
BuildRequires:  inews

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
%setup  -q
%patch0 -p1 -b .nostrip~

%build
# Fix install of slrnpull man page, seems to be broken upstream
# - AdamW 2008/02
sed -i -e 's,slrn.1,*.1,g' src/Makefile.in
# Better default browser - AdamW 2008/02
sed -i -e 's,netscape,www-browser,g' doc/slrn.rc
# FHS compliant install
%configure2_5x --sysconfdir=%{_sysconfdir}/news --with-slanginc=%{_includedir}/slang \
               --with-slanglib=%{_libdir} --with-slrnpull \
               --with-slanginc=%{_includedir}/slang --with-nss-compat --enable-inews --enable-setgid-code

%make
# Force build of slrnpull, again seems broken upstream - AdaMw 2008/02
%make slrnpull

%install
%makeinstall_std
%find_lang %{name}

mkdir -p %{buildroot}/etc/{cron.daily,logrotate.d,news}
install doc/slrn.rc %{buildroot}/etc/news/
chmod 644 %{buildroot}/etc/news/slrn.rc

#(peroyvind) remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}

%files -f %{name}.lang
%doc doc/{FIRST_STEPS,README.SSL,help.txt,score.txt,slrnfuns.txt,README.macros,THANKS,manual.txt,slrn-doc.html,FAQ,README.GroupLens,README.multiuser,score.sl,slrn.rc} COPYRIGHT README changes.txt
%attr(755,root,root) %{_bindir}/slrn
%{_mandir}/man1/slrn.1*
%config(noreplace) %{_sysconfdir}/news/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files pull
%doc doc/slrnpull/*
%{_mandir}/man1/slrnpull*
%{_bindir}/slrnpull
