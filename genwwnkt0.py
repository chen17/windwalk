import cv2
import fontforge
import subprocess
import time
import urllib

# Create new font WindWalkNewKaiTi0.
newfont = fontforge.font()
newfont.fontname="WWNKT0"
newfont.save("WWNKT0.sfd")

font = fontforge.open("WWNKT0.sfd")

# Get Char_List.txt
charlist = open("NewKaiTi0.txt", "r").readlines()
#charlist = urllib.urlopen("https://raw.githubusercontent.com/chen17/windwalk/master/NewKaiTi0.txt").readlines()

print('There are total %d characters' % len(charlist))

for i in range(len(charlist)):
  url = charlist[i].split()[0]
  # >>> charlist[0].split()[1].decode('utf-8')
  # u'\u4e00'
  # >>> ord(charlist[0].split()[1].decode('utf-8'))
  # 19968
  char = int(ord(charlist[i].split()[1]))
  charjpg = "jpg/" + charlist[i].split()[1] + '.jpg'
  charbmp = "bmp/" + str(char) + '.bmp'
  charsvg = "svg/" + str(char) + '.svg'

  print('Working on ' + charlist[i].split()[1])

  # Get jpg file.
  #urllib.urlretrieve(url, charjpg)
  #time.sleep(7)

  # Clean noise and convert into bmp.
  print('Convert into bmp.')
  img = cv2.imread(charjpg)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  median = cv2.medianBlur(gray, 3)
  ret,output = cv2.threshold(median, 150, 255, cv2.THRESH_BINARY)
  output = cv2.blur(output, (5,5))
  cv2.imwrite(charbmp, output)

  # Convert into svg.
  subprocess.check_call(['/usr/bin/potrace', '-s', charbmp, '-o', charsvg]) 

  # Paste svg into fonts.
  glyph = font.createChar(char) 
  glyph.importOutlines(charsvg) 

  # Remove processed bmp and svg files.
  subprocess.check_call(['rm', charbmp, charsvg])

font.generate("WWNKT0.ttf")
