#!/bin/bash
make -C iocs/test
rm -rf zebraGui
#ZEBRAGUI=/dls_sw/work/tools/RHEL6-x86_64/zebraGui
ZEBRAGUI=/dls_sw/prod/tools/RHEL6-x86_64/zebraGui/1-2/
cp -rf $ZEBRAGUI/prefix zebraGui
cp -rf $ZEBRAGUI/zebraGui zebraGui/src

