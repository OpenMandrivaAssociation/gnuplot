%define	modeversion 0.6.0

# Work around _Float32 issue
%ifarch x86_64
%global optflags %{optflags} -O3
%endif

Summary:	A program for plotting mathematical expressions and data
Name:		gnuplot
Version:	6.0.2
Release:	1
License:	Freeware-like
Group:		Sciences/Other
Url:		https://www.gnuplot.info/
Source0:	http://downloads.sourceforge.net/project/gnuplot/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:	http://cars9.uchicago.edu/~ravel/software/gnuplot-mode/gnuplot-mode.%{modeversion}.tar.gz
Source2:	http://www.gnuplot.info/faq/faq.html
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch0:		gnuplot-4.0.0-emacs-mode--disable-f9.patch
BuildRequires:	locales-extra-charsets
BuildRequires:	fontconfig
BuildRequires:	emacs-bin
BuildRequires:  texinfo
BuildRequires:	texlive-epstopdf
BuildRequires:	tetex-latex
BuildRequires:	latex-picins
BuildRequires:	latex2html
BuildRequires:	texlive-latex-bin
BuildRequires:  giflib-devel
BuildRequires:	readline-devel
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:  pkgconfig(cairo)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libotf)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gdlib)
Requires:	gnuplot-nox
Suggests:	gnuplot-mode
Suggests:	gnuplot-doc

%description
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

%package	nox
Summary:	A program for plotting mathematical expressions and data
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description	nox
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides GNUPlot without any X dependency.

%package	mode
Summary:	Yet another Gnuplot mode for Emacs
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

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

%package	doc
Summary:	GNUPlot Documentation
Group:		Sciences/Other
Conflicts:	gnuplot < 4.4.3

%description	doc
Gnuplot is a command-line driven, interactive function plotting program
especially suited for scientific data representation. Gnuplot can be used to
plot functions and data points in both two and three dimensions and in many
different formats.

Install gnuplot if you need a graphics package for scientific data
representation.

This package provides the additional documentation.

%prep
%setup -q -a 1
%autopatch -p1

perl -pi -e 's|(^\s*)mkinstalldirs\s|$1./mkinstalldirs |' gnuplot-mode.%{modeversion}/Makefile.in
# Non-free stuff. Ouch. -- Geoff
rm -f demo/prob.dem demo/prob2.dem

%build
export CFLAGS="%{optflags} -fno-fast-math"
export CONFIGURE_TOP=..

mkdir build-nox
pushd build-nox
%configure \
	--with-readline=gnu \
	--with-png \
	--without-linux-vga \
	--without-x \
	--disable-wxwidgets \
	--without-qt

%make_build -C src/
# building docs with parallel make
# fails on a 32-thread box
%make_build -j1 -C docs/ info
popd

mkdir build-x11
pushd build-x11
%configure \
	--with-readline=gnu \
	--with-png \
	--without-linux-vga \
	--disable-wxwidgets \
	--with-qt=qt6
%make_build
popd

pushd gnuplot-mode.%{modeversion} && {
    ./configure --prefix=/usr
    %make_build
} && popd

cp -f %SOURCE2 .
chmod 644 faq.html

%install
pushd build-nox
%make_install
mv %{buildroot}%{_bindir}/gnuplot %{buildroot}%{_bindir}/gnuplot-nox
popd

pushd build-x11
%make_install
popd

pushd gnuplot-mode.%{modeversion} && {
    make install prefix=%{buildroot}/usr
    pdflatex gpelcard
    install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
    install -m 644 dotemacs %{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
} && popd

# menu

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Version=1.0
Name=Gnuplot
Comment=The famous function plotting program
Exec=%{name}
Icon=%{name}
Terminal=true
Type=Application
StartupNotify=true
Categories=Education;Science;Math;DataVisualization;
EOF

# icon
install -m644 %{SOURCE11} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_liconsdir}/%{name}.png

cd %{buildroot}%{_datadir}
mv texmf-local texmf-dist

%post -p %{_bindir}/texhash

%postun -p %{_bindir}/texhash

%files
%{_bindir}/gnuplot
%{_datadir}/texmf-dist/tex/latex/gnuplot
%{_libexecdir}/gnuplot/%(echo %{version}|cut -d. -f1-2)/gnuplot_x11
%{_libexecdir}/gnuplot/%(echo %{version}|cut -d. -f1-2)/gnuplot_qt

%files nox
%doc Copyright
%doc README
%doc NEWS
%{_bindir}/gnuplot-nox
%{_mandir}/*/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files doc
%doc demo docs/gnuplot.pdf
%{_datadir}/gnuplot

%files mode
%doc gnuplot-mode.%{modeversion}/gpelcard.pdf
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*.el
%{_datadir}/emacs/site-lisp/*

