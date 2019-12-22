from subprocess import call

acrobat = "C:/Program Files (x86)/Adobe/Acrobat Reader DC\Reader/AcroRd32.exe"
file = "C:/Users/anjae/Desktop/영상인식중/Example.pdf"
printer = "Samsung M2020 Series (USB001)"

call([acrobat, "/T", file, printer])
