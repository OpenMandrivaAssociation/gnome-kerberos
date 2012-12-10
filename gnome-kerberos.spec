Name:		gnome-kerberos
Version:	0.3.2
Release:	%mkrel 6
License:	GPL
Group:		Networking/Other
BuildRequires:	krb5-devel
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(popt)
BuildRequires:	texinfo
BuildRequires:  desktop-file-utils
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}_icons.tar.bz2
Patch0:		krb-desktop-entry-fix.patch
Patch1:		gnome-kerberos-0.3.2-fix-str-fmt.patch
Summary:	Kerberos 5 tools for GNOME

%description
This package contains krb5, a tool for managing Kerberos 5 tickets, and
gkadmin, a tool for managing Kerberos realms that uses the kadmin protocols.

%prep
%setup -q -a 1
%patch0 -p0
%patch1 -p0

%build
# never call autoconf. configure.in and configure are out of sync.
%configure2_5x --with-krb5=%{_sysconfdir}/kerberos
%make LIBS="-lcom_err"

%install
%makeinstall
mkdir -p %{buildroot}%{_datadir}/gnome/apps/Utilities/
mv %{buildroot}%{_datadir}/applications/redhat-krb5.desktop %{buildroot}%{_datadir}/gnome/apps/Utilities/krb5.desktop

rm -rf RPM_BUILD_ROOT%{_datadir}/applications

%find_lang %name

#icons entries
install -m644 %{name}-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{name}-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{name}-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

#%menu entries 
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/krb5
Icon=%{name}
Categories=Network;
Name=Gnome-Kerberos
Comment=Kerberos 5 tools for GNOME
EOF

%files -f %{name}.lang
%doc README COPYING AUTHORS ChangeLog INSTALL ABOUT-NLS
%{_datadir}/gnome/apps/Utilities/krb5.desktop
%{_datadir}/pixmaps/kerberos.png
%{_datadir}/%{name}/
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_bindir}/*
