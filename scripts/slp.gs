'reinit'
'sdfopen E:\NCEP\surface\slp\slp.1998.nc '
'set mpdset cnworld cnriver'
'set map 15 1 3'
'set lat 0 90'
'set lon 30 180'
*'set lev 600'
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
'q file '
rec=sublin(result,7)
fil=subwrd(rec,1)
'set cint 4'
'd smth9(' fil '/100)'
'draw title Ncep_Surface_' fil  '_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'
'printim E:\NCEP\picture\surface\Ncep_Surface_' fil '_' file '.gif gif x800 y600 white '
;
