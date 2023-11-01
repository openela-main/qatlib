# SPDX-License-Identifier: MIT

%global libqat_soversion  3
%global libusdm_soversion 0
Name:             qatlib
Version:          23.02.0
Release:          2%{?dist}
Summary:          Intel QuickAssist user space library
# The entire source code is released under BSD.
# For a breakdown of inbound licenses see the INSTALL file.
License:          BSD and (BSD or GPLv2)
URL:              https://github.com/intel/%{name}
Source0:          https://github.com/intel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    systemd gcc make autoconf automake libtool systemd-devel openssl-devel zlib-devel nasm
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
* Fri Mar 03 2023 Vladis Dronov <vdronov@redhat.com> - 23.02.0-2
- Update to qatlib 23.02.0 (bz 2176873)

* Fri Jul 22 2022 Vladis Dronov <vdronov@redhat.com> - 22.07.0-1
- Update to qatlib 22.07 (bz 2040744)
- Moved qat.service to separate rpm

* Thu Nov 11 2021 Vladis Dronov <vdronov@redhat.com> - 21.11.0-1
- Update to qatlib 21.11 (bz 2012939)
- Add qatlib-tests package
- Add OSCI testing harness

* Mon Aug 16 2021 Vladis Dronov <vdronov@redhat.com> - 21.05.0-1
- Update to qatlib 21.05 with openssl-3 support (bz 1920444, bz 1953498)
- Add documentation files to a package

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 20.10.0-7
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 16 2021 Mohan Boddu <mboddu@redhat.com> - 20.10.0-6
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 20.10.0-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20.10.0-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  14 2020 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 20.10.0-2
- Add ExcludeArch i686

* Mon Nov  16 2020 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 20.10.0-1
- Update to qatlib 20.10
- Fixes to spec to address comments from Fedora review

* Mon Aug  10 2020 Mateusz Polrola <mateuszx.potrola@intel.com> - 20.08.0-1
- Initial version of the package
