sed -e "s/test_expanded.db'/test_expanded.db' \"ZEBRAPREFIX=\$(ZEBRAPREFIX)\"/" \
    -e "s/cd \"\$(TOP)\"//" \
    -e "5a cd ../.." \
    -i $1/iocBoot/ioctest/sttest.cmd
echo "STATIC_BUILD=YES" >> $1/configure/CONFIG_SITE
cat <<'EOF' > $1/iocBoot/ioctest/sttest.sh
#!/bin/bash
cd "$(dirname "$0")"
export ZEBRAPREFIX="${1:-TESTZEBRA}"
exec ./test sttest.boot
EOF
sed -e 's/testTop.edl/-m "ZEBRAPREFIX=${1:-TESTZEBRA}" testTop.edl/' \
    -i $1/testApp/opi/edl/sttest-gui
