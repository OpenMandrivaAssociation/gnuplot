%define	modeversion 0.6.0

Name:		gnuplot
Summary:	A program for plotting mathematical expressions and data
Version:	4.4.3
Release:	3
License:	Freeware-like
Group:		Sciences/Other
URL:		http://www.gnuplot.info/
Source0:	http://downloads.sourceforge.net/project/gnuplot/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:	http://cars9.uchicago.edu/~ravel/software/gnuplot-mode/gnuplot-mode.%{modeversion}.tar.bz2
Source2:	http://www.gnuplot.info/faq/faq.html
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		gnuplot-4.0.0-emacs-mode--disable-f9.patch
Patch1:		gnuplot-4.2.4-fix-format-errors.patch
Requires:	gnuplot-nox
Suggests:	gnuplot-mode
Suggests:	gnuplot-doc
Requires(preun): info-install
BuildRequires:	libx11-devel
BuildRequires:	emacs-bin
BuildRequires:	ncurses-devel
BuildRequires:	png-devel
BuildRequires:	readline-devel
BuildRequires:	tetex-latex
BuildRequires:  texinfo
BuildRequires:  gd-devel
BuildRequires:  cairo-devel
BuildRequires:	lua-devel
BuildRequires:	wxgtku2.8-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

%package nox
Summary:	A program for plotting mathematical expressions and data
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description nox
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides GNUPlot without any X dependency.

%package mode
Summary:	Yet another Gnuplot mode for Emacs
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description mode
Gnuplot is a major mode for Emacs flavours with the following features:

 - Functions for plotting lines, regions, entire scripts, or entire files
 - Graphical interface to setting command arguments
 - Syntax colorization
 - Completion of common words in Gnuplot
 - Code indentation
 - On-line help using Info for Gnuplot functions and features
 - Interaction with Gnuplot using comint
 - Pull-down menus plus a toolbar in XEmacs
 - Distributed with a quick reference sheet in postscript.

%package doc
Summary:	GNUPlot Documentation
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description doc
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides the additional documentation.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1

perl -pi -e 's|(^\s*)mkinstalldirs\s|$1./mkinstalldirs |' gnuplot-mode.%{modeversion}/Makefile.in
# Non-free stuff. Ouch. -- Geoff
rm -f demo/prob.dem demo/prob2.dem

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-fast-math"
export CONFIGURE_TOP=..

mkdir build-nox
pushd build-nox
%configure2_5x --with-readline=gnu --with-png --without-linux-vga --without-x --disable-wxwidgets
%make -C src/
%make -C docs/ ps
%make -C docs/ pdf
popd

mkdir build-x11
pushd build-x11
%configure2_5x --with-readline=gnu --with-png --without-linux-vga
%make
popd

pushd gnuplot-mode.%{modeversion} && {
    ./configure --prefix=/usr
    %make
} && popd

cp -f %SOURCE2 .
chmod 644 faq.html

%install
rm -rf $RPM_BUILD_ROOT

pushd build-nox
%{makeinstall_std}
%__mv %{buildroot}/%{_bindir}/gnuplot %{buildroot}/%{_bindir}/gnuplot-nox
popd

pushd build-x11
%{makeinstall_std}
popd

pushd gnuplot-mode.%{modeversion} && {
    make install prefix=$RPM_BUILD_ROOT/usr
    pdflatex gpelcard
    install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
    install -m 644 dotemacs $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el
} && popd

# Copy back from build dir to be able to package those files
pushd build-nox
%__mv docs/gnuplot.pdf ../docs/
%__mv docs/gnuplot.ps ../docs/
%__mv docs/gpcard.ps ../docs/
popd

# menu

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gnuplot
Comment=The famous function plotting program
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=true
Type=Application
StartupNotify=true
Categories=Sciences;
EOF

# icon
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%post
%if %mdkversion < 200900
%{update_menus}
%endif
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/gnuplot

%files nox
%defattr(-,root,root)
%doc Copyright faq.html
%doc README README.1ST
%doc TODO NEWS PORTING
%{_bindir}/gnuplot-nox
%{_mandir}/*/*
%{_libdir}/gnuplot
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/texmf/tex/latex/gnuplot

%files doc
%defattr(-,root,root)
%doc demo docs/psdoc docs/gnuplot.pdf
%{_datadir}/gnuplot
%{_infodir}/*

%files mode
%defattr(-,root,root)
%doc gnuplot-mode.%{modeversion}/gpelcard.pdf
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_datadir}/emacs/site-lisp/*
