from lxml import etree
import os
from BeautifulSoup import BeautifulSoup
from itertools import chain

def replacements(text):
    text = text.replace('&gt;', '\\textgreater ')
    text = text.replace('&lt;', '\\textless ')
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
            content = content.replace('\\backslash', '\\textbackslash')
            content = content.replace('|', '\\textbar ')
            retTxt += content
        elif str(type(content)) == "<class 'BeautifulSoup.Tag'>":
            if content.name == 'b':
                retTxt += '\\textbf{' + convertToTex(str(content)) + '}'
            elif content.name == 'u':
                retTxt += '\underline{' + convertToTex(str(content)) + '}'
            elif content.name == 'i':
                retTxt += '\\textit{' + convertToTex(str(content)) + '}'
            elif content.name == 'ul':
                retTxt += '\n\\begin{itemize}'
                for item in content.contents:
                    if str(type(item)) == "<class 'BeautifulSoup.Tag'>":
                        retTxt += '\n  \item ' + convertToTex(str(item))
                retTxt += '\n\end{itemize}\n'
            elif content.name == 'chapter':
                attrs = dict(content.attrs)
                if not attrs.has_key('name'):
                    print "One of the chapters do not have a 'name' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif attrs['name'] == '':
                    print "One of the chapters' name is empty. Please correct it and re-run."
                    exit(0)
                else:
                    retTxt += '\\begin{projChapter}{' + attrs['name'] + '}' + convertToTex(str(content)) + '\\end{projChapter}'
            elif content.name == 'section':
                attrs = dict(content.attrs)
                if not attrs.has_key('name'):
                    print "One of the sections do not have a 'name' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif attrs['name'] == '':
                    print "One of the sections' name is empty. Please correct it and re-run."
                    exit(0)
                else:
                    retTxt += '\\begin{projSection}{' + attrs['name'] + '}' + convertToTex(str(content)) + '\\end{projSection}'
            elif content.name == 'subsection':
                attrs = dict(content.attrs)
                if not attrs.has_key('name'):
                    print "One of the subsections do not have a 'name' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif attrs['name'] == '':
                    print "One of the subsections' name is empty. Please correct it and re-run."
                    exit(0)
                else:
                    retTxt += '\\begin{projSubSection}{' + attrs['name'] + '}' + convertToTex(str(content)) + '\\end{projSubSection}'
            elif content.name == 'img':
                props = dict(content.attrs)
                if not props.has_key('id'):
                    print "One of the images do not have an 'id' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif not props.has_key('src'):
                    print "One of the images do not have a 'src' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif not props.has_key('caption'):
                    print "One of the images do not have a 'caption' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif not props.has_key('scale'):
                    print "One of the images do not have a 'scale' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif props['id'] == '':
                    print "One of the images has an empty 'id'. Please correct it and re-run."
                    exit(0)
                elif props['src'] == '':
                    print "One of the images has an empty 'src'. Please correct it and re-run."
                    exit(0)
                elif props['scale'] == '':
                    print "Scaling factor for one of the images hasnt been defined. Please correct it and re-run."
                    exit(0)
                else:
                    if figInTabular:
                        retTxt += '\\raisebox{-\\totalheight}{\centering\n\includegraphics[scale=' + props['scale'] + ']{' + props['src'] + '}\n\label{' + props['id'] + '}}\n'
                    else:
                        retTxt += '\\begin{figure}[ht!]\n\centering\n\includegraphics[scale=' + props['scale'] + ']{' + props['src'] + '}\n\caption{' + props['caption'] + '}\n\label{' + props['id'] + '}\n\end{figure}\n'
            elif content.name == 'ref':
                props = dict(content.attrs)
                if not props.has_key('type'):
                    print "One of the references doesnt have a 'type' attribute. Please correct it and re-run."
                    exit(0)
                elif props['type'] == '':
                    print "One of the references has an empty string for 'type'. Please correct it and re-run."
                    exit(0)
                else:
                    if props['type'] == 'figure':
                        retTxt += 'Figure \\ref{' + content.text + '}'
                    elif props['type'] == 'table':
                        retTxt += 'Table \\ref{' + content.text +'}'
            elif content.name == 'table':
                props = dict(content.attrs)
                if not props.has_key('id'):
                    print "One of the tables do not have an 'id' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif not props.has_key('alignments'):
                    print "One of the tables do not have a 'alignments' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif not props.has_key('caption'):
                    print "One of the tables do not have a 'caption' attribute or is misspelled. Please correct it and re-run."
                    exit(0)
                elif props['id'] == '':
                    print "One of the tables has an empty 'id'. Please correct it and re-run."
                    exit(0)
                elif props['alignments'] == '':
                    print "One of the tables has an empty 'alignments'. Please correct it and re-run."
                    exit(0)
                else:
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
                    retTxt += '\\end{tabular}\\end{center}\\caption{' + props['caption'] + '}\\label{' + props['id'] + '}\\end{table}'
    return retTxt

