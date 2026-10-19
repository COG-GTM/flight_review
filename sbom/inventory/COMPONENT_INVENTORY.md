# Component inventory

Human-readable view of the CycloneDX SBOMs in `cyclonedx/`. The JSON files are authoritative; this table exists so a reviewer can skim without tooling.

| Artifact | Components | Ecosystems |
|---|---:|---|
| `flight_review-source` | 8 | github (7), pypi (1) |
| `flight_review-app-image` | 265 | deb (121), npm (18), operating-system (1), pypi (125) |
| `flight_review-nginx-image` | 154 | deb (152), maven (1), operating-system (1) |
| `flight_review-certbot-image` | 1126 | apk (36), application (14), cargo (1038), generic (1), operating-system (1), pypi (36) |
| `flight_review-browser-runtime` | 18 | npm (18) |

## flight_review-source

Git working tree: declared Python requirements, CI workflow actions, vendored npm metadata

| Ecosystem | Name | Version | License | Supplier / publisher | purl |
|---|---|---|---|---|---|
| github | actions/checkout | master | - | - | `pkg:github/actions/checkout@master` |
| github | actions/checkout | v2 | - | - | `pkg:github/actions/checkout@v2` |
| github | actions/setup-python | v2 | - | - | `pkg:github/actions/setup-python@v2` |
| github | ad-m/github-push-action | master | - | - | `pkg:github/ad-m/github-push-action@master` |
| pypi | bokeh | 3.8.2 | - | - | `pkg:pypi/bokeh@3.8.2` |

## flight_review-app-image

Tornado/Bokeh application container (ubuntu:noble + apt + pip), the primary deployable

