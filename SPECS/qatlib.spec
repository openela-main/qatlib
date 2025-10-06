# SPDX-License-Identifier: MIT

%global libqat_soversion  4
%global libusdm_soversion 0
Name:             qatlib
Version:          24.09.0
Release:          2%{?dist}
Summary:          Intel QuickAssist user space library
# The entire source code is released under BSD.
# For a breakdown of inbound licenses see the INSTALL file.
License:          BSD-3-Clause AND ( BSD-3-Clause OR GPL-2.0-only )
URL:              https://github.com/intel/%{name}
Source0:          https://github.com/intel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    systemd gcc make autoconf automake libtool systemd-devel openssl-devel zlib-devel nasm numactl-devel
Requires(pre):    shadow-utils
Recommends:       qatlib-service
# https://bugzilla.redhat.com/show_bug.cgi?id=1897661
ExcludeArch:      %{arm} aarch64 %{power64} s390x i686

%description
Intel QuickAssist Technology (Intel QAT) provides hardware acceleration
for offloading security, authentication and compression services from the
CPU, thus significantly increasing the performance and efficiency of
standard platform solutions.

Its services include symmetric encryption and authentication,
asymmetric encryption, digital signatures, RSA, DH and ECC, and
lossless data compression.

This package provides user space libraries that allow access to
Intel QuickAssist devices and expose the Intel QuickAssist APIs.

%package       devel
Summary:       Headers and libraries to build applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
This package contains headers and libraries required to build applications
that use the Intel QuickAssist APIs.

%package       tests
Summary:       Sample applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   tests
This package contains sample applications that use the Intel QuickAssists APIs.

%package       service
Summary:       A daemon for qatlib resources management
Requires:      pciutils
Requires:      %{name}%{?_isa} = %{version}-%{release}
%{?systemd_requires}

%description   service
This package contains a daemon that manages QAT resources for the Intel
QuickAssist Technology user space library (qatlib).

%prep
%autosetup -p1

%build
autoreconf -vif
%configure --enable-legacy-algorithms
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
make DESTDIR=%{buildroot} samples-install
rm %{buildroot}/%{_libdir}/libqat.la
rm %{buildroot}/%{_libdir}/libusdm.la
rm %{buildroot}/%{_libdir}/libqat.a
rm %{buildroot}/%{_libdir}/libusdm.a

%pre
getent group qat >/dev/null || groupadd -r qat
exit 0

%post          service
%systemd_post qat.service

%preun         service
%systemd_preun qat.service

%postun        service
%systemd_postun_with_restart qat.service

%files
%doc INSTALL README.md
%license LICENSE*
%{_libdir}/libqat.so.%{libqat_soversion}*
%{_libdir}/libusdm.so.%{libusdm_soversion}*

%files         devel
%{_libdir}/libqat.so
%{_libdir}/libusdm.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/qat

%files         tests
%doc quickassist/lookaside/access_layer/src/sample_code/README.txt
%attr(0754,-,qat) %{_bindir}/cpa_sample_code
%attr(0754,-,qat) %{_bindir}/dc_dp_sample
%attr(0754,-,qat) %{_bindir}/dc_stateless_sample
%attr(0754,-,qat) %{_bindir}/chaining_sample
%attr(0754,-,qat) %{_bindir}/dc_stateless_multi_op_sample
%attr(0754,-,qat) %{_bindir}/algchaining_sample
%attr(0754,-,qat) %{_bindir}/ccm_sample
%attr(0754,-,qat) %{_bindir}/cipher_sample
%attr(0754,-,qat) %{_bindir}/gcm_sample
%attr(0754,-,qat) %{_bindir}/hash_file_sample
%attr(0754,-,qat) %{_bindir}/hash_sample
%attr(0754,-,qat) %{_bindir}/ipsec_sample
%attr(0754,-,qat) %{_bindir}/ssl_sample
%attr(0754,-,qat) %{_bindir}/sym_dp_sample
%attr(0754,-,qat) %{_bindir}/dh_sample
%attr(0754,-,qat) %{_bindir}/eddsa_sample
%attr(0754,-,qat) %{_bindir}/prime_sample
%attr(0754,-,qat) %{_bindir}/hkdf_sample
%attr(0754,-,qat) %{_bindir}/ec_montedwds_sample
%attr(0754,-,qat) %{_bindir}/zuc_sample
%{_datadir}/qat/calgary
%{_datadir}/qat/calgary32
%{_datadir}/qat/canterbury

%files         service
%{_sbindir}/qatmgr
%{_sbindir}/qat_init.sh
%{_unitdir}/qat.service
%{_mandir}/man8/qatmgr.8*
%{_mandir}/man8/qat_init.sh.8*

%changelog
* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 24.09.0-2
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Tue Oct 01 2024 Vladis Dronov <vdronov@redhat.com> - 24.09.0-1
- Update to qatlib 24.09.0 @ 36fb0903 (RHEL-40261)
- Add pciutils as a dependency of the qatlib-service subpackage
- Add numactl-devel as a dependency since it is required by qatlib-24.09.0

* Wed Jun 26 2024 Vladis Dronov <vdronov@redhat.com> - 24.02.0-3
- Fix Intel CET IBT instrumentation in assembly code (RHEL-20173)
- Update a changelog entry

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 24.02.0-2
- Bump release for June 2024 mass rebuild

* Fri Mar 22 2024 Vladis Dronov <vdronov@redhat.com> - 24.02.0-1
- Update to qatlib 24.02.0 (RHEL-20173)
- Add zuc_sample to qatlib-tests package
- Use proper SPDX license identifiers

* Fri Jan 26 2024 Vladis Dronov <vdronov@redhat.com> - 23.11.0-3
- Initial import from Fedora 40
