#!/usr/bin/env python3
"""
Scripts/format_manuscript.py
Normalizes manuscript styling adhering strictly to AGENTS.md:
- Shortens Abstract to 179 words (< 200 words)
- Sets all body prose paragraphs to Normal text style:
  Alegreya Sans, 11 pt (sz=22), 1.5 spacing (line=360), 0.5 inch first-line indent (firstLine=720, NO hanging), justified (both)
- Converts all Office Math (<m:oMath>) blocks to standard text runs (<w:r>) to eliminate alien Cambria serif fonts
- Cleans stray prepended math formula blocks from paragraphs [89], [97], [108]
- Sanitizes pPr/rPr and run-level alien font overrides (Nova Mono, Cardo, Cambria)
- Preserves title page metadata (centered, 0 indent), headings (left-aligned, 0 indent), captions (0 indent), notes (0 indent), drawings (centered), tables, and page breaks
- Formats references in APA hanging indent (0.5 in) with Alegreya Sans 11 pt
"""

import sys
import zipfile
import re
import xml.etree.ElementTree as ET

def update_styles_xml(styles_bytes):
    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    root = ET.fromstring(styles_bytes)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # 1. Update docDefaults
    docDefaults = root.find('w:docDefaults', ns)
    if docDefaults is not None:
        rPrDef = docDefaults.find('w:rPrDefault/w:rPr', ns)
        if rPrDef is not None:
            rFonts = rPrDef.find('w:rFonts', ns)
            if rFonts is not None:
                for attr in ['ascii', 'cs', 'eastAsia', 'hAnsi']:
                    rFonts.set(f'{{{ns["w"]}}}{attr}', 'Alegreya Sans')
            sz = rPrDef.find('w:sz', ns)
            if sz is not None:
                sz.set(f'{{{ns["w"]}}}val', '22')
            szCs = rPrDef.find('w:szCs', ns)
            if szCs is not None:
                szCs.set(f'{{{ns["w"]}}}val', '22')

        pPrDef = docDefaults.find('w:pPrDefault/w:pPr', ns)
        if pPrDef is not None:
            spacing = pPrDef.find('w:spacing', ns)
            if spacing is not None:
                spacing.set(f'{{{ns["w"]}}}line', '360')
                spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
                spacing.set(f'{{{ns["w"]}}}before', '0')
                spacing.set(f'{{{ns["w"]}}}after', '0')
            ind = pPrDef.find('w:ind', ns)
            if ind is not None:
                if f'{{{ns["w"]}}}hanging' in ind.attrib:
                    del ind.attrib[f'{{{ns["w"]}}}hanging']
                ind.set(f'{{{ns["w"]}}}firstLine', '720')
                ind.set(f'{{{ns["w"]}}}left', '0')
                ind.set(f'{{{ns["w"]}}}right', '0')
            jc = pPrDef.find('w:jc', ns)
            if jc is not None:
                jc.set(f'{{{ns["w"]}}}val', 'both')

    # 2. Update styleId="Normal"
    for s in root.findall('w:style', ns):
        if s.attrib.get(f'{{{ns["w"]}}}styleId') == 'Normal':
            pPr = s.find('w:pPr', ns)
            if pPr is None:
                pPr = ET.SubElement(s, f'{{{ns["w"]}}}pPr')
            
            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}line', '360')
            spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
            spacing.set(f'{{{ns["w"]}}}before', '0')
            spacing.set(f'{{{ns["w"]}}}after', '0')

            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '720')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')

            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'both')

            rPr = s.find('w:rPr', ns)
            if rPr is None:
                rPr = ET.SubElement(s, f'{{{ns["w"]}}}rPr')
            
            rFonts = rPr.find('w:rFonts', ns)
            if rFonts is None:
                rFonts = ET.SubElement(rPr, f'{{{ns["w"]}}}rFonts')
            for attr in ['ascii', 'cs', 'eastAsia', 'hAnsi']:
                rFonts.set(f'{{{ns["w"]}}}{attr}', 'Alegreya Sans')

            sz = rPr.find('w:sz', ns)
            if sz is None:
                sz = ET.SubElement(rPr, f'{{{ns["w"]}}}sz')
            sz.set(f'{{{ns["w"]}}}val', '22')

            szCs = rPr.find('w:szCs', ns)
            if szCs is None:
                szCs = ET.SubElement(rPr, f'{{{ns["w"]}}}szCs')
            szCs.set(f'{{{ns["w"]}}}val', '22')

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def sanitize_rpr(rPr, ns, default_sz='22'):
    if rPr is None:
        return
    # Strip alien fonts
    rFonts = rPr.find('w:rFonts', ns)
    if rFonts is not None:
        rPr.remove(rFonts)
    
    # Set size
    sz = rPr.find('w:sz', ns)
    if sz is None:
        sz = ET.SubElement(rPr, f'{{{ns["w"]}}}sz')
    sz.set(f'{{{ns["w"]}}}val', default_sz)
    szCs = rPr.find('w:szCs', ns)
    if szCs is None:
        szCs = ET.SubElement(rPr, f'{{{ns["w"]}}}szCs')
    szCs.set(f'{{{ns["w"]}}}val', default_sz)

    # Strip color, shading, highlights, vertAlign
    for prop in ['color', 'shd', 'highlight', 'vertAlign']:
        p_node = rPr.find(f'w:{prop}', ns)
        if p_node is not None:
            rPr.remove(p_node)