| Ecosystem | Name | Version | License | Supplier / publisher | purl |
|---|---|---|---|---|---|
| deb | apt | 2.8.3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, Expat | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/apt@2.8.3?arch=amd64&distro=ubuntu-24.04` |
| deb | apt-utils | 2.8.3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, Expat | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/apt-utils@2.8.3?arch=amd64&distro=ubuntu-24.04&upstream=apt` |
| deb | base-files | 13ubuntu10.5 | sha256:fd7e4aae7e7b05f217bcf2d02322825c360e66c52c4c2f1b28d784d6297a1c23 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/base-files@13ubuntu10.5?arch=amd64&distro=ubuntu-24.04` |
| deb | base-passwd | 3.6.3build1 | GPL-2.0-only, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/base-passwd@3.6.3build1?arch=amd64&distro=ubuntu-24.04` |
| deb | bash | 5.2.21-2ubuntu4 | BSD-4-Clause-UC, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, Latex2e, GFDL-NIV-1.3, MIT-like, permissive | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/bash@5.2.21-2ubuntu4?arch=amd64&distro=ubuntu-24.04` |
| deb | bsdutils | 1:2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/bsdutils@1%3A2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux%402.39.3-9ubuntu6.6` |
| deb | ca-certificates | 20260601~24.04.1 | GPL-2.0-only, GPL-2.0-or-later, MPL-2.0 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/ca-certificates@20260601~24.04.1?arch=all&distro=ubuntu-24.04` |
| deb | coreutils | 9.4-3ubuntu6.3 | BSD-4-Clause-UC, FSFULLR, GFDL-1.3-only, GPL-3.0-only, GPL-3.0-or-later, ISC, GFDL-NIV-1.3 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/coreutils@9.4-3ubuntu6.3?arch=amd64&distro=ubuntu-24.04` |
| deb | dash | 0.5.12-6ubuntu5 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/dash@0.5.12-6ubuntu5?arch=amd64&distro=ubuntu-24.04` |
| deb | debconf | 1.5.86ubuntu1 | BSD-2-Clause | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/debconf@1.5.86ubuntu1?arch=all&distro=ubuntu-24.04` |
| deb | debianutils | 5.17build1 | GPL-2.0-only, GPL-2.0-or-later, SMAIL-GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/debianutils@5.17build1?arch=amd64&distro=ubuntu-24.04` |
| deb | diffutils | 1:3.10-1ubuntu0.1 | FSFAP, FSFULLR, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, X11, GFDL-NIV-1.3, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/diffutils@1%3A3.10-1ubuntu0.1?arch=amd64&distro=ubuntu-24.04` |
| deb | dpkg | 1.22.6ubuntu6.6 | GPL-2.0-only, GPL-2.0-or-later, public-domain-s-s-d | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/dpkg@1.22.6ubuntu6.6?arch=amd64&distro=ubuntu-24.04` |
| deb | e2fsprogs | 1.47.0-2.4~exp1ubuntu4.1 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, GPL | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/e2fsprogs@1.47.0-2.4~exp1ubuntu4.1?arch=amd64&distro=ubuntu-24.04` |
| deb | findutils | 4.9.0-5build1 | BSD-3-Clause, FSFAP, FSFULLR, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, X11, GFDL-NIV-1.3+, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/findutils@4.9.0-5build1?arch=amd64&distro=ubuntu-24.04` |
| deb | gcc-14-base | 14.2.0-4ubuntu2~24.04.1 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Ubuntu Core developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/gcc-14-base@14.2.0-4ubuntu2~24.04.1?arch=amd64&distro=ubuntu-24.04&upstream=gcc-14` |
| deb | gpgv | 2.4.4-2ubuntu17.6 | BSD-3-Clause, CC0-1.0, GPL-2.0-or-later, GPL-2.0-only, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Expat, RFC-Reference, TinySCHEME, permissive | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/gpgv@2.4.4-2ubuntu17.6?arch=amd64&distro=ubuntu-24.04&upstream=gnupg2` |
| deb | grep | 3.11-4build1 | GPL-3.0-only, GPL-3.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/grep@3.11-4build1?arch=amd64&distro=ubuntu-24.04` |
| deb | gzip | 1.12-1ubuntu3.2 | GPL-3.0-only, GPL-3.0-or-later, FSF-manpages, GFDL-1.3+-no-invariant, GFDL-3 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/gzip@1.12-1ubuntu3.2?arch=amd64&distro=ubuntu-24.04` |
| deb | hostname | 3.23+nmu2ubuntu2 | GPL-2.0-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/hostname@3.23%2Bnmu2ubuntu2?arch=amd64&distro=ubuntu-24.04` |
| deb | init-system-helpers | 1.66ubuntu1 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/init-system-helpers@1.66ubuntu1?arch=all&distro=ubuntu-24.04` |
| deb | libacl1 | 2.3.2-1build1.1 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-or-later, LGPL-2.1-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libacl1@2.3.2-1build1.1?arch=amd64&distro=ubuntu-24.04&upstream=acl` |
| deb | libapt-pkg6.0t64 | 2.8.3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, Expat | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libapt-pkg6.0t64@2.8.3?arch=amd64&distro=ubuntu-24.04&upstream=apt` |
| deb | libassuan0 | 2.5.6-1build1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, GAP, GAP~FSF | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libassuan0@2.5.6-1build1?arch=amd64&distro=ubuntu-24.04&upstream=libassuan` |
| deb | libattr1 | 1:2.5.2-1ubuntu0.1 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-or-later, LGPL-2.1-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libattr1@1%3A2.5.2-1ubuntu0.1?arch=amd64&distro=ubuntu-24.04&upstream=attr` |
| deb | libaudit-common | 1:3.1.2-2.1ubuntu0.1 | GPL-1.0-only, GPL-2.0-only, LGPL-2.1-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libaudit-common@1%3A3.1.2-2.1ubuntu0.1?arch=all&distro=ubuntu-24.04&upstream=audit` |
| deb | libaudit1 | 1:3.1.2-2.1ubuntu0.1 | GPL-1.0-only, GPL-2.0-only, LGPL-2.1-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libaudit1@1%3A3.1.2-2.1ubuntu0.1?arch=amd64&distro=ubuntu-24.04&upstream=audit` |
| deb | libblkid1 | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libblkid1@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux` |
| deb | libbz2-1.0 | 1.0.8-5.1ubuntu0.1 | GPL-2.0-only, BSD-variant | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libbz2-1.0@1.0.8-5.1ubuntu0.1?arch=amd64&distro=ubuntu-24.04&upstream=bzip2` |
| deb | libc-bin | 2.39-0ubuntu8.9 | sha256:d3c95b56fa33e28b57860580f0baf4e4f4de2a268a2b80f1d031a5191bade265 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libc-bin@2.39-0ubuntu8.9?arch=amd64&distro=ubuntu-24.04&upstream=glibc` |
| deb | libc6 | 2.39-0ubuntu8.9 | sha256:d3c95b56fa33e28b57860580f0baf4e4f4de2a268a2b80f1d031a5191bade265 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libc6@2.39-0ubuntu8.9?arch=amd64&distro=ubuntu-24.04&upstream=glibc` |
| deb | libcap-ng0 | 0.8.4-2build2 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libcap-ng0@0.8.4-2build2?arch=amd64&distro=ubuntu-24.04&upstream=libcap-ng` |
| deb | libcap2 | 1:2.66-5ubuntu2.4 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libcap2@1%3A2.66-5ubuntu2.4?arch=amd64&distro=ubuntu-24.04` |
| deb | libcom-err2 | 1.47.0-2.4~exp1ubuntu4.1 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, GPL | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libcom-err2@1.47.0-2.4~exp1ubuntu4.1?arch=amd64&distro=ubuntu-24.04&upstream=e2fsprogs` |
| deb | libcrypt1 | 1:4.4.36-4build1 | sha256:5a5e7ca0e9f3f9679977e3a3e9ede45ad92885a3297ea78e766979f9866c5a16 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libcrypt1@1%3A4.4.36-4build1?arch=amd64&distro=ubuntu-24.04&upstream=libxcrypt` |
| deb | libdb5.3t64 | 5.3.28+dfsg2-7 | BSD-3-Clause, GPL-3.0-only, MS-PL, Sleepycat, X11, Zlib, Artistic, BSD-3-clause-fjord, GPL, MIT-old, TCL-like | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libdb5.3t64@5.3.28%2Bdfsg2-7?arch=amd64&distro=ubuntu-24.04&upstream=db5.3` |
| deb | libdebconfclient0 | 0.271ubuntu3 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libdebconfclient0@0.271ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=cdebconf` |
| deb | libexpat1 | 2.6.1-2ubuntu0.6 | MIT | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libexpat1@2.6.1-2ubuntu0.6?arch=amd64&distro=ubuntu-24.04&upstream=expat` |
| deb | libext2fs2t64 | 1.47.0-2.4~exp1ubuntu4.1 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, GPL | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libext2fs2t64@1.47.0-2.4~exp1ubuntu4.1?arch=amd64&distro=ubuntu-24.04&upstream=e2fsprogs` |
| deb | libffi8 | 3.4.6-1build1 | GPL-2.0-or-later, GPL-3.0-or-later, MPL-1.1, X11, Expat, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libffi8@3.4.6-1build1?arch=amd64&distro=ubuntu-24.04&upstream=libffi` |
| deb | libfftw3-bin | 3.3.10-1ubuntu3 | GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libfftw3-bin@3.3.10-1ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=fftw3` |
| deb | libfftw3-double3 | 3.3.10-1ubuntu3 | GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libfftw3-double3@3.3.10-1ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=fftw3` |
| deb | libfftw3-long3 | 3.3.10-1ubuntu3 | GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libfftw3-long3@3.3.10-1ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=fftw3` |
| deb | libfftw3-quad3 | 3.3.10-1ubuntu3 | GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libfftw3-quad3@3.3.10-1ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=fftw3` |
| deb | libfftw3-single3 | 3.3.10-1ubuntu3 | GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libfftw3-single3@3.3.10-1ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=fftw3` |
| deb | libgcc-s1 | 14.2.0-4ubuntu2~24.04.1 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Ubuntu Core developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgcc-s1@14.2.0-4ubuntu2~24.04.1?arch=amd64&distro=ubuntu-24.04&upstream=gcc-14` |
| deb | libgcrypt20 | 1.10.3-2ubuntu0.2 | sha256:40162167dff80843a4b24aa8d0a4ffc50be5338d004ebe38f86ae3397ba9de3e | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgcrypt20@1.10.3-2ubuntu0.2?arch=amd64&distro=ubuntu-24.04` |
| deb | libgmp10 | 2:6.3.0+dfsg-2ubuntu6.1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgmp10@2%3A6.3.0%2Bdfsg-2ubuntu6.1?arch=amd64&distro=ubuntu-24.04&upstream=gmp` |
| deb | libgnutls30t64 | 3.8.3-1.1ubuntu3.6 | sha256:51da5214308b87d6a0a2fbcaea1f7dbd15510be733e5921d9548ff6b88d84dd8 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgnutls30t64@3.8.3-1.1ubuntu3.6?arch=amd64&distro=ubuntu-24.04&upstream=gnutls28` |
| deb | libgomp1 | 14.2.0-4ubuntu2~24.04.1 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Ubuntu Core developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgomp1@14.2.0-4ubuntu2~24.04.1?arch=amd64&distro=ubuntu-24.04&upstream=gcc-14` |
| deb | libgpg-error0 | 1.47-3build2.1 | BSD-3-Clause, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, g10-permissive | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libgpg-error0@1.47-3build2.1?arch=amd64&distro=ubuntu-24.04&upstream=libgpg-error` |
| deb | libhogweed6t64 | 3.9.1-2.2build1.1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-3.0-or-later, Expat, GAP, GPL, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libhogweed6t64@3.9.1-2.2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=nettle` |
| deb | libidn2-0 | 2.3.7-2build1.1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Unicode | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libidn2-0@2.3.7-2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=libidn2` |
| deb | liblz4-1 | 1.9.4-1build1.1 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/liblz4-1@1.9.4-1build1.1?arch=amd64&distro=ubuntu-24.04&upstream=lz4` |
| deb | liblzma5 | 5.6.1+really5.4.5-1ubuntu0.3 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.0-only, LGPL-2.1-only, LGPL-2.1-or-later, Autoconf, PD, PD-debian, config-h, noderivs, permissive-fsf, permissive-nowarranty, probably-PD | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/liblzma5@5.6.1%2Breally5.4.5-1ubuntu0.3?arch=amd64&distro=ubuntu-24.04&upstream=xz-utils` |
| deb | libmd0 | 1.1.0-2build1.1 | BSD-2-Clause, BSD-3-Clause, Beerware, ISC, BSD-3-clause-Aaron-D-Gifford, public-domain-md4, public-domain-md5, public-domain-sha1 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libmd0@1.1.0-2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=libmd` |
| deb | libmount1 | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libmount1@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux` |
| deb | libncursesw6 | 6.4+20240113-1ubuntu2.2 | BSD-3-Clause, X11, MIT/X11 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libncursesw6@6.4%2B20240113-1ubuntu2.2?arch=amd64&distro=ubuntu-24.04&upstream=ncurses` |
| deb | libnettle8t64 | 3.9.1-2.2build1.1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-3.0-or-later, Expat, GAP, GPL, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libnettle8t64@3.9.1-2.2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=nettle` |
| deb | libnpth0t64 | 1.6-3.1build1 | LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libnpth0t64@1.6-3.1build1?arch=amd64&distro=ubuntu-24.04&upstream=npth` |
| deb | libp11-kit0 | 0.25.3-4ubuntu2.2 | Apache-2.0, BSD-3-Clause, FSFAP, FSFULLR, GPL-2.0-or-later, GPL-3.0-or-later, ISC, LGPL-2.1-only, LGPL-2.1-or-later, X11, customFSFUL, customFSFULLRWD | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libp11-kit0@0.25.3-4ubuntu2.2?arch=amd64&distro=ubuntu-24.04&upstream=p11-kit` |
| deb | libpam-modules | 1.5.3-5ubuntu5.7 | BSD-3-Clause, Beerware, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpam-modules@1.5.3-5ubuntu5.7?arch=amd64&distro=ubuntu-24.04&upstream=pam` |
| deb | libpam-modules-bin | 1.5.3-5ubuntu5.7 | BSD-3-Clause, Beerware, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpam-modules-bin@1.5.3-5ubuntu5.7?arch=amd64&distro=ubuntu-24.04&upstream=pam` |
| deb | libpam-runtime | 1.5.3-5ubuntu5.7 | BSD-3-Clause, Beerware, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpam-runtime@1.5.3-5ubuntu5.7?arch=all&distro=ubuntu-24.04&upstream=pam` |
| deb | libpam0g | 1.5.3-5ubuntu5.7 | BSD-3-Clause, Beerware, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, GPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpam0g@1.5.3-5ubuntu5.7?arch=amd64&distro=ubuntu-24.04&upstream=pam` |
| deb | libpcre2-8-0 | 10.42-4ubuntu2.1 | BSD-2-Clause, BSD-3-Clause, X11, BSD-3-clause-Cambridge, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpcre2-8-0@10.42-4ubuntu2.1?arch=amd64&distro=ubuntu-24.04&upstream=pcre2` |
| deb | libproc2-0 | 2:4.0.4-4ubuntu3.3 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libproc2-0@2%3A4.0.4-4ubuntu3.3?arch=amd64&distro=ubuntu-24.04&upstream=procps` |
| deb | libpython3-stdlib | 3.12.3-0ubuntu2.1 | sha256:5b274dbb44b28a54b795b9471c07ab045054d6b8a86273cb9feb632b6fd2760d | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpython3-stdlib@3.12.3-0ubuntu2.1?arch=amd64&distro=ubuntu-24.04&upstream=python3-defaults` |
| deb | libpython3.12-minimal | 3.12.3-1ubuntu0.17 | sha256:f1cbf908e1daa8789b389fdcf17811ed36b675d736b39a103591399861350382 | Ubuntu Core Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpython3.12-minimal@3.12.3-1ubuntu0.17?arch=amd64&distro=ubuntu-24.04&upstream=python3.12` |
| deb | libpython3.12-stdlib | 3.12.3-1ubuntu0.17 | sha256:f1cbf908e1daa8789b389fdcf17811ed36b675d736b39a103591399861350382 | Ubuntu Core Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libpython3.12-stdlib@3.12.3-1ubuntu0.17?arch=amd64&distro=ubuntu-24.04&upstream=python3.12` |
| deb | libquadmath0 | 14.2.0-4ubuntu2~24.04.1 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Ubuntu Core developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libquadmath0@14.2.0-4ubuntu2~24.04.1?arch=amd64&distro=ubuntu-24.04&upstream=gcc-14` |
| deb | libreadline8t64 | 8.2-4build1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, GFDL, GFDL-NIV-1.3+, ISC-no-attribution | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libreadline8t64@8.2-4build1?arch=amd64&distro=ubuntu-24.04&upstream=readline` |
| deb | libseccomp2 | 2.5.5-1ubuntu3.1 | LGPL-2.1-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libseccomp2@2.5.5-1ubuntu3.1?arch=amd64&distro=ubuntu-24.04&upstream=libseccomp` |
| deb | libselinux1 | 3.5-2ubuntu2.1 | GPL-2.0-only, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libselinux1@3.5-2ubuntu2.1?arch=amd64&distro=ubuntu-24.04&upstream=libselinux` |
| deb | libsemanage-common | 3.5-1build5 | GPL-2.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsemanage-common@3.5-1build5?arch=all&distro=ubuntu-24.04&upstream=libsemanage` |
| deb | libsemanage2 | 3.5-1build5 | GPL-2.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsemanage2@3.5-1build5?arch=amd64&distro=ubuntu-24.04&upstream=libsemanage` |
| deb | libsepol2 | 3.5-2build1 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Zlib | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsepol2@3.5-2build1?arch=amd64&distro=ubuntu-24.04&upstream=libsepol` |
| deb | libsmartcols1 | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsmartcols1@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux` |
| deb | libsqlite3-0 | 3.45.1-1ubuntu2.8 | GPL-2.0-only, GPL-2.0-or-later, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsqlite3-0@3.45.1-1ubuntu2.8?arch=amd64&distro=ubuntu-24.04&upstream=sqlite3` |
| deb | libss2 | 1.47.0-2.4~exp1ubuntu4.1 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, GPL | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libss2@1.47.0-2.4~exp1ubuntu4.1?arch=amd64&distro=ubuntu-24.04&upstream=e2fsprogs` |
| deb | libssl3t64 | 3.0.13-0ubuntu3.16 | Apache-2.0, GPL-1.0-only, GPL-1.0-or-later, Artistic | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libssl3t64@3.0.13-0ubuntu3.16?arch=amd64&distro=ubuntu-24.04&upstream=openssl` |
| deb | libstdc++6 | 14.2.0-4ubuntu2~24.04.1 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Ubuntu Core developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libstdc%2B%2B6@14.2.0-4ubuntu2~24.04.1?arch=amd64&distro=ubuntu-24.04&upstream=gcc-14` |
| deb | libsystemd0 | 255.4-1ubuntu8.17 | CC0-1.0, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Expat, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libsystemd0@255.4-1ubuntu8.17?arch=amd64&distro=ubuntu-24.04&upstream=systemd` |
| deb | libtasn1-6 | 4.19.0-3ubuntu0.24.04.2 | sha256:572ad60ad184d8f52c6dc66d83a61a68f137db560b3452ce00588c9ecf128a65 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libtasn1-6@4.19.0-3ubuntu0.24.04.2?arch=amd64&distro=ubuntu-24.04` |
| deb | libtinfo6 | 6.4+20240113-1ubuntu2.2 | BSD-3-Clause, X11, MIT/X11 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libtinfo6@6.4%2B20240113-1ubuntu2.2?arch=amd64&distro=ubuntu-24.04&upstream=ncurses` |
| deb | libudev1 | 255.4-1ubuntu8.17 | CC0-1.0, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Expat, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libudev1@255.4-1ubuntu8.17?arch=amd64&distro=ubuntu-24.04&upstream=systemd` |
| deb | libunistring5 | 1.1-2build1.1 | GFDL-1.2-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, X11, FreeSoftware, GFDL-NIV-1.2+ | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libunistring5@1.1-2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=libunistring` |
| deb | libuuid1 | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libuuid1@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux` |
| deb | libxxhash0 | 0.8.2-2build1 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libxxhash0@0.8.2-2build1?arch=amd64&distro=ubuntu-24.04&upstream=xxhash` |
| deb | libzstd1 | 1.5.5+dfsg2-2build1.1 | BSD-3-Clause, GPL-2.0-only, Zlib, Expat | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/libzstd1@1.5.5%2Bdfsg2-2build1.1?arch=amd64&distro=ubuntu-24.04&upstream=libzstd` |
| deb | login | 1:4.13+dfsg1-4ubuntu3.2 | BSD-3-Clause, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/login@1%3A4.13%2Bdfsg1-4ubuntu3.2?arch=amd64&distro=ubuntu-24.04&upstream=shadow` |
| deb | logsave | 1.47.0-2.4~exp1ubuntu4.1 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, GPL | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/logsave@1.47.0-2.4~exp1ubuntu4.1?arch=amd64&distro=ubuntu-24.04&upstream=e2fsprogs` |
| deb | mawk | 1.3.4.20240123-1build1 | CC-BY-3.0, GPL-2.0-only, X11 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/mawk@1.3.4.20240123-1build1?arch=amd64&distro=ubuntu-24.04` |
| deb | media-types | 10.1.0 | ad-hoc | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/media-types@10.1.0?arch=all&distro=ubuntu-24.04` |
| deb | mount | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/mount@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04&upstream=util-linux` |
| deb | ncurses-base | 6.4+20240113-1ubuntu2.2 | BSD-3-Clause, X11, MIT/X11 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/ncurses-base@6.4%2B20240113-1ubuntu2.2?arch=all&distro=ubuntu-24.04&upstream=ncurses` |
| deb | ncurses-bin | 6.4+20240113-1ubuntu2.2 | BSD-3-Clause, X11, MIT/X11 | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/ncurses-bin@6.4%2B20240113-1ubuntu2.2?arch=amd64&distro=ubuntu-24.04&upstream=ncurses` |
| deb | netbase | 6.4 | GPL-2.0-only | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/netbase@6.4?arch=all&distro=ubuntu-24.04` |
| deb | openssl | 3.0.13-0ubuntu3.16 | Apache-2.0, GPL-1.0-only, GPL-1.0-or-later, Artistic | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/openssl@3.0.13-0ubuntu3.16?arch=amd64&distro=ubuntu-24.04` |
| deb | passwd | 1:4.13+dfsg1-4ubuntu3.2 | BSD-3-Clause, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/passwd@1%3A4.13%2Bdfsg1-4ubuntu3.2?arch=amd64&distro=ubuntu-24.04&upstream=shadow` |
| deb | perl-base | 5.38.2-3.2ubuntu0.6 | Artistic-2.0, Artistic-dist, BSD-3-Clause, FSFAP, GPL-1.0-only, GPL-1.0-or-later, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, Zlib, Artistic, BSD-3-clause-GENERIC, BSD-3-clause-with-weird-numbering, BSD-4-clause-POWERDOG, BZIP, DONT-CHANGE-THE-GPL, Expat, GPL-3+-WITH-BISON-EXCEPTION, REGCOMP, REGCOMP,, SDBM-PUBLIC-DOMAIN, TEXT-TABS, Unicode | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/perl-base@5.38.2-3.2ubuntu0.6?arch=amd64&distro=ubuntu-24.04&upstream=perl` |
| deb | procps | 2:4.0.4-4ubuntu3.3 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/procps@2%3A4.0.4-4ubuntu3.3?arch=amd64&distro=ubuntu-24.04` |
| deb | python3 | 3.12.3-0ubuntu2.1 | sha256:5b274dbb44b28a54b795b9471c07ab045054d6b8a86273cb9feb632b6fd2760d | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3@3.12.3-0ubuntu2.1?arch=amd64&distro=ubuntu-24.04&upstream=python3-defaults` |
| deb | python3-minimal | 3.12.3-0ubuntu2.1 | sha256:5b274dbb44b28a54b795b9471c07ab045054d6b8a86273cb9feb632b6fd2760d | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3-minimal@3.12.3-0ubuntu2.1?arch=amd64&distro=ubuntu-24.04&upstream=python3-defaults` |
| deb | python3-pip | 24.0+dfsg-1ubuntu1.3 | Apache-2.0, ISC, LGPL-2.1-only, LGPL-2.1-or-later, MPL-2.0, BSD-2, BSD-3, Expat, Python | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3-pip@24.0%2Bdfsg-1ubuntu1.3?arch=all&distro=ubuntu-24.04&upstream=python-pip` |
| deb | python3-pkg-resources | 68.1.2-2ubuntu1.2 | Apache-2.0, BSD-3-Clause, MIT | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3-pkg-resources@68.1.2-2ubuntu1.2?arch=all&distro=ubuntu-24.04&upstream=setuptools` |
| deb | python3-setuptools | 68.1.2-2ubuntu1.2 | Apache-2.0, BSD-3-Clause, MIT | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3-setuptools@68.1.2-2ubuntu1.2?arch=all&distro=ubuntu-24.04&upstream=setuptools` |
| deb | python3-wheel | 0.42.0-2 | Apache-2.0, BSD-2-Clause, GPL-3.0-only, Expat | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3-wheel@0.42.0-2?arch=all&distro=ubuntu-24.04&upstream=wheel` |
| deb | python3.12 | 3.12.3-1ubuntu0.17 | sha256:f1cbf908e1daa8789b389fdcf17811ed36b675d736b39a103591399861350382 | Ubuntu Core Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3.12@3.12.3-1ubuntu0.17?arch=amd64&distro=ubuntu-24.04` |
| deb | python3.12-minimal | 3.12.3-1ubuntu0.17 | sha256:f1cbf908e1daa8789b389fdcf17811ed36b675d736b39a103591399861350382 | Ubuntu Core Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/python3.12-minimal@3.12.3-1ubuntu0.17?arch=amd64&distro=ubuntu-24.04&upstream=python3.12` |
| deb | readline-common | 8.2-4build1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, GFDL, GFDL-NIV-1.3+, ISC-no-attribution | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/readline-common@8.2-4build1?arch=all&distro=ubuntu-24.04&upstream=readline` |
| deb | sed | 4.9-2ubuntu0.24.04.1 | BSD-4-Clause-UC, BSL-1.0, GFDL-1.3-only, GPL-3.0-only, GPL-3.0-or-later, ISC, X11, GFDL-NIV-1.3+, pcre | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/sed@4.9-2ubuntu0.24.04.1?arch=amd64&distro=ubuntu-24.04` |
| deb | sensible-utils | 0.0.22 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later, All-permissive, configure, installsh | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/sensible-utils@0.0.22?arch=all&distro=ubuntu-24.04` |
| deb | sqlite3 | 3.45.1-1ubuntu2.8 | GPL-2.0-only, GPL-2.0-or-later, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/sqlite3@3.45.1-1ubuntu2.8?arch=amd64&distro=ubuntu-24.04` |
| deb | sysvinit-utils | 3.08-6ubuntu3 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/sysvinit-utils@3.08-6ubuntu3?arch=amd64&distro=ubuntu-24.04&upstream=sysvinit` |
| deb | tar | 1.35+dfsg-3ubuntu0.4 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/tar@1.35%2Bdfsg-3ubuntu0.4?arch=amd64&distro=ubuntu-24.04` |
| deb | tzdata | 2026e-0ubuntu0.24.04.1 | ICU, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/tzdata@2026e-0ubuntu0.24.04.1?arch=all&distro=ubuntu-24.04` |
| deb | ubuntu-keyring | 2023.11.28.1 | sha256:191cdb1291b2fc3b9fdcd8648b16ab7f9e4f15b74dc5b30959a9fdcfb4782b6c | Dimitri John Ledkov <dimitri.ledkov@canonical.com> | `pkg:deb/ubuntu/ubuntu-keyring@2023.11.28.1?arch=all&distro=ubuntu-24.04` |
| deb | unminimize | 0.2.1 | GPL-2.0-only, GPL-2.0-or-later | Utkarsh Gupta <utkarsh@ubuntu.com> | `pkg:deb/ubuntu/unminimize@0.2.1?arch=amd64&distro=ubuntu-24.04` |
| deb | util-linux | 2.39.3-9ubuntu6.6 | BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, MIT, BSLA, LGPL, public-domain | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/util-linux@2.39.3-9ubuntu6.6?arch=amd64&distro=ubuntu-24.04` |
| deb | zlib1g | 1:1.3.dfsg-3.1ubuntu2.2 | Zlib | Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com> | `pkg:deb/ubuntu/zlib1g@1%3A1.3.dfsg-3.1ubuntu2.2?arch=amd64&distro=ubuntu-24.04&upstream=zlib` |
| npm | @jupyter-notebook/lab-extension | 7.6.3 | BSD-3-Clause | - | `pkg:npm/%40jupyter-notebook/lab-extension@7.6.3` |
| npm | @jupyter-widgets/jupyterlab-manager | 5.0.16 | BSD-3-Clause | - | `pkg:npm/%40jupyter-widgets/jupyterlab-manager@5.0.16` |
| npm | @jupyterlab/application-top | 4.6.4 | BSD-3-Clause | - | `pkg:npm/%40jupyterlab/application-top@4.6.4` |
| npm | @jupyterlab/galata-extension | 5.6.3 | BSD-3-Clause | - | `pkg:npm/%40jupyterlab/galata-extension@5.6.3` |
| npm | @jupyterlab/mock-consumer | 4.6.4 | - | - | `pkg:npm/%40jupyterlab/mock-consumer@4.6.4` |
| npm | @jupyterlab/mock-extension | 4.6.4 | - | - | `pkg:npm/%40jupyterlab/mock-extension@4.6.4` |
| npm | @jupyterlab/mock-incompat | 0.1.0 | - | - | `pkg:npm/%40jupyterlab/mock-incompat@0.1.0` |
| npm | @jupyterlab/mock-mime-extension | 0.3.0 | - | - | `pkg:npm/%40jupyterlab/mock-mime-extension@0.3.0` |
| npm | @jupyterlab/mock-package | 0.1.0 | - | - | `pkg:npm/%40jupyterlab/mock-package@0.1.0` |
| npm | @jupyterlab/mock-provider | 4.6.4 | - | - | `pkg:npm/%40jupyterlab/mock-provider@4.6.4` |
| npm | @jupyterlab/mock-service-manager-extension | 4.6.4 | - | - | `pkg:npm/%40jupyterlab/mock-service-manager-extension@4.6.4` |
| npm | @jupyterlab/mock-token | 4.6.4 | - | - | `pkg:npm/%40jupyterlab/mock-token@4.6.4` |
| npm | jupyterlab_pygments | 0.3.0 | BSD-3-Clause | - | `pkg:npm/jupyterlab_pygments@0.3.0` |
| npm | test-hyphens | 3.0.2 | - | - | `pkg:npm/test-hyphens@3.0.2` |
| npm | test-hyphens-underscore | 3.0.2 | - | - | `pkg:npm/test-hyphens-underscore@3.0.2` |
| npm | test_no_hyphens | 3.0.2 | - | - | `pkg:npm/test_no_hyphens@3.0.2` |
| operating-system | ubuntu | 24.04 | - | - | `-` |
| pypi | anyio | 4.15.1 | MIT | - | `pkg:pypi/anyio@4.15.1` |
| pypi | argon2-cffi | 25.1.0 | MIT | - | `pkg:pypi/argon2-cffi@25.1.0` |
| pypi | argon2-cffi-bindings | 26.1.0 | MIT | - | `pkg:pypi/argon2-cffi-bindings@26.1.0` |
| pypi | arrow | 1.4.0 | - | - | `pkg:pypi/arrow@1.4.0` |
| pypi | astroid | 4.3.4 | LGPL-2.1-or-later | - | `pkg:pypi/astroid@4.3.4` |
| pypi | asttokens | 3.0.2 | Apache 2.0 | - | `pkg:pypi/asttokens@3.0.2` |
| pypi | async-lru | 2.4.0 | MIT License | - | `pkg:pypi/async-lru@2.4.0` |
| pypi | attrs | 26.1.0 | MIT | - | `pkg:pypi/attrs@26.1.0` |
| pypi | babel | 2.18.0 | BSD-3-Clause | - | `pkg:pypi/babel@2.18.0` |
| pypi | beautifulsoup4 | 4.15.0 | MIT License | - | `pkg:pypi/beautifulsoup4@4.15.0` |
| pypi | bleach | 6.4.0 | Apache Software License | - | `pkg:pypi/bleach@6.4.0` |
| pypi | bokeh | 3.8.2 | BSD-3-Clause | - | `pkg:pypi/bokeh@3.8.2` |
| pypi | certifi | 2026.10.18 | MPL-2.0 | - | `pkg:pypi/certifi@2026.10.18` |
| pypi | cffi | 2.1.1 | MIT-0 | - | `pkg:pypi/cffi@2.1.1` |
| pypi | charset-normalizer | 3.5.2 | MIT | - | `pkg:pypi/charset-normalizer@3.5.2` |
| pypi | comm | 0.2.3 | BSD-3-Clause | - | `pkg:pypi/comm@0.2.3` |
| pypi | contourpy | 1.4.0 | BSD-3-Clause | - | `pkg:pypi/contourpy@1.4.0` |
| pypi | cycler | 0.12.1 | BSD-3-Clause | - | `pkg:pypi/cycler@0.12.1` |
| pypi | debugpy | 1.8.22 | MIT | - | `pkg:pypi/debugpy@1.8.22` |
| pypi | defusedxml | 0.7.1 | PSFL | - | `pkg:pypi/defusedxml@0.7.1` |
| pypi | dill | 0.4.1 | BSD-3-Clause | - | `pkg:pypi/dill@0.4.1` |
| pypi | executing | 2.3.0 | MIT | - | `pkg:pypi/executing@2.3.0` |
| pypi | fastjsonschema | 2.22.2 | BSD-3-Clause | - | `pkg:pypi/fastjsonschema@2.22.2` |
| pypi | fonttools | 4.67.0 | MIT | - | `pkg:pypi/fonttools@4.67.0` |
| pypi | fqdn | 1.6.0 | MPL-2.0 | - | `pkg:pypi/fqdn@1.6.0` |
| pypi | h11 | 0.16.0 | MIT | - | `pkg:pypi/h11@0.16.0` |
| pypi | html5lib | 1.1 | MIT License | - | `pkg:pypi/html5lib@1.1` |
| pypi | httpcore | 1.0.9 | BSD-3-Clause | - | `pkg:pypi/httpcore@1.0.9` |
| pypi | httpx | 0.28.1 | BSD-3-Clause | - | `pkg:pypi/httpx@0.28.1` |
| pypi | idna | 3.20 | BSD-3-Clause | - | `pkg:pypi/idna@3.20` |
| pypi | ipykernel | 7.4.0 | BSD-3-Clause | - | `pkg:pypi/ipykernel@7.4.0` |
| pypi | ipython | 9.17.1 | BSD-3-Clause | - | `pkg:pypi/ipython@9.17.1` |
| pypi | ipython-pygments-lexers | 1.1.1 | BSD-3-Clause | - | `pkg:pypi/ipython-pygments-lexers@1.1.1` |
| pypi | ipywidgets | 8.1.9 | BSD 3-Clause License | - | `pkg:pypi/ipywidgets@8.1.9` |
| pypi | isoduration | 20.11.0 | UNKNOWN | - | `pkg:pypi/isoduration@20.11.0` |
| pypi | isort | 9.0.2 | MIT | - | `pkg:pypi/isort@9.0.2` |
| pypi | jedi | 0.20.1 | MIT | - | `pkg:pypi/jedi@0.20.1` |
| pypi | jinja2 | 3.1.6 | - | - | `pkg:pypi/jinja2@3.1.6` |
| pypi | json5 | 0.17.3 | Apache-2.0 | - | `pkg:pypi/json5@0.17.3` |
| pypi | jsonpointer | 3.4 | Modified BSD License | - | `pkg:pypi/jsonpointer@3.4` |
| pypi | jsonschema | 4.26.0 | MIT | - | `pkg:pypi/jsonschema@4.26.0` |
| pypi | jsonschema-specifications | 2025.9.1 | MIT | - | `pkg:pypi/jsonschema-specifications@2025.9.1` |
| pypi | jupyter | 1.1.1 | BSD | - | `pkg:pypi/jupyter@1.1.1` |
| pypi | jupyter-builder | 1.2.3 | Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT | - | `pkg:pypi/jupyter-builder@1.2.3` |
| pypi | jupyter-client | 8.10.0 | BSD-3-Clause | - | `pkg:pypi/jupyter-client@8.10.0` |
| pypi | jupyter-console | 6.6.3 | BSD-3-Clause | - | `pkg:pypi/jupyter-console@6.6.3` |
| pypi | jupyter-core | 5.9.1 | BSD-3-Clause | - | `pkg:pypi/jupyter-core@5.9.1` |
| pypi | jupyter-events | 0.12.1 | BSD-3-Clause | - | `pkg:pypi/jupyter-events@0.12.1` |
| pypi | jupyter-lsp | 2.3.1 | BSD-3-Clause | - | `pkg:pypi/jupyter-lsp@2.3.1` |
| pypi | jupyter-server | 2.21.1 | BSD-3-Clause | - | `pkg:pypi/jupyter-server@2.21.1` |
| pypi | jupyter-server-terminals | 0.5.4 | sha256:2f1df1e6b58c0673787203ad4c5cedfe326927ac7e82574c5d9ea74f6f9805f4 | - | `pkg:pypi/jupyter-server-terminals@0.5.4` |
| pypi | jupyterlab | 4.6.4 | BSD-3-Clause | - | `pkg:pypi/jupyterlab@4.6.4` |
| pypi | jupyterlab-pygments | 0.3.0 | BSD-3-Clause | - | `pkg:pypi/jupyterlab-pygments@0.3.0` |
| pypi | jupyterlab-server | 2.28.1 | BSD-3-Clause | - | `pkg:pypi/jupyterlab-server@2.28.1` |
| pypi | jupyterlab-widgets | 3.0.17 | BSD-3-Clause | - | `pkg:pypi/jupyterlab-widgets@3.0.17` |
| pypi | kiwisolver | 1.5.1 | sha256:4e89b2eeb82ea10ec61119c814f2ca0bbccdc22b72d0eb4f5542ef08f6a73ed2 | - | `pkg:pypi/kiwisolver@1.5.1` |
| pypi | lark | 1.3.1 | MIT | - | `pkg:pypi/lark@1.3.1` |
| pypi | markupsafe | 3.0.4 | BSD-3-Clause | - | `pkg:pypi/markupsafe@3.0.4` |
| pypi | matplotlib | 3.11.2 | sha256:3596f4f7d52f77bb4ae3b2b11fe14abbae564b43b566f64ea452c46a248b1157 | - | `pkg:pypi/matplotlib@3.11.2` |
| pypi | matplotlib-inline | 0.2.2 | BSD-3-Clause | - | `pkg:pypi/matplotlib-inline@0.2.2` |
| pypi | mccabe | 0.7.0 | Expat license | - | `pkg:pypi/mccabe@0.7.0` |
| pypi | mistune | 3.4.0 | BSD-3-Clause | - | `pkg:pypi/mistune@3.4.0` |
| pypi | mypy-extensions | 1.1.0 | MIT | - | `pkg:pypi/mypy-extensions@1.1.0` |
| pypi | narwhals | 2.27.1 | MIT | - | `pkg:pypi/narwhals@2.27.1` |
| pypi | nbclient | 0.11.0 | BSD-3-Clause | - | `pkg:pypi/nbclient@0.11.0` |
| pypi | nbconvert | 7.17.2 | BSD-3-Clause | - | `pkg:pypi/nbconvert@7.17.2` |
| pypi | nbformat | 5.11.1 | BSD-3-Clause | - | `pkg:pypi/nbformat@5.11.1` |
| pypi | nest-asyncio2 | 1.7.4 | BSD | - | `pkg:pypi/nest-asyncio2@1.7.4` |
| pypi | notebook | 7.6.3 | BSD-3-Clause | - | `pkg:pypi/notebook@7.6.3` |
| pypi | notebook-shim | 0.2.4 | BSD-3-Clause | - | `pkg:pypi/notebook-shim@0.2.4` |
| pypi | numpy | 2.5.4 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | - | `pkg:pypi/numpy@2.5.4` |
| pypi | packaging | 26.3 | Apache-2.0 OR BSD-2-Clause | - | `pkg:pypi/packaging@26.3` |
| pypi | pandas | 3.0.6 | sha256:6dc1ad62d707e8dda646a5461c66fff8e6497c8656e04ccee9a64d411b017d65 | - | `pkg:pypi/pandas@3.0.6` |
| pypi | pandocfilters | 1.5.1 | BSD-3-Clause | - | `pkg:pypi/pandocfilters@1.5.1` |
| pypi | parso | 0.8.7 | MIT | - | `pkg:pypi/parso@0.8.7` |
| pypi | pexpect | 4.9.0 | ISC license | - | `pkg:pypi/pexpect@4.9.0` |
| pypi | pillow | 13.0.0 | MIT-CMU | - | `pkg:pypi/pillow@13.0.0` |
| pypi | pip | 24.0 | MIT | - | `pkg:pypi/pip@24.0` |
| pypi | platformdirs | 4.13.5 | MIT | - | `pkg:pypi/platformdirs@4.13.5` |
| pypi | prometheus-client | 0.26.0 | Apache-2.0 AND BSD-2-Clause | - | `pkg:pypi/prometheus-client@0.26.0` |
| pypi | prompt-toolkit | 3.0.53 | - | - | `pkg:pypi/prompt-toolkit@3.0.53` |
| pypi | psutil | 7.2.2 | BSD-3-Clause | - | `pkg:pypi/psutil@7.2.2` |
| pypi | ptyprocess | 0.7.0 | UNKNOWN | - | `pkg:pypi/ptyprocess@0.7.0` |
| pypi | pure-eval | 0.2.4 | MIT | - | `pkg:pypi/pure-eval@0.2.4` |
| pypi | pycparser | 3.11 | BSD-3-Clause | - | `pkg:pypi/pycparser@3.11` |
| pypi | pycryptodome | 4.1.0 | BSD-2-Clause AND Unlicense AND MIT | - | `pkg:pypi/pycryptodome@4.1.0` |
| pypi | pyfftw | 0.15.1 | BSD-3-Clause | - | `pkg:pypi/pyfftw@0.15.1` |
| pypi | pygments | 2.21.0 | BSD-2-Clause | - | `pkg:pypi/pygments@2.21.0` |
| pypi | pylint | 4.1.3 | GPL-2.0-or-later | - | `pkg:pypi/pylint@4.1.3` |
| pypi | pyparsing | 3.3.3 | MIT | - | `pkg:pypi/pyparsing@3.3.3` |
| pypi | python-dateutil | 2.9.0.post0 | Dual License | - | `pkg:pypi/python-dateutil@2.9.0.post0` |
| pypi | python-json-logger | 4.2.0 | BSD-2-Clause | - | `pkg:pypi/python-json-logger@4.2.0` |
| pypi | pyulog | 1.2.4 | BSD-3-Clause | - | `pkg:pypi/pyulog@1.2.4` |
| pypi | pyyaml | 6.0.3 | MIT | - | `pkg:pypi/pyyaml@6.0.3` |
| pypi | pyzmq | 27.2.0 | BSD-3-Clause | - | `pkg:pypi/pyzmq@27.2.0` |
| pypi | referencing | 0.37.0 | MIT | - | `pkg:pypi/referencing@0.37.0` |
| pypi | requests | 2.34.2 | Apache-2.0 | - | `pkg:pypi/requests@2.34.2` |
| pypi | rfc3339-validator | 0.1.4 | MIT license | - | `pkg:pypi/rfc3339-validator@0.1.4` |
| pypi | rfc3986-validator | 0.1.1 | MIT license | - | `pkg:pypi/rfc3986-validator@0.1.1` |
| pypi | rfc3987-syntax | 1.1.0 | MIT | - | `pkg:pypi/rfc3987-syntax@1.1.0` |
| pypi | rpds-py | 2026.9.1 | MIT | - | `pkg:pypi/rpds-py@2026.9.1` |
| pypi | scipy | 1.18.1 | BSD-3-Clause | - | `pkg:pypi/scipy@1.18.1` |
| pypi | send2trash | 2.1.0 | BSD-3-Clause | - | `pkg:pypi/send2trash@2.1.0` |
| pypi | setuptools | 68.1.2 | - | - | `pkg:pypi/setuptools@68.1.2` |
| pypi | simplekml | 1.3.6 | GNU Lesser General Public License v3+ | - | `pkg:pypi/simplekml@1.3.6` |
| pypi | six | 1.17.0 | MIT | - | `pkg:pypi/six@1.17.0` |
| pypi | smopy | 0.0.8 | BSD | - | `pkg:pypi/smopy@0.0.8` |
| pypi | soupsieve | 3.0.3 | MIT | - | `pkg:pypi/soupsieve@3.0.3` |
| pypi | stack-data | 0.6.3 | MIT | - | `pkg:pypi/stack-data@0.6.3` |
| pypi | terminado | 0.18.1 | BSD-2-Clause | - | `pkg:pypi/terminado@0.18.1` |
| pypi | tinycss2 | 1.5.1 | - | - | `pkg:pypi/tinycss2@1.5.1` |
| pypi | tomlkit | 0.15.2 | MIT | - | `pkg:pypi/tomlkit@0.15.2` |
| pypi | tornado | 6.5.10 | Apache-2.0 | - | `pkg:pypi/tornado@6.5.10` |
| pypi | traitlets | 5.16.1 | BSD-3-Clause | - | `pkg:pypi/traitlets@5.16.1` |
| pypi | typing-extensions | 4.16.0 | PSF-2.0 | - | `pkg:pypi/typing-extensions@4.16.0` |
| pypi | tzdata | 2026.5 | Apache-2.0 | - | `pkg:pypi/tzdata@2026.5` |
| pypi | uri-template | 1.3.0 | MIT License | - | `pkg:pypi/uri-template@1.3.0` |
| pypi | urllib3 | 2.8.0 | MIT | - | `pkg:pypi/urllib3@2.8.0` |
| pypi | wcwidth | 0.9.2 | - | - | `pkg:pypi/wcwidth@0.9.2` |
| pypi | webcolors | 25.10.0 | BSD-3-Clause | - | `pkg:pypi/webcolors@25.10.0` |
| pypi | webencodings | 0.6.1 | - | - | `pkg:pypi/webencodings@0.6.1` |
| pypi | websocket-client | 1.9.2 | Apache-2.0 | - | `pkg:pypi/websocket-client@1.9.2` |
| pypi | wheel | 0.42.0 | - | - | `pkg:pypi/wheel@0.42.0` |
| pypi | widgetsnbextension | 4.0.16 | BSD 3-Clause License | - | `pkg:pypi/widgetsnbextension@4.0.16` |
| pypi | xyzservices | 2026.9.1 | BSD-3-Clause | - | `pkg:pypi/xyzservices@2026.9.1` |

