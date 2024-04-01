<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Community Inventory Filtering Library Collection
[![CI](https://github.com/ansible-collections/community.library_inventory_filtering/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.library_inventory_filtering/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.library_inventory_filtering)](https://codecov.io/gh/ansible-collections/community.library_inventory_filtering)

This repository contains the `community.library_inventory_filtering_v1` Ansible Collection. The collection includes helpers for use with other collections, that allow inventory plugins to offer common filtering functionality.

## Tested with Ansible

Tested with the current Ansible 2.9, ansible-base 2.10, ansible-core 2.11, ansible-core 2.12, ansible-core 2.13, ansible-core 2.14, ansible-core 2.15, and ansible-core 2.16 releases and the current development version of ansible-core. Ansible versions before 2.9.10 are not supported.

## Included content

- `inventory_filter` docs fragment and plugin utils.

## Using this collection

Usually this collection is installed as a dependency of another collection. You do not need to install it explicitly.

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for general instructions on how to use collections.

## Contributing to this collection

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

You can find more information in the [developer guide for collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## Release notes

See the [changelog](https://github.com/ansible-collections/community.library_inventory_filtering/tree/stable-1/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

This collection is primarily licensed and distributed as a whole under the GNU General Public License v3.0 or later.

See [LICENSES/GPL-3.0-or-later.txt](https://github.com/ansible-collections/community.library_inventory_filtering/blob/stable-1/COPYING) for the full text.

All files have a machine readable `SDPX-License-Identifier:` comment denoting its respective license(s) or an equivalent entry in an accompanying `.license` file. Only changelog fragments (which will not be part of a release) are covered by a blanket statement in `.reuse/dep5`. This conforms to the [REUSE specification](https://reuse.software/spec/).
