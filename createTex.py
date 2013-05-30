from lxml import etree
import os
from BeautifulSoup import BeautifulSoup
from itertools import chain

def replacements(text):
    text = text.replace('&', '\&')
    text = text.replace('_', '\_')
    text = text.replace('%', '\%')
    text = text.replace('[', '\lbrack')
    text = text.replace(']', '\\rbrack')
    return text

def fillContent(tex, srchStr, insStr):
    insStr = replacements(insStr)
    insIndex = tex.index(srchStr)
    tex = tex[:insIndex+len(srchStr)] + insStr + tex[insIndex+len(srchStr):]
    return tex

def convertToTex(text, figInTabular=False):
    text = replacements(text)
    soup = BeautifulSoup(text)
    contents = soup.contents[0].contents
    retTxt = ''
    for content in contents:
        if str(type(content)) == "<class 'BeautifulSoup.NavigableString'>":
            content = content.replace('\\newline', '~\\\\')
            content = content.replace('\\newpara', '~\\\\\\\\')
            retTxt += content
        elif str(type(content)) == "<class 'BeautifulSoup.Tag'>":
            if content.name == 'b':
                retTxt += '\\textbf{' + convertToTex(str(content)) + '}'
            elif content.name == 'u':
                retTxt += '\underline{' + convertToTex(str(content)) + '}'
            elif content.name == 'ul':
                retTxt += '\n\\begin{itemize}'
                for item in content.contents:
                    if str(type(item)) == "<class 'BeautifulSoup.Tag'>":
                        retTxt += '\n  \item ' + convertToTex(str(item))
                retTxt += '\n\end{itemize}\n'
            elif content.name == 'chapter':
                retTxt += '\\begin{projChapter}{' + dict(content.attrs)['name'] + '}' + convertToTex(str(content)) + '\\end{projChapter}'
            elif content.name == 'section':
                retTxt += '\\begin{projSection}{' + dict(content.attrs)['name'] + '}' + convertToTex(str(content)) + '\\end{projSection}'
            elif content.name == 'subsection':
                retTxt += '\\begin{projSubSection}{' + dict(content.attrs)['name'] + '}' + convertToTex(str(content)) + '\\end{projSubSection}'
            elif content.name == 'img':
                if figInTabular:
                    props = dict(content.attrs)
                    retTxt += '\\raisebox{-\\totalheight}{\centering\n\includegraphics[scale=' + props['scale'] + ']{' + props['src'] + '}\n\label{' + props['id'] + '}}\n'
                else:
                    props = dict(content.attrs)
                    retTxt += '\\begin{figure}[ht!]\n\centering\n\includegraphics[scale=' + props['scale'] + ']{' + props['src'] + '}\n\caption{' + props['caption'] + '}\n\label{' + props['id'] + '}\n\end{figure}\n'
            elif content.name == 'ref':
                props = dict(content.attrs)
                if props['type'] == 'figure':
                    retTxt += 'Figure \\ref{' + content.text + '}'
                elif props['type'] == 'table':
                    retTxt += 'Table \\ref{' + content.text +'}'
            elif content.name == 'table':
                props = dict(content.attrs)
                alignments = props['alignments']
                retTxt += '\\begin{table}[h]\\begin{center}\\begin{tabular}{' + alignments + '}'
                for horizontal in content.contents:
                    if str(type(horizontal)) == "<class 'BeautifulSoup.Tag'>":
                        if horizontal.name == "tr":
                            cols = horizontal.contents
                            numOfCols = len(cols)
                            for i in range(numOfCols):
                                if str(type(cols[i])) == "<class 'BeautifulSoup.Tag'>":
                                    retTxt += convertToTex(str(cols[i]), figInTabular=True)
                                    print str(cols[i])
                                    if i != numOfCols - 2:
                                        retTxt += ' & '
                                    else:
                                        retTxt += ' \\\\\n'
                        elif horizontal.name == 'hline':
                            retTxt += '\hline\n'
                retTxt += '\\end{tabular}\\end{center}\\caption{' + props['caption'] + '}\\end{table}'


    return retTxt

