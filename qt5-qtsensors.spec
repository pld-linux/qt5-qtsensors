# TODO:
# - cleanup
#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qtsensors
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Sensors library
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors
Name:		qt5-%{orgname}
Version:	5.2.0
Release:	0.1
License:	LGPL v2.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.2/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	718606a6f76afa20c6cd2e0433356ac2
URL:		http://qt-project.org/
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	qt5-qtdeclarative-devel = %{version}
BuildRequires:	qt5-qttools-devel = %{version}
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Sensors libraries.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera biblioteki Qt5 Sensors.

%package -n Qt5Sensors
Summary:	The Qt5 Sensors library
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Obsoletes:	qt5-qtsensors

%description -n Qt5Sensors
Qt5 Sensors library (TODO: description).

%description -n Qt5Sensors -l pl.UTF_8
Biblioteka Qt5 Sensors (TODO: ...).

%package -n Qt5Sensors-devel
Summary:	Qt5 Sensors library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Sensors = %{version}-%{release}
Obsoletes:	qt5-qtsensors-devel

%description -n Qt5Sensors-devel
Qt5 Sensors library - development files.

%description -n Qt5Sensors-devel -l pl.UTF-8
Biblioteka Qt5 Sensors - pliki programistyczne.

%package doc
Summary:	Qt5 Sensors documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Sensors w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Sensors documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Sensors w formacie HTML.

%package doc-qch
Summary:	Qt5 Sensors documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Sensors w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Sensors documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Sensors w formacie QCH.

%package examples
Summary:	Qt5 Sensors examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Sensors
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 Sensors examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Sensors.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	RESULT=`echo $RPM_BUILD_ROOT$2 2>/dev/null`
	[ "$RESULT" == "" ] && return # XXX this is never true due $RPM_BUILD_ROOT being set
	r=`echo $RESULT | awk '{ print $1 }'`

	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho examples %{_examplesdir}/qt5
for f in `find $RPM_BUILD_ROOT%{_examplesdir}/qt5 -printf "%%P "`; do
	ifecho examples %{_examplesdir}/qt5/$f
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Sensors -p /sbin/ldconfig
%postun	-n Qt5Sensors -p /sbin/ldconfig

%files -n Qt5Sensors
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Sensors.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Sensors.so.5
%attr(755,root,root) %{qt5dir}/plugins
%attr(755,root,root) %{qt5dir}/qml

%files -n Qt5Sensors-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Sensors.so
%{_libdir}/libQt5Sensors.prl
%{_includedir}/qt5/QtSensors
%{_pkgconfigdir}/Qt5Sensors.pc
%{_libdir}/cmake/Qt5Sensors
%{qt5dir}/mkspecs/modules/*.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsensors

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsensors.qch
%endif

%files examples -f examples.files
