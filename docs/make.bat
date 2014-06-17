REM taskkill /im AcroRd32.exe 
pdflatex %1 
bibtex %1 
pdflatex %1 
gbk2uni %1.out 
pdflatex %1 
start %1.pdf