f = open("assignment_1.sty", "r")
sty = f.read()
f.close()

f = open("assignment_1.tex", "r")
tex = f.read()
f.close()

f = open("fyp.xml", "r")
xmlStr = f.read()
f.close()

root = etree.fromstring(xmlStr)
projectTitle = root.find('projectTitle').text
guide = root.find('guide').text
principal = root.find('principal').text
HOD = root.find('HOD').text
durationLong = root.find('durationLong').text
headerLineWidth = root.find('headerLineWidth').text
footerLineWidth = root.find('footerLineWidth').text
collLogoPath = root.find('collLogoPath').text

defaultFontFamily = root.find('defaultFontFamily').text
fontLevelOne = root.find('fontLevelOne').text
fontLevelTwo = root.find('fontLevelTwo').text
fontLevelThree = root.find('fontLevelThree').text
fontLevelFour = root.find('fontLevelFour').text

students = []

studentOneObj = root.find('studentOne')
if studentOneObj is not None:
    studentOne = studentOneObj.text
    usnOne = root.find('usnOne').text
    students.append(('One', studentOne, usnOne))

studentTwoObj = root.find('studentTwo')
if studentTwoObj is not None:
    studentTwo = studentTwoObj.text
    usnTwo = root.find('usnTwo').text
    students.append(('Two', studentTwo, usnTwo))

studentThreeObj = root.find('studentThree')
if studentThreeObj is not None:
    studentThree = studentThreeObj.text
    usnThree = root.find('usnThree').text
    students.append(('Three', studentThree, usnThree))

studentFourObj = root.find('studentFour')
if studentFourObj is not None:
    studentFour = studentFourObj.text
    usnFour = root.find('usnFour').text
    students.append(('Four', studentFour, usnFour))

headerLogoScale = root.find('headerLogoScale').text
headerTitleSize = root.find('headerTitleSize').text

dept = root.find('dept').text
durationShort = root.find('durationShort').text

chapterFontFamily = root.find('chapterFontFamily').text

coverFontFamily = root.find('coverFontFamily').text
univName = root.find('univName').text
univLogoPath = root.find('univLogoPath').text
univLogoScale = root.find('univLogoScale').text
course = root.find('course').text
stream = root.find('stream').text
deptName = root.find('deptName').text
collName = root.find('collName').text
affiliation = root.find('affiliation').text
address = root.find('address').text
collCoverLogoScale = root.find('collCoverLogoScale').text
vspaceInterblock = root.find('vspaceInterblock').text
vspaceIntrablock = root.find('vspaceIntrablock').text

certificateLogoScale = root.find('certificateLogoScale').text

abstractFontFamily = root.find('abstractFontFamily').text

tex = fillContent(tex, 'newcommand{\projectTitle}{', projectTitle)
tex = fillContent(tex, 'newcommand{\guide}{', guide)
tex = fillContent(tex, 'newcommand{\principal}{', principal)
tex = fillContent(tex, 'newcommand{\HOD}{', HOD)
tex = fillContent(tex, 'newcommand{\durationLong}{', durationLong)
tex = fillContent(tex, 'newcommand{\headerLineWidth}{', headerLineWidth)
tex = fillContent(tex, 'newcommand{\\footerLineWidth}{', footerLineWidth)
tex = fillContent(tex, 'newcommand{\collLogoPath}{', collLogoPath)
tex = fillContent(tex, 'newcommand{\defaultFontFamily}{', defaultFontFamily)
tex = fillContent(tex, 'newcommand{\\fontLevelOne}{', fontLevelOne)
tex = fillContent(tex, 'newcommand{\\fontLevelTwo}{', fontLevelTwo)
tex = fillContent(tex, 'newcommand{\\fontLevelThree}{', fontLevelThree)
tex = fillContent(tex, 'newcommand{\\fontLevelFour}{', fontLevelFour)

insIndex = tex.index('@studentsList')
insStr = ''
for student in students:
    insStr += '\\newcommand{\\student' + student[0] + '}{' + student[1] + '}\n'
    insStr += '\\newcommand{\\usn' + student[0] + '}{' + student[2] + '}\n'
