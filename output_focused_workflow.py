exec(open('build_workflow.py',encoding='utf-8').read().split("d.add_heading('M Pesa wallet reconciliation workflow',0)")[0])
from PIL import Image, ImageDraw, ImageFont

d.add_heading('M Pesa reconciliation outputs and workflow',0)
p('WasaaChat Ltd | Finance Revenue Analyst | Version 3.0 | 17 November 2026 | Proposed procedure for Finance review')
p('Each reconciliation must deliver an approved report that proves the M-Pesa statement ending balance agrees to the cleared platform movements for the same account and cutoff. The report must also identify every unmatched item and show who will resolve it. The workflow below defines the output required at each stage and the evidence needed to accept it.')
h('The final output')
p('A signed reconciliation pack containing the balance summary, transaction clearing schedule, exception register, approved adjustment log and supporting source files. The closing position becomes the next period’s opening position only after approval. All amounts are KES; timestamps are displayed in EAT.')
table(['Required output','Acceptance condition'],[
('Balance summary','Verified opening balance, statement cutoff and closing balance, cleared deposits, withdrawals and charges, calculated cleared balance and zero difference.'),
('Transaction clearing schedule','Every eligible platform movement is listed with its reference, timestamp, direction, amount, matching evidence and clearing status.'),
('Exception register','Every unticked platform item and statement-only item is individually recorded, including offsetting items, with owner, evidence, due date and status.'),
('Adjustment and approval log','Each correction links to an exception and evidence, identifies maker and separate approver, and has a posting reference.'),
('Signed report and archive','Preparer and separate reviewer approval, retained source files, locked ending position and traceable carry-forward.')],[1.7,5.0])
h('The completion decision')
p('Difference = statement ending balance minus cleared balance. A zero difference permits reviewer sign-off only after all unmatched items have been reviewed and assigned. If the difference is nonzero, investigate and correct the underlying entries, then rerun the calculation. Recording an explanation or posting an unapproved adjustment never completes the reconciliation.')
p('Open items may remain only when the cleared difference is zero, each item has an evidence-backed explanation and the reviewer explicitly accepts its carry-forward. Report the status as Reconciled with open items. Use Fully reconciled when no open items remain. A supporting bridge may explain a nonzero difference, but the run remains a draft under this completion rule.')

page('Stage outputs and acceptance checks')
h('1 Validated source pack')
p('Output: retained M-Pesa statement or validated Daraja export, platform wallet export, and an import control summary for the same account. The summary records filenames, extraction times, source counts and amounts, duplicates, exclusions and rejected rows.')
p('Accept when timestamps and movement directions are normalized, conflicting duplicates and invalid records are resolved, and only completed in-scope KES M-Pesa movements enter period totals. Exclude failed attempts, pending items, internal transfers and other rails. Preserve reversals with original references and correct balance effects. Verify blank rail values against statement evidence. Include two days either side of the cutoff in investigation extracts, without adding out-of-period rows to period totals. Owner: preparer.')
h('2 Confirmed statement position')
p('Output: statement ending date and time, independently entered ending balance and the statement evidence reference. Record charges separately where the source has no charge rows; never count them twice or substitute platform service fees for M-Pesa charges.')
p('Accept when the statement account and cutoff are verified and the ending timestamp follows the approved opening cutoff. Periods longer than seven days require Finance lead approval. For the first run, the Finance lead verifies the opening balance and timestamp from independent evidence. Owner: preparer; Finance lead approves initial setup.')
h('3 Populated reconciliation schedule')
p('Output: the locked opening position from the prior approved statement ending position and every completed platform movement strictly after opening and at or before ending, sorted oldest first. Show transaction ID, M-Pesa receipt when available, counterparty, deposit, withdrawal and clearing status.')
p('Accept when the period has no gaps or overlaps and transactions exactly at the ending timestamp are included. Use completion timestamps for the financial cutoff; creation-only timestamps require a documented cutoff review. Search and filters must not change period totals. Owner: system, checked by preparer.')
h('4 Cleared transaction schedule and live difference')
p('Output: matched rows with evidence, cleared deposit and withdrawal amounts and counts, confirmed charges, cleared balance and live difference. Match uniquely by M-Pesa receipt, amount, direction and currency. Amount and MSISDN within 15 minutes may support a suggested match, subject to preparer confirmation and reviewer sampling. Manual matches need a reason and reviewer approval.')
p('Accept when every checked row has supporting statement evidence and ambiguous matches remain unresolved. Bulk clearing requires the same evidence as individual clearing. Owner: preparer; reviewer checks inferred matches.')

