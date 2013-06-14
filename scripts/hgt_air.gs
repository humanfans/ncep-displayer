'reinit'
'sdfopen E:\NCEP\pressure\hgt.2000.nc '
'sdfopen E:\NCEP\pressure\air.2000.nc '
'set mpdset cnworld'
'set map 15 1 3'
'set lat 10 90'
'set lon 30 180'
'set lev 850'
'set time 00Z01MAR2000 ' 
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
'q file 2 '
rec=sublin(result,7)
fil=subwrd(rec,1)
'set gxout shaded'
'set cint 4'
'd smth9(' fil '.2-273.15)'
'cbarn 1 0 '
'set lev 500'
'set gxout contour'
'set cint 40'
'd smth9(hgt)'
'draw title Ncep_500hPa.Height & 850hPa.Temperature_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'
'printim E:\NCEP\picture\pressure\Ncep_500hPa.Height_850hPa.Temperature_' file '.gif gif x800 y600 white '
;