## flight_review-nginx-image

Reverse proxy / TLS terminator container (nginx:latest)

| Ecosystem | Name | Version | License | Supplier / publisher | purl |
|---|---|---|---|---|---|
| deb | apt | 3.0.3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, curl, Expat | APT Development Team <deity@lists.debian.org> | `pkg:deb/debian/apt@3.0.3?arch=amd64&distro=debian-13.7` |
| deb | base-files | 13.8+deb13u7 | GPL-2.0-only, GPL-2.0-or-later, verbatim | Santiago Vila <sanvila@debian.org> | `pkg:deb/debian/base-files@13.8%2Bdeb13u7?arch=amd64&distro=debian-13.7` |
| deb | base-passwd | 3.6.7 | GPL-2.0-only, public-domain | Shadow package maintainers <pkg-shadow-devel@lists.alioth.debian.org> | `pkg:deb/debian/base-passwd@3.6.7?arch=amd64&distro=debian-13.7` |
| deb | bash | 5.2.37-2+b10 | BSD-4-Clause-UC, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, Latex2e, GFDL-NIV-1.3, MIT-like, permissive | Matthias Klose <doko@debian.org> | `pkg:deb/debian/bash@5.2.37-2%2Bb10?arch=amd64&distro=debian-13.7&upstream=bash%405.2.37-2` |
| deb | bsdutils | 1:2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/bsdutils@1%3A2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux%402.41.5-0%2Bdeb13u1` |
| deb | ca-certificates | 20250419 | GPL-2.0-only, GPL-2.0-or-later, MPL-2.0 | Julien Cristau <jcristau@debian.org> | `pkg:deb/debian/ca-certificates@20250419?arch=all&distro=debian-13.7` |
| deb | coreutils | 9.7-3 | BSD-4-Clause-UC, FSFULLR, GFDL-1.3-only, GPL-3.0-only, GPL-3.0-or-later, ISC, GFDL-NIV-1.3 | Michael Stone <mstone@debian.org> | `pkg:deb/debian/coreutils@9.7-3?arch=amd64&distro=debian-13.7` |
| deb | curl | 8.14.1-2+deb13u7 | BSD-3-Clause, BSD-4-Clause-UC, FSFULLR, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, ISC, OLDAP-2.8, X11, curl | Debian Curl Maintainers <team+curl@tracker.debian.org> | `pkg:deb/debian/curl@8.14.1-2%2Bdeb13u7?arch=amd64&distro=debian-13.7` |
| deb | dash | 0.5.12-12 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, public-domain | Andrej Shadura <andrewsh@debian.org> | `pkg:deb/debian/dash@0.5.12-12?arch=amd64&distro=debian-13.7` |
| deb | debconf | 1.5.91 | BSD-2-Clause | Debconf Developers <debconf-devel@lists.alioth.debian.org> | `pkg:deb/debian/debconf@1.5.91?arch=all&distro=debian-13.7` |
| deb | debian-archive-keyring | 2025.1 | sha256:8f918c0bebd1454a084698a95c09d9a03cec8453dad1fc6eab9e6427da9d33a9 | Debian Release Team <packages@release.debian.org> | `pkg:deb/debian/debian-archive-keyring@2025.1?arch=all&distro=debian-13.7` |
| deb | debianutils | 5.23.2 | GPL-2.0-only, GPL-2.0-or-later, SMAIL-GPL, public-domain | Ileana Dumitrescu <ileanadumitrescu95@gmail.com> | `pkg:deb/debian/debianutils@5.23.2?arch=amd64&distro=debian-13.7` |
| deb | diffutils | 1:3.10-4 | FSFAP, FSFULLR, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, X11, GFDL-NIV-1.3, public-domain | Santiago Vila <sanvila@debian.org> | `pkg:deb/debian/diffutils@1%3A3.10-4?arch=amd64&distro=debian-13.7` |
| deb | dpkg | 1.22.22 | GPL-2.0-only, GPL-2.0-or-later, public-domain-s-s-d | Dpkg Developers <debian-dpkg@lists.debian.org> | `pkg:deb/debian/dpkg@1.22.22?arch=amd64&distro=debian-13.7` |
| deb | findutils | 4.10.0-3 | BSD-3-Clause, FSFAP, FSFULLR, GFDL-1.3-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, X11, GFDL-NIV-1.3+, GPL, LGPL, public-domain | Andreas Metzler <ametzler@debian.org> | `pkg:deb/debian/findutils@4.10.0-3?arch=amd64&distro=debian-13.7` |
| deb | fontconfig-config | 2.15.0-2.3 | HPND-sell-variant | Debian freedesktop.org maintainers <pkg-freedesktop-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/fontconfig-config@2.15.0-2.3?arch=amd64&distro=debian-13.7&upstream=fontconfig` |
| deb | fonts-dejavu-core | 2.37-8 | GPL-2.0-only, GPL-2.0-or-later, Bitstream-Vera | Debian Fonts Task Force <debian-fonts@lists.debian.org> | `pkg:deb/debian/fonts-dejavu-core@2.37-8?arch=all&distro=debian-13.7&upstream=fonts-dejavu` |
| deb | fonts-dejavu-mono | 2.37-8 | GPL-2.0-only, GPL-2.0-or-later, Bitstream-Vera | Debian Fonts Task Force <debian-fonts@lists.debian.org> | `pkg:deb/debian/fonts-dejavu-mono@2.37-8?arch=all&distro=debian-13.7&upstream=fonts-dejavu` |
| deb | gcc-14-base | 14.2.0-19 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Debian GCC Maintainers <debian-gcc@lists.debian.org> | `pkg:deb/debian/gcc-14-base@14.2.0-19?arch=amd64&distro=debian-13.7&upstream=gcc-14` |
| deb | gettext-base | 0.23.1-2 | GFDL-1.2-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, FDL-1.2+ | Santiago Vila <sanvila@debian.org> | `pkg:deb/debian/gettext-base@0.23.1-2?arch=amd64&distro=debian-13.7&upstream=gettext` |
| deb | grep | 3.11-4 | GPL-3.0-only, GPL-3.0-or-later | Anibal Monsalve Salazar <anibal@debian.org> | `pkg:deb/debian/grep@3.11-4?arch=amd64&distro=debian-13.7` |
| deb | gzip | 1.13-1+deb13u1 | GPL-3.0-only, GPL-3.0-or-later, FSF-manpages, GFDL-1.3+-no-invariant, GFDL-3 | Milan Kupcevic <milan@debian.org> | `pkg:deb/debian/gzip@1.13-1%2Bdeb13u1?arch=amd64&distro=debian-13.7` |
| deb | hostname | 3.25 | GPL-2.0-only | Michael Meskes <meskes@debian.org> | `pkg:deb/debian/hostname@3.25?arch=amd64&distro=debian-13.7` |
| deb | init-system-helpers | 1.69~deb13u1 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later | Debian systemd Maintainers <pkg-systemd-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/init-system-helpers@1.69~deb13u1?arch=all&distro=debian-13.7` |
| deb | libabsl20240722 | 20240722.0-4 | Apache-2.0 | Benjamin Barenblat <bbaren@debian.org> | `pkg:deb/debian/libabsl20240722@20240722.0-4?arch=amd64&distro=debian-13.7&upstream=abseil` |
| deb | libacl1 | 2.3.2-2+b1 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-or-later, LGPL-2.1-only | Guillem Jover <guillem@debian.org> | `pkg:deb/debian/libacl1@2.3.2-2%2Bb1?arch=amd64&distro=debian-13.7&upstream=acl%402.3.2-2` |
| deb | libaom3 | 3.12.1-1+deb13u1 | BSD-2-Clause, BSD-3-Clause, ISC, Expat, public-domain-md5 | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libaom3@3.12.1-1%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=aom` |
| deb | libapt-pkg7.0 | 3.0.3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, curl, Expat | APT Development Team <deity@lists.debian.org> | `pkg:deb/debian/libapt-pkg7.0@3.0.3?arch=amd64&distro=debian-13.7&upstream=apt` |
| deb | libattr1 | 1:2.5.2-3 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-or-later, LGPL-2.1-only | Guillem Jover <guillem@debian.org> | `pkg:deb/debian/libattr1@1%3A2.5.2-3?arch=amd64&distro=debian-13.7&upstream=attr` |
| deb | libaudit-common | 1:4.0.2-2+deb13u1 | GPL-1.0-only, GPL-2.0-only, LGPL-2.1-only | Laurent Bigonville <bigon@debian.org> | `pkg:deb/debian/libaudit-common@1%3A4.0.2-2%2Bdeb13u1?arch=all&distro=debian-13.7&upstream=audit` |
| deb | libaudit1 | 1:4.0.2-2+deb13u1 | GPL-1.0-only, GPL-2.0-only, LGPL-2.1-only | Laurent Bigonville <bigon@debian.org> | `pkg:deb/debian/libaudit1@1%3A4.0.2-2%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=audit` |
| deb | libavif16 | 1.2.1-1.2 | Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC0-1.0, MIT, custom-1 | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libavif16@1.2.1-1.2?arch=amd64&distro=debian-13.7&upstream=libavif` |
| deb | libblkid1 | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/libblkid1@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | libbrotli1 | 1.1.0-2+b7 | MIT | Tomasz Buchert <tomasz@debian.org> | `pkg:deb/debian/libbrotli1@1.1.0-2%2Bb7?arch=amd64&distro=debian-13.7&upstream=brotli%401.1.0-2` |
| deb | libbsd0 | 0.12.2-2 | BSD-2-Clause, BSD-3-Clause, Beerware, ISC, BSD-2-clause-author, BSD-2-clause-verbatim, BSD-3-clause-John-Birrell, BSD-3-clause-Regents, BSD-3-clause-author, BSD-5-clause-Peter-Wemm, Expat, ISC-Original, public-domain | Guillem Jover <guillem@debian.org> | `pkg:deb/debian/libbsd0@0.12.2-2?arch=amd64&distro=debian-13.7&upstream=libbsd` |
| deb | libbz2-1.0 | 1.0.8-6 | GPL-2.0-only, BSD-variant | Anibal Monsalve Salazar <anibal@debian.org> | `pkg:deb/debian/libbz2-1.0@1.0.8-6?arch=amd64&distro=debian-13.7&upstream=bzip2` |
| deb | libc-bin | 2.41-12+deb13u4 | BSD-2-Clause, BSL-1.0, FSFAP, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, SunPro, Unicode-DFS-2016, BSD-3-clause-Berkeley, BSD-3-clause-Carnegie, BSD-3-clause-Oracle, BSD-3-clause-WIDE, BSD-like-Spencer, CORE-MATH, Carnegie, DEC, GPL-2+-with-link-exception, IBM, Inner-Net, LGPL-2.1+-with-link-exception, MIT-like-Lord, PCRE, Univ-Coimbra, public-domain | GNU Libc Maintainers <debian-glibc@lists.debian.org> | `pkg:deb/debian/libc-bin@2.41-12%2Bdeb13u4?arch=amd64&distro=debian-13.7&upstream=glibc` |
| deb | libc6 | 2.41-12+deb13u4 | BSD-2-Clause, BSL-1.0, FSFAP, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, SunPro, Unicode-DFS-2016, BSD-3-clause-Berkeley, BSD-3-clause-Carnegie, BSD-3-clause-Oracle, BSD-3-clause-WIDE, BSD-like-Spencer, CORE-MATH, Carnegie, DEC, GPL-2+-with-link-exception, IBM, Inner-Net, LGPL-2.1+-with-link-exception, MIT-like-Lord, PCRE, Univ-Coimbra, public-domain | GNU Libc Maintainers <debian-glibc@lists.debian.org> | `pkg:deb/debian/libc6@2.41-12%2Bdeb13u4?arch=amd64&distro=debian-13.7&upstream=glibc` |
| deb | libcap-ng0 | 0.8.5-4+b1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Håvard F. Aasen <havard.f.aasen@pfft.no> | `pkg:deb/debian/libcap-ng0@0.8.5-4%2Bb1?arch=amd64&distro=debian-13.7&upstream=libcap-ng%400.8.5-4` |
| deb | libcap2 | 1:2.75-10+deb13u1+b3 | BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later | Christian Kastner <ckk@debian.org> | `pkg:deb/debian/libcap2@1%3A2.75-10%2Bdeb13u1%2Bb3?arch=amd64&distro=debian-13.7&upstream=libcap2%401%3A2.75-10%2Bdeb13u1` |
| deb | libcom-err2 | 1.47.2-3+b12 | 0BSD, Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, ISC, Kazlib, LGPL-2.0-only, Latex2e, BSD-3-Clause-Variant, BSD-4-Clause-CMU, Expat, GPL | Theodore Y. Ts'o <tytso@mit.edu> | `pkg:deb/debian/libcom-err2@1.47.2-3%2Bb12?arch=amd64&distro=debian-13.7&upstream=e2fsprogs%401.47.2-3` |
| deb | libcrypt1 | 1:4.4.38-1 | sha256:5a5e7ca0e9f3f9679977e3a3e9ede45ad92885a3297ea78e766979f9866c5a16 | Marco d'Itri <md@linux.it> | `pkg:deb/debian/libcrypt1@1%3A4.4.38-1?arch=amd64&distro=debian-13.7&upstream=libxcrypt` |
| deb | libcurl4t64 | 8.14.1-2+deb13u7 | BSD-3-Clause, BSD-4-Clause-UC, FSFULLR, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, ISC, OLDAP-2.8, X11, curl | Debian Curl Maintainers <team+curl@tracker.debian.org> | `pkg:deb/debian/libcurl4t64@8.14.1-2%2Bdeb13u7?arch=amd64&distro=debian-13.7&upstream=curl` |
| deb | libdav1d7 | 1.5.1-1 | BSD-2-Clause, ISC, public-domain | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libdav1d7@1.5.1-1?arch=amd64&distro=debian-13.7&upstream=dav1d` |
| deb | libdb5.3t64 | 5.3.28+dfsg2-9 | BSD-3-Clause, GPL-3.0-only, MS-PL, Sleepycat, X11, Zlib, Artistic, BSD-3-clause-fjord, GPL, MIT-old, TCL-like | Debian QA Group <packages@qa.debian.org> | `pkg:deb/debian/libdb5.3t64@5.3.28%2Bdfsg2-9?arch=amd64&distro=debian-13.7&upstream=db5.3` |
| deb | libde265-0 | 1.0.15-1+deb13u2 | BSD-4-Clause, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, other-1, public-domain-1 | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libde265-0@1.0.15-1%2Bdeb13u2?arch=amd64&distro=debian-13.7&upstream=libde265` |
| deb | libdebconfclient0 | 0.280 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Debian Install System Team <debian-boot@lists.debian.org> | `pkg:deb/debian/libdebconfclient0@0.280?arch=amd64&distro=debian-13.7&upstream=cdebconf` |
| deb | libdeflate0 | 1.23-2 | Expat | Deflate Team <libdeflate@packages.debian.org> | `pkg:deb/debian/libdeflate0@1.23-2?arch=amd64&distro=debian-13.7&upstream=libdeflate` |
| deb | libedit2 | 3.1-20250104-1 | BSD-3-Clause | LLVM Packaging Team <pkg-llvm-team@lists.alioth.debian.org> | `pkg:deb/debian/libedit2@3.1-20250104-1?arch=amd64&distro=debian-13.7&upstream=libedit` |
| deb | libexpat1 | 2.8.3-1~deb13u1 | MIT | Laszlo Boszormenyi (GCS) <gcs@debian.org> | `pkg:deb/debian/libexpat1@2.8.3-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=expat` |
| deb | libffi8 | 3.4.8-2 | GPL-2.0-or-later, GPL-3.0-or-later, MPL-1.1, X11, Expat, GPL, public-domain | Debian GCC Maintainers <debian-gcc@lists.debian.org> | `pkg:deb/debian/libffi8@3.4.8-2?arch=amd64&distro=debian-13.7&upstream=libffi` |
| deb | libfontconfig1 | 2.15.0-2.3 | HPND-sell-variant | Debian freedesktop.org maintainers <pkg-freedesktop-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/libfontconfig1@2.15.0-2.3?arch=amd64&distro=debian-13.7&upstream=fontconfig` |
| deb | libfreetype6 | 2.13.3+dfsg-1+deb13u1 | BSD-3-Clause, BSL-1.0, FSFAP, FTL, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, MIT-Modern-Variant, Zlib, Expat, MIT-SMC, OpenGroup-MIT, Public-Domain | Hugh McMaster <hmc@debian.org> | `pkg:deb/debian/libfreetype6@2.13.3%2Bdfsg-1%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=freetype` |
| deb | libgav1-1 | 0.19.0-3+b1 | Apache-2.0, BSD-3-Clause | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libgav1-1@0.19.0-3%2Bb1?arch=amd64&distro=debian-13.7&upstream=libgav1%400.19.0-3` |
| deb | libgcc-s1 | 14.2.0-19 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Debian GCC Maintainers <debian-gcc@lists.debian.org> | `pkg:deb/debian/libgcc-s1@14.2.0-19?arch=amd64&distro=debian-13.7&upstream=gcc-14` |
| deb | libgcrypt20 | 1.11.0-7+deb13u1 | sha256:4feae258cab1ad4743fb569a77e0b2a5b7a0199520bdbc0a613916291b9aa8a8 | Debian GnuTLS Maintainers <pkg-gnutls-maint@lists.alioth.debian.org> | `pkg:deb/debian/libgcrypt20@1.11.0-7%2Bdeb13u1?arch=amd64&distro=debian-13.7` |
| deb | libgd3 | 2.3.3-14~deb13u1 | sha256:53c9aa3ebfa5ab3aa28a5467aca74c10446b2e7ed21d68bdc8cc372f32d551ee | GD Team <team+gd@tracker.debian.org> | `pkg:deb/debian/libgd3@2.3.3-14~deb13u1?arch=amd64&distro=debian-13.7&upstream=libgd2` |
| deb | libgeoip1t64 | 1.6.12-11.2~deb13u1 | ISC, LGPL-2.1-only, LGPL-2.1-or-later | Patrick Matthäi <pmatthaei@debian.org> | `pkg:deb/debian/libgeoip1t64@1.6.12-11.2~deb13u1?arch=amd64&distro=debian-13.7&upstream=geoip` |
| deb | libgmp10 | 2:6.3.0+dfsg-3 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later | Debian Science Maintainers <debian-science-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/libgmp10@2%3A6.3.0%2Bdfsg-3?arch=amd64&distro=debian-13.7&upstream=gmp` |
| deb | libgnutls30t64 | 3.8.9-3+deb13u4 | sha256:a07e99815cf1998f1dabbc21fe199460bfa09b85ead0d56b49a32cac3d1791b5 | Debian GnuTLS Maintainers <pkg-gnutls-maint@lists.alioth.debian.org> | `pkg:deb/debian/libgnutls30t64@3.8.9-3%2Bdeb13u4?arch=amd64&distro=debian-13.7&upstream=gnutls28` |
| deb | libgomp1 | 14.2.0-19 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Debian GCC Maintainers <debian-gcc@lists.debian.org> | `pkg:deb/debian/libgomp1@14.2.0-19?arch=amd64&distro=debian-13.7&upstream=gcc-14` |
| deb | libgpg-error0 | 1.51-4 | BSD-3-Clause, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, g10-permissive | Debian GnuPG Maintainers <pkg-gnupg-maint@lists.alioth.debian.org> | `pkg:deb/debian/libgpg-error0@1.51-4?arch=amd64&distro=debian-13.7&upstream=libgpg-error` |
| deb | libgssapi-krb5-2 | 1.21.3-5+deb13u1 | sha256:936728f4181718f42951b881c1e8f1386bf6b2723c4fbc533c374d6f42c71816 | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libgssapi-krb5-2@1.21.3-5%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=krb5` |
| deb | libheif-plugin-dav1d | 1.23.4-1~deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause-UC, BSL-1.0, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Expat | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libheif-plugin-dav1d@1.23.4-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=libheif` |
| deb | libheif-plugin-libde265 | 1.23.4-1~deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause-UC, BSL-1.0, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Expat | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libheif-plugin-libde265@1.23.4-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=libheif` |
| deb | libheif1 | 1.23.4-1~deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause-UC, BSL-1.0, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Expat | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libheif1@1.23.4-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=libheif` |
| deb | libhogweed6t64 | 3.10.1-1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-3.0-or-later, Expat, GAP, GPL, LGPL, public-domain | Magnus Holmgren <holmgren@debian.org> | `pkg:deb/debian/libhogweed6t64@3.10.1-1?arch=amd64&distro=debian-13.7&upstream=nettle` |
| deb | libidn2-0 | 2.3.8-2 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Expat, Unicode | Debian Libidn team <help-libidn@gnu.org> | `pkg:deb/debian/libidn2-0@2.3.8-2?arch=amd64&distro=debian-13.7&upstream=libidn2` |
| deb | libimagequant0 | 2.18.0-1+b2 | GPL-3.0-only, GPL-3.0-or-later, MIT, CC0 | Debian PhotoTools Maintainers <pkg-phototools-devel@lists.alioth.debian.org> | `pkg:deb/debian/libimagequant0@2.18.0-1%2Bb2?arch=amd64&distro=debian-13.7&upstream=libimagequant%402.18.0-1` |
| deb | libjbig0 | 2.1-6.1+b2 | GPL-2.0-only, GPL-2.0-or-later | Michael van der Kolff <mvanderkolff@gmail.com> | `pkg:deb/debian/libjbig0@2.1-6.1%2Bb2?arch=amd64&distro=debian-13.7&upstream=jbigkit%402.1-6.1` |
| deb | libjpeg62-turbo | 1:2.1.5-4 | BSD-3-Clause, NTP, Zlib, BSD-BY-LC-NE, Expat | Ondřej Surý <ondrej@debian.org> | `pkg:deb/debian/libjpeg62-turbo@1%3A2.1.5-4?arch=amd64&distro=debian-13.7&upstream=libjpeg-turbo` |
| deb | libk5crypto3 | 1.21.3-5+deb13u1 | sha256:936728f4181718f42951b881c1e8f1386bf6b2723c4fbc533c374d6f42c71816 | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libk5crypto3@1.21.3-5%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=krb5` |
| deb | libkeyutils1 | 1.6.3-6 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later | Christian Kastner <ckk@debian.org> | `pkg:deb/debian/libkeyutils1@1.6.3-6?arch=amd64&distro=debian-13.7&upstream=keyutils` |
| deb | libkrb5-3 | 1.21.3-5+deb13u1 | sha256:936728f4181718f42951b881c1e8f1386bf6b2723c4fbc533c374d6f42c71816 | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libkrb5-3@1.21.3-5%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=krb5` |
| deb | libkrb5support0 | 1.21.3-5+deb13u1 | sha256:936728f4181718f42951b881c1e8f1386bf6b2723c4fbc533c374d6f42c71816 | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libkrb5support0@1.21.3-5%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=krb5` |
| deb | liblastlog2-2 | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/liblastlog2-2@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | libldap2 | 2.6.10+dfsg-1 | BSD-3-Clause, Beerware, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, BSD-3-clause-California, BSD-3-clause-variant, BSD-4-clause-California, Expat, Expat-ISC, Expat-UNM, F5, FSF-unlimited, JCG, MIT-XC, NeoSoft-permissive, OpenLDAP-2.8, UMich, public-domain | Debian OpenLDAP Maintainers <pkg-openldap-devel@lists.alioth.debian.org> | `pkg:deb/debian/libldap2@2.6.10%2Bdfsg-1?arch=amd64&distro=debian-13.7&upstream=openldap` |
| deb | liblerc4 | 4.0.0+ds-5 | Apache-2.0 | Debian GIS Project <pkg-grass-devel@lists.alioth.debian.org> | `pkg:deb/debian/liblerc4@4.0.0%2Bds-5?arch=amd64&distro=debian-13.7&upstream=lerc` |
| deb | liblz4-1 | 1.10.0-4 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Nobuhiro Iwamatsu <iwamatsu@debian.org> | `pkg:deb/debian/liblz4-1@1.10.0-4?arch=amd64&distro=debian-13.7&upstream=lz4` |
| deb | liblzma5 | 5.8.1-1+deb13u1 | 0BSD, FSFUL, FSFULLR, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.1-only, LGPL-2.1-or-later, GPL-3.0-or-later-WITH-Autoconf-exception-macro, PD, PD-debian, noderivs, permissive-nowarranty | Sebastian Andrzej Siewior <sebastian@breakpoint.cc> | `pkg:deb/debian/liblzma5@5.8.1-1%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=xz-utils` |
| deb | libmaxminddb0 | 1.12.2-1 | Apache-2.0, BSD-2-Clause, LGPL-3.0-only, LGPL-3.0-or-later, Expat | Faidon Liambotis <paravoid@debian.org> | `pkg:deb/debian/libmaxminddb0@1.12.2-1?arch=amd64&distro=debian-13.7&upstream=libmaxminddb` |
| deb | libmd0 | 1.1.0-2+b1 | BSD-2-Clause, BSD-3-Clause, Beerware, ISC, BSD-3-clause-Aaron-D-Gifford, public-domain-md4, public-domain-md5, public-domain-sha1 | Guillem Jover <guillem@debian.org> | `pkg:deb/debian/libmd0@1.1.0-2%2Bb1?arch=amd64&distro=debian-13.7&upstream=libmd%401.1.0-2` |
| deb | libmount1 | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/libmount1@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | libnettle8t64 | 3.10.1-1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-3.0-or-later, Expat, GAP, GPL, LGPL, public-domain | Magnus Holmgren <holmgren@debian.org> | `pkg:deb/debian/libnettle8t64@3.10.1-1?arch=amd64&distro=debian-13.7&upstream=nettle` |
| deb | libnghttp2-14 | 1.64.0-1.1+deb13u1 | BSD-2-Clause, GPL-3.0-only, GPL-3.0-or-later, MIT, Expat, all-permissive | Tomasz Buchert <tomasz@debian.org> | `pkg:deb/debian/libnghttp2-14@1.64.0-1.1%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=nghttp2` |
| deb | libnghttp3-9 | 1.8.0-1 | FSFAP, FSFUL, FSFULLR, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, MIT | Debian Curl Maintainers <team+curl@tracker.debian.org> | `pkg:deb/debian/libnghttp3-9@1.8.0-1?arch=amd64&distro=debian-13.7&upstream=nghttp3` |
| deb | libp11-kit0 | 0.25.5-3 | Apache-2.0, BSD-3-Clause, FSFAP, FSFULLR, GPL-2.0-or-later, GPL-3.0-or-later, ISC, LGPL-2.1-only, LGPL-2.1-or-later, X11, customFSFUL, customFSFULLRWD | Debian GnuTLS Maintainers <pkg-gnutls-maint@lists.alioth.debian.org> | `pkg:deb/debian/libp11-kit0@0.25.5-3?arch=amd64&distro=debian-13.7&upstream=p11-kit` |
| deb | libpam-modules | 1.7.0-5 | BSD-3-Clause, Beerware, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, public-domain | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libpam-modules@1.7.0-5?arch=amd64&distro=debian-13.7&upstream=pam` |
| deb | libpam-modules-bin | 1.7.0-5 | BSD-3-Clause, Beerware, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, public-domain | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libpam-modules-bin@1.7.0-5?arch=amd64&distro=debian-13.7&upstream=pam` |
| deb | libpam-runtime | 1.7.0-5 | BSD-3-Clause, Beerware, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, public-domain | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libpam-runtime@1.7.0-5?arch=all&distro=debian-13.7&upstream=pam` |
| deb | libpam0g | 1.7.0-5 | BSD-3-Clause, Beerware, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.0-only, LGPL-2.0-or-later, BSD-tcp_wrappers, public-domain | Sam Hartman <hartmans@debian.org> | `pkg:deb/debian/libpam0g@1.7.0-5?arch=amd64&distro=debian-13.7&upstream=pam` |
| deb | libpcre2-8-0 | 10.46-1~deb13u3 | BSD-2-Clause, BSD-3-Clause, X11, BSD-3-clause-Cambridge, public-domain | Matthew Vernon <matthew@debian.org> | `pkg:deb/debian/libpcre2-8-0@10.46-1~deb13u3?arch=amd64&distro=debian-13.7&upstream=pcre2` |
| deb | libpng16-16t64 | 1.6.48-1+deb13u6 | Apache-2.0, BSD-3-Clause, GPL-2.0-only, GPL-2.0-or-later, Libpng, BSD-like-with-advertising-clause, expat | Maintainers of libpng1.6 packages <libpng1.6@packages.debian.org> | `pkg:deb/debian/libpng16-16t64@1.6.48-1%2Bdeb13u6?arch=amd64&distro=debian-13.7&upstream=libpng1.6` |
| deb | libpsl5t64 | 0.21.2-1.1+b1 | MIT, Chromium, gnulib | Tim Rühsen <tim.ruehsen@gmx.de> | `pkg:deb/debian/libpsl5t64@0.21.2-1.1%2Bb1?arch=amd64&distro=debian-13.7&upstream=libpsl%400.21.2-1.1` |
| deb | librav1e0.7 | 0.7.1-9+b2 | BSD-2-Clause, ISC | Debian Rust Maintainers <pkg-rust-maintainers@alioth-lists.debian.net> | `pkg:deb/debian/librav1e0.7@0.7.1-9%2Bb2?arch=amd64&distro=debian-13.7&upstream=rust-rav1e%400.7.1-9` |
| deb | librtmp1 | 2.4+20151223.gitfa8646d.1-2+b5 | sha256:4302abcc1ea1b6cbe8d19c79b892acf78878030220210707c19006828866207c | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/librtmp1@2.4%2B20151223.gitfa8646d.1-2%2Bb5?arch=amd64&distro=debian-13.7&upstream=rtmpdump%402.4%2B20151223.gitfa8646d.1-2` |
| deb | libsasl2-2 | 2.1.28+dfsg1-9 | BSD-2-Clause, BSD-3-Clause-Attribution, BSD-3-Clause, BSD-4-Clause-UC, FSFULLR, GPL-3.0-only, GPL-3.0-or-later, MIT-CMU, RSA-MD, BSD-2.2-clause, BSD-3-clause-JANET, BSD-3-clause-PADL, IBM-as-is, MIT-Export, MIT-OpenVision, OpenLDAP | Debian Cyrus Team <team+cyrus@tracker.debian.org> | `pkg:deb/debian/libsasl2-2@2.1.28%2Bdfsg1-9?arch=amd64&distro=debian-13.7&upstream=cyrus-sasl2` |
| deb | libsasl2-modules-db | 2.1.28+dfsg1-9 | BSD-2-Clause, BSD-3-Clause-Attribution, BSD-3-Clause, BSD-4-Clause-UC, FSFULLR, GPL-3.0-only, GPL-3.0-or-later, MIT-CMU, RSA-MD, BSD-2.2-clause, BSD-3-clause-JANET, BSD-3-clause-PADL, IBM-as-is, MIT-Export, MIT-OpenVision, OpenLDAP | Debian Cyrus Team <team+cyrus@tracker.debian.org> | `pkg:deb/debian/libsasl2-modules-db@2.1.28%2Bdfsg1-9?arch=amd64&distro=debian-13.7&upstream=cyrus-sasl2` |
| deb | libseccomp2 | 2.6.0-2 | LGPL-2.1-only | Kees Cook <kees@debian.org> | `pkg:deb/debian/libseccomp2@2.6.0-2?arch=amd64&distro=debian-13.7&upstream=libseccomp` |
| deb | libselinux1 | 3.8.1-1 | GPL-2.0-only, public-domain | Debian SELinux maintainers <selinux-devel@lists.alioth.debian.org> | `pkg:deb/debian/libselinux1@3.8.1-1?arch=amd64&distro=debian-13.7&upstream=libselinux` |
| deb | libsemanage-common | 3.8.1-1 | GPL-2.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Debian SELinux maintainers <selinux-devel@lists.alioth.debian.org> | `pkg:deb/debian/libsemanage-common@3.8.1-1?arch=all&distro=debian-13.7&upstream=libsemanage` |
| deb | libsemanage2 | 3.8.1-1 | GPL-2.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Debian SELinux maintainers <selinux-devel@lists.alioth.debian.org> | `pkg:deb/debian/libsemanage2@3.8.1-1?arch=amd64&distro=debian-13.7&upstream=libsemanage` |
| deb | libsepol2 | 3.8.1-1 | GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Zlib | Debian SELinux maintainers <selinux-devel@lists.alioth.debian.org> | `pkg:deb/debian/libsepol2@3.8.1-1?arch=amd64&distro=debian-13.7&upstream=libsepol` |
| deb | libsharpyuv0 | 1.5.0-0.1 | Apache-2.0, BSD-3-Clause | Jeff Breidenbach <jab@debian.org> | `pkg:deb/debian/libsharpyuv0@1.5.0-0.1?arch=amd64&distro=debian-13.7&upstream=libwebp` |
| deb | libsmartcols1 | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/libsmartcols1@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | libsqlite3-0 | 3.46.1-7+deb13u2 | GPL-2.0-only, GPL-2.0-or-later, public-domain | Laszlo Boszormenyi (GCS) <gcs@debian.org> | `pkg:deb/debian/libsqlite3-0@3.46.1-7%2Bdeb13u2?arch=amd64&distro=debian-13.7&upstream=sqlite3` |
| deb | libssh2-1t64 | 1.11.1-1+deb13u2 | ISC, BSD3 | Nicolas Mora <babelouest@debian.org> | `pkg:deb/debian/libssh2-1t64@1.11.1-1%2Bdeb13u2?arch=amd64&distro=debian-13.7&upstream=libssh2` |
| deb | libssl3t64 | 3.5.7-1~deb13u3 | Apache-2.0, GPL-1.0-only, GPL-1.0-or-later, Artistic | Debian OpenSSL Team <pkg-openssl-devel@alioth-lists.debian.net> | `pkg:deb/debian/libssl3t64@3.5.7-1~deb13u3?arch=amd64&distro=debian-13.7&upstream=openssl` |
| deb | libstdc++6 | 14.2.0-19 | sha256:20390f8a6f3b1e4d7cb45dd8652dabb259bbef688cbad839bcdb0b9ba7252f79 | Debian GCC Maintainers <debian-gcc@lists.debian.org> | `pkg:deb/debian/libstdc%2B%2B6@14.2.0-19?arch=amd64&distro=debian-13.7&upstream=gcc-14` |
| deb | libsvtav1enc2 | 2.3.0+dfsg-1 | BSD-2-Clause, BSD-3-Clause-Clear, BSD-3-Clause, ISC, LGPL-2.1-only, LGPL-2.1-or-later, Expat | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libsvtav1enc2@2.3.0%2Bdfsg-1?arch=amd64&distro=debian-13.7&upstream=svt-av1` |
| deb | libsystemd0 | 257.13-1~deb13u1 | CC0-1.0, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Expat, public-domain | Debian systemd Maintainers <pkg-systemd-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/libsystemd0@257.13-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=systemd` |
| deb | libtasn1-6 | 4.20.0-2+deb13u1 | sha256:5f9f7b538d221104bdb561ae80fd794ec5f813eb8fd04650293bddcc0f856e7d | Debian GnuTLS Maintainers <pkg-gnutls-maint@lists.alioth.debian.org> | `pkg:deb/debian/libtasn1-6@4.20.0-2%2Bdeb13u1?arch=amd64&distro=debian-13.7` |
| deb | libtiff6 | 4.7.0-3+deb13u3 | Hylafax | Laszlo Boszormenyi (GCS) <gcs@debian.org> | `pkg:deb/debian/libtiff6@4.7.0-3%2Bdeb13u3?arch=amd64&distro=debian-13.7&upstream=tiff` |
| deb | libtinfo6 | 6.5+20250216-2 | BSD-3-Clause, X11, MIT/X11 | Ncurses Maintainers <ncurses@packages.debian.org> | `pkg:deb/debian/libtinfo6@6.5%2B20250216-2?arch=amd64&distro=debian-13.7&upstream=ncurses` |
| deb | libudev1 | 257.13-1~deb13u1 | CC0-1.0, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, Expat, public-domain | Debian systemd Maintainers <pkg-systemd-maintainers@lists.alioth.debian.org> | `pkg:deb/debian/libudev1@257.13-1~deb13u1?arch=amd64&distro=debian-13.7&upstream=systemd` |
| deb | libunistring5 | 1.3-2 | BSD-3-Clause, GFDL-1.2-or-later, GFDL-1.3-or-later, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, Unicode-DFS-2016, X11, FreeSoftware, public-domain | Jörg Frings-Fürst <debian@jff.email> | `pkg:deb/debian/libunistring5@1.3-2?arch=amd64&distro=debian-13.7&upstream=libunistring` |
| deb | libuuid1 | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/libuuid1@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | libwebp7 | 1.5.0-0.1 | Apache-2.0, BSD-3-Clause | Jeff Breidenbach <jab@debian.org> | `pkg:deb/debian/libwebp7@1.5.0-0.1?arch=amd64&distro=debian-13.7&upstream=libwebp` |
| deb | libx11-6 | 2:1.8.12-1 | BSD-1-Clause, HPND, HPND-sell-variant, MIT | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libx11-6@2%3A1.8.12-1?arch=amd64&distro=debian-13.7&upstream=libx11` |
| deb | libx11-data | 2:1.8.12-1 | BSD-1-Clause, HPND, HPND-sell-variant, MIT | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libx11-data@2%3A1.8.12-1?arch=all&distro=debian-13.7&upstream=libx11` |
| deb | libxau6 | 1:1.0.11-1 | sha256:118dd263a7b91c8f21c489f949bf13281dff9e766deea92b829dac4dce66601a | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libxau6@1%3A1.0.11-1?arch=amd64&distro=debian-13.7&upstream=libxau` |
| deb | libxcb1 | 1.17.0-2+b1 | sha256:4f7cb9db6bf6542f5417e3d674c780d3a5fd12291a54d63054fb576ee0cfae80 | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libxcb1@1.17.0-2%2Bb1?arch=amd64&distro=debian-13.7&upstream=libxcb%401.17.0-2` |
| deb | libxdmcp6 | 1:1.1.5-1 | sha256:1bcbb50f8603fe8b86d330bfa460b772ea04fbd3c70e4499f0768b5340b9fd6e | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libxdmcp6@1%3A1.1.5-1?arch=amd64&distro=debian-13.7&upstream=libxdmcp` |
| deb | libxml2 | 2.12.7+dfsg+really2.9.14-2.1+deb13u3 | ISC, MIT-1 | Debian XML/SGML Group <debian-xml-sgml-pkgs@lists.alioth.debian.org> | `pkg:deb/debian/libxml2@2.12.7%2Bdfsg%2Breally2.9.14-2.1%2Bdeb13u3?arch=amd64&distro=debian-13.7` |
| deb | libxpm4 | 1:3.5.17-1+deb13u1 | MIT | Debian X Strike Force <debian-x@lists.debian.org> | `pkg:deb/debian/libxpm4@1%3A3.5.17-1%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=libxpm` |
| deb | libxslt1.1 | 1.1.35-1.2+deb13u3 | sha256:4b82c8dd6e55001a5921bea1d6db20be5c51e5976d892e870324026c23f37b6f | Debian XML/SGML Group <debian-xml-sgml-pkgs@lists.alioth.debian.org> | `pkg:deb/debian/libxslt1.1@1.1.35-1.2%2Bdeb13u3?arch=amd64&distro=debian-13.7&upstream=libxslt` |
| deb | libxxhash0 | 0.8.3-2 | BSD-2-Clause, GPL-2.0-only, GPL-2.0-or-later | Josue Ortega <josue@debian.org> | `pkg:deb/debian/libxxhash0@0.8.3-2?arch=amd64&distro=debian-13.7&upstream=xxhash` |
| deb | libyuv0 | 0.0.1904.20250204-1 | BSD-3-Clause, public-domain | Debian Multimedia Maintainers <debian-multimedia@lists.debian.org> | `pkg:deb/debian/libyuv0@0.0.1904.20250204-1?arch=amd64&distro=debian-13.7&upstream=libyuv` |
| deb | libzstd1 | 1.5.7+dfsg-1 | BSD-3-Clause, GPL-2.0-only, Zlib, Expat | RPM packaging team <team+pkg-rpm@tracker.debian.org> | `pkg:deb/debian/libzstd1@1.5.7%2Bdfsg-1?arch=amd64&distro=debian-13.7&upstream=libzstd` |
| deb | login | 1:4.16.0-2+really2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/login@1%3A4.16.0-2%2Breally2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux%402.41.5-0%2Bdeb13u1` |
| deb | login.defs | 1:4.17.4-2 | BSD-3-Clause, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later | Shadow package maintainers <pkg-shadow-devel@lists.alioth.debian.org> | `pkg:deb/debian/login.defs@1%3A4.17.4-2?arch=all&distro=debian-13.7&upstream=shadow` |
| deb | mawk | 1.3.4.20250131-1 | CC-BY-3.0, GPL-2.0-only, X11 | Boyuan Yang <byang@debian.org> | `pkg:deb/debian/mawk@1.3.4.20250131-1?arch=amd64&distro=debian-13.7` |
| deb | mount | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/mount@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=util-linux` |
| deb | ncurses-base | 6.5+20250216-2 | BSD-3-Clause, X11, MIT/X11 | Ncurses Maintainers <ncurses@packages.debian.org> | `pkg:deb/debian/ncurses-base@6.5%2B20250216-2?arch=all&distro=debian-13.7&upstream=ncurses` |
| deb | ncurses-bin | 6.5+20250216-2 | BSD-3-Clause, X11, MIT/X11 | Ncurses Maintainers <ncurses@packages.debian.org> | `pkg:deb/debian/ncurses-bin@6.5%2B20250216-2?arch=amd64&distro=debian-13.7&upstream=ncurses` |
| deb | nginx | 1.31.7-1~trixie | BSD-2-Clause | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx@1.31.7-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | nginx-module-acme | 1.31.7+0.4.1-1~trixie | Apache-2.0 | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx-module-acme@1.31.7%2B0.4.1-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | nginx-module-geoip | 1.31.7-1~trixie | BSD-2-Clause | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx-module-geoip@1.31.7-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | nginx-module-image-filter | 1.31.7-1~trixie | BSD-2-Clause | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx-module-image-filter@1.31.7-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | nginx-module-njs | 1.31.7+1.0.2-1~trixie | BSD-2-Clause | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx-module-njs@1.31.7%2B1.0.2-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | nginx-module-xslt | 1.31.7-1~trixie | BSD-2-Clause | NGINX Packaging <nginx-packaging@f5.com> | `pkg:deb/debian/nginx-module-xslt@1.31.7-1~trixie?arch=amd64&distro=debian-13.7` |
| deb | openssl | 3.5.7-1~deb13u3 | Apache-2.0, GPL-1.0-only, GPL-1.0-or-later, Artistic | Debian OpenSSL Team <pkg-openssl-devel@alioth-lists.debian.net> | `pkg:deb/debian/openssl@3.5.7-1~deb13u3?arch=amd64&distro=debian-13.7` |
| deb | openssl-provider-legacy | 3.5.7-1~deb13u3 | Apache-2.0, GPL-1.0-only, GPL-1.0-or-later, Artistic | Debian OpenSSL Team <pkg-openssl-devel@alioth-lists.debian.net> | `pkg:deb/debian/openssl-provider-legacy@3.5.7-1~deb13u3?arch=amd64&distro=debian-13.7&upstream=openssl` |
| deb | passwd | 1:4.17.4-2 | BSD-3-Clause, GPL-1.0-only, GPL-2.0-only, GPL-2.0-or-later | Shadow package maintainers <pkg-shadow-devel@lists.alioth.debian.org> | `pkg:deb/debian/passwd@1%3A4.17.4-2?arch=amd64&distro=debian-13.7&upstream=shadow` |
| deb | perl-base | 5.40.1-6+deb13u1 | Artistic-2.0, Artistic-dist, BSD-3-Clause, FSFAP, GPL-1.0-only, GPL-1.0-or-later, GPL-2.0-only, GPL-2.0-or-later, LGPL-2.1-only, Zlib, Artistic, BSD-3-clause-GENERIC, BSD-3-clause-with-weird-numbering, BSD-4-clause-POWERDOG, BZIP, DONT-CHANGE-THE-GPL, Expat, GPL-3+-WITH-BISON-EXCEPTION, REGCOMP, REGCOMP,, SDBM-PUBLIC-DOMAIN, TEXT-TABS, Unicode | Niko Tyni <ntyni@debian.org> | `pkg:deb/debian/perl-base@5.40.1-6%2Bdeb13u1?arch=amd64&distro=debian-13.7&upstream=perl` |
| deb | sed | 4.9-2+deb13u1 | BSD-4-Clause-UC, BSL-1.0, GFDL-1.3-only, GPL-3.0-only, GPL-3.0-or-later, ISC, X11, GFDL-NIV-1.3+, pcre | Clint Adams <clint@debian.org> | `pkg:deb/debian/sed@4.9-2%2Bdeb13u1?arch=amd64&distro=debian-13.7` |
| deb | sqv | 1.3.0-3+b2 | LGPL-2.0-only, LGPL-2.0-or-later | Debian Rust Maintainers <pkg-rust-maintainers@alioth-lists.debian.net> | `pkg:deb/debian/sqv@1.3.0-3%2Bb2?arch=amd64&distro=debian-13.7&upstream=rust-sequoia-sqv%401.3.0-3` |
| deb | sysvinit-utils | 3.14-4 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, LGPL-2.1-only, LGPL-2.1-or-later | Debian sysvinit maintainers <debian-init-diversity@chiark.greenend.org.uk> | `pkg:deb/debian/sysvinit-utils@3.14-4?arch=amd64&distro=debian-13.7&upstream=sysvinit` |
| deb | tar | 1.35+dfsg-3.1 | GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later | Janos Lenart <ocsi@debian.org> | `pkg:deb/debian/tar@1.35%2Bdfsg-3.1?arch=amd64&distro=debian-13.7` |
| deb | tzdata | 2026c-0+deb13u1 | public-domain | GNU Libc Maintainers <debian-glibc@lists.debian.org> | `pkg:deb/debian/tzdata@2026c-0%2Bdeb13u1?arch=all&distro=debian-13.7` |
| deb | util-linux | 2.41.5-0+deb13u1 | BSD-2-Clause, BSD-3-Clause, BSD-4-Clause, GPL-2.0-only, GPL-2.0-or-later, GPL-3.0-only, GPL-3.0-or-later, ISC, LGPL-2.0-only, LGPL-2.0-or-later, LGPL-2.1-only, LGPL-2.1-or-later, LGPL-3.0-only, LGPL-3.0-or-later, BSLA, Expat, LGPL, public-domain | Chris Hofstaedtler <zeha@debian.org> | `pkg:deb/debian/util-linux@2.41.5-0%2Bdeb13u1?arch=amd64&distro=debian-13.7` |
| deb | zlib1g | 1:1.3.dfsg+really1.3.1-1+b1 | Zlib | Mark Brown <broonie@debian.org> | `pkg:deb/debian/zlib1g@1%3A1.3.dfsg%2Breally1.3.1-1%2Bb1?arch=amd64&distro=debian-13.7&upstream=zlib%401%3A1.3.dfsg%2Breally1.3.1-1` |
| maven | libintl | 0.23.1 | - | - | `pkg:maven/libintl/libintl@0.23.1` |
| operating-system | debian | 13.7 | - | - | `-` |

