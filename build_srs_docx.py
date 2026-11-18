import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


SOURCE = Path('Reconciliation-SRS-Requirements.md')
OUTPUT = Path('M-Pesa-Reconciliation-SRS-Requirements.docx')

TEAL = '0B5D5B'
PALE = 'EAF4F1'
PALE_ALT = 'F6F9F8'
LIGHT = 'D9D9D9'
BLACK = '000000'
WHITE = 'FFFFFF'


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tc_pr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_borders(cell, color=LIGHT, size='5'):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn('w:tcBorders'))
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tc_pr.append(borders)
    for edge_name in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge = borders.find(qn('w:' + edge_name))
        if edge is None:
            edge = OxmlElement('w:' + edge_name)
            borders.append(edge)
        edge.set(qn('w:val'), 'single')
        edge.set(qn('w:sz'), size)
        edge.set(qn('w:color'), color)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in('w:tcMar')
    if tc_mar is None:
        tc_mar = OxmlElement('w:tcMar')
        tc_pr.append(tc_mar)
    for side, value in (('top', top), ('start', start), ('bottom', bottom), ('end', end)):
        node = tc_mar.find(qn('w:' + side))
        if node is None:
            node = OxmlElement('w:' + side)
            tc_mar.append(node)
        node.set(qn('w:w'), str(value))
        node.set(qn('w:type'), 'dxa')


def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement('w:tblHeader')
    header.set(qn('w:val'), 'true')
    tr_pr.append(header)


def set_font(run, name='Aptos', size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:ascii'), name)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hAnsi'), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_inline(paragraph, text, default_size=None, default_color=BLACK):
    tokens = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = paragraph.add_run(token[2:-2])
            set_font(run, size=default_size, bold=True, color=default_color)
        elif token.startswith('`') and token.endswith('`'):
            run = paragraph.add_run(token[1:-1])
            set_font(run, name='Consolas', size=(default_size or 10.5) - 0.5, color=default_color)
        else:
            run = paragraph.add_run(token)
            set_font(run, size=default_size, color=default_color)


def plain_markdown(text):
    return re.sub(r'\*\*(.*?)\*\*', r'\1', re.sub(r'`(.*?)`', r'\1', text)).strip()


def is_separator_row(line):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return bool(cells) and all(re.fullmatch(r':?-{3,}:?', c) for c in cells)


def set_table_widths(table, headers):
    count = len(headers)
    labels = [h.lower() for h in headers]
    widths = None
    if count == 2:
        if labels[0] in ('id', 'field', 'term', 'actor', 'state', 'component', 'rule', 'area', 'process step'):
            widths = [1.55, 5.05]
        else:
            widths = [2.0, 4.6]
    elif count == 3:
        widths = [1.2, 2.35, 3.05]
        if labels[0] == 'id':
            widths = [1.05, 2.25, 3.30]
    elif count == 4:
        widths = [1.15, 1.45, 1.0, 3.0]
        if labels[0] == 'state':
            widths = [1.1, 1.8, 1.9, 1.8]
    if widths:
        for col, width in zip(table.columns, widths):
            for cell in col.cells:
                cell.width = Inches(width)


