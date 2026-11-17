from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

d=Document()
s=d.sections[0]; s.top_margin=s.bottom_margin=Inches(.7); s.left_margin=s.right_margin=Inches(.8)
for name in ['Normal','Title','Heading 1','Heading 2']:
 st=d.styles[name]; st.font.name='Calibri'; st.font.color.rgb=RGBColor(0,0,0)
d.styles['Normal'].font.size=Pt(11)
d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Title'].font.size=Pt(25)
d.styles['Heading 1'].font.size=Pt(17)
d.styles['Heading 2'].font.size=Pt(12)
def p(t): d.add_paragraph(t)
def h(t): d.add_heading(t,2)
def page(t): d.add_page_break(); d.add_heading(t,1)
def table(headers, rows, widths):
 t=d.add_table(rows=1, cols=len(headers)); t.autofit=False
 for c,w in zip(t.columns,widths): c.width=Inches(w)
 for c,tx in zip(t.rows[0].cells,headers): c.text=tx
 for row in rows:
  for c,tx in zip(t.add_row().cells,row): c.text=tx
 for i,row in enumerate(t.rows):
  for c in row.cells:
   pr=c._tc.get_or_add_tcPr(); shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'E8EEF3' if i==0 else ('F5F7F9' if i%2==0 else 'FFFFFF')); pr.append(shade)
   borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9'); borders.append(e)
   pr.append(borders)
   for pa in c.paragraphs:
    pa.paragraph_format.space_after=Pt(5); pa.paragraph_format.space_before=Pt(5)
    for r in pa.runs: r.font.size=Pt(10); r.bold=i==0
  if i==0: row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))

d.add_heading('M Pesa wallet reconciliation workflow',0)
p('Operating procedure and implementation requirements for the Recon finance workspace')
p('WasaaChat Ltd | Owner Finance Revenue Analyst | Version 2.0 | 17 November 2026 | Proposed revision for Finance review')
h('Purpose and required output')
p('For each statement cutoff, produce a saved reconciliation that connects the independent M-Pesa balance to completed platform wallet movements, identifies every unmatched item, and records a separate reviewer decision. A zero number alone does not establish that transactions are correct.')
p('The output pack contains the period and opening source, statement ending balance, cleared totals, cleared difference, a bridge to the full platform ledger, exceptions, evidence and approval. The browser screen is the working view; the retained report and supporting files form the review record.')
h('Scope and account basis')
p('Include completed KES C2B deposits, B2C withdrawals, confirmed M-Pesa charges and supported reversals affecting the same paybill or account. Exclude internal wallet transfers, failed or pending attempts and other payment rails. Reconcile distinct M-Pesa accounts separately. Platform service fees are not M-Pesa charges unless evidenced as such.')
p('Use the M-Pesa asset account perspective throughout: deposits increase the balance; withdrawals and charges reduce it. If the source describes customer wallet liability movements, map direction to this account perspective before calculation.')
h('Completion rule')
p('Use two distinct measures. Cleared difference compares the statement with matched movements. Unexplained difference compares the adjusted statement with the full platform balance. Logging an exception does not change either balance. An explained reconciliation may be approved with open items only when the bridge is zero and every item has evidence, an owner, a due date and reviewer acceptance. Label this status Reconciled with open items; reserve Fully reconciled for no remaining open items.')
h('Roles and cadence')
p('The preparer reconciles daily and investigates exceptions. A different reviewer checks matching, adjustments and the bridge. The Finance lead authorizes the first opening position, periods longer than seven days and overdue escalation. Engineering resolves callback failures. The Fraud or AML lead handles unsupported wallet credits through the existing fraud process independently of the adjustment maker.')

