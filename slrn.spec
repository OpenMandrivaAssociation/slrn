Name:		slrn
Summary:	A powerful, easy to use, threaded Internet news reader
Version:	0.9.9p1
Release:	13
License:	GPLv2+
Group:		Networking/News
URL:		http://www.slrn.org/
Source0:	ftp://slrn.sourceforge.net/pub/slrn/%{name}-%{version}.tar.bz2
Source1:	slrnpull-expire
Source2:	slrnpull.log
Source3:	README.rpm-slrnpull
Patch0:		slrn-0.9.9p1-dont-strip-binaries-on-install.patch
Patch1:		slrn-0.9.9p1-no-rpath.patch
Requires:	inews
Suggests:	lynx
BuildRequires:	slang-devel >= 2.0.0
BuildRequires:	sendmail-command
BuildRequires:	gettext-devel
BuildRequires:	inews

%description
SLRN is a powerful, easy to use, threaded Internet news reader.  SLRN is
highly customizable and allows you to design complex filters to sort or kill
news articles.  SLRN works well over slow network connections, and includes
a utility for reading news off-line.

Install slrn if you need a full-featured news reader, if you have a slow
network connection, or if you'D like to save on-line time by reading your
news off-line.

%package	pull
Summary:	Offline news reading support for slrn
Group:		Networking/News
Requires:	%{name} = %{EVRD}

%description pull
This package provides slrnpull, which allows set up of a small news
spool for offline news reading.

%prep
%setup -q
%patch0 -p1 -b .nostrip~
%patch1 -p1 -b .norpath~

%build
# Fix install of slrnpull man page, seems to be broken upstream
# - AdamW 2008/02
sed -i -e 's,slrn.1,*.1,g' src/Makefile.in
# Better default browser - AdamW 2008/02
sed -i -e 's,netscape,www-browser,g' doc/slrn.rc
# FHS compliant install
%configure2_5x	--sysconfdir=%{_sysconfdir}/news \
		--with-slanginc=%{_includedir}/slang \
		--with-slanglib=%{_libdir} \
		--with-slrnpull \
		--with-slanginc=%{_includedir}/slang \
		--with-nss-compat \
		--enable-inews \
		--enable-setgid-code \
		--disable-rpath
%make
# Force build of slrnpull, again seems broken upstream - AdaMw 2008/02
%make slrnpull

%install
%makeinstall_std
%find_lang %{name}

mkdir -p %{buildroot}%{_sysconfdir}/{cron.daily,logrotate.d,news}
install -m644 doc/slrn.rc -D %{buildroot}%{_sysconfdir}/news/slrn.rc

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


%changelog
* Wed May 30 2012 Per √òyvind Karlsen <peroyvind@mandriva.org> 0.9.9p1-6
+ Revision: 801349
- get rid of rpath (P1)
- cleanups
- drop legacy rpm junk
- fix st00pid makefiles stripping binaries on install (P0)
- drop broken explicit slang dependency

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.9p1-5
+ Revision: 669988
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9p1-4mdv2011.0
+ Revision: 607544
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9p1-3mdv2010.1
+ Revision: 524116
- rebuilt for 2010.1

* Mon Aug 24 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.9.9p1-2mdv2010.0
+ Revision: 420298
+ rebuild (emptylog)

* Fri Jan 23 2009 J√©r√¥me Soyer <saispo@mandriva.org> 0.9.9p1-1mdv2009.1
+ Revision: 333110
- Add inews support
- New release upstream

  + Adam Williamson <awilliamson@mandriva.org>
    - fix configure line: a parameter had its name changed, and specifying slang's
      location doesn't work unless you specify both include and lib dir

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.9.9-0.266.2mdv2009.0
+ Revision: 225445
- rebuild

* Wed Feb 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.9.9-0.266.2mdv2008.1
+ Revision: 166930
- suggest lynx as it's the default browser for non-X situations
- use www-browser, not netscape, as the browser if X is detected

* Wed Feb 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.9.9-0.266.1mdv2008.1
+ Revision: 166906
- don't run %%update_menus as there's no menu entry
- quick fix for slrnpull build / install (broken upstream)
- new svn snapshot 266
- see if makeinstall_std fixes the installation problem
- new snapshot
- some spec cleanups
- upstream switched from CVS to SVN, adapt
- new license policy
- drop menu entry (this is a console-only app)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 08 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.8.2-0.20070607.1mdv2008.0
+ Revision: 37236
- specify slang location for autogen and configure (fix x86-64 build)
- BuildRequire gettext-devel (for autopoint)
- go to CVS snapshot
- rebuild for new era
- XDG menu
- add two patches from upstream


* Tue Feb 28 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.9.8.1-4mdk
- Don't ship slrn man page in both packages

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.9.8.1-3mdk
- Rebuild

* Tue Jul 26 2005 Nicolas LÈcureuil <neoclust@mandriva.org> 0.9.8.1-2mdk
- Fix BuildRequires

* Mon Mar 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.9.8.1-1mdk
- new version 0.9.8.1
- system slrn.rc should not be executable

* Mon Jan 17 2005 Marcel Pol <mpol@mandrake.org> 0.9.8.0-4mdk
- do not send 8859-1 characters to UTF-8 slang [Suse #37854]

* Fri Jul 23 2004 Marcel Pol <mpol@mandrake.org> 0.9.8.0-3mdk
- again build against new slang

* Wed Jul 21 2004 Marcel Pol <mpol@mandrake.org> 0.9.8.0-2mdk
- build against new slang

* Mon Dec 22 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 0.9.8.0-1mdk
- version 0.9.8.0
- remove merged patches
- no more doc/SCORE_FAQ

* Thu Jun 05 2003 Per ÿyvind Karlsen <peroyvind@sintrax.net> 0.9.7.4-3mdk
- fix unpackaged files
- macroize (light;)

