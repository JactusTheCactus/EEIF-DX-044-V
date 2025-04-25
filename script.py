import json
import os
import shutil
import re
import pdfkit
fileName = 'index'
docName = 'EEIF-DX-044-V'
styling = '''<style>
    body {
        background-color: #fff;
        font-family: "Times New Roman";
        font-size: 20px;
    }
    hr {
        height: 1em;
        color: #000;
        background-color: #000;
    }
    .redacted {
        background-color: #000;
        color: #000;
        padding: 0 0.2em;
    }
    .watermark {
        display: inline-block;
        position: relative;
        top: 50%;
        left: 50%;
        font-size: 6em;
        color: rgba(200, 0, 0, 0.1);
        transform: translate(-50%, -50%) rotate(-45deg);
        -moz-transform: translate(-50%, -50%) rotate(-45deg);
        -ms-transform: translate(-50%, -50%) rotate(-45deg);
        -webkit-transform: translate(-50%, -50%) rotate(-45deg);
        transform-origin: center center;
        z-index: -1;
    }
    @media print {
        body {
            margin: 0.75in;
        }
        h2 {
            page-break-after: avoid;
        }
    }
</style>'''
styling = re.sub(r'/\*(.*)\*/',r'',styling)
styling = re.sub(r'\n',r'',styling)
styling = re.sub(r'( ){2,}',r'\1',styling)
styling = re.sub(r' ?(;) ?',r'\1',styling)
styling = re.sub(r' ?(\{|\}|:|;|,) ?',r'\1',styling)
styling = re.sub(r'(<.*>) *(.*) *(</.*>)',r'\1\2\3',styling)
charFiles = []
def mdList(html: str) -> str:
    depth = 0
    # This pattern matches either:
    #  1. group(1) = 'ul' or '/ul'    for <ul> / </ul>
    #  2. group(2) = the content inside <li>…</li>
    pattern = re.compile(r'<(/?ul)>|<li>(.*?)</li>', re.DOTALL)

    def repl(m):
        nonlocal depth
        if m.group(1):
            # we saw a <ul> or </ul>
            if m.group(1) == 'ul':
                depth += 1
            else:
                depth -= 1
            return ''                    # drop the tags themselves
        else:
            # we saw an <li>…</li>
            text = m.group(2).strip()
            indent = '    ' * (depth - 1)
            return f'{indent}- {text}\n'

    # run the substitution and strip any leading/trailing blank lines
    return pattern.sub(repl, html)#.strip()
def charFormat(file):
    file = file.replace('CLASSIFIED','')
    file = file.replace('<div class="watermark"></div>','')
    file = re.sub(r'<div id=".*" style=".*?">(.*)</div>',r'\1',file)
    file = re.sub(r'<div id=".*">(.*)</div>',r'\1',file)
    file = re.sub(r'ENTITY \d\d\d &mdash; ',r'',file)
    file = re.sub(r'<h2>(.*?)</h2>',r'# \1\n\n',file)
    file = re.sub(r'<h3>(.*?)</h3>',r'## \1\n\n',file)
    file = re.sub(r'<h4>(.*?)</h4>',r'### \1\n\n',file)
    file = re.sub(r'<h5>(.*?)</h5>',r'#### \1\n\n',file)
    file = re.sub(r'<h6>(.*?)</h6>',r'##### \1\n\n',file)
    file = re.sub(r'<code>(.*?)</code>',r'\1',file)
    file = re.sub(r'&mdash;',r'—',file)
    file = re.sub(r'<b>(.*?)</b>',r'**\1**',file)
    file = re.sub(r'<i>(.*?)</i>',r'*\1*',file)
    file = re.sub(r'<p>(.*?)</p>',r'\n\1\n',file)
    file = re.sub(r'&nbsp;',r'',file)
    file = re.sub(r'<sup>(.*?)</sup>',r'\1',file)
    file = re.sub(r'<span class="redacted">(.*?)</span>',lambda m:'█'*len(m.group(1)),file)
    file = mdList(file)
    return file
def clearDir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
def mdFormat(html):
    html = re.sub(r'<style>.*</style>',r'',html)
    html = re.sub(r'<!DOCTYPE html>',r'',html)
    html = re.sub(r'<title>.*</title>',r'',html)
    html = re.sub(r'<head></head>',r'',html)
    html = re.sub(r'<div class="watermark">CLASSIFIED</div>',r'',html)
    html = re.sub(r'<span class="redacted">(.*?)</span>',lambda m:'█'*len(m.group(1)),html)
    return html
def getFileName(name, type):
    return name + '.' + type
def repeat(string:str='',repetitions:int=1)->str:
    try:
        string
    except:
        return 'Invalid String'
    try:
        repetitions
    except:
        return 'Invalid Integer'
    return string * repetitions
def redact(text,length=None):
    if text == '':
        text = repeat('-',length)
    if '<span class="redacted">' in text:
        pass
    if length:
        text = text[:length]
    text = '█'*len(text)
    text = f'<span class="redacted">{text}</span>'
    return text
