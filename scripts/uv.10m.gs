'reinit'
'sdfopen E:\NCEP\surface\uv10m\uwnd.10m.gauss.1998.nc '
'sdfopen E:\NCEP\surface\uv10m\vwnd.10m.gauss.1998.nc '
'set mpdset cnworld cnriver'
'set map 15 1 3'
'set lat 0 90'
'set lon 30 180'
*'set lev 600'
'q file 1 '
'set time 00Z01MAR1998' 
'q dims '
rec=sublin(result,5)
t1=subwrd(rec,9)
'set t ' t1
'set xlint 20'
'set ylint 10'
'set xlopts 1 4 0.15'
'set ylopts 1 4 0.15'
'set clopts 5 0 0.08'
'set grid on'
'set grads off'
'q dims '
rec=sublin(result,5)
file=subwrd(rec,6)
rec1=sublin(result,4)
lev1=subwrd(rec1,6)
'set gxout vector '
'd uwnd.1;vwnd.2;sqrt(uwnd.1*uwnd.1+vwnd.2*vwnd.2)'
'draw title Ncep__Surface_wind_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'
'printim E:\NCEP\picture\surface\Ncep_Surface_vector_' file '.gif gif x800 y600 white '
;