page('Prepare and run the reconciliation')
h('1 Establish the opening position')
p('For the first run, the Finance lead verifies the M-Pesa opening balance at an exact EAT timestamp and records the account, statement reference and approval. Never assume zero because the platform export starts late. For later runs, carry forward the prior approved statement ending balance and cutoff automatically. Carry unresolved items separately so they remain visible and are not counted twice. Reopening requires reviewer approval and an audit trail.')
h('2 Obtain and validate both sources')
p('Retain the M-Pesa statement and the platform export, including two days either side of the cutoff for investigation. Use only transactions strictly after the opening timestamp and at or before the ending timestamp in period totals. Display EAT and preserve source timestamps. Use completion time for the required financial cutoff; where only creation time is available, identify and investigate the cutoff limitation.')
p('Record source filenames, account, extraction time, record counts and totals. Deduplicate by a stable transaction identifier; stop on conflicting duplicates or invalid amounts and timestamps. Count and explain exclusions. Inspect missing payment rail values before treating them as M-Pesa. Preserve reversals with their original transaction link and direction; do not silently discard them.')
h('3 Enter the statement position')
p('Enter the statement ending date and time and the independent ending balance. Enter evidenced B2C charges separately if the transaction source has no charge rows. Attach or securely reference the statement. A period exceeding seven days requires a Finance lead approval reference. Charges must be counted once only, either as rows or in the separate charge total.')
h('4 Match and clear')
p('List eligible platform transactions oldest first, with date and time, transaction ID, M-Pesa receipt, counterparty, deposit, withdrawal and clearing status. Show opening, closing, cleared totals and difference. Search and filters must not alter period totals. A bulk selection applies to all matching rows across pages and requires the same evidence as individual clearing.')
p('Tier 1: uniquely match receipt, direction, currency and amount. Tier 2: suggest a unique match using amount, normalized MSISDN and timestamps within 15 minutes; require preparer confirmation and reviewer sampling. Tier 3: require a written reason, evidence and reviewer approval before acceptance. Never force an ambiguous or many-to-one match. Do not infer an M-Pesa receipt from an undocumented reference field.')
h('5 Investigate and retain the output')
p('Record platform-only and statement-only items independently, including offsetting errors even when the net difference is zero. Post corrections under maker-checker approval and rerun against the corrected source. Save a draft during investigation. Submit the bridge and evidence for review, then approve, lock and export the report. Preserve open items for the next run and review ageing weekly; agree the M-Pesa control account to the general ledger monthly.')

page('Calculation rules and worked output')
p('All calculations use integer KES cents internally and display two decimal places. O is the verified opening balance; S is the independent statement ending balance; Dc and Wc are cleared deposits and withdrawals; Cc is the evidenced charge total included in cleared movements.')
h('Cleared balance and cleared difference')
p('Cleared balance = O + Dc - Wc - Cc')
p('Cleared difference = S - cleared balance = S - O - Dc + Wc + Cc')
p('A negative cleared difference means the statement balance is lower than the matched balance. Investigate additional payouts or charges, overstated matched receipts and cutoff errors. A positive value indicates the reverse possibilities. The sign guides investigation; it does not establish the cause.')
h('Worked example for 7 October 2026')
table(['Cleared position','KES'],[
('Opening at 30 September cutoff','2,184,300.00'),('Cleared deposits 412 of 412','3,412,000.00'),('Cleared withdrawals 318 of 319','1,233,800.00'),('Confirmed charges','8,400.00'),('Cleared balance','4,354,100.00'),('Statement ending balance','4,339,400.00'),('Cleared difference','-14,700.00')],[4.8,1.9])
p('Assume investigation confirms two statement-only payouts of KES 8,500 and KES 6,200, plus platform-only withdrawal WD-104377 of KES 2,500. These causes require evidence; the numbers alone do not prove them.')
h('Bridge from statement to full platform balance')
table(['Reconciliation statement','KES'],[
('M-Pesa statement ending balance','4,339,400.00'),('Add statement-only payouts not recorded on platform','14,700.00'),('Less platform-only withdrawal not paid by M-Pesa','(2,500.00)'),('Adjusted statement balance','4,351,600.00'),('Full platform balance including the unticked withdrawal','4,351,600.00'),('Unexplained difference','0.00')],[4.8,1.9])
p('The cleared difference remains -14,700.00 until supported corrections change the matched calculation. The bridge explains the difference and supports Reconciled with open items after reviewer approval. It does not manufacture a zero cleared difference. Opening for the next statement period remains the approved statement balance of KES 4,339,400.00, with all three open items carried separately.')