def add_table(doc, rows):
    headers = rows[0]
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_widths(table, headers)
    for index, text in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = ''
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_inline(paragraph, plain_markdown(text), default_size=9.5, default_color=WHITE)
        for run in paragraph.runs:
            run.bold = True
        set_cell_shading(cell, TEAL)
        set_cell_borders(cell)
        set_cell_margins(cell, 110, 130, 110, 130)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    repeat_header(table.rows[0])
    for row_index, row_values in enumerate(rows[1:], start=1):
        row = table.add_row()
        for col_index, text in enumerate(row_values):
            cell = row.cells[col_index]
            cell.text = ''
            paragraph = cell.paragraphs[0]
            if col_index == 0 and len(plain_markdown(text)) < 28:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(paragraph, plain_markdown(text), default_size=9.2)
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.line_spacing = 1.05
            set_cell_shading(cell, PALE_ALT if row_index % 2 == 0 else WHITE)
            set_cell_borders(cell)
            set_cell_margins(cell, 100, 120, 100, 120)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def add_image(doc, path, alt_text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    run.add_picture(str(path), width=Inches(5.35))
    drawing = run._r.xpath('.//wp:docPr')
    if drawing:
        drawing[0].set('descr', alt_text)
    paragraph.paragraph_format.space_after = Pt(4)


def build():
    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.68)
    section.bottom_margin = Inches(0.62)
    section.left_margin = Inches(0.76)
    section.right_margin = Inches(0.76)

    styles = doc.styles
    for style_name in ('Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3'):
        style = styles[style_name]
        style.font.name = 'Aptos'
        style._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos')
        style._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
        style.font.color.rgb = RGBColor(0, 0, 0)
    styles['Normal'].font.size = Pt(10.5)
    styles['Normal'].paragraph_format.space_after = Pt(6)
    styles['Normal'].paragraph_format.line_spacing = 1.08
    styles['Title'].font.size = Pt(26)
    styles['Title'].font.bold = True
    styles['Title'].paragraph_format.space_after = Pt(10)
    styles['Heading 1'].font.size = Pt(16)
    styles['Heading 1'].font.bold = True
    styles['Heading 1'].paragraph_format.space_before = Pt(12)
    styles['Heading 1'].paragraph_format.space_after = Pt(6)
    styles['Heading 1'].paragraph_format.keep_with_next = True
    styles['Heading 2'].font.size = Pt(13)
    styles['Heading 2'].font.bold = True
    styles['Heading 2'].paragraph_format.space_before = Pt(10)
    styles['Heading 2'].paragraph_format.space_after = Pt(4)
    styles['Heading 2'].paragraph_format.keep_with_next = True
    styles['Heading 3'].font.size = Pt(11)
    styles['Heading 3'].font.bold = True
    styles['Heading 3'].paragraph_format.keep_with_next = True

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run('WasaaChat M Pesa Reconciliation Software Requirements  |  Draft 1.0')
    set_font(footer_run, size=8, color='5C6870')

    index = 0
    metadata = []
    while index < len(lines):
        raw = lines[index]
        line = raw.strip()
        if line.startswith('# '):
            p = doc.add_paragraph(style='Title')
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_inline(p, line[2:].strip(), default_size=26)
            index += 1
            while index < len(lines):
                meta = lines[index].strip()
                if not meta:
                    index += 1
                    if metadata:
                        break
                    continue
                match = re.match(r'\*\*(.+?):\*\*\s*(.*?)(?:\s{2})?$', meta)
                if not match:
                    break
                metadata.append((match.group(1), match.group(2)))
                index += 1
            if metadata:
                table = doc.add_table(rows=0, cols=2)
                table.alignment = WD_TABLE_ALIGNMENT.LEFT
                table.autofit = False
                for label, value in metadata:
                    row = table.add_row()
                    row.cells[0].width = Inches(1.25)
                    row.cells[1].width = Inches(5.35)
                    for cell in row.cells:
                        set_cell_borders(cell, color='E7E7E7', size='2')
                        set_cell_margins(cell, 70, 100, 70, 100)
                    set_cell_shading(row.cells[0], PALE)
                    row.cells[0].text = ''
                    add_inline(row.cells[0].paragraphs[0], label, default_size=9.3)
                    row.cells[0].paragraphs[0].runs[0].bold = True
                    row.cells[1].text = ''
                    add_inline(row.cells[1].paragraphs[0], value, default_size=9.3)
                doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue
        break

    page_break_headings = {
        'Functional requirements', 'Calculation rules', 'Data requirements',
        'Acceptance criteria', 'Current implementation impact'
    }
    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith('## '):
            heading_text = stripped[3:].strip()
            if heading_text in page_break_headings and len(doc.paragraphs) > 3:
                doc.add_page_break()
            doc.add_heading(heading_text, level=1)
            index += 1
            continue
        if stripped.startswith('### '):
            doc.add_heading(stripped[4:].strip(), level=2)
            index += 1
            continue
        if stripped.startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
            if match:
                add_image(doc, SOURCE.parent / match.group(2), match.group(1))
            index += 1
            continue
        if stripped.startswith('|') and index + 1 < len(lines) and is_separator_row(lines[index + 1]):
            rows = []
            rows.append([c.strip() for c in stripped.strip('|').split('|')])
            index += 2
            while index < len(lines) and lines[index].strip().startswith('|'):
                rows.append([c.strip() for c in lines[index].strip().strip('|').split('|')])
                index += 1
            add_table(doc, rows)
            continue
        if re.match(r'^\d+\.\s+', stripped):
            paragraph = doc.add_paragraph(style='List Number')
            add_inline(paragraph, re.sub(r'^\d+\.\s+', '', stripped), default_size=10.5)
            paragraph.paragraph_format.space_after = Pt(3)
            index += 1
            continue
        if stripped.startswith('- '):
            paragraph = doc.add_paragraph(style='List Bullet')
            add_inline(paragraph, stripped[2:].strip(), default_size=10.5)
            paragraph.paragraph_format.space_after = Pt(3)
            index += 1
            continue
        paragraph = doc.add_paragraph()
        add_inline(paragraph, stripped, default_size=10.5)
        index += 1

    props = doc.core_properties
    props.title = 'M Pesa Reconciliation Software Requirements'
    props.subject = 'SRS ready requirements for the WasaaChat reconciliation module'
    props.author = 'WasaaChat Ltd'
    props.keywords = 'M Pesa, reconciliation, SRS, finance, wallet'
    doc.save(OUTPUT)
    print(f'Saved {OUTPUT}')


if __name__ == '__main__':
    build()

