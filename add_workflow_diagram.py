from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import math

im=Image.new('RGB',(1600,1780),'white'); g=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',29)
bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',30)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
ink='#18364A'; line='#476172'
def label(x,y,lines,f=font):
 for n,t in enumerate(lines.split('\n')):
  g.text((x,y+n*38),t,font=f,fill=ink,anchor='mm')
def box(x1,y1,x2,y2,txt):
 g.rounded_rectangle((x1,y1,x2,y2),radius=14,fill='#EEF4F7',outline=line,width=3)
 lines=txt.split('\n'); label((x1+x2)/2,(y1+y2)/2-(len(lines)-1)*19,txt)
def arrow(points):
 g.line(points,fill=line,width=4)
 x,y=points[-1]; px,py=points[-2]; a=math.atan2(y-py,x-px)
 g.polygon([(x,y),(x-17*math.cos(a-.45),y-17*math.sin(a-.45)),(x-17*math.cos(a+.45),y-17*math.sin(a+.45))],fill=line)

box(400,20,1200,130,'Verify opening balance and cutoff\nFinance lead approval for first run')
box(400,180,1200,290,'Retain statement and platform export\nValidate account, scope and duplicates')
box(400,340,1200,450,'Enter statement ending time and balance\nRecord evidenced charges once')
box(400,500,1200,610,'Match and clear eligible transactions\nRetain receipt and approval evidence')
box(400,660,1200,808,'Investigate unmatched items on both sides\nAssign evidence, owner and due date\nApprove and post supported corrections')
box(400,858,1200,968,'Recalculate totals and prepare bridge\nCompare with the full platform balance')
for y1,y2 in [(130,180),(290,340),(450,500),(610,660),(808,858),(968,1018)]:arrow([(800,y1),(800,y2)])
g.polygon([(800,1018),(1170,1113),(800,1208),(430,1113)],fill='#F5F7F9',outline=line,width=3)
label(800,1090,'Unexplained difference zero\nand review pack complete?',small)
arrow([(430,1113),(190,1113),(190,734),(400,734)])
label(235,1060,'No',bold)
arrow([(800,1208),(800,1270)]); label(860,1235,'Yes',bold)
box(400,1270,1200,1380,'Independent reviewer approval\nAccept each remaining open item')
arrow([(800,1380),(800,1440)])
box(65,1440,750,1550,'Open items remain\nReconciled with open items')
box(850,1440,1535,1550,'No open items remain\nFully reconciled')
# Fork arrows connect approval to both outcome boxes.
g.rectangle((780,1400,820,1438),fill='white')
arrow([(800,1380),(800,1410),(408,1410),(408,1440)])
arrow([(800,1410),(1192,1410),(1192,1440)])
arrow([(408,1550),(408,1590),(800,1590),(800,1630)])
arrow([(1192,1550),(1192,1590),(800,1590)])
box(220,1630,1380,1750,'Lock and archive report, sources and approvals\nNext opening = approved statement ending balance\nCarry open exceptions separately and review ageing')
im.save('workflow-flowchart.png',dpi=(240,240))
d=Document('MPesa-Wallet-Reconciliation-Workflow-Optimized.docx')
d.add_page_break(); d.add_heading('Reconciliation process flow',1)
d.add_paragraph('Follow the process from the verified opening position to the approved output. Return to investigation whenever the bridge or review evidence is incomplete.')
p=d.add_paragraph(); r=p.add_run(); r.add_picture('workflow-flowchart.png',width=Inches(6.45))
pr=r._r.xpath('.//wp:docPr')[0]; pr.set('descr','Reconciliation flow from opening verification through source validation, statement inputs, matching, exception investigation and bridge calculation. Incomplete review or nonzero unexplained difference returns to investigation. Independent approval leads to reconciled with open items or fully reconciled, followed by archiving and carry forward.')
d.save('MPesa-Wallet-Reconciliation-Workflow-Optimized.docx')
print('Added flowchart page and alternative text')