page('Exceptions evidence and approval')
h('Exception record')
p('Assign each item a unique reference, account, source side, transaction and receipt references, type, direction, amount, timestamp, reason, evidence location, owner, due date, age and status. Include its signed bridge effect and link any correction and approval. Record statement-only items even when no platform row exists. Closing an item requires evidence of settlement or correction.')
table(['Type','Owner','Required action and deadline'],[
('M-Pesa only','Engineering or Finance','Investigate missing callbacks or portal payments; replay or post only after validation. Target one business day.'),
('Platform only','Fraud or AML lead','Escalate the same day. Unsupported wallet credits are never assumed to be timing. Apply wallet restrictions under the approved fraud procedure; reverse only after validation.'),
('Amount differs','Finance','Investigate fees, partial payouts and mapping; approve the correction. Target two business days.'),
('Timing only','Finance','Evidence both timestamps; carry forward and confirm at the next reconciliation. Escalate if not cleared.')],[1.2,1.3,4.2])
h('Reviewer gates')
p('The reviewer confirms the account and cutoffs, opening source and continuity, import completeness, charge treatment, clearing evidence and all unmatched items. Review Tier 2 samples and every Tier 3 decision. Confirm the bridge is mathematically zero and every open item is individually accepted. An exception entry alone never reduces the difference.')
p('Ledger corrections require a second person to approve before posting. Record maker, approver, timestamps and links to the underlying exception. Do not post an unsupported balancing adjustment. Escalate open items older than seven days to the Finance lead and retain the original due date and history.')
h('Minimum retained output pack')
p('Retain a readable reconciliation statement and machine-readable detail with account, run ID, opening and ending EAT timestamps, opening evidence, source counts, cleared deposits and withdrawals with counts, charges, cleared balance and difference, full platform balance, signed bridge, unexplained difference, exceptions and reviewer decision. Include creation, completion and approval timestamps and the preceding run reference.')
p('Keep the original statement and exports with the report in an access-controlled shared location. A filename is not a retained attachment. Browser storage is device-specific and may be cleared; it is not the sole audit archive. Review and archive each approved run before moving to the next period.')

page('Recon implementation requirements and acceptance')
p('The current browser app provides CSV import, an opening setup, EAT period filtering, manual clearing, draft history and JSON export. The following gaps must be resolved before the workflow can rely on its Completed status as Finance approval.')
h('Priority requirements')
p('1 Correct the calculation and displayed explanation. The current difference is S - O - Cc + Dc - Wc; replace it with S - O - Dc + Wc + Cc. Keep the cleared balance, displayed difference, completion checks and export consistent.')
p('2 Add the statement-to-platform bridge, statement-only exceptions and carried open items. The present Finish action requires a zero cleared difference and cannot approve the worked example as explained. Distinguish draft, submitted, reconciled with open items and fully reconciled statuses.')
p('3 Enforce separate reviewer approval, evidence retention and immutable approved snapshots. The present attachment records filename and size, manual checks need no approval, and completion checks zero difference without validating the review pack. Record evidence and approvals per run and prevent later imports or edits from changing approved results.')
p('4 Carry forward the prior approved statement cutoff and balance automatically. The present completion action does not advance the opening position. Protect continuity and retain correction history rather than silently editing an approved opening.')
p('5 Expand source coverage. The current importer accepts completed KES deposit and withdrawal rows with Daraja or blank rail and filters on created_at. Add validated completion timestamps, dedicated M-Pesa receipts, statement ingestion and explicit reversal handling. Verify blank rails manually until mapping is reliable. Keep charges separate until row-level charge support exists.')
h('Acceptance checks')
table(['Scenario','Required result'],[
('Simple balanced period','O 1,000; deposits 500; withdrawals 200; charges 10; S 1,290. Cleared balance 1,290 and difference 0.'),
('Cutoff boundaries','Exclude the row exactly at opening; include the row exactly at ending. UTC and EAT representations produce identical inclusion.'),
('Worked example','Cleared difference -14,700; bridge and full platform balance 4,351,600; unexplained difference 0; three open exceptions retained.'),
('Zero net with unmatched items','Retain and investigate both items. Zero difference does not bypass exception evidence or reviewer approval.'),
('Import and continuity','Reject invalid or conflicting records; skip exact duplicates; preserve approved snapshots and bring forward the approved statement position.'),
('Approval and export','Block approval without evidence, owners or a different reviewer. Export reproduces the saved totals and includes retained evidence references.')],[1.5,5.2])
d.save('MPesa-Wallet-Reconciliation-Workflow-Optimized.docx')
