#!/usr/bin/env sh
wget https://www.xilinx.com/support/documentation-navigation/design-hubs/dh0050-zynq-7000-design-overview-hub.html
cat dh0050-zynq-7000-design-overview-hub.html |grep "\.pdf"|sed "s:.*\(HREF\|href\)=\('\|\"\)\(.*\.pdf\)\('\|\"\).*:\3:"|xargs -i{} wget https://www.xilinx.com/{}
