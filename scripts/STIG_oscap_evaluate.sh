#!/bin/bash

# This script will evaluate a system against the DISA STIGs

yum -y install openscap-scanner scap-security-guide
oscap xccdf eval --report /tmp/report.html --profile xccdf_org.ssgproject.content_profile_stig /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
