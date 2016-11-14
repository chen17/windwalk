import fontforge
import subprocess
import urllib

# Create new font WindWalkNewKaiTi0.
newfont = fontforge.font()
newfont.fontname="WWNKT0"
newfont.save("WWNKT0.sfd")

font = fontforge.open("WWNKT0.sfd")

# Get Char_List.txt
charlist = urllib.urlopen("https://raw.githubusercontent.com/chen17/windwalk/master/NewKaiTi0.txt").readlines()

print 'There are total %d characters' % len(charlist)

for i in range(len(charlist)):
  url = charlist[i].split()[0]
  # >>> charlist[0].split()[1].decode('utf-8')
  # u'\u4e00'
  # >>> ord(charlist[0].split()[1].decode('utf-8'))
  # 19968
  char = int(ord(charlist[i].split()[1].decode('utf-8')))
  charjpg = charlist[i].split()[1] + '.jpg'
  charbmp = str(char) + '.bmp'
  charsvg = str(char) + '.svg'

  print 'Working on ' + charlist[i].split()[1]

  # Get jpg file.
  urllib.urlretrieve(url, charjpg)

  # Convert into bmp.
  subprocess.check_call(['/usr/bin/convert', charjpg, charbmp]) 

  # Convert into svg.
  subprocess.check_call(['/usr/bin/potrace', '-s', charbmp]) 

  # Paste svg into fonts.
  glyph = font.createChar(char) 
  glyph.importOutlines(charsvg) 

  # Remove processed bmp and svg files.
  subprocess.check_call(['rm', charbmp, charsvg])

font.generate("WWNKT0.ttf")
