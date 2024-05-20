#!/bin/bash

# This script will evaluate a system against the DISA STIGs and generate an ansible playbook to remediate it.

yum -y install openscap-scanner scap-security-guide
oscap xccdf generate fix --profile stig --fetch-remote-resources --template urn:xccdf:fix:script:ansible /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml > /tmp/remediation_playbook.yml