## flight_review-certbot-image

ACME certificate renewal sidecar (certbot/certbot), production profile only

| Ecosystem | Name | Version | License | Supplier / publisher | purl |
|---|---|---|---|---|---|
| apk | .certbot-deps | 20260901.175409 | - | - | `pkg:apk/alpine/.certbot-deps@20260901.175409?arch=noarch&distro=alpine-3.23.5` |
| apk | .python-rundeps | 20260901.000242 | - | - | `pkg:apk/alpine/.python-rundeps@20260901.000242?arch=noarch&distro=alpine-3.23.5` |
| apk | alpine-baselayout | 3.7.2-r0 | GPL-2.0-only | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/alpine-baselayout@3.7.2-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | alpine-baselayout-data | 3.7.2-r0 | GPL-2.0-only | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/alpine-baselayout-data@3.7.2-r0?arch=x86_64&distro=alpine-3.23.5&upstream=alpine-baselayout` |
| apk | alpine-keys | 2.6-r0 | MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/alpine-keys@2.6-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | alpine-release | 3.23.5-r0 | MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/alpine-release@3.23.5-r0?arch=x86_64&distro=alpine-3.23.5&upstream=alpine-base` |
| apk | apk-tools | 3.0.6-r0 | GPL-2.0-only | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/apk-tools@3.0.6-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | binutils | 2.45.1-r0 | GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-3-Clause | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/binutils@2.45.1-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | busybox | 1.37.0-r30 | GPL-2.0-only | Sören Tempel <soeren+alpine@soeren-tempel.net> | `pkg:apk/alpine/busybox@1.37.0-r30?arch=x86_64&distro=alpine-3.23.5` |
| apk | busybox-binsh | 1.37.0-r30 | GPL-2.0-only | Sören Tempel <soeren+alpine@soeren-tempel.net> | `pkg:apk/alpine/busybox-binsh@1.37.0-r30?arch=x86_64&distro=alpine-3.23.5&upstream=busybox` |
| apk | ca-certificates | 20260611-r0 | MPL-2.0 AND MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/ca-certificates@20260611-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | ca-certificates-bundle | 20260611-r0 | MPL-2.0 AND MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/ca-certificates-bundle@20260611-r0?arch=x86_64&distro=alpine-3.23.5&upstream=ca-certificates` |
| apk | gdbm | 1.26-r0 | GPL-3.0-or-later | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/gdbm@1.26-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | jansson | 2.14.1-r0 | MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/jansson@2.14.1-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | libapk | 3.0.6-r0 | GPL-2.0-only | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libapk@3.0.6-r0?arch=x86_64&distro=alpine-3.23.5&upstream=apk-tools` |
| apk | libbz2 | 1.0.8-r6 | bzip2-1.0.6 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libbz2@1.0.8-r6?arch=x86_64&distro=alpine-3.23.5&upstream=bzip2` |
| apk | libcrypto3 | 3.5.8-r0 | Apache-2.0 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libcrypto3@3.5.8-r0?arch=x86_64&distro=alpine-3.23.5&upstream=openssl` |
| apk | libffi | 3.5.2-r0 | MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libffi@3.5.2-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | libgcc | 15.2.0-r2 | GPL-2.0-or-later AND LGPL-2.1-or-later | Ariadne Conill <ariadne@dereferenced.org> | `pkg:apk/alpine/libgcc@15.2.0-r2?arch=x86_64&distro=alpine-3.23.5&upstream=gcc` |
| apk | libncursesw | 6.5_p20251123-r0 | X11 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libncursesw@6.5_p20251123-r0?arch=x86_64&distro=alpine-3.23.5&upstream=ncurses` |
| apk | libpanelw | 6.5_p20251123-r0 | X11 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libpanelw@6.5_p20251123-r0?arch=x86_64&distro=alpine-3.23.5&upstream=ncurses` |
| apk | libssl3 | 3.5.8-r0 | Apache-2.0 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libssl3@3.5.8-r0?arch=x86_64&distro=alpine-3.23.5&upstream=openssl` |
| apk | libstdc++ | 15.2.0-r2 | GPL-2.0-or-later AND LGPL-2.1-or-later | Ariadne Conill <ariadne@dereferenced.org> | `pkg:apk/alpine/libstdc%2B%2B@15.2.0-r2?arch=x86_64&distro=alpine-3.23.5&upstream=gcc` |
| apk | libuuid | 2.41.4-r0 | BSD-3-Clause | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/libuuid@2.41.4-r0?arch=x86_64&distro=alpine-3.23.5&upstream=util-linux` |
| apk | musl | 1.2.5-r23 | MIT | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/musl@1.2.5-r23?arch=x86_64&distro=alpine-3.23.5` |
| apk | musl-utils | 1.2.5-r23 | MIT AND BSD-2-Clause AND GPL-2.0-or-later | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/musl-utils@1.2.5-r23?arch=x86_64&distro=alpine-3.23.5&upstream=musl` |
| apk | ncurses-terminfo-base | 6.5_p20251123-r0 | X11 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/ncurses-terminfo-base@6.5_p20251123-r0?arch=x86_64&distro=alpine-3.23.5&upstream=ncurses` |
| apk | openssl | 3.5.8-r0 | Apache-2.0 | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/openssl@3.5.8-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | readline | 8.3.1-r0 | GPL-3.0-or-later | Celeste <cielesti@protonmail.com> | `pkg:apk/alpine/readline@8.3.1-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | scanelf | 1.3.8-r2 | GPL-2.0-only | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/scanelf@1.3.8-r2?arch=x86_64&distro=alpine-3.23.5&upstream=pax-utils` |
| apk | sqlite-libs | 3.53.4-r0 | blessing | Celeste <cielesti@protonmail.com> | `pkg:apk/alpine/sqlite-libs@3.53.4-r0?arch=x86_64&distro=alpine-3.23.5&upstream=sqlite` |
| apk | ssl_client | 1.37.0-r30 | GPL-2.0-only | Sören Tempel <soeren+alpine@soeren-tempel.net> | `pkg:apk/alpine/ssl_client@1.37.0-r30?arch=x86_64&distro=alpine-3.23.5&upstream=busybox` |
| apk | tzdata | 2026c-r0 | Public-Domain | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/tzdata@2026c-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | xz-libs | 5.8.3-r0 | 0BSD, GPL-2.0-or-later, LGPL-2.1-or-later, AND, Public-Domain | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/xz-libs@5.8.3-r0?arch=x86_64&distro=alpine-3.23.5&upstream=xz` |
| apk | zlib | 1.3.2-r0 | Zlib | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/zlib@1.3.2-r0?arch=x86_64&distro=alpine-3.23.5` |
| apk | zstd-libs | 1.5.7-r2 | BSD-3-Clause OR GPL-2.0-or-later | Natanael Copa <ncopa@alpinelinux.org> | `pkg:apk/alpine/zstd-libs@1.5.7-r2?arch=x86_64&distro=alpine-3.23.5&upstream=zstd` |
| application | cli | UNKNOWN | - | - | `-` |
| application | cli-32 | UNKNOWN | - | - | `-` |
| application | cli-64 | UNKNOWN | - | - | `-` |
| application | cli-arm64 | UNKNOWN | - | - | `-` |
| application | gui | UNKNOWN | - | - | `-` |
| application | gui-32 | UNKNOWN | - | - | `-` |
| application | gui-64 | UNKNOWN | - | - | `-` |
| application | gui-arm64 | UNKNOWN | - | - | `-` |
| application | Simple Launcher | 1.1.0.14 | - | - | `-` |
| cargo | adler2 | 2.0.1 | - | - | `pkg:cargo/adler2@2.0.1` |
| cargo | aes | 0.8.4 | - | - | `pkg:cargo/aes@0.8.4` |
| cargo | aho-corasick | 1.1.4 | - | - | `pkg:cargo/aho-corasick@1.1.4` |
| cargo | allocator-api2 | 0.2.21 | - | - | `pkg:cargo/allocator-api2@0.2.21` |
| cargo | ambient-id | 0.0.11 | - | - | `pkg:cargo/ambient-id@0.0.11` |
| cargo | anstream | 1.0.0 | - | - | `pkg:cargo/anstream@1.0.0` |
| cargo | anstyle | 1.0.14 | - | - | `pkg:cargo/anstyle@1.0.14` |
| cargo | anstyle-parse | 1.0.0 | - | - | `pkg:cargo/anstyle-parse@1.0.0` |
| cargo | anstyle-query | 1.1.5 | - | - | `pkg:cargo/anstyle-query@1.1.5` |
| cargo | anyhow | 1.0.104 | - | - | `pkg:cargo/anyhow@1.0.104` |
| cargo | arcstr | 1.2.0 | - | - | `pkg:cargo/arcstr@1.2.0` |
| cargo | asn1-rs | 0.7.1 | - | - | `pkg:cargo/asn1-rs@0.7.1` |
| cargo | asn1-rs-impl | 0.2.0 | - | - | `pkg:cargo/asn1-rs-impl@0.2.0` |
| cargo | assert-json-diff | 2.0.2 | - | - | `pkg:cargo/assert-json-diff@2.0.2` |
| cargo | assert_cmd | 2.2.2 | - | - | `pkg:cargo/assert_cmd@2.2.2` |
| cargo | assert_fs | 1.1.4 | - | - | `pkg:cargo/assert_fs@1.1.4` |
| cargo | astral-pubgrub | 0.6.0 | - | - | `pkg:cargo/astral-pubgrub@0.6.0` |
| cargo | astral-reqwest-middleware | 0.5.1 | - | - | `pkg:cargo/astral-reqwest-middleware@0.5.1` |
| cargo | astral-reqwest-retry | 0.9.1 | - | - | `pkg:cargo/astral-reqwest-retry@0.9.1` |
| cargo | astral-tl | 0.7.11 | - | - | `pkg:cargo/astral-tl@0.7.11` |
| cargo | astral-tokio-tar | 0.6.4 | - | - | `pkg:cargo/astral-tokio-tar@0.6.4` |
| cargo | astral-version-ranges | 0.2.1 | - | - | `pkg:cargo/astral-version-ranges@0.2.1` |
| cargo | astral_async_http_range_reader | 0.11.0 | - | - | `pkg:cargo/astral_async_http_range_reader@0.11.0` |
| cargo | astral_async_zip | 0.0.20 | - | - | `pkg:cargo/astral_async_zip@0.0.20` |
| cargo | async-broadcast | 0.7.2 | - | - | `pkg:cargo/async-broadcast@0.7.2` |
| cargo | async-channel | 2.5.0 | - | - | `pkg:cargo/async-channel@2.5.0` |
| cargo | async-compression | 0.4.19 | - | - | `pkg:cargo/async-compression@0.4.19` |
| cargo | async-recursion | 1.1.1 | - | - | `pkg:cargo/async-recursion@1.1.1` |
| cargo | async-trait | 0.1.89 | - | - | `pkg:cargo/async-trait@0.1.89` |
| cargo | atomic-waker | 1.1.2 | - | - | `pkg:cargo/atomic-waker@1.1.2` |
| cargo | aws-lc-rs | 1.16.2 | - | - | `pkg:cargo/aws-lc-rs@1.16.2` |
| cargo | aws-lc-sys | 0.39.0 | - | - | `pkg:cargo/aws-lc-sys@0.39.0` |
| cargo | axoasset | 2.0.1 | - | - | `pkg:cargo/axoasset@2.0.1` |
| cargo | axoprocess | 0.2.1 | - | - | `pkg:cargo/axoprocess@0.2.1` |
| cargo | axotag | 0.3.0 | - | - | `pkg:cargo/axotag@0.3.0` |
| cargo | axoupdater | 0.10.0 | - | - | `pkg:cargo/axoupdater@0.10.0` |
| cargo | base64 | 0.22.1 | - | - | `pkg:cargo/base64@0.22.1` |
| cargo | base64 | 0.23.1 | - | - | `pkg:cargo/base64@0.23.1` |
| cargo | base64ct | 1.8.3 | - | - | `pkg:cargo/base64ct@1.8.3` |
| cargo | bitflags | 1.3.2 | - | - | `pkg:cargo/bitflags@1.3.2` |
| cargo | bitflags | 2.13.1 | - | - | `pkg:cargo/bitflags@2.13.1` |
| cargo | blake2 | 0.11.0-rc.6 | - | - | `pkg:cargo/blake2@0.11.0-rc.6` |
| cargo | block-buffer | 0.10.4 | - | - | `pkg:cargo/block-buffer@0.10.4` |
| cargo | block-buffer | 0.12.1 | - | - | `pkg:cargo/block-buffer@0.12.1` |
| cargo | block-padding | 0.3.3 | - | - | `pkg:cargo/block-padding@0.3.3` |
| cargo | borrow-or-share | 0.2.4 | - | - | `pkg:cargo/borrow-or-share@0.2.4` |
| cargo | boxcar | 0.2.14 | - | - | `pkg:cargo/boxcar@0.2.14` |
| cargo | bstr | 1.12.1 | - | - | `pkg:cargo/bstr@1.12.1` |
| cargo | bytecheck | 0.8.2 | - | - | `pkg:cargo/bytecheck@0.8.2` |
| cargo | bytemuck | 1.25.0 | - | - | `pkg:cargo/bytemuck@1.25.0` |
| cargo | byteorder-lite | 0.1.0 | - | - | `pkg:cargo/byteorder-lite@0.1.0` |
| cargo | bytes | 1.12.1 | - | - | `pkg:cargo/bytes@1.12.1` |
| cargo | camino | 1.2.2 | - | - | `pkg:cargo/camino@1.2.2` |
| cargo | cargo-util | 0.2.30 | - | - | `pkg:cargo/cargo-util@0.2.30` |
| cargo | cbc | 0.1.2 | - | - | `pkg:cargo/cbc@0.1.2` |
| cargo | cfg-if | 1.0.4 | - | - | `pkg:cargo/cfg-if@1.0.4` |
| cargo | charset | 0.1.5 | - | - | `pkg:cargo/charset@0.1.5` |
| cargo | cipher | 0.4.4 | - | - | `pkg:cargo/cipher@0.4.4` |
| cargo | clap | 4.6.4 | - | - | `pkg:cargo/clap@4.6.4` |
| cargo | clap_builder | 4.6.2 | - | - | `pkg:cargo/clap_builder@4.6.2` |
| cargo | clap_complete | 4.6.0 | - | - | `pkg:cargo/clap_complete@4.6.0` |
| cargo | clap_complete_command | 0.6.1 | - | - | `pkg:cargo/clap_complete_command@0.6.1` |
| cargo | clap_complete_nushell | 4.6.0 | - | - | `pkg:cargo/clap_complete_nushell@4.6.0` |
| cargo | clap_lex | 1.1.0 | - | - | `pkg:cargo/clap_lex@1.1.0` |
| cargo | cmov | 0.5.4 | - | - | `pkg:cargo/cmov@0.5.4` |
| cargo | colorchoice | 1.0.5 | - | - | `pkg:cargo/colorchoice@1.0.5` |
| cargo | concurrent-queue | 2.5.0 | - | - | `pkg:cargo/concurrent-queue@2.5.0` |
| cargo | configparser | 3.2.0 | - | - | `pkg:cargo/configparser@3.2.0` |
| cargo | console | 0.16.4 | - | - | `pkg:cargo/console@0.16.4` |
| cargo | const-oid | 0.10.2 | - | - | `pkg:cargo/const-oid@0.10.2` |
| cargo | const-oid | 0.9.6 | - | - | `pkg:cargo/const-oid@0.9.6` |
| cargo | const-random | 0.1.18 | - | - | `pkg:cargo/const-random@0.1.18` |
| cargo | cpufeatures | 0.2.17 | - | - | `pkg:cargo/cpufeatures@0.2.17` |
| cargo | cpufeatures | 0.3.0 | - | - | `pkg:cargo/cpufeatures@0.3.0` |
| cargo | crc32fast | 1.5.0 | - | - | `pkg:cargo/crc32fast@1.5.0` |
| cargo | crossbeam-channel | 0.5.15 | - | - | `pkg:cargo/crossbeam-channel@0.5.15` |
| cargo | crossbeam-deque | 0.8.6 | - | - | `pkg:cargo/crossbeam-deque@0.8.6` |
| cargo | crossbeam-epoch | 0.9.18 | - | - | `pkg:cargo/crossbeam-epoch@0.9.18` |
| cargo | crossbeam-utils | 0.8.21 | - | - | `pkg:cargo/crossbeam-utils@0.8.21` |
| cargo | crypto-common | 0.1.7 | - | - | `pkg:cargo/crypto-common@0.1.7` |
| cargo | crypto-common | 0.2.2 | - | - | `pkg:cargo/crypto-common@0.2.2` |
| cargo | csv | 1.4.0 | - | - | `pkg:cargo/csv@1.4.0` |
| cargo | csv-core | 0.1.13 | - | - | `pkg:cargo/csv-core@0.1.13` |
| cargo | ctrlc | 3.5.2 | - | - | `pkg:cargo/ctrlc@3.5.2` |
| cargo | ctutils | 0.4.2 | - | - | `pkg:cargo/ctutils@0.4.2` |
| cargo | cyclonedx-bom | 0.8.1 | - | - | `pkg:cargo/cyclonedx-bom@0.8.1` |
| cargo | cyclonedx-bom-macros | 0.1.0 | - | - | `pkg:cargo/cyclonedx-bom-macros@0.1.0` |
| cargo | data-encoding | 2.11.0 | - | - | `pkg:cargo/data-encoding@2.11.0` |
| cargo | deadpool | 0.12.3 | - | - | `pkg:cargo/deadpool@0.12.3` |
| cargo | deadpool-runtime | 0.1.4 | - | - | `pkg:cargo/deadpool-runtime@0.1.4` |
| cargo | defmt | 1.1.0 | - | - | `pkg:cargo/defmt@1.1.0` |
| cargo | defmt-macros | 1.1.0 | - | - | `pkg:cargo/defmt-macros@1.1.0` |
| cargo | defmt-parser | 1.0.0 | - | - | `pkg:cargo/defmt-parser@1.0.0` |
| cargo | der | 0.7.10 | - | - | `pkg:cargo/der@0.7.10` |
| cargo | der-parser | 10.0.0 | - | - | `pkg:cargo/der-parser@10.0.0` |
| cargo | deranged | 0.5.8 | - | - | `pkg:cargo/deranged@0.5.8` |
| cargo | difflib | 0.4.0 | - | - | `pkg:cargo/difflib@0.4.0` |
| cargo | digest | 0.10.7 | - | - | `pkg:cargo/digest@0.10.7` |
| cargo | digest | 0.11.3 | - | - | `pkg:cargo/digest@0.11.3` |
| cargo | dirs | 6.0.0 | - | - | `pkg:cargo/dirs@6.0.0` |
| cargo | dirs-sys | 0.5.0 | - | - | `pkg:cargo/dirs-sys@0.5.0` |
| cargo | diskus | 0.9.0 | - | - | `pkg:cargo/diskus@0.9.0` |
| cargo | displaydoc | 0.2.5 | - | - | `pkg:cargo/displaydoc@0.2.5` |
| cargo | dlv-list | 0.5.2 | - | - | `pkg:cargo/dlv-list@0.5.2` |
| cargo | dotenvy | 0.15.7 | - | - | `pkg:cargo/dotenvy@0.15.7` |
| cargo | dunce | 1.0.5 | - | - | `pkg:cargo/dunce@1.0.5` |
| cargo | dyn-clone | 1.0.20 | - | - | `pkg:cargo/dyn-clone@1.0.20` |
| cargo | either | 1.17.0 | - | - | `pkg:cargo/either@1.17.0` |
| cargo | encoding_rs | 0.8.35 | - | - | `pkg:cargo/encoding_rs@0.8.35` |
| cargo | encoding_rs_io | 0.1.7 | - | - | `pkg:cargo/encoding_rs_io@0.1.7` |
| cargo | endi | 1.1.1 | - | - | `pkg:cargo/endi@1.1.1` |
| cargo | enumflags2 | 0.7.12 | - | - | `pkg:cargo/enumflags2@0.7.12` |
| cargo | equivalent | 1.0.2 | - | - | `pkg:cargo/equivalent@1.0.2` |
| cargo | erased-serde | 0.4.10 | - | - | `pkg:cargo/erased-serde@0.4.10` |
| cargo | errno | 0.3.14 | - | - | `pkg:cargo/errno@0.3.14` |
| cargo | etcetera | 0.11.0 | - | - | `pkg:cargo/etcetera@0.11.0` |
| cargo | event-listener | 5.4.1 | - | - | `pkg:cargo/event-listener@5.4.1` |
| cargo | event-listener-strategy | 0.5.4 | - | - | `pkg:cargo/event-listener-strategy@0.5.4` |
| cargo | fastrand | 2.5.0 | - | - | `pkg:cargo/fastrand@2.5.0` |
| cargo | filetime | 0.2.29 | - | - | `pkg:cargo/filetime@0.2.29` |
| cargo | fixedbitset | 0.5.7 | - | - | `pkg:cargo/fixedbitset@0.5.7` |
| cargo | flate2 | 1.1.9 | - | - | `pkg:cargo/flate2@1.1.9` |
| cargo | float-cmp | 0.10.0 | - | - | `pkg:cargo/float-cmp@0.10.0` |
| cargo | fluent-uri | 0.4.1 | - | - | `pkg:cargo/fluent-uri@0.4.1` |
| cargo | fnv | 1.0.7 | - | - | `pkg:cargo/fnv@1.0.7` |
| cargo | foldhash | 0.1.5 | - | - | `pkg:cargo/foldhash@0.1.5` |
| cargo | foldhash | 0.2.0 | - | - | `pkg:cargo/foldhash@0.2.0` |
| cargo | form_urlencoded | 1.2.2 | - | - | `pkg:cargo/form_urlencoded@1.2.2` |
| cargo | fs-err | 3.3.1 | - | - | `pkg:cargo/fs-err@3.3.1` |
| cargo | futures | 0.3.33 | - | - | `pkg:cargo/futures@0.3.33` |
| cargo | futures-channel | 0.3.33 | - | - | `pkg:cargo/futures-channel@0.3.33` |
| cargo | futures-core | 0.3.33 | - | - | `pkg:cargo/futures-core@0.3.33` |
| cargo | futures-executor | 0.3.33 | - | - | `pkg:cargo/futures-executor@0.3.33` |
| cargo | futures-io | 0.3.33 | - | - | `pkg:cargo/futures-io@0.3.33` |
| cargo | futures-lite | 2.6.1 | - | - | `pkg:cargo/futures-lite@2.6.1` |
| cargo | futures-sink | 0.3.33 | - | - | `pkg:cargo/futures-sink@0.3.33` |
| cargo | futures-task | 0.3.33 | - | - | `pkg:cargo/futures-task@0.3.33` |
| cargo | futures-util | 0.3.33 | - | - | `pkg:cargo/futures-util@0.3.33` |
| cargo | generic-array | 0.14.7 | - | - | `pkg:cargo/generic-array@0.14.7` |
| cargo | getrandom | 0.2.16 | - | - | `pkg:cargo/getrandom@0.2.16` |
| cargo | getrandom | 0.3.4 | - | - | `pkg:cargo/getrandom@0.3.4` |
| cargo | getrandom | 0.4.3 | - | - | `pkg:cargo/getrandom@0.4.3` |
| cargo | glob | 0.3.4 | - | - | `pkg:cargo/glob@0.3.4` |
| cargo | globset | 0.4.19 | - | - | `pkg:cargo/globset@0.4.19` |
| cargo | globwalk | 0.9.1 | - | - | `pkg:cargo/globwalk@0.9.1` |
| cargo | goblin | 0.10.7 | - | - | `pkg:cargo/goblin@0.10.7` |
| cargo | h2 | 0.4.15 | - | - | `pkg:cargo/h2@0.4.15` |
| cargo | hashbrown | 0.14.5 | - | - | `pkg:cargo/hashbrown@0.14.5` |
| cargo | hashbrown | 0.15.5 | - | - | `pkg:cargo/hashbrown@0.15.5` |
| cargo | hashbrown | 0.17.1 | - | - | `pkg:cargo/hashbrown@0.17.1` |
| cargo | hex | 0.4.3 | - | - | `pkg:cargo/hex@0.4.3` |
| cargo | hkdf | 0.12.4 | - | - | `pkg:cargo/hkdf@0.12.4` |
| cargo | hmac | 0.12.1 | - | - | `pkg:cargo/hmac@0.12.1` |
| cargo | hmac | 0.13.0 | - | - | `pkg:cargo/hmac@0.13.0` |
| cargo | homedir | 0.3.6 | - | - | `pkg:cargo/homedir@0.3.6` |
| cargo | html-escape | 0.2.14 | - | - | `pkg:cargo/html-escape@0.2.14` |
| cargo | http | 1.4.2 | - | - | `pkg:cargo/http@1.4.2` |
| cargo | http-body | 1.0.1 | - | - | `pkg:cargo/http-body@1.0.1` |
| cargo | http-body-util | 0.1.4 | - | - | `pkg:cargo/http-body-util@0.1.4` |
| cargo | http-content-range | 0.2.4 | - | - | `pkg:cargo/http-content-range@0.2.4` |
| cargo | httparse | 1.10.1 | - | - | `pkg:cargo/httparse@1.10.1` |
| cargo | httpdate | 1.0.3 | - | - | `pkg:cargo/httpdate@1.0.3` |
| cargo | hybrid-array | 0.4.13 | - | - | `pkg:cargo/hybrid-array@0.4.13` |
| cargo | hyper | 1.10.1 | - | - | `pkg:cargo/hyper@1.10.1` |
| cargo | hyper-rustls | 0.27.7 | - | - | `pkg:cargo/hyper-rustls@0.27.7` |
| cargo | hyper-util | 0.1.20 | - | - | `pkg:cargo/hyper-util@0.1.20` |
| cargo | icu_collections | 2.1.1 | - | - | `pkg:cargo/icu_collections@2.1.1` |
| cargo | icu_locale_core | 2.1.1 | - | - | `pkg:cargo/icu_locale_core@2.1.1` |
| cargo | icu_normalizer | 2.1.1 | - | - | `pkg:cargo/icu_normalizer@2.1.1` |
| cargo | icu_normalizer_data | 2.1.1 | - | - | `pkg:cargo/icu_normalizer_data@2.1.1` |
| cargo | icu_properties | 2.1.2 | - | - | `pkg:cargo/icu_properties@2.1.2` |
| cargo | icu_properties_data | 2.1.2 | - | - | `pkg:cargo/icu_properties_data@2.1.2` |
| cargo | icu_provider | 2.1.1 | - | - | `pkg:cargo/icu_provider@2.1.1` |
| cargo | idna | 1.1.0 | - | - | `pkg:cargo/idna@1.1.0` |
| cargo | idna_adapter | 1.2.1 | - | - | `pkg:cargo/idna_adapter@1.2.1` |
| cargo | ignore | 0.4.31 | - | - | `pkg:cargo/ignore@0.4.31` |
| cargo | image | 0.25.10 | - | - | `pkg:cargo/image@0.25.10` |
| cargo | indexmap | 2.14.0 | - | - | `pkg:cargo/indexmap@2.14.0` |
| cargo | indicatif | 0.18.6 | - | - | `pkg:cargo/indicatif@0.18.6` |
| cargo | indoc | 2.0.7 | - | - | `pkg:cargo/indoc@2.0.7` |
| cargo | inout | 0.1.4 | - | - | `pkg:cargo/inout@0.1.4` |
| cargo | insta | 1.48.0 | - | - | `pkg:cargo/insta@1.48.0` |
| cargo | ipnet | 2.12.0 | - | - | `pkg:cargo/ipnet@2.12.0` |
| cargo | iri-string | 0.7.10 | - | - | `pkg:cargo/iri-string@0.7.10` |
| cargo | is-docker | 0.2.0 | - | - | `pkg:cargo/is-docker@0.2.0` |
| cargo | is-wsl | 0.4.0 | - | - | `pkg:cargo/is-wsl@0.4.0` |
| cargo | is_ci | 1.2.0 | - | - | `pkg:cargo/is_ci@1.2.0` |
| cargo | is_terminal_polyfill | 1.70.2 | - | - | `pkg:cargo/is_terminal_polyfill@1.70.2` |
| cargo | itertools | 0.14.0 | - | - | `pkg:cargo/itertools@0.14.0` |
| cargo | itoa | 1.0.17 | - | - | `pkg:cargo/itoa@1.0.17` |
| cargo | jiff | 0.2.35 | - | - | `pkg:cargo/jiff@0.2.35` |
| cargo | jiff-core | 0.1.0 | - | - | `pkg:cargo/jiff-core@0.1.0` |
| cargo | jobserver | 0.1.35 | - | - | `pkg:cargo/jobserver@0.1.35` |
| cargo | lazy_static | 1.5.0 | - | - | `pkg:cargo/lazy_static@1.5.0` |
| cargo | libc | 0.2.186 | - | - | `pkg:cargo/libc@0.2.186` |
| cargo | libm | 0.2.16 | - | - | `pkg:cargo/libm@0.2.16` |
| cargo | linux-raw-sys | 0.12.1 | - | - | `pkg:cargo/linux-raw-sys@0.12.1` |
| cargo | litemap | 0.8.1 | - | - | `pkg:cargo/litemap@0.8.1` |
| cargo | lock_api | 0.4.14 | - | - | `pkg:cargo/lock_api@0.4.14` |
| cargo | log | 0.4.29 | - | - | `pkg:cargo/log@0.4.29` |
| cargo | lru-slab | 0.1.2 | - | - | `pkg:cargo/lru-slab@0.1.2` |
| cargo | mailparse | 0.16.1 | - | - | `pkg:cargo/mailparse@0.16.1` |
| cargo | matchers | 0.2.0 | - | - | `pkg:cargo/matchers@0.2.0` |
| cargo | md-5 | 0.11.0 | - | - | `pkg:cargo/md-5@0.11.0` |
| cargo | memchr | 2.8.3 | - | - | `pkg:cargo/memchr@2.8.3` |
| cargo | memmap2 | 0.9.10 | - | - | `pkg:cargo/memmap2@0.9.10` |
| cargo | miette | 7.6.0 | - | - | `pkg:cargo/miette@7.6.0` |
| cargo | mime | 0.3.17 | - | - | `pkg:cargo/mime@0.3.17` |
| cargo | mime_guess | 2.0.5 | - | - | `pkg:cargo/mime_guess@2.0.5` |
| cargo | minimal-lexical | 0.2.1 | - | - | `pkg:cargo/minimal-lexical@0.2.1` |
| cargo | miniz_oxide | 0.8.9 | - | - | `pkg:cargo/miniz_oxide@0.8.9` |
| cargo | mio | 1.2.0 | - | - | `pkg:cargo/mio@1.2.0` |
| cargo | moxcms | 0.8.1 | - | - | `pkg:cargo/moxcms@0.8.1` |
| cargo | munge | 0.4.7 | - | - | `pkg:cargo/munge@0.4.7` |
| cargo | nix | 0.30.1 | - | - | `pkg:cargo/nix@0.30.1` |
| cargo | nix | 0.31.3 | - | - | `pkg:cargo/nix@0.31.3` |
| cargo | nom | 7.1.3 | - | - | `pkg:cargo/nom@7.1.3` |
| cargo | normalize-line-endings | 0.3.0 | - | - | `pkg:cargo/normalize-line-endings@0.3.0` |
| cargo | nu-ansi-term | 0.50.3 | - | - | `pkg:cargo/nu-ansi-term@0.50.3` |
| cargo | num | 0.4.3 | - | - | `pkg:cargo/num@0.4.3` |
| cargo | num-bigint | 0.4.6 | - | - | `pkg:cargo/num-bigint@0.4.6` |
| cargo | num-bigint-dig | 0.8.6 | - | - | `pkg:cargo/num-bigint-dig@0.8.6` |
| cargo | num-complex | 0.4.6 | - | - | `pkg:cargo/num-complex@0.4.6` |
| cargo | num-conv | 0.2.0 | - | - | `pkg:cargo/num-conv@0.2.0` |
| cargo | num-integer | 0.1.46 | - | - | `pkg:cargo/num-integer@0.1.46` |
| cargo | num-iter | 0.1.45 | - | - | `pkg:cargo/num-iter@0.1.45` |
| cargo | num-rational | 0.4.2 | - | - | `pkg:cargo/num-rational@0.4.2` |
| cargo | num-traits | 0.2.19 | - | - | `pkg:cargo/num-traits@0.2.19` |
| cargo | num_cpus | 1.17.0 | - | - | `pkg:cargo/num_cpus@1.17.0` |
| cargo | oid-registry | 0.8.1 | - | - | `pkg:cargo/oid-registry@0.8.1` |
| cargo | once_cell | 1.21.4 | - | - | `pkg:cargo/once_cell@1.21.4` |
| cargo | open | 5.4.0 | - | - | `pkg:cargo/open@5.4.0` |
| cargo | openssl-probe | 0.2.1 | - | - | `pkg:cargo/openssl-probe@0.2.1` |
| cargo | option-ext | 0.2.0 | - | - | `pkg:cargo/option-ext@0.2.0` |
| cargo | ordered-float | 5.3.0 | - | - | `pkg:cargo/ordered-float@5.3.0` |
| cargo | ordered-multimap | 0.7.3 | - | - | `pkg:cargo/ordered-multimap@0.7.3` |
| cargo | ordered-stream | 0.2.0 | - | - | `pkg:cargo/ordered-stream@0.2.0` |
| cargo | os_str_bytes | 6.6.1 | - | - | `pkg:cargo/os_str_bytes@6.6.1` |
| cargo | owo-colors | 4.3.0 | - | - | `pkg:cargo/owo-colors@4.3.0` |
| cargo | papaya | 0.2.4 | - | - | `pkg:cargo/papaya@0.2.4` |
| cargo | parking | 2.2.1 | - | - | `pkg:cargo/parking@2.2.1` |
| cargo | parking_lot | 0.12.5 | - | - | `pkg:cargo/parking_lot@0.12.5` |
| cargo | parking_lot_core | 0.9.12 | - | - | `pkg:cargo/parking_lot_core@0.9.12` |
| cargo | path-slash | 0.2.1 | - | - | `pkg:cargo/path-slash@0.2.1` |
| cargo | pathdiff | 0.2.3 | - | - | `pkg:cargo/pathdiff@0.2.3` |
| cargo | pbkdf2 | 0.12.2 | - | - | `pkg:cargo/pbkdf2@0.12.2` |
| cargo | pem | 3.0.6 | - | - | `pkg:cargo/pem@3.0.6` |
| cargo | pem-rfc7468 | 0.7.0 | - | - | `pkg:cargo/pem-rfc7468@0.7.0` |
| cargo | percent-encoding | 2.3.2 | - | - | `pkg:cargo/percent-encoding@2.3.2` |
| cargo | pest | 2.8.6 | - | - | `pkg:cargo/pest@2.8.6` |
| cargo | pest_derive | 2.8.6 | - | - | `pkg:cargo/pest_derive@2.8.6` |
| cargo | pest_generator | 2.8.6 | - | - | `pkg:cargo/pest_generator@2.8.6` |
| cargo | pest_meta | 2.8.6 | - | - | `pkg:cargo/pest_meta@2.8.6` |
| cargo | petgraph | 0.8.3 | - | - | `pkg:cargo/petgraph@0.8.3` |
| cargo | pin-project | 1.1.11 | - | - | `pkg:cargo/pin-project@1.1.11` |
| cargo | pin-project-lite | 0.2.17 | - | - | `pkg:cargo/pin-project-lite@0.2.17` |
| cargo | pkcs1 | 0.7.5 | - | - | `pkg:cargo/pkcs1@0.7.5` |
| cargo | pkcs5 | 0.7.1 | - | - | `pkg:cargo/pkcs5@0.7.1` |
| cargo | pkcs8 | 0.10.2 | - | - | `pkg:cargo/pkcs8@0.10.2` |
| cargo | plain | 0.2.3 | - | - | `pkg:cargo/plain@0.2.3` |
| cargo | portable-atomic | 1.13.1 | - | - | `pkg:cargo/portable-atomic@1.13.1` |
| cargo | potential_utf | 0.1.4 | - | - | `pkg:cargo/potential_utf@0.1.4` |
| cargo | powerfmt | 0.2.0 | - | - | `pkg:cargo/powerfmt@0.2.0` |
| cargo | ppv-lite86 | 0.2.21 | - | - | `pkg:cargo/ppv-lite86@0.2.21` |
| cargo | predicates | 3.1.4 | - | - | `pkg:cargo/predicates@3.1.4` |
| cargo | predicates-core | 1.0.10 | - | - | `pkg:cargo/predicates-core@1.0.10` |
| cargo | predicates-tree | 1.0.13 | - | - | `pkg:cargo/predicates-tree@1.0.13` |
| cargo | priority-queue | 2.7.0 | - | - | `pkg:cargo/priority-queue@2.7.0` |
| cargo | proc-macro-crate | 3.5.0 | - | - | `pkg:cargo/proc-macro-crate@3.5.0` |
| cargo | proc-macro-error2 | 2.0.1 | - | - | `pkg:cargo/proc-macro-error2@2.0.1` |
| cargo | proc-macro2 | 1.0.107 | - | - | `pkg:cargo/proc-macro2@1.0.107` |
| cargo | procfs | 0.18.0 | - | - | `pkg:cargo/procfs@0.18.0` |
| cargo | procfs-core | 0.18.0 | - | - | `pkg:cargo/procfs-core@0.18.0` |
| cargo | ptr_meta | 0.3.1 | - | - | `pkg:cargo/ptr_meta@0.3.1` |
| cargo | purl | 0.1.6 | - | - | `pkg:cargo/purl@0.1.6` |
| cargo | pxfm | 0.1.28 | - | - | `pkg:cargo/pxfm@0.1.28` |
| cargo | quick-xml | 0.41.0 | - | - | `pkg:cargo/quick-xml@0.41.0` |
| cargo | quinn | 0.11.9 | - | - | `pkg:cargo/quinn@0.11.9` |
| cargo | quinn-proto | 0.11.15 | - | - | `pkg:cargo/quinn-proto@0.11.15` |
| cargo | quinn-udp | 0.5.15 | - | - | `pkg:cargo/quinn-udp@0.5.15` |
| cargo | quote | 1.0.47 | - | - | `pkg:cargo/quote@1.0.47` |
| cargo | quoted_printable | 0.5.1 | - | - | `pkg:cargo/quoted_printable@0.5.1` |
| cargo | rancor | 0.1.1 | - | - | `pkg:cargo/rancor@0.1.1` |
| cargo | rand | 0.8.6 | - | - | `pkg:cargo/rand@0.8.6` |
| cargo | rand | 0.9.4 | - | - | `pkg:cargo/rand@0.9.4` |
| cargo | rand_chacha | 0.3.1 | - | - | `pkg:cargo/rand_chacha@0.3.1` |
| cargo | rand_chacha | 0.9.0 | - | - | `pkg:cargo/rand_chacha@0.9.0` |
| cargo | rand_core | 0.6.4 | - | - | `pkg:cargo/rand_core@0.6.4` |
| cargo | rand_core | 0.9.5 | - | - | `pkg:cargo/rand_core@0.9.5` |
| cargo | rayon | 1.12.0 | - | - | `pkg:cargo/rayon@1.12.0` |
| cargo | rayon-core | 1.13.0 | - | - | `pkg:cargo/rayon-core@1.13.0` |
| cargo | ref-cast | 1.0.26 | - | - | `pkg:cargo/ref-cast@1.0.26` |
| cargo | reflink-copy | 0.1.30 | - | - | `pkg:cargo/reflink-copy@0.1.30` |
| cargo | regex | 1.13.1 | - | - | `pkg:cargo/regex@1.13.1` |
| cargo | regex-automata | 0.4.16 | - | - | `pkg:cargo/regex-automata@0.4.16` |
| cargo | regex-syntax | 0.8.11 | - | - | `pkg:cargo/regex-syntax@0.8.11` |
| cargo | rend | 0.5.3 | - | - | `pkg:cargo/rend@0.5.3` |
| cargo | reqsign | 0.20.3 | - | - | `pkg:cargo/reqsign@0.20.3` |
| cargo | reqsign-aws-core | 3.0.3 | - | - | `pkg:cargo/reqsign-aws-core@3.0.3` |
| cargo | reqsign-aws-v4 | 3.1.0 | - | - | `pkg:cargo/reqsign-aws-v4@3.1.0` |
| cargo | reqsign-azure-storage | 3.1.2 | - | - | `pkg:cargo/reqsign-azure-storage@3.1.2` |
| cargo | reqsign-command-execute-tokio | 3.0.4 | - | - | `pkg:cargo/reqsign-command-execute-tokio@3.0.4` |
| cargo | reqsign-core | 3.2.1 | - | - | `pkg:cargo/reqsign-core@3.2.1` |
| cargo | reqsign-file-read-tokio | 3.0.4 | - | - | `pkg:cargo/reqsign-file-read-tokio@3.0.4` |
| cargo | reqsign-google | 3.0.4 | - | - | `pkg:cargo/reqsign-google@3.0.4` |
| cargo | reqsign-http-send-reqwest | 4.0.4 | - | - | `pkg:cargo/reqsign-http-send-reqwest@4.0.4` |
| cargo | reqwest | 0.13.4 | - | - | `pkg:cargo/reqwest@0.13.4` |
| cargo | retry-policies | 0.5.1 | - | - | `pkg:cargo/retry-policies@0.5.1` |
| cargo | ring | 0.17.14 | - | - | `pkg:cargo/ring@0.17.14` |
| cargo | rkyv | 0.8.17 | - | - | `pkg:cargo/rkyv@0.8.17` |
| cargo | rmp | 0.8.15 | - | - | `pkg:cargo/rmp@0.8.15` |
| cargo | rmp-serde | 1.3.1 | - | - | `pkg:cargo/rmp-serde@1.3.1` |
| cargo | rsa | 0.9.10 | - | - | `pkg:cargo/rsa@0.9.10` |
| cargo | rust-ini | 0.21.3 | - | - | `pkg:cargo/rust-ini@0.21.3` |
| cargo | rustc-hash | 2.1.3 | - | - | `pkg:cargo/rustc-hash@2.1.3` |
| cargo | rusticata-macros | 4.1.0 | - | - | `pkg:cargo/rusticata-macros@4.1.0` |
| cargo | rustix | 1.1.4 | - | - | `pkg:cargo/rustix@1.1.4` |
| cargo | rustls | 0.23.42 | - | - | `pkg:cargo/rustls@0.23.42` |
| cargo | rustls-native-certs | 0.8.4 | - | - | `pkg:cargo/rustls-native-certs@0.8.4` |
| cargo | rustls-pki-types | 1.15.1 | - | - | `pkg:cargo/rustls-pki-types@1.15.1` |
| cargo | rustls-platform-verifier | 0.7.0 | - | - | `pkg:cargo/rustls-platform-verifier@0.7.0` |
| cargo | rustls-webpki | 0.103.13 | - | - | `pkg:cargo/rustls-webpki@0.103.13` |
| cargo | ryu | 1.0.23 | - | - | `pkg:cargo/ryu@1.0.23` |
| cargo | salsa20 | 0.10.2 | - | - | `pkg:cargo/salsa20@0.10.2` |
| cargo | same-file | 1.0.6 | - | - | `pkg:cargo/same-file@1.0.6` |
| cargo | schemars | 1.2.1 | - | - | `pkg:cargo/schemars@1.2.1` |
| cargo | scopeguard | 1.2.0 | - | - | `pkg:cargo/scopeguard@1.2.0` |
| cargo | scroll | 0.13.0 | - | - | `pkg:cargo/scroll@0.13.0` |
| cargo | scrypt | 0.11.0 | - | - | `pkg:cargo/scrypt@0.11.0` |
| cargo | seahash | 4.1.0 | - | - | `pkg:cargo/seahash@4.1.0` |
| cargo | secrecy | 0.10.3 | - | - | `pkg:cargo/secrecy@0.10.3` |
| cargo | secret-service | 5.1.0 | - | - | `pkg:cargo/secret-service@5.1.0` |
| cargo | seize | 0.5.1 | - | - | `pkg:cargo/seize@0.5.1` |
| cargo | semver | 1.0.27 | - | - | `pkg:cargo/semver@1.0.27` |
| cargo | serde | 1.0.229 | - | - | `pkg:cargo/serde@1.0.229` |
| cargo | serde-untagged | 0.1.9 | - | - | `pkg:cargo/serde-untagged@0.1.9` |
| cargo | serde_core | 1.0.229 | - | - | `pkg:cargo/serde_core@1.0.229` |
| cargo | serde_json | 1.0.151 | - | - | `pkg:cargo/serde_json@1.0.151` |
| cargo | serde_repr | 0.1.20 | - | - | `pkg:cargo/serde_repr@0.1.20` |
| cargo | serde_spanned | 1.1.1 | - | - | `pkg:cargo/serde_spanned@1.1.1` |
| cargo | serde_urlencoded | 0.7.1 | - | - | `pkg:cargo/serde_urlencoded@0.7.1` |
| cargo | sha1 | 0.11.0 | - | - | `pkg:cargo/sha1@0.11.0` |
| cargo | sha2 | 0.10.9 | - | - | `pkg:cargo/sha2@0.10.9` |
| cargo | sha2 | 0.11.0 | - | - | `pkg:cargo/sha2@0.11.0` |
| cargo | sharded-slab | 0.1.7 | - | - | `pkg:cargo/sharded-slab@0.1.7` |
| cargo | shell-escape | 0.1.5 | - | - | `pkg:cargo/shell-escape@0.1.5` |
| cargo | shellexpand | 3.1.2 | - | - | `pkg:cargo/shellexpand@3.1.2` |
| cargo | signal-hook-registry | 1.4.8 | - | - | `pkg:cargo/signal-hook-registry@1.4.8` |
| cargo | signature | 2.2.0 | - | - | `pkg:cargo/signature@2.2.0` |
| cargo | simd-adler32 | 0.3.8 | - | - | `pkg:cargo/simd-adler32@0.3.8` |
| cargo | simdutf8 | 0.1.5 | - | - | `pkg:cargo/simdutf8@0.1.5` |
| cargo | similar | 2.7.0 | - | - | `pkg:cargo/similar@2.7.0` |
| cargo | similar | 3.1.1 | - | - | `pkg:cargo/similar@3.1.1` |
| cargo | slab | 0.4.12 | - | - | `pkg:cargo/slab@0.4.12` |
| cargo | smallvec | 1.15.2 | - | - | `pkg:cargo/smallvec@1.15.2` |
| cargo | smawk | 0.3.2 | - | - | `pkg:cargo/smawk@0.3.2` |
| cargo | socket2 | 0.6.3 | - | - | `pkg:cargo/socket2@0.6.3` |
| cargo | spdx | 0.13.4 | - | - | `pkg:cargo/spdx@0.13.4` |
| cargo | spin | 0.9.8 | - | - | `pkg:cargo/spin@0.9.8` |
| cargo | spki | 0.7.3 | - | - | `pkg:cargo/spki@0.7.3` |
| cargo | stable_deref_trait | 1.2.1 | - | - | `pkg:cargo/stable_deref_trait@1.2.1` |
| cargo | strip-ansi-escapes | 0.2.1 | - | - | `pkg:cargo/strip-ansi-escapes@0.2.1` |
| cargo | strsim | 0.11.1 | - | - | `pkg:cargo/strsim@0.11.1` |
| cargo | strum | 0.28.0 | - | - | `pkg:cargo/strum@0.28.0` |
| cargo | subtle | 2.6.1 | - | - | `pkg:cargo/subtle@2.6.1` |
| cargo | supports-color | 3.0.2 | - | - | `pkg:cargo/supports-color@3.0.2` |
| cargo | supports-hyperlinks | 3.2.0 | - | - | `pkg:cargo/supports-hyperlinks@3.2.0` |
| cargo | supports-unicode | 3.0.0 | - | - | `pkg:cargo/supports-unicode@3.0.0` |
| cargo | syn | 2.0.118 | - | - | `pkg:cargo/syn@2.0.118` |
| cargo | sync_wrapper | 1.0.2 | - | - | `pkg:cargo/sync_wrapper@1.0.2` |
| cargo | synstructure | 0.13.2 | - | - | `pkg:cargo/synstructure@0.13.2` |
| cargo | target-lexicon | 0.13.5 | - | - | `pkg:cargo/target-lexicon@0.13.5` |
| cargo | temp-env | 0.3.6 | - | - | `pkg:cargo/temp-env@0.3.6` |
| cargo | tempfile | 3.27.0 | - | - | `pkg:cargo/tempfile@3.27.0` |
| cargo | terminal_size | 0.4.4 | - | - | `pkg:cargo/terminal_size@0.4.4` |
| cargo | termtree | 0.5.1 | - | - | `pkg:cargo/termtree@0.5.1` |
| cargo | textwrap | 0.16.2 | - | - | `pkg:cargo/textwrap@0.16.2` |
| cargo | thiserror | 2.0.19 | - | - | `pkg:cargo/thiserror@2.0.19` |
| cargo | thread_local | 1.1.9 | - | - | `pkg:cargo/thread_local@1.1.9` |
| cargo | tikv-jemalloc-sys | 0.6.1+5.3.0-1-ge13ca993e8ccb9ba9847cc330696e02839f328f7 | - | - | `pkg:cargo/tikv-jemalloc-sys@0.6.1%2B5.3.0-1-ge13ca993e8ccb9ba9847cc330696e02839f328f7` |
| cargo | tikv-jemallocator | 0.6.1 | - | - | `pkg:cargo/tikv-jemallocator@0.6.1` |
| cargo | time | 0.3.47 | - | - | `pkg:cargo/time@0.3.47` |
| cargo | time-core | 0.1.8 | - | - | `pkg:cargo/time-core@0.1.8` |
| cargo | tinystr | 0.8.2 | - | - | `pkg:cargo/tinystr@0.8.2` |
| cargo | tinyvec | 1.11.0 | - | - | `pkg:cargo/tinyvec@1.11.0` |
| cargo | tinyvec_macros | 0.1.1 | - | - | `pkg:cargo/tinyvec_macros@0.1.1` |
| cargo | tokio | 1.53.1 | - | - | `pkg:cargo/tokio@1.53.1` |
| cargo | tokio-rustls | 0.26.4 | - | - | `pkg:cargo/tokio-rustls@0.26.4` |
| cargo | tokio-stream | 0.1.19 | - | - | `pkg:cargo/tokio-stream@0.1.19` |
| cargo | tokio-util | 0.7.19 | - | - | `pkg:cargo/tokio-util@0.7.19` |
| cargo | toml | 1.1.3+spec-1.1.0 | - | - | `pkg:cargo/toml@1.1.3%2Bspec-1.1.0` |
| cargo | toml_datetime | 1.1.1+spec-1.1.0 | - | - | `pkg:cargo/toml_datetime@1.1.1%2Bspec-1.1.0` |
| cargo | toml_edit | 0.25.13+spec-1.1.0 | - | - | `pkg:cargo/toml_edit@0.25.13%2Bspec-1.1.0` |
| cargo | toml_parser | 1.1.2+spec-1.1.0 | - | - | `pkg:cargo/toml_parser@1.1.2%2Bspec-1.1.0` |
| cargo | toml_writer | 1.1.2+spec-1.1.0 | - | - | `pkg:cargo/toml_writer@1.1.2%2Bspec-1.1.0` |
| cargo | tower | 0.5.3 | - | - | `pkg:cargo/tower@0.5.3` |
| cargo | tower-http | 0.6.8 | - | - | `pkg:cargo/tower-http@0.6.8` |
| cargo | tower-layer | 0.3.3 | - | - | `pkg:cargo/tower-layer@0.3.3` |
| cargo | tower-service | 0.3.3 | - | - | `pkg:cargo/tower-service@0.3.3` |
| cargo | tracing | 0.1.44 | - | - | `pkg:cargo/tracing@0.1.44` |
| cargo | tracing-attributes | 0.1.31 | - | - | `pkg:cargo/tracing-attributes@0.1.31` |
| cargo | tracing-core | 0.1.36 | - | - | `pkg:cargo/tracing-core@0.1.36` |
| cargo | tracing-log | 0.2.0 | - | - | `pkg:cargo/tracing-log@0.2.0` |
| cargo | tracing-subscriber | 0.3.23 | - | - | `pkg:cargo/tracing-subscriber@0.3.23` |
| cargo | tracing-tree | 0.4.1 | - | - | `pkg:cargo/tracing-tree@0.4.1` |
| cargo | try-lock | 0.2.5 | - | - | `pkg:cargo/try-lock@0.2.5` |
| cargo | typeid | 1.0.3 | - | - | `pkg:cargo/typeid@1.0.3` |
| cargo | typenum | 1.20.1 | - | - | `pkg:cargo/typenum@1.20.1` |
| cargo | ucd-trie | 0.1.7 | - | - | `pkg:cargo/ucd-trie@0.1.7` |
| cargo | unicase | 2.9.0 | - | - | `pkg:cargo/unicase@2.9.0` |
| cargo | unicode-ident | 1.0.24 | - | - | `pkg:cargo/unicode-ident@1.0.24` |
| cargo | unicode-linebreak | 0.1.5 | - | - | `pkg:cargo/unicode-linebreak@0.1.5` |
| cargo | unicode-width | 0.1.14 | - | - | `pkg:cargo/unicode-width@0.1.14` |
| cargo | unicode-width | 0.2.2 | - | - | `pkg:cargo/unicode-width@0.2.2` |
| cargo | unit-prefix | 0.5.2 | - | - | `pkg:cargo/unit-prefix@0.5.2` |
| cargo | unscanny | 0.1.0 | - | - | `pkg:cargo/unscanny@0.1.0` |
| cargo | untrusted | 0.9.0 | - | - | `pkg:cargo/untrusted@0.9.0` |
| cargo | url | 2.5.8 | - | - | `pkg:cargo/url@2.5.8` |
| cargo | utf8_iter | 1.0.4 | - | - | `pkg:cargo/utf8_iter@1.0.4` |
| cargo | utf8parse | 0.2.2 | - | - | `pkg:cargo/utf8parse@0.2.2` |
| cargo | uuid | 1.24.0 | - | - | `pkg:cargo/uuid@1.24.0` |
| cargo | uv | 0.12.2 | - | - | `pkg:cargo/uv@0.12.2` |
| cargo | uv-audit | 0.0.69 | - | - | `pkg:cargo/uv-audit@0.0.69` |
| cargo | uv-auth | 0.0.69 | - | - | `pkg:cargo/uv-auth@0.0.69` |
| cargo | uv-bin-install | 0.0.69 | - | - | `pkg:cargo/uv-bin-install@0.0.69` |
| cargo | uv-build-backend | 0.0.69 | - | - | `pkg:cargo/uv-build-backend@0.0.69` |
| cargo | uv-build-frontend | 0.0.69 | - | - | `pkg:cargo/uv-build-frontend@0.0.69` |
| cargo | uv-cache | 0.0.69 | - | - | `pkg:cargo/uv-cache@0.0.69` |
| cargo | uv-cache-info | 0.0.69 | - | - | `pkg:cargo/uv-cache-info@0.0.69` |
| cargo | uv-cache-key | 0.0.69 | - | - | `pkg:cargo/uv-cache-key@0.0.69` |
| cargo | uv-cli | 0.0.69 | - | - | `pkg:cargo/uv-cli@0.0.69` |
| cargo | uv-client | 0.0.69 | - | - | `pkg:cargo/uv-client@0.0.69` |
| cargo | uv-configuration | 0.0.69 | - | - | `pkg:cargo/uv-configuration@0.0.69` |
| cargo | uv-console | 0.0.69 | - | - | `pkg:cargo/uv-console@0.0.69` |
| cargo | uv-dirs | 0.0.69 | - | - | `pkg:cargo/uv-dirs@0.0.69` |
| cargo | uv-dispatch | 0.0.69 | - | - | `pkg:cargo/uv-dispatch@0.0.69` |
| cargo | uv-distribution | 0.0.69 | - | - | `pkg:cargo/uv-distribution@0.0.69` |
| cargo | uv-distribution-filename | 0.0.69 | - | - | `pkg:cargo/uv-distribution-filename@0.0.69` |
| cargo | uv-distribution-types | 0.0.69 | - | - | `pkg:cargo/uv-distribution-types@0.0.69` |
| cargo | uv-errors | 0.0.69 | - | - | `pkg:cargo/uv-errors@0.0.69` |
| cargo | uv-extract | 0.0.69 | - | - | `pkg:cargo/uv-extract@0.0.69` |
| cargo | uv-fastid | 0.0.69 | - | - | `pkg:cargo/uv-fastid@0.0.69` |
| cargo | uv-flags | 0.0.69 | - | - | `pkg:cargo/uv-flags@0.0.69` |
| cargo | uv-fs | 0.0.69 | - | - | `pkg:cargo/uv-fs@0.0.69` |
| cargo | uv-git | 0.0.69 | - | - | `pkg:cargo/uv-git@0.0.69` |
| cargo | uv-git-types | 0.0.69 | - | - | `pkg:cargo/uv-git-types@0.0.69` |
| cargo | uv-globfilter | 0.0.69 | - | - | `pkg:cargo/uv-globfilter@0.0.69` |
| cargo | uv-install-wheel | 0.0.69 | - | - | `pkg:cargo/uv-install-wheel@0.0.69` |
| cargo | uv-installer | 0.0.69 | - | - | `pkg:cargo/uv-installer@0.0.69` |
| cargo | uv-keyring | 0.0.69 | - | - | `pkg:cargo/uv-keyring@0.0.69` |
| cargo | uv-logging | 0.0.69 | - | - | `pkg:cargo/uv-logging@0.0.69` |
| cargo | uv-metadata | 0.0.69 | - | - | `pkg:cargo/uv-metadata@0.0.69` |
| cargo | uv-netrc | 0.0.69 | - | - | `pkg:cargo/uv-netrc@0.0.69` |
| cargo | uv-normalize | 0.0.69 | - | - | `pkg:cargo/uv-normalize@0.0.69` |
| cargo | uv-once-map | 0.0.69 | - | - | `pkg:cargo/uv-once-map@0.0.69` |
| cargo | uv-options-metadata | 0.0.69 | - | - | `pkg:cargo/uv-options-metadata@0.0.69` |
| cargo | uv-pep440 | 0.0.69 | - | - | `pkg:cargo/uv-pep440@0.0.69` |
| cargo | uv-pep508 | 0.0.69 | - | - | `pkg:cargo/uv-pep508@0.0.69` |
| cargo | uv-performance-memory-allocator | 0.0.69 | - | - | `pkg:cargo/uv-performance-memory-allocator@0.0.69` |
| cargo | uv-platform | 0.0.69 | - | - | `pkg:cargo/uv-platform@0.0.69` |
| cargo | uv-platform-tags | 0.0.69 | - | - | `pkg:cargo/uv-platform-tags@0.0.69` |
| cargo | uv-preview | 0.0.69 | - | - | `pkg:cargo/uv-preview@0.0.69` |
| cargo | uv-publish | 0.0.69 | - | - | `pkg:cargo/uv-publish@0.0.69` |
| cargo | uv-pypi-types | 0.0.69 | - | - | `pkg:cargo/uv-pypi-types@0.0.69` |
| cargo | uv-python | 0.0.69 | - | - | `pkg:cargo/uv-python@0.0.69` |
| cargo | uv-redacted | 0.0.69 | - | - | `pkg:cargo/uv-redacted@0.0.69` |
| cargo | uv-requirements | 0.0.69 | - | - | `pkg:cargo/uv-requirements@0.0.69` |
| cargo | uv-requirements-txt | 0.0.69 | - | - | `pkg:cargo/uv-requirements-txt@0.0.69` |
| cargo | uv-resolver | 0.0.69 | - | - | `pkg:cargo/uv-resolver@0.0.69` |
| cargo | uv-scripts | 0.0.69 | - | - | `pkg:cargo/uv-scripts@0.0.69` |
| cargo | uv-settings | 0.0.69 | - | - | `pkg:cargo/uv-settings@0.0.69` |
| cargo | uv-shell | 0.0.69 | - | - | `pkg:cargo/uv-shell@0.0.69` |
| cargo | uv-small-str | 0.0.69 | - | - | `pkg:cargo/uv-small-str@0.0.69` |
| cargo | uv-state | 0.0.69 | - | - | `pkg:cargo/uv-state@0.0.69` |
| cargo | uv-static | 0.0.69 | - | - | `pkg:cargo/uv-static@0.0.69` |
| cargo | uv-test | 0.0.69 | - | - | `pkg:cargo/uv-test@0.0.69` |
| cargo | uv-toml | 0.0.69 | - | - | `pkg:cargo/uv-toml@0.0.69` |
| cargo | uv-tool | 0.0.69 | - | - | `pkg:cargo/uv-tool@0.0.69` |
| cargo | uv-torch | 0.0.69 | - | - | `pkg:cargo/uv-torch@0.0.69` |
| cargo | uv-trampoline-builder | 0.0.69 | - | - | `pkg:cargo/uv-trampoline-builder@0.0.69` |
| cargo | uv-types | 0.0.69 | - | - | `pkg:cargo/uv-types@0.0.69` |
| cargo | uv-unix | 0.0.69 | - | - | `pkg:cargo/uv-unix@0.0.69` |
| cargo | uv-version | 0.12.2 | - | - | `pkg:cargo/uv-version@0.12.2` |
| cargo | uv-virtualenv | 0.0.69 | - | - | `pkg:cargo/uv-virtualenv@0.0.69` |
| cargo | uv-warnings | 0.0.69 | - | - | `pkg:cargo/uv-warnings@0.0.69` |
| cargo | uv-workspace | 0.0.69 | - | - | `pkg:cargo/uv-workspace@0.0.69` |
| cargo | vte | 0.14.1 | - | - | `pkg:cargo/vte@0.14.1` |
| cargo | wait-timeout | 0.2.1 | - | - | `pkg:cargo/wait-timeout@0.2.1` |
| cargo | walkdir | 2.5.0 | - | - | `pkg:cargo/walkdir@2.5.0` |
| cargo | want | 0.3.1 | - | - | `pkg:cargo/want@0.3.1` |
| cargo | webpki-root-certs | 1.0.9 | - | - | `pkg:cargo/webpki-root-certs@1.0.9` |
| cargo | which | 8.0.5 | - | - | `pkg:cargo/which@8.0.5` |
| cargo | winnow | 1.0.3 | - | - | `pkg:cargo/winnow@1.0.3` |
| cargo | wiremock | 0.6.5 | - | - | `pkg:cargo/wiremock@0.6.5` |
| cargo | writeable | 0.6.2 | - | - | `pkg:cargo/writeable@0.6.2` |
| cargo | x509-parser | 0.18.1 | - | - | `pkg:cargo/x509-parser@0.18.1` |
| cargo | xattr | 1.6.1 | - | - | `pkg:cargo/xattr@1.6.1` |
| cargo | xml-rs | 0.8.28 | - | - | `pkg:cargo/xml-rs@0.8.28` |
| cargo | yoke | 0.8.1 | - | - | `pkg:cargo/yoke@0.8.1` |
| cargo | yoke-derive | 0.8.1 | - | - | `pkg:cargo/yoke-derive@0.8.1` |
| cargo | zbus | 5.15.0 | - | - | `pkg:cargo/zbus@5.15.0` |
| cargo | zbus_macros | 5.15.0 | - | - | `pkg:cargo/zbus_macros@5.15.0` |
| cargo | zbus_names | 4.3.2 | - | - | `pkg:cargo/zbus_names@4.3.2` |
| cargo | zerocopy | 0.8.42 | - | - | `pkg:cargo/zerocopy@0.8.42` |
| cargo | zerocopy-derive | 0.8.42 | - | - | `pkg:cargo/zerocopy-derive@0.8.42` |
| cargo | zerofrom | 0.1.6 | - | - | `pkg:cargo/zerofrom@0.1.6` |
| cargo | zerofrom-derive | 0.1.6 | - | - | `pkg:cargo/zerofrom-derive@0.1.6` |
| cargo | zeroize | 1.9.0 | - | - | `pkg:cargo/zeroize@1.9.0` |
| cargo | zerotrie | 0.2.3 | - | - | `pkg:cargo/zerotrie@0.2.3` |
| cargo | zerovec | 0.11.5 | - | - | `pkg:cargo/zerovec@0.11.5` |
| cargo | zerovec-derive | 0.11.2 | - | - | `pkg:cargo/zerovec-derive@0.11.2` |
| cargo | zlib-rs | 0.6.3 | - | - | `pkg:cargo/zlib-rs@0.6.3` |
| cargo | zmij | 1.0.21 | - | - | `pkg:cargo/zmij@1.0.21` |
| cargo | zstd | 0.13.3 | - | - | `pkg:cargo/zstd@0.13.3` |
| cargo | zstd-safe | 7.2.4 | - | - | `pkg:cargo/zstd-safe@7.2.4` |
| cargo | zstd-sys | 2.0.16+zstd.1.5.7 | - | - | `pkg:cargo/zstd-sys@2.0.16%2Bzstd.1.5.7` |
| cargo | zvariant | 5.11.0 | - | - | `pkg:cargo/zvariant@5.11.0` |
| cargo | zvariant_derive | 5.11.0 | - | - | `pkg:cargo/zvariant_derive@5.11.0` |
| cargo | zvariant_utils | 3.3.1 | - | - | `pkg:cargo/zvariant_utils@3.3.1` |
| generic | python | 3.14.7 | - | - | `pkg:generic/python@3.14.7` |
| operating-system | alpine | 3.23.5 | - | - | `-` |
| pypi | acme | 5.8.0 | Apache-2.0 | - | `pkg:pypi/acme@5.8.0` |
| pypi | autocommand | 2.2.2 | LGPLv3 | - | `pkg:pypi/autocommand@2.2.2` |
| pypi | backports-tarfile | 1.2.0 | MIT | - | `pkg:pypi/backports-tarfile@1.2.0` |
| pypi | certbot | 5.8.0 | Apache-2.0 | - | `pkg:pypi/certbot@5.8.0` |
| pypi | certifi | 2026.7.22 | MPL-2.0 | - | `pkg:pypi/certifi@2026.7.22` |
| pypi | cffi | 2.1.1 | MIT-0 | - | `pkg:pypi/cffi@2.1.1` |
| pypi | charset-normalizer | 3.4.9 | MIT | - | `pkg:pypi/charset-normalizer@3.4.9` |
| pypi | configargparse | 1.7.5 | MIT | - | `pkg:pypi/configargparse@1.7.5` |
| pypi | configobj | 5.0.9 | BSD-3-Clause | - | `pkg:pypi/configobj@5.0.9` |
| pypi | cryptography | 50.0.0 | Apache-2.0 OR BSD-3-Clause | - | `pkg:pypi/cryptography@50.0.0` |
| pypi | distro | 1.9.0 | Apache License, Version 2.0 | - | `pkg:pypi/distro@1.9.0` |
| pypi | idna | 3.18 | BSD-3-Clause | - | `pkg:pypi/idna@3.18` |
| pypi | importlib-metadata | 8.7.1 | Apache-2.0 | - | `pkg:pypi/importlib-metadata@8.7.1` |
| pypi | jaraco-context | 6.1.0 | MIT | - | `pkg:pypi/jaraco-context@6.1.0` |
| pypi | jaraco-functools | 4.4.0 | MIT | - | `pkg:pypi/jaraco-functools@4.4.0` |
| pypi | jaraco-text | 4.0.0 | MIT | - | `pkg:pypi/jaraco-text@4.0.0` |
| pypi | josepy | 2.2.0 | Apache-2.0 | - | `pkg:pypi/josepy@2.2.0` |
| pypi | more-itertools | 10.8.0 | MIT | - | `pkg:pypi/more-itertools@10.8.0` |
| pypi | packaging | 26.0 | Apache-2.0 OR BSD-2-Clause | - | `pkg:pypi/packaging@26.0` |
| pypi | packaging | 26.3 | Apache-2.0 OR BSD-2-Clause | - | `pkg:pypi/packaging@26.3` |
| pypi | parsedatetime | 2.6 | Apache License 2.0 | - | `pkg:pypi/parsedatetime@2.6` |
| pypi | pip | 26.2.1 | MIT | - | `pkg:pypi/pip@26.2.1` |
| pypi | platformdirs | 4.4.0 | MIT | - | `pkg:pypi/platformdirs@4.4.0` |
| pypi | pycparser | 3.0 | BSD-3-Clause | - | `pkg:pypi/pycparser@3.0` |
| pypi | pyopenssl | 26.4.0 | Apache License, Version 2.0 | - | `pkg:pypi/pyopenssl@26.4.0` |
| pypi | pyrfc3339 | 2.1.0 | MIT | - | `pkg:pypi/pyrfc3339@2.1.0` |
| pypi | requests | 2.34.2 | Apache-2.0 | - | `pkg:pypi/requests@2.34.2` |
| pypi | setuptools | 83.0.0 | MIT | - | `pkg:pypi/setuptools@83.0.0` |
| pypi | tomli | 2.4.0 | MIT | - | `pkg:pypi/tomli@2.4.0` |
| pypi | urllib3 | 2.7.0 | MIT | - | `pkg:pypi/urllib3@2.7.0` |
| pypi | uv | 0.12.2 | MIT OR Apache-2.0 | - | `pkg:pypi/uv@0.12.2` |
| pypi | wheel | 0.46.3 | MIT | - | `pkg:pypi/wheel@0.46.3` |
| pypi | wheel | 0.47.0 | MIT | - | `pkg:pypi/wheel@0.47.0` |
| pypi | zipp | 3.23.0 | MIT | - | `pkg:pypi/zipp@3.23.0` |

## flight_review-browser-runtime

Client-side JS/CSS fetched from CDNs or served from app/plot_app/static, plus external services

| Ecosystem | Name | Version | License | Supplier / publisher | purl |
|---|---|---|---|---|---|
| npm | @fortawesome/fontawesome-free | 6.5.1 | MIT AND CC-BY-4.0 AND OFL-1.1 | Fonticons, Inc. | `pkg:npm/%40fortawesome/fontawesome-free@6.5.1` |
| npm | animate.css | - | MIT | Daniel Eden | `pkg:npm/animate.css` |
| npm | bootstrap | 5.3.8 | MIT | The Bootstrap Authors | `pkg:npm/bootstrap@5.3.8` |
| npm | bootstrap-filestyle | 2.1.0 | MIT | Markus Vinicius da Silva Lima | `pkg:npm/bootstrap-filestyle@2.1.0` |
| npm | bootswatch | 5.3.8 | MIT | Thomas Park | `pkg:npm/bootswatch@5.3.8` |
| npm | cesium | 1.123.0 | Apache-2.0 | Cesium GS, Inc. | `pkg:npm/cesium@1.123.0` |
| npm | chosen-js | 1.8.3 | MIT | Harvest | `pkg:npm/chosen-js@1.8.3` |
| npm | datatables.net | 2.3.4 | MIT | SpryMedia Ltd | `pkg:npm/datatables.net@2.3.4` |
| npm | datatables.net-bs5 | 2.3.4 | MIT | SpryMedia Ltd | `pkg:npm/datatables.net-bs5@2.3.4` |
| npm | jquery | 3.1.0 | MIT | OpenJS Foundation | `pkg:npm/jquery@3.1.0` |
| npm | jquery | 3.7.0 | MIT | OpenJS Foundation | `pkg:npm/jquery@3.7.0` |
| npm | leaflet | 1.3.4 | BSD-2-Clause | Vladimir Agafonkin | `pkg:npm/leaflet@1.3.4` |
| npm | lightbox2 | 2.7.1 | MIT | Lokesh Dhakar | `pkg:npm/lightbox2@2.7.1` |
| npm | pace-js | 1.0.2 | MIT | HubSpot | `pkg:npm/pace-js@1.0.2` |
| npm | popper.js | - | MIT | Federico Zivolo | `pkg:npm/popper.js` |
| npm | two.js | 0.7.0 | MIT | Jono Brandel | `pkg:npm/two.js@0.7.0` |