page('Exception resolution and approved output')
h('5 Owned exception register')
p('Output: one record for each statement-only, platform-only, amount mismatch or cutoff item, whether or not the net difference is zero. Include exception ID, account, source references, timestamp, direction, amount, evidence, reason, owner, due date, status and any adjustment reference.')
table(['Exception','Accountable owner','Resolution target'],[
('Statement only','Engineering for callbacks; Finance for portal payouts','One business day'),
('Platform only','Fraud or AML lead with Finance','Escalate same day'),
('Amount mismatch','Finance','Two business days'),
('Timing difference','Finance','Confirm at next reconciliation')],[1.5,3.3,1.9])
p('Unsupported platform credits must not be assumed to be timing items. Follow the approved fraud process for investigation and restrictions. Escalate items older than seven days to the Finance lead and review ageing weekly. Owner: assigned investigator; preparer maintains the register.')
h('6 Posted corrections and refreshed reconciliation')
p('Output: evidence-backed correction requests, independent maker-checker approvals, actual ledger posting references and a refreshed transaction schedule. Replay callbacks or reverse failed payouts only after confirming the real movement. Keep the original entry, correction and audit trail linked.')
p('Accept when corrections address specific exceptions and the reconciliation is recalculated from the corrected source. Return to matching and difference review after every change. A narrative explanation cannot set the difference to zero; unsupported balancing entries are prohibited. Owner: maker and separate approver.')
h('7 Signed reconciliation report and next opening')
p('Output: the approved balance summary and clearing schedule, the exception register including accepted open items, correction log, source evidence, preparer and reviewer names, approval timestamps and a locked period identifier.')
p('Accept when the cleared difference is exactly zero, source completeness is checked, every unmatched item is reviewed, and maker-checker requirements are satisfied. The reviewer must be a different person from the preparer. Archive the report and sources in an access-controlled shared location; browser storage or an attachment filename alone is insufficient.')
p('Carry the approved statement ending balance and exact ending timestamp to the next opening position. Carry unresolved exceptions separately with their original age and references, avoiding duplicate recognition. Reopening an approved period requires approval and a retained change history. Finance agrees the M-Pesa control account to the general ledger monthly.')

page('Balance output specification')
h('Required calculation')
p('Cleared balance = opening balance + checked deposits - checked withdrawals - confirmed M-Pesa charges.')
p('Difference = statement ending balance - cleared balance.')
p('Calculate in integer KES cents and display two decimals. Charges are included once. Deposits increase the M-Pesa asset balance; withdrawals and charges decrease it. Use the same formula on screen, in completion checks and in the exported report.')
h('Balanced acceptance example')
table(['Report line','KES'],[('Verified opening balance','1,000.00'),('Checked deposits','500.00'),('Checked withdrawals','(200.00)'),('Confirmed charges','(10.00)'),('Cleared balance','1,290.00'),('Statement ending balance','1,290.00'),('Difference','0.00')],[4.8,1.9])
p('Expected result: the run becomes eligible for independent review. Approval still requires the clearing evidence and exception review; a zero value does not prove that all items are matched correctly.')
h('Exception acceptance example')
p('Using the original worked figures: opening 2,184,300.00 plus checked deposits 3,412,000.00 less checked withdrawals 1,233,800.00 and charges 8,400.00 gives cleared balance 4,354,100.00. Statement balance 4,339,400.00 gives difference -14,700.00. The run stays a draft.')
p('Record the two statement-only payouts of 8,500.00 and 6,200.00 and the unticked platform withdrawal of 2,500.00 separately. An explanatory bridge ties the adjusted statement and full platform balance at 4,351,600.00, but it does not change the cleared difference. Validate and approve the appropriate corrections, refresh the source, match again and recalculate before sign-off.')
h('App requirements needed to produce these outputs')
p('Correct the app difference formula to closing minus opening minus checked deposits plus checked withdrawals plus charges. Add statement-only exceptions, evidence retention and independent review gates. Preserve approved snapshots, automatically carry forward the approved statement position, and retain open-item ageing. Add validated receipt and completion-time fields and explicit reversal handling. The existing JSON export and local history need these controls before they can serve as the approved output pack.')

