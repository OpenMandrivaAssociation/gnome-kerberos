Name:		gnome-kerberos
Version: 0.3.2
Release:  %mkrel 2
License:	GPL
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	krb5-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	popt-devel
BuildRequires:	texinfo
BuildRequires:  desktop-file-utils
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}_icons.tar.bz2
Patch0:		krb-desktop-entry-fix.patch
Summary:	Kerberos 5 tools for GNOME

%description
This package contains krb5, a tool for managing Kerberos 5 tickets, and
gkadmin, a tool for managing Kerberos realms that uses the kadmin protocols.

%prep
%setup -q -a 1
%patch0 -p0

%build
# never call autoconf. configure.in and configure are out of sync.
%configure --with-krb5=%{_sysconfdir}/kerberos
%make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Utilities/
mv $RPM_BUILD_ROOT%{_datadir}/applications/redhat-krb5.desktop $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Utilities/krb5.desktop

rm -rf RPM_BUILD_ROOT%{_datadir}/applications

%find_lang %name

#icons entries
install -m644 %{name}-16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{name}-32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{name}-48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

#%menu entries 
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/krb5
Icon=%{name}
Categories=Network;
Name=Gnome-Kerberos
Comment=Kerberos 5 tools for GNOME
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc README COPYING AUTHORS ChangeLog INSTALL ABOUT-NLS
%{_datadir}/gnome/apps/Utilities/krb5.desktop
%{_datadir}/pixmaps/kerberos.png
%{_datadir}/%{name}/
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_bindir}/*