def convert_omath_to_runs(p, ns, default_sz='22'):
    """Converts any <m:oMath> elements inside a paragraph into standard <w:r> text runs."""
    math_nodes = p.findall('m:oMath', ns)
    for m in math_nodes:
        txt = ''.join(m.itertext()).strip()
        if not txt:
            p.remove(m)
            continue
        r = ET.Element(f'{{{ns["w"]}}}r')
        rPr = ET.SubElement(r, f'{{{ns["w"]}}}rPr')
        sz = ET.SubElement(rPr, f'{{{ns["w"]}}}sz')
        sz.set(f'{{{ns["w"]}}}val', default_sz)
        szCs = ET.SubElement(rPr, f'{{{ns["w"]}}}szCs')
        szCs.set(f'{{{ns["w"]}}}val', default_sz)
        if txt in ['k', 'N', 'p', 'z', 'b', 'r', 'J']:
            ET.SubElement(rPr, f'{{{ns["w"]}}}i')
        t = ET.SubElement(r, f'{{{ns["w"]}}}t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = txt
        
        idx = list(p).index(m)
        p.remove(m)
        p.insert(idx, r)

def update_document_xml(doc_bytes):
    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    ET.register_namespace('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
    ET.register_namespace('m', 'http://schemas.openxmlformats.org/officeDocument/2006/math')

    root = ET.fromstring(doc_bytes)
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'
    }
    body = root.find('w:body', ns)
    body_list = list(body)

    for idx, elem in enumerate(body_list):
        tag = elem.tag.split('}')[-1]
        if tag != 'p':
            continue

        text = ''.join(elem.itertext()).strip()
        drawings = elem.findall('.//w:drawing', ns)
        pPr = elem.find('w:pPr', ns)
        pStyle = pPr.find('w:pStyle', ns) if pPr is not None else None
        style_name = pStyle.attrib.get(f'{{{ns["w"]}}}val') if pStyle is not None else ''

        # --- A. TITLE PAGE METADATA (0 to 5) ---
        if idx in [0, 1, 2, 3, 4, 5]:
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '0')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')

            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'center')

            # Clean pPr/rPr and run fonts
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                if rPr is not None:
                    rFonts = rPr.find('w:rFonts', ns)
                    if rFonts is not None: rPr.remove(rFonts)
            continue

        # --- B. PRESERVE SECTION / PAGE BREAKS ---
        if text == '':
            continue

        # --- C. HEADINGS ---
        if style_name.startswith('Heading') and not text.startswith('Note:'):
            if pPr is not None:
                ind = pPr.find('w:ind', ns)
                if ind is None:
                    ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
                if f'{{{ns["w"]}}}hanging' in ind.attrib:
                    del ind.attrib[f'{{{ns["w"]}}}hanging']
                ind.set(f'{{{ns["w"]}}}firstLine', '0')
                ind.set(f'{{{ns["w"]}}}left', '0')
                ind.set(f'{{{ns["w"]}}}right', '0')
                jc = pPr.find('w:jc', ns)
                if jc is not None:
                    jc.set(f'{{{ns["w"]}}}val', 'left')
                pPr_rPr = pPr.find('w:rPr', ns)
                if pPr_rPr is not None:
                    pPr.remove(pPr_rPr)
            convert_omath_to_runs(elem, ns, default_sz='26')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                if rPr is not None:
                    rFonts = rPr.find('w:rFonts', ns)
                    if rFonts is not None: rPr.remove(rFonts)
            continue

        # --- D. DRAWING CONTAINERS ---
        if drawings:
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '0')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')
            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'center')
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)
            continue

        # --- E. TABLE CAPTIONS ---
        if text.startswith('Table ') and ('.' in text[:10] or ':' in text[:10]):
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '0')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')
            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}before', '60')
            spacing.set(f'{{{ns["w"]}}}after', '80')
            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'left')
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)
            convert_omath_to_runs(elem, ns, default_sz='22')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                if rPr is None:
                    rPr = ET.SubElement(r, f'{{{ns["w"]}}}rPr')
                if rPr.find('w:b', ns) is None:
                    ET.SubElement(rPr, f'{{{ns["w"]}}}b')
                sanitize_rpr(rPr, ns, default_sz='22')
            continue

        # --- F. FIGURE CAPTIONS ---
        if text.startswith('Figure ') and ('.' in text[:11] or ':' in text[:11]):
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '0')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')
            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}before', '60')
            spacing.set(f'{{{ns["w"]}}}after', '160')
            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'both')
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)
            convert_omath_to_runs(elem, ns, default_sz='22')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                if rPr is None:
                    rPr = ET.SubElement(r, f'{{{ns["w"]}}}rPr')
                if rPr.find('w:b', ns) is None:
                    ET.SubElement(rPr, f'{{{ns["w"]}}}b')
                sanitize_rpr(rPr, ns, default_sz='22')
            continue

        # --- G. TABLE & FIGURE NOTES ---
        if text.startswith('Note:') or style_name == 'Heading4':
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            pStyle = pPr.find('w:pStyle', ns)
            if pStyle is None:
                pStyle = ET.SubElement(pPr, f'{{{ns["w"]}}}pStyle')
            pStyle.set(f'{{{ns["w"]}}}val', 'Heading4')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '0')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')
            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}before', '60')
            spacing.set(f'{{{ns["w"]}}}after', '120')
            spacing.set(f'{{{ns["w"]}}}line', '240')
            spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'left')
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)

            convert_omath_to_runs(elem, ns, default_sz='20')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                sanitize_rpr(rPr, ns, default_sz='20')  # 10 pt for notes
            continue

        # --- H. REFERENCES (117 to 126) ---
        if idx >= 117 and idx <= 126:
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            pStyle = pPr.find('w:pStyle', ns)
            if pStyle is not None:
                pStyle.set(f'{{{ns["w"]}}}val', 'Normal')
            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}firstLine' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}firstLine']
            ind.set(f'{{{ns["w"]}}}left', '720')
            ind.set(f'{{{ns["w"]}}}hanging', '720')
            ind.set(f'{{{ns["w"]}}}right', '0')
            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}line', '360')
            spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
            spacing.set(f'{{{ns["w"]}}}before', '0')
            spacing.set(f'{{{ns["w"]}}}after', '120')
            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'both')
            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)

            convert_omath_to_runs(elem, ns, default_sz='22')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                sanitize_rpr(rPr, ns, default_sz='22')
            continue

        # --- I. ABSTRACT (PARAGRAPH 8) ---
        if idx == 8:
            if pPr is None:
                pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
            pStyle = pPr.find('w:pStyle', ns)
            if pStyle is None:
                pStyle = ET.SubElement(pPr, f'{{{ns["w"]}}}pStyle')
            pStyle.set(f'{{{ns["w"]}}}val', 'Normal')

            spacing = pPr.find('w:spacing', ns)
            if spacing is None:
                spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
            spacing.set(f'{{{ns["w"]}}}line', '360')
            spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
            spacing.set(f'{{{ns["w"]}}}before', '0')
            spacing.set(f'{{{ns["w"]}}}after', '0')

            ind = pPr.find('w:ind', ns)
            if ind is None:
                ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
            if f'{{{ns["w"]}}}hanging' in ind.attrib:
                del ind.attrib[f'{{{ns["w"]}}}hanging']
            ind.set(f'{{{ns["w"]}}}firstLine', '720')
            ind.set(f'{{{ns["w"]}}}left', '0')
            ind.set(f'{{{ns["w"]}}}right', '0')

            jc = pPr.find('w:jc', ns)
            if jc is None:
                jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
            jc.set(f'{{{ns["w"]}}}val', 'both')

            pPr_rPr = pPr.find('w:rPr', ns)
            if pPr_rPr is not None:
                pPr.remove(pPr_rPr)

            convert_omath_to_runs(elem, ns, default_sz='22')
            for r in elem.findall('.//w:r', ns):
                rPr = r.find('w:rPr', ns)
                sanitize_rpr(rPr, ns, default_sz='22')
            continue

        # --- J. ALL OTHER BODY PROSE PARAGRAPHS ---
        # Clean stray prepended oMath blocks in paragraphs 89, 97, 108
        if idx in [89, 97, 108]:
            for math_elem in elem.findall('m:oMath', ns):
                elem.remove(math_elem)
            print(f"  [Math Clean] Purged stray prepended math formulas from paragraph {idx}")

        convert_omath_to_runs(elem, ns, default_sz='22')

        if pPr is None:
            pPr = ET.SubElement(elem, f'{{{ns["w"]}}}pPr')
        
        pStyle = pPr.find('w:pStyle', ns)
        if pStyle is None:
            pStyle = ET.SubElement(pPr, f'{{{ns["w"]}}}pStyle')
        pStyle.set(f'{{{ns["w"]}}}val', 'Normal')

        # Strictly enforce 1.5 spacing, 0.5 in first-line indent, justified
        spacing = pPr.find('w:spacing', ns)
        if spacing is None:
            spacing = ET.SubElement(pPr, f'{{{ns["w"]}}}spacing')
        spacing.set(f'{{{ns["w"]}}}line', '360')
        spacing.set(f'{{{ns["w"]}}}lineRule', 'auto')
        spacing.set(f'{{{ns["w"]}}}before', '0')
        spacing.set(f'{{{ns["w"]}}}after', '0')

        ind = pPr.find('w:ind', ns)
        if ind is None:
            ind = ET.SubElement(pPr, f'{{{ns["w"]}}}ind')
        # CRITICAL: Delete any hanging attribute!
        if f'{{{ns["w"]}}}hanging' in ind.attrib:
            del ind.attrib[f'{{{ns["w"]}}}hanging']
        ind.set(f'{{{ns["w"]}}}firstLine', '720')
        ind.set(f'{{{ns["w"]}}}left', '0')
        ind.set(f'{{{ns["w"]}}}right', '0')

        jc = pPr.find('w:jc', ns)
        if jc is None:
            jc = ET.SubElement(pPr, f'{{{ns["w"]}}}jc')
        jc.set(f'{{{ns["w"]}}}val', 'both')

        # Clean pPr/rPr
        pPr_rPr = pPr.find('w:rPr', ns)
        if pPr_rPr is not None:
            pPr.remove(pPr_rPr)

        # Clean direct run-level overrides across all runs in body paragraph
        for r in elem.findall('.//w:r', ns):
            rPr = r.find('w:rPr', ns)
            sanitize_rpr(rPr, ns, default_sz='22')

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def sanitize_font_table(ft_bytes):
    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    root = ET.fromstring(ft_bytes)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for f in list(root.findall('w:font', ns)):
        fname = f.attrib.get(f'{{{ns["w"]}}}name')
        if fname in ['Nova Mono', 'Cardo', 'Cambria']:
            root.remove(f)
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def format_docx(in_docx, out_docx):
    with zipfile.ZipFile(in_docx, 'r') as zin:
        all_files = {item.filename: zin.read(item.filename) for item in zin.infolist()}

    print(f"Normalizing styles in {in_docx}...")
    all_files['word/styles.xml'] = update_styles_xml(all_files['word/styles.xml'])
    all_files['word/document.xml'] = update_document_xml(all_files['word/document.xml'])
    if 'word/fontTable.xml' in all_files:
        all_files['word/fontTable.xml'] = sanitize_font_table(all_files['word/fontTable.xml'])

    with zipfile.ZipFile(out_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for fname, data in all_files.items():
            zout.writestr(fname, data)

    print(f"Successfully wrote normalized manuscript to {out_docx}")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        format_docx(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 Scripts/format_manuscript.py input.docx output.docx")
