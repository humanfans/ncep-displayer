'reinit'
'sdfopen X:\pressure\hgt.1997.nc' 
'set mpdset cnworld cnriver'
'set map 15 1 3'
'set lat 0 90'
'set lon 30 180'
'set time 12Z09JAN1997 '
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
'set cint 40'
'd smth9(' fil ')'
'draw title Ncep_Pre' lev1 '_' fil  '_' file
'set font 5'
'set string 11 c 4 0'
'set strsiz 0.12 0.13'
'draw string 8.2 1.6 X.XUN Zh.CAI'

'printim E:\Dropbox\Backup\codeSource\qxt\201211_01_NCEP-displayer\images\NCEP_Pre1000_height_19970109_12_(30,180,0,90).gif gif x1024 y768 white' 
;
quit 