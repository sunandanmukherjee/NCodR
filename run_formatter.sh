#!/bin/bash
sed -i '1d' $1.genstats.tsv
sed -i '1d' $1.tsv
sed -i '1d' windowsize3.tsv
cut -f 1 $1.genstats.tsv|cut -f 1 -d ' ' >$1.ids
grep -wf $1.ids $1.tsv|cut -f 1,3-5 |sort >$1_temp1
grep -wf $1.ids windowsize3.tsv |cut -f 1,3-66 |sort|cut -f 2-  >$1_temp2
sort $1.genstats.tsv|cut -f 2-  >$1_temp3
paste $1_temp1 $1_temp2 $1_temp3 >$1.data
sed 's/	/, /g' $1.data >$1_data.csv
