#!/bin/bash

cat clrz | parallel -j 1   'f=$(echo {} |cut -d , -f 1);b=$(echo {} | cut -d , -f 2); colr ">->->-> >>==||***>>===// ===|> This package is available from  https://github.com/iamh2o/rgbw_colorspace_converter  <|=== //===<<***||==<<-<-<-<-<" "$f" "$b"; sleep 2'