# Static flowchart with direct output labels and a correction loop.
im=Image.new('RGB',(1500,1700),'white'); g=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',27)
def text(x,y,t):
 lines=t.split('\n')
 for i,line in enumerate(lines):g.text((x,y+(i-(len(lines)-1)/2)*34),line,font=font,fill='#173E48',anchor='mm')
def box(rect,t,fill='#E9F4F0'):
 g.rounded_rectangle(rect,radius=20,fill=fill,outline='#417A70',width=3); text((rect[0]+rect[2])/2,(rect[1]+rect[3])/2,t)
def arrow(pts):
 import math
 g.line(pts,fill='#53626A',width=4); x,y=pts[-1]; a=math.atan2(y-pts[-2][1],x-pts[-2][0]); g.polygon([(x,y),(x-17*math.cos(a-.45),y-17*math.sin(a-.45)),(x-17*math.cos(a+.45),y-17*math.sin(a+.45))],fill='#53626A')
box((40,20,690,120),'M-Pesa statement\nRetained independent source')
box((810,20,1460,120),'Platform wallet ledger\nRetained transaction export','#EEEFFA')
arrow([(365,120),(750,180)]); arrow([(1135,120),(750,180)])
nodes=[(180,290,'OUTPUT 1   Validated source pack\nNormalized records and import controls'),(340,450,'OUTPUT 2   Confirmed statement position\nEnding cutoff, balance and charge evidence'),(500,610,'OUTPUT 3   Reconciliation schedule\nVerified opening and eligible transactions'),(660,770,'OUTPUT 4   Cleared schedule\nMatched evidence, totals and live difference')]
for y1,y2,t in nodes:box((250,y1,1250,y2),t)
for a,b in [(290,340),(450,500),(610,660),(770,825)]:arrow([(750,a),(750,b)])
g.polygon([(750,825),(1070,910),(750,995),(430,910)],fill='#F5F6F6',outline='#53626A',width=3); text(750,910,'Difference = zero?')
arrow([(430,910),(225,910),(225,1320)]); text(220,960,'Yes')
arrow([(1070,910),(1130,910),(1130,1040)]); text(1200,965,'No')
box((720,1040,1470,1150),'OUTPUT 5   Owned exception register\nBoth source sides, evidence, owner and SLA','#FFF1DE')
arrow([(1095,1150),(1095,1200)])
box((720,1200,1470,1320),'OUTPUT 6   Approved posted corrections\nMaker-checker log and refreshed source','#FFF1DE')
arrow([(1470,1260),(1490,1260),(1490,635),(1260,635),(1260,715),(1250,715)])
text(1100,1370,'Recalculate before sign-off')
box((40,1320,650,1450),'Review all unmatched items\nAccept evidence and open-item owners\nIndependent reviewer approval')
arrow([(345,1450),(345,1510),(750,1510),(750,1550)])
box((140,1550,1360,1680),'OUTPUT 7   Signed report and locked period\nArchive sources and approvals\nCarry statement ending position and open items forward')
im.save('workflow-flowchart.png',dpi=(240,240))
page('Output focused process flow')
p('Each stage produces a reviewable output. Nonzero differences return through investigation and approved corrections to matching and recalculation. Sign-off requires zero difference and independent review.')
r=d.add_paragraph().add_run(); r.add_picture('workflow-flowchart.png',width=Inches(6.45))
r._r.xpath('.//wp:docPr')[0].set('descr','Two retained sources produce validated data, statement position, a reconciliation schedule and cleared totals. Nonzero difference leads to owned exceptions and approved corrections, then returns to matching. Zero difference leads to unmatched-item review, independent approval, a signed report, archiving and carry forward.')
d.save('MPesa-Wallet-Reconciliation-Workflow-Optimized.docx')
print('Saved output focused workflow with embedded diagram')
