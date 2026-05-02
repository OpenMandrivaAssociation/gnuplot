%define	modeversion 0.11

# Work around _Float32 issue
%ifarch x86_64
%global optflags %{optflags} -O3
%endif

Summary:	A program for plotting mathematical expressions and data
Name:		gnuplot
Version:		6.0.4
Release:		1
License:		Freeware-like
Group:		Sciences/Other
Url:		https://www.gnuplot.info/
Source0:	https://downloads.sourceforge.net/project/gnuplot/%{name}/%{version}/%{name}-%{version}.tar.gz
#Source1:	http://cars9.uchicago.edu/~ravel/software/gnuplot-mode/gnuplot-mode.%%{modeversion}.tar.gz
Source1:	https://github.com/emacs-gnuplot/gnuplot/archive/refs/tags/gnuplot-%{modeversion}.tar.gz
Source2:	https://www.gnuplot.info/faq/faq.html
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		gnuplot-6.0.4-fix-test-data-building.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	locales-extra-charsets
BuildRequires:	fontconfig
BuildRequires:	emacs-bin
BuildRequires:	latex2html
BuildRequires:	latex-picins
BuildRequires:	make
BuildRequires:	slibtool
BuildRequires:	texinfo
BuildRequires:	texlive-epstopdf
BuildRequires:	texlive-latex-bin
BuildRequires:	tetex-latex
BuildRequires:	giflib-devel
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairo-pdf)
BuildRequires:	pkgconfig(cairo-ps)
BuildRequires:	pkgconfig(gdlib)
BuildRequires:	pkgconfig(libcerf)
BuildRequires:	pkgconfig(libotf)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
Requires:	gnuplot-nox
Suggests:	gnuplot-mode
Suggests:	gnuplot-doc
# Package not provided yet: libamos

%description
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.
Install gnuplot if you need a graphics package for scientific data
representation.

%files
%{_bindir}/%{name}
%{_datadir}/texmf-dist/tex/latex/%{name}
%{_libexecdir}/%{name}/%(echo %{version}|cut -d. -f1-2)/%{name}_x11
%{_libexecdir}/%{name}/%(echo %{version}|cut -d. -f1-2)/%{name}_qt

#-----------------------------------------------------------------------------

%package	nox
Summary:	A program for plotting mathematical expressions and data
Group:	Sciences/Other
Conflicts:	%{name} < 4.4.3

%description	nox
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.
Install gnuplot if you need a graphics package for scientific data
representation.
This package provides GNUPlot without any X dependency.

%files nox
%doc Copyright NEWS README RELEASE_NOTES
%{_bindir}/%{name}-nox
%{_mandir}/ja/man1/%{name}.1*
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/openmandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

#-----------------------------------------------------------------------------

%package	mode
Summary:	Yet another Gnuplot mode for Emacs
Group:	Sciences/Other
Conflicts:	%{name} < 4.4.3
Requires:	emacs

%description	mode
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

%files mode
#doc %%{name}-%%{modeversion}/gpelcard.pdf
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el
%{_datadir}/emacs/site-lisp/*

 #-----------------------------------------------------------------------------
 
%package	doc
Summary:	GNUPlot Documentation
Group:		Sciences/Other
Conflicts:	%{name} < 4.4.3

%description	doc
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.
Install gnuplot if you need a graphics package for scientific data
representation.
This package provides the additional documentation.

%files doc
%doc faq.html
%doc demo
#docs/%%{name}%%{name}.pdf
%{_datadir}/%{name}

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -a1

# Install faq
cp -f %{SOURCE2} .
chmod 644 faq.html

#perl -pi -e 's|(^\s*)mkinstalldirs\s|$1./mkinstalldirs |' %%{name}-mode.%%{modeversion}/Makefile.in

# Non-free stuff. Ouch. -- Geoff
rm -f demo/prob.dem demo/prob2.dem


%build
# Needed because we are patching makefiles
autoreconf -vfi

export CFLAGS="%{optflags} -fno-fast-math"
export CONFIGURE_TOP=..

# Build without X
mkdir build-nox
pushd build-nox
	%configure \
		--with-readline=gnu \
		--without-x \
		--without-amos \
		--disable-wxwidgets \
		--without-qt

	%make_build -C src/
# building docs with parallel make it fail on a 32-thread box
	%make_build -j1 -C docs/ info
popd

# Qt build
mkdir build-x11
pushd build-x11
	%configure \
		--with-readline=gnu \
		--without-amos \
		--disable-wxwidgets \
		--with-qt=qt6

	%make_build
popd

# Emacs mode
pushd %{name}-%{modeversion}
	%make_build
popd


%install
pushd build-nox
	%make_install
	mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-nox
popd

pushd build-x11
	%make_install
popd

pushd %{name}-%{modeversion}
# No automated install in makefile
	mkdir -p %{buildroot}%{_sysconfdir}/emacs/site-start.d
	mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
	install -m 644 %{name}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
	install -m 644 *.el %{buildroot}%{_datadir}/emacs/site-lisp/
	install -m 644 *.elc %{buildroot}%{_datadir}/emacs/site-lisp/
popd

# Provide menu entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Gnuplot
GenericName=Function plotting program
Comment=The famous function plotting program
Exec=%{name}
Icon=%{name}
Terminal=true
Type=Application
StartupNotify=true
Categories=Graphics;Education;Science;Math;DataVisualization;
EOF

# Install our icons
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

pushd %{buildroot}%{_datadir}
	mv texmf-local texmf-dist
popd

# Drop unwanted stuff after build
rm -f demo/Makefile.*
rm -f demo/html/Makefile.*
rm -f demo/html/*.pl
rm -f demo/html/*.orig
rm -f demo/plugin/Makefile.*


%post -p %{_bindir}/texhash

%postun -p %{_bindir}/texhash