header = (
    f"<code><hr>UNITED STATES DEPARTMENT OF DEFENSE<br>"
    f"ENHANCED ENTITY INTELLIGENCE FILE (EEIF)<br>" 
    f"CLASSIFIED — LEVEL 5 CLEARANCE REQUIRED<br>" 
    f"REFERENCE CODE: {docName}<hr>" 
    f"<b>NOTICE:</b> This document contains sensitive data pertaining to enhanced, supernatural, and anomalous entities. " 
    f"Unauthorized access is punishable under Federal Statute {redact('|||')}-{redact('|||')}. " 
    f"All field agents must refer to this file when encountering subjects listed herein.<hr></code>"
)
indent = repeat('&nbsp;',4)
def listStat(label, stat):
    if stat in ['',None]:
        return ''
    else:
        return f'<p>{label}: <b>{stat}</b></p>'
def indentFormat(text):
    output1 = re.sub(r'(</h1>)(.*?)(<h1>|$)', r'\1<ul>\2</ul>\3', text)
    output2 = re.sub(r'(</h2>)(.*?)(<h2>|</div>)', r'\1<ul>\2</ul>\3', output1)
    output3 = re.sub(r'(</h3>)(.*?)(<h3>|</div>)', r'\1<ul>\2</ul>\3', output2)
    output4 = re.sub(r'(</h4>)(.*?)(<h4>|</div>)', r'\1<ul>\2</ul>\3', output3)
    output5 = re.sub(r'(</h5>)(.*?)(<h5>|</div>)', r'\1<ul>\2</ul>\3', output4)
    output6 = re.sub(r'(</h6>)(.*?)(<h6>|</div>)', r'\1<ul>\2</ul>\3', output5)
    output7 = re.sub(r'(</?ul>)\1+', r'\1', output6)
    return output7
if not os.path.exists(f'{fileName}.html'):
    with open(f'{fileName}.html','') as f:
        f.write('')
with open('characters.json','r',encoding='utf-8') as f:
    file_ = f.read()
file = json.loads(file_)
file__ = list(sorted(file, key=lambda char: char["name"][-2][0]))
file = file__
def format(text,mode=''):
    text = text.replace('<br>','')
    text = text.replace('h5','h6').replace('h4','h5').replace('h3','h4').replace('h2','h3').replace('h1','h2')
    if mode == 'one-line':
        text = text.replace('<br>','')
    return text
with open(f'{fileName}.html','w') as f:
    f.write('')
