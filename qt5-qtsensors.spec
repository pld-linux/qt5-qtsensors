# maybe TODO: 
# plugins/simulator (BR: Qt5Simulator)
# plugins/sensorfw for MeeGo (sensorfw / sensord-qt)
#
# Conditional build:
%bcond_with	bootstrap	# disable features to able to build without installed qt5
%bcond_without	doc		# documentation
%bcond_without	qtbluetooth	# sensortag plugin (using Qt5Bluetooth)

%if %{with bootstrap}
%undefine	with_doc
%endif

%define		orgname		qtsensors
%define		qtbase_ver		%{version}
%define		qtconnectivity_ver	%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		5.9
Summary:	The Qt5 Sensors library
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors
Name:		qt5-%{orgname}
Version:	5.15.9
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	8ee181640bdece1abd1d5e97e679302f
URL:		https://www.qt.io/
%{?with_qtbluetooth:BuildRequires:	Qt5Bluetooth-devel >= %{qtconnectivity_ver}}
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5DBus-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Sensors library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Sensors.

%package -n Qt5Sensors
Summary:	The Qt5 Sensors library
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors
Group:		Libraries
%{?with_qtbluetooth:Requires:	Qt5Bluetooth >= %{qtconnectivity_ver}}
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5DBus >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Obsoletes:	qt5-qtsensors < 5.2.0-1

%description -n Qt5Sensors
Qt5 Sensors library provides classes for reading sensor data.

%description -n Qt5Sensors -l pl.UTF-8
Biblioteka Qt5 Sensors dostarcza klasy do odczytu danych z czujników.

%package -n Qt5Sensors-devel
Summary:	Qt5 Sensors library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Sensors - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Sensors = %{version}-%{release}
Obsoletes:	qt5-qtsensors-devel < 5.2.0-1

%description -n Qt5Sensors-devel
Qt5 Sensors library - development files.

%description -n Qt5Sensors-devel -l pl.UTF-8
Biblioteka Qt5 Sensors - pliki programistyczne.

%package doc
Summary:	Qt5 Sensors documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Sensors w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Sensors documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Sensors w formacie HTML.

%package doc-qch
Summary:	Qt5 Sensors documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Sensors w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Sensors documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Sensors w formacie QCH.

%package examples
Summary:	Qt5 Sensors examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Sensors
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Sensors examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Sensors.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%{__sed} -i -e 's/SENSORS_PLUGINS = sensortag generic/SENSORS_PLUGINS += sensortag/' src/plugins/sensors/sensors.pro

%build
%{qmake_qt5} \
	%{?with_qtbluetooth:CONFIG+=sensortag}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
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
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/sensors

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Sensors -p /sbin/ldconfig
%postun	-n Qt5Sensors -p /sbin/ldconfig

%files -n Qt5Sensors
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5Sensors.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Sensors.so.5
%dir %{qt5dir}/plugins/sensorgestures
# R: Core Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensorgestures/libqtsensorgestures_plugin.so
# R: Core Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensorgestures/libqtsensorgestures_shakeplugin.so
%dir %{qt5dir}/plugins/sensors
# R: Core Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensors/libqtsensors_generic.so
# R: Core DBus Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensors/libqtsensors_iio-sensor-proxy.so
# R: Core Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensors/libqtsensors_linuxsys.so
# R: Bluetooth Core Sensors
%attr(755,root,root) %{qt5dir}/plugins/sensors/libqtsensors_sensortag.so
%dir %{qt5dir}/qml/QtSensors
# R: Core Qml Sensors [Quick for scriping]
%attr(755,root,root) %{qt5dir}/qml/QtSensors/libdeclarative_sensors.so
%{qt5dir}/qml/QtSensors/plugins.qmltypes
%{qt5dir}/qml/QtSensors/qmldir

%files -n Qt5Sensors-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Sensors.so
%{_libdir}/libQt5Sensors.prl
%{_includedir}/qt5/QtSensors
%{_pkgconfigdir}/Qt5Sensors.pc
%{_libdir}/cmake/Qt5Sensors
%{qt5dir}/mkspecs/modules/qt_lib_sensors.pri
%{qt5dir}/mkspecs/modules/qt_lib_sensors_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsensors

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtsensors.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
