'reinit'
'sdfopen E:\NCEP\pressure\uwnd.1998.nc '
'sdfopen E:\NCEP\pressure\vwnd.1998.nc '
'sdfopen E:\NCEP\pressure\rhum.1998.nc '

'set mpdset cnworld'
'set map 15 1 3'
'set lat 10 90'
'set lon 30 180'
'set lev 850'
'q file 1 '
'set time 00Z01MAR1998 '
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
'set gxout shaded'
'set cmin 20'
'set cint 10'
'd smth9(rhum.3)'
'cbarn 1 0 '
'set gxout barb '
'd uwnd.1;vwnd.2;sqrt(uwnd.1*uwnd.1+vwnd.2*vwnd.2)'
'draw title Ncep_850hPa.wind & RH_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'
'printim E:\NCEP\picture\pressure\Ncep_' lev1 'hPa_vecotrRH_' file '.gif gif x800 y600 white '
;
