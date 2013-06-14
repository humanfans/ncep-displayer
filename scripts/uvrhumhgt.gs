'reinit'
'sdfopen E:\NCEP\pressure\uwnd.2000.nc '
'sdfopen E:\NCEP\pressure\vwnd.2000.nc '
'sdfopen E:\NCEP\pressure\rhum.2000.nc '
'sdfopen E:\NCEP\pressure\hgt.2000.nc '

'set mpdset cnworld cnriver'
'set map 15 1 3'
'set lat 10 90'
'set lon 30 180'
'set lev 850'
'q file 1 '
'set time 00Z01JAN2000 ' 
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
'set cmin 40'
'set cint 10'
'd smth9(rhum.3)'
'cbarn 1 0 '
'set gxout barb '
'd uwnd.1;vwnd.2;sqrt(uwnd.1*uwnd.1+vwnd.2*vwnd.2)'
'set lev 500'
'set gxout contour'
'set ccolor 1'
'set cint 40'
'd smth9(hgt.4)'
'draw title Ncep_500hPa.Hgt 850hPa.wind & RH_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'
'printim E:\NCEP\picture\pressure\Ncep_500.850hPa_vecotrRHhgt_' file '.gif gif x800 y600 white '
;