with open(f'{fileName}.html','a',encoding='utf-8') as f:
    fullFile = f'<!DOCTYPE html><head><title>{docName}</title></head>{styling}<body>{header}'
    index = 0
    for item in file:
        entityNum = f'{file.index(item) + 1}'
        if len(entityNum) == 1:
            entityNum = '00' + entityNum
        elif len(entityNum) == 2:
            entityNum = '0' + entityNum
        prefName = item.get("name")[-1][0]
        nameList = []
        if item.get("name")[0][0] == '':
            continue
        for i in range(len(item.get("name"))):
            try:
                nameList.append(item.get("name")[i][0])
            except:
                pass
        nameList.pop(-1)
        name = ' '.join(nameList)
        proNameList = []
        if item.get("name")[0][1] == '':
            continue
        for i in range(len(item.get("name"))-1):
            try:
                proNameList.append(item.get("name")[i][1])
            except:
                pass
        if len(item.get("name")) == 3 and len(item.get("name")[-1]) > 1:
            proNameList.append(item.get("name")[2][1])
        proName = '&mdash;'.join(proNameList)
        altNameList = []
        if len(item.get("name")[0]) > 2:
            for i in item.get("name"):
                if len(i) > 2:
                    altNameList.append(i[2])
        if len(altNameList) != 0:
            altName = " ".join(altNameList)
        else:
            altName = None
        description = item.get("description")
        clearance = [
            'TOP SECRET',
            'SECRET',
            'CONFIDENTIAL',
            'Unacknowledged Special Access Program',
            'Alternative or Compensatory Control Measures'
        ]
        if description == None:
            clearanceLevel = item.get("alignment")["risk"]
            if type(clearanceLevel) is str:
                clearanceLevel = 0
            description = f'Further Information About <b>{name}</b> Requires Higher Clearance Than <code>{clearance[clearanceLevel]}</code> To View.'
        description = format(description)
        pobList = []
        getPob = item.get("pob")
        if getPob:
            for i in reversed(range(3)):
                try:
                    pobList.append(getPob[i])
                except IndexError:
                    pass
        pob = ', '.join(pobList)
        profession = ''
        try:
            profession = item.get('profession')
        except:
            pass
        sex = item.get("sex")
        species = ''
        try:
            species += item.get("species")[0]
        except:
            pass
        try:
            species += f' ({item.get("species")[1]})'
        except:
            pass
        languages = ''
        try:
            languageList = item.get("languages")
        except:
            pass
        languageList[0] = f'<i>{languageList[0]}</i>'
        languages = ', '.join(languageList)
        threatLevel = ''
        eDict = {
            'good': 'Benevolent',
            'neutral': 'Neutral',
            'evil': 'Malevolent'
        }
        oDict = {
            'lawful': 'Structured',
            'neutral': 'Unpredictable',
            'chaotic': 'Chaotic'
        }
        try:
            ethics = item.get("alignment")["empathy"]
            if ethics == '':
                ethics = redact(ethics,10)
            else:
                ethics = eDict[ethics]
        except:
            pass
        try:
            order = item.get("alignment")["morals"]
            if order == '':
                order = redact(order,10)
            else:
                order = oDict[order]
        except:
            pass
        risk_dict = {
            4: "Minimum Risk &mdash; Passive or Cooperative",
            3: "Low Risk &mdash; Requires Monitoring",
            2: "Moderate Risk &mdash; Field Agent Required",
            1: "High Risk &mdash; Armed Containment Authorized",
            0: "Extreme Risk &mdash; Termination Protocol Approved"
        }
        if item.get("alignment")["risk"] == '':
            risk = redact(risk)
        else:
            risk = str(item.get("alignment")["risk"])
        threatList = [x for x in (ethics, order, risk) if x]
        threatListDesc = [x for x in (ethics, order, risk_dict.get(item.get("alignment")["risk"], redact('CLASSIFIED'))) if x]
        threatListShort = []
        for threat in threatList:
            if threat:
                if threat[0] != '<':
                    threatListShort.append(threat[0])
                elif threat[0] == '<':
                    threat = redact(threat[23])
                    threatListShort.append(threat)
        if ethics or order or risk:
            threatLevel = listStat(
                'Threat Level',
                f"<code>{'&mdash;'.join(threatListShort)}</code> "
                f"<i>{'(' + ', '.join(threatListDesc) + ')' if (ethics or order) else ''}</i>"
             )
        clean_id = re.sub(r'"', '', name.lower().replace(' ', '-'))
        content = f'''
<div class="watermark">CLASSIFIED</div>
<div id="{clean_id}" style="page-break-before: always;">
  <h2>
    ENTITY {entityNum} &mdash; {name.upper()}
    {f"<br><sup><i>{indent + altName}</i></sup>" if altName is not None else ""}
    {f"<br><sup><i>{indent + proName}</i></sup>" if preName is not None else ""}
    {f"<br>{indent}Preferred Name: <code>{prefName}</code>" if prefName else ""}
  </h2>
  {threatLevel}
  {listStat("Species", species)}
  {listStat("Sex", sex)}
  {listStat("Profession", profession)}
  {listStat("Place of Birth", pob)}
  {listStat("Spoken Languages", languages)}
  <div id="description">{description}</div>
</div>
'''.strip()
        fullFile += content
        charDir = 'obsidian/EEIF-DX-044-V/characters' 
        clearDir(charDir)
        name = re.sub(r" \".*\" ",r" ",name)
        name = name.lower()
        charNameList = name.split()
        for i in range(len(charNameList)):
            charNameList[i] = charNameList[i].capitalize()
        name = ' '.join(charNameList)
        charFile = getFileName(f'{charDir}/{name}','md')
        charFiles.append([charFile,content])
        with open(charFile,'w',encoding='utf-8') as char:
            char.write(mdFormat(content))
        index += 1
    fullFile += "</body>"
    f.write(indentFormat(fullFile))

pdfkit.from_file(
    getFileName(fileName, 'html'),
    getFileName(docName, 'pdf'),
    options={
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }
)
for i in range(len(charFiles)):
    with open(charFiles[i][0],'w',encoding='utf-8') as f:
        f.write(charFormat(charFiles[i][1]))
with open(getFileName(fileName,'html'),'r',encoding='utf-8') as f:
    htmlFile = f.read()
header = charFormat(mdFormat(header))
header = re.sub(r'<pre>(.*)</pre>',r'\1',header)
header = re.sub(r'<hr>',r'\n\n---\n\n',header)
header = re.sub(r'<br>',r'  \n',header)
header = re.sub(r'^\n',r'',header)
header = re.sub(r'\n$',r'',header)
with open(getFileName('README','md'),'w',encoding='utf-8') as f:
    f.write(header)
charFileList = [f for f in os.listdir(charDir) if os.path.isfile(os.path.join(charDir, f))]
for i in range(len(charFileList)):
    charFileList[i] = f'{charDir}/{charFileList[i]}'
with open(f'{docName}.md','w',encoding='utf-8') as f:
    f.write(f'{header}\n')
for i in charFileList:
    with open(i,'r',encoding='utf-8') as c:
        character = c.read()
    with open(f'{docName}.md','a',encoding='utf-8') as f:
        f.write(f'\n---\n\n{character}\n\n---\n')