def main():
    f = open("fyp.stmplt", "r")
    sty = f.read()
    f.close()

    f = open("fyp.ttmplt", "r")
    tex = f.read()
    f.close()

    f = open("report.xml", "r")
    xmlStr = f.read()
    f.close()

    root = etree.fromstring(xmlStr)
    projectTitle = root.find('projectDetails').find('projectTitle').text
    guide = root.find('projectDetails').find('guide').text
    principal = root.find('projectDetails').find('principal').text
    HOD = root.find('projectDetails').find('HOD').text
    durationLong = root.find('projectDetails').find('duration').text
    collLogoPath = root.find('projectDetails').find('collLogoPath').text

    defaultFontFamily = root.find('font').find('defaultFontFamily').text
    fontLevelOne = root.find('font').find('levelOne').text
    fontLevelTwo = root.find('font').find('levelTwo').text
    fontLevelThree = root.find('font').find('levelThree').text
    fontLevelFour = root.find('font').find('levelFour').text

    numberStrings = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    students = [ (student.find('name').text, student.find('usn').text) for student in root.find('students').getchildren() if student.tag == 'student']
    students = [ (numberStrings[i], students[i][0], students[i][1]) for i in range(len(students))]

    headerLogoScale = root.find('header').find('logoScale').text
    headerTitleSize = root.find('header').find('titleSize').text
    headerLineWidth = root.find('header').find('lineWidth').text

    dept = root.find('footer').find('dept').text
    durationShort = root.find('footer').find('duration').text
    footerLineWidth = root.find('footer').find('lineWidth').text

    chapterFontFamily = root.find('chapterControls').find('fontFamily').text

    coverFontFamily = root.find('cover').find('fontFamily').text
    univName = root.find('cover').find('univName').text
    univLogoPath = root.find('cover').find('univLogoPath').text
    univLogoScale = root.find('cover').find('univLogoScale').text
    course = root.find('cover').find('course').text
    stream = root.find('cover').find('stream').text
    deptName = root.find('cover').find('deptName').text
    collName = root.find('cover').find('collName').text
    affiliation = root.find('cover').find('affiliation').text
    address = root.find('cover').find('address').text
    collCoverLogoScale = root.find('cover').find('collCoverLogoScale').text
    vspaceInterblock = root.find('cover').find('vspaceInterblock').text
    vspaceIntrablock = root.find('cover').find('vspaceIntrablock').text

    certificateLogoScale = root.find('certificate').find('logoScale').text
    certificateCourse = root.find('certificate').find('course').text
    certificateStream = root.find('certificate').find('stream').text
    certificateUnivName = root.find('certificate').find('univName').text

    abstractFontFamily = root.find('abstractControls').find('fontFamily').text

    '''
    modifying the tex file
    '''
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
    tex = fillContent(tex, 'newcommand{\certificateCourse}{', certificateCourse)
    tex = fillContent(tex, 'newcommand{\certificateStream}{', certificateStream)
    tex = fillContent(tex, 'newcommand{\certificateUnivName}{', certificateUnivName)
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

    f = open("sample.tex", "w")
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

    f = open("sample.sty", "w")
    f.write(sty)
    f.close()
    os.system("pdflatex sample.tex")
    os.system("pdflatex sample.tex") #it must be compiled twice in order to get the table of contents updated properly

if __name__ == '__main__':
    main()