tex = tex[:insIndex] + insStr + tex[insIndex + len('@studentsList'):]

tex = fillContent(tex, 'newcommand{\headerLogoScale}{', headerLogoScale)
tex = fillContent(tex, 'newcommand{\headerTitleSize}{', headerTitleSize)
tex = fillContent(tex, 'newcommand{\dept}{', dept)
tex = fillContent(tex, 'newcommand{\durationShort}{', durationShort)
tex = fillContent(tex, 'newcommand{\chapterFontFamily}{', chapterFontFamily)
tex = fillContent(tex, 'newcommand{\coverFontFamily}{', coverFontFamily)
tex = fillContent(tex, 'newcommand{\univName}{', univName)
tex = fillContent(tex, 'newcommand{\univLogoPath}{', univLogoPath)
tex = fillContent(tex, 'newcommand{\univLogoScale}{', univLogoScale)
tex = fillContent(tex, 'newcommand{\course}{', course)
tex = fillContent(tex, 'newcommand{\stream}{', stream)
tex = fillContent(tex, 'newcommand{\deptName}{', deptName)
tex = fillContent(tex, 'newcommand{\collName}{', collName)
tex = fillContent(tex, 'newcommand{\\affiliation}{', affiliation)
tex = fillContent(tex, 'newcommand{\\address}{', address)
tex = fillContent(tex, 'newcommand{\collCoverLogoScale}{', collCoverLogoScale)
tex = fillContent(tex, 'newcommand{\\vspaceInterblock}{', vspaceInterblock)
tex = fillContent(tex, 'newcommand{\\vspaceIntrablock}{', vspaceIntrablock)
tex = fillContent(tex, 'newcommand{\certificateLogoScale}{', certificateLogoScale)
tex = fillContent(tex, 'newcommand{\\abstractFontFamily}{', abstractFontFamily)

insIndex = tex.index('@acknowledgement')
insStr = etree.tostring(root.find('acknowledgement'))
insStr = convertToTex(insStr)
tex = tex[:insIndex] + insStr + tex[insIndex + len('@acknowledgement'):]

insIndex = tex.index('@abstract')
insStr = etree.tostring(root.find('abstract'))
insStr = convertToTex(insStr)
tex = tex[:insIndex] + insStr + tex[insIndex + len('@abstract'):]

insIndex = tex.index('@chapters')
insStr = ''
chapters = root.findall('chapter')
for chapter in chapters:
    insStrTemp = etree.tostring(chapter)
    insStrTemp = convertToTex('<content>' + insStrTemp + '</content>')
    insStr += insStrTemp + '\n'
tex = tex[:insIndex] + insStr + tex[insIndex + len('@chapters'):]

f = open("output.tex", "w")
f.write(tex)
f.close()

'''
modifying the style file
'''
#modifying the cover page
coverIndex = sty.index("@studentsListCover")
insStrCover = ''
for i in range(len(students)):
    if i == 0:
        insStrCover += '\\vspace{\\vspaceInterblock}\n\\textbf{\\student' + students[i][0] + ' - \usn' + students[i][0] + '}\n\n'
    else:
        insStrCover += '\\vspace{\\vspaceIntrablock}\n\\textbf{\\student' + students[i][0] + ' - \usn' + students[i][0] + '}\n\n'
sty = sty[:coverIndex] + insStrCover + sty[coverIndex + len('@studentsListCover'):]

#modifying the certificate
certIndex = sty.index("@studentsListCertificate")
insStrCertificate = ''
for i in range(len(students)):
    if i == 0:
        insStrCertificate += '\\vspace{\\vspaceInterblock}\n\\textbf{\student' + students[i][0] + ', \usn' + students[i][0] + '}\n\n'
    else:
        insStrCertificate += '\\vspace{\\vspaceIntrablock}\n\\textbf{\student' + students[i][0] + ', \usn' + students[i][0] + '}\n\n'
print insStrCertificate
sty = sty[:certIndex] + insStrCertificate + sty[certIndex + len('@studentsListCertificate'):]

f = open("output.sty", "w")
f.write(sty)
f.close()
os.system("pdflatex output.tex")