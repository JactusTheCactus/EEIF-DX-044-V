import json
import os
import re
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
fileName = 'index.html'
if not os.path.exists(fileName):
    with open(fileName,'x') as f:
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
with open(fileName,'w') as f:
    f.write('')
with open(fileName,'a',encoding='utf-8') as f:
    fullFile ='<code><hr style="height: 1em;color:black;background-color: black;">UNITED STATES DEPARTMENT OF DEFENSE<br>ENHANCED ENTITY INTELLIGENCE FILE (EEIF)<br>CLASSIFIED — LEVEL 5 CLEARANCE REQUIRED<br>REFERENCE CODE: EEIF-DX-044-V<hr style="height: 1em;color:black;background-color: black;"><b>NOTICE:</b> This document contains sensitive data pertaining to enhanced, supernatural, and anomalous entities. Unauthorized access is punishable under Federal Statute ███-███. All field agents must refer to this file when encountering subjects listed herein.<hr style="height: 1em;color:black;background-color: black;"></code><h3>Threat Level: [Ethics]-[Order]</h3><ul><li>Ethics: B (Benevolent), N (Neutral), M (Malevolent)</li><li>Order: S (Structured), U (Unpredictable), C (Chaotic)</li></ul>'
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
            'USAP',
            'ACCM'
        ]
        if description == None:
            description = f'Further Information About <b>{name}</b> Requires Higher Clearance Than <code>{clearance[2]}</code> To View.'
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
            ethics = eDict[ethics]
        except:
            pass
        try:
            order = item.get("alignment")["morals"]
            order = oDict[order]
        except:
            pass
        threatList = []
        if ethics: threatList.append(ethics)
        if order: threatList.append(order)
        if ethics or order:
            threatLevel = listStat('Threat Level',f'<code>{'&mdash;'.join([threat[0] for threat in threatList if threat])}</code> <i>({', '.join(threatList)})</i>')
        content = f"<div id=\"{name.lower().replace(' ','-')}\"><h2>ENTITY {entityNum} &mdash; {name.upper()}{f'<br>Preferred Name: <code>{prefName}</code>' if prefName else ''}<br><sup><i>{proName}</i></sup></h2>{threatLevel}{listStat('Species',species)}{listStat('Sex',sex)}{listStat('Profession',profession)}{listStat('Place of Birth',pob)}{listStat('Spoken Languages',languages)}<div id=\"description\">{description}</div></div>"
        fullFile += content
    f.write(indentFormat(fullFile))