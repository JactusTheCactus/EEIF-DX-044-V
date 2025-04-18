import json
import os
import re
import pdfkit
styling = '''<style>
    body {
        background-color: #fff;
        font-family: "Times New Roman"
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
    text = f'<span class="redacted">{text}</span>'
    return text
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
fileName = 'index'
if not os.path.exists(f'{fileName}.html'):
    with open(f'{fileName}.html','') as f:
        f.write('')
with open('characters.json','r',encoding='utf-8') as f:
    file_ = f.read()
file = json.loads(file_)
def format(text,mode=''):
    text = text.replace('<br>','')
    text = text.replace('h5','h6').replace('h4','h5').replace('h3','h4').replace('h2','h3').replace('h1','h2')
    if mode == 'one-line':
        text = text.replace('<br>','')
    return text
with open(f'{fileName}.html','w') as f:
    f.write('')
with open(f'{fileName}.html','a',encoding='utf-8') as f:
    fullFile = f'<!DOCTYPE html><head><title>EEIF-DX-044-V</title></head>{styling}<body><code><hr>UNITED STATES DEPARTMENT OF DEFENSE<br>ENHANCED ENTITY INTELLIGENCE FILE (EEIF)<br>CLASSIFIED — LEVEL 5 CLEARANCE REQUIRED<br>REFERENCE CODE: EEIF-DX-044-V<hr><b>NOTICE:</b> This document contains sensitive data pertaining to enhanced, supernatural, and anomalous entities. Unauthorized access is punishable under Federal Statute {redact('|||')}-{redact('|||')}. All field agents must refer to this file when encountering subjects listed herein.<hr></code>'
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
            0: "Minimum Risk &mdash; Passive or Cooperative",
            1: "Low Risk &mdash; Requires Monitoring",
            2: "Moderate Risk &mdash; Field Agent Required",
            3: "High Risk &mdash; Armed Containment Authorized",
            4: "Extreme Risk &mdash; Termination Protocol Approved"
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
            threatLevel = listStat('Threat Level',f'<code>{'&mdash;'.join(threatListShort)}</code> <i>{f'({', '.join(threatListDesc)})' if ethics or order else ''}</i>')
        content = f"<div class=\"watermark\">CLASSIFIED</div><div id=\"{re.sub(r'"',r'',name.lower().replace(' ','-'))}\" style=\"page-break-before: always;\"><h2>ENTITY {entityNum} &mdash; {name.upper()}<br><sup><i>{indent+proName}</i></sup>{f'<br>{indent}Preferred Name: <code>{prefName}</code>' if prefName else ''}</h2>{threatLevel}{listStat('Species',species)}{listStat('Sex',sex)}{listStat('Profession',profession)}{listStat('Place of Birth',pob)}{listStat('Spoken Languages',languages)}<div id=\"description\">{description}</div></div>"
        fullFile += content
    fullFile += "</body>"
    f.write(indentFormat(fullFile))
config = pdfkit.configuration(wkhtmltopdf=r'D:\Downoads\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_file(
    getFileName(fileName, 'html'),
    getFileName(fileName, 'pdf'),
    configuration=config,
    options={
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }
)
