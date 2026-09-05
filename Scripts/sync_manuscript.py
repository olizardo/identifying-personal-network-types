#!/usr/bin/env python3
"""
Scripts/sync_manuscript.py
DOM-based OpenXML table & figure injector adhering strictly to AGENTS.md:
- In-place XML injection preserving live styles, paragraph hierarchies, and page breaks
- 6.5-inch full printable text width scaling (9360 dxa / 5,943,600 EMUs)
- Dual DrawingML extent synchronization (cx, cy)
- Mandatory XML escaping and strict ECMA-376 tag ordering
- Universal APA 7th table standards (no vertical borders, 1pt top/bottom, 0.5pt header-bottom)
- Canonical Source of Truth: does NOT overwrite remote user-edited tables unless --inject-tables is passed
"""

import os
import re
import sys
import glob
import zipfile
import struct
import xml.etree.ElementTree as ET

def xml_escape(s):
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def get_png_dimensions(image_path):
    with open(image_path, "rb") as f:
        data = f.read(24)
        if len(data) >= 24 and data.startswith(b'\x89PNG\r\n\x1a\n'):
            return struct.unpack('>II', data[16:24])
    return 1950, 1200

def parse_markdown_table(file_path):
    if not os.path.exists(file_path):
        return [], []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    table_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    if len(table_lines) < 3: return [], []
    headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[2:]:
        row = [c.strip() for c in line.strip("|").split("|")]
        rows.append(row)
    return headers, rows

def format_cell_runs(text, is_header=False):
    parts = re.split(r"<br\s*/?>", text, flags=re.IGNORECASE)
    runs_xml = []
    for idx, part in enumerate(parts):
        if idx > 0:
            runs_xml.append('<w:r><w:br/></w:r>')
        escaped = xml_escape(part.strip())
        if is_header:
            if escaped.startswith('(') and escaped.endswith(')'):
                runs_xml.append(f'<w:r><w:rPr><w:b/><w:i/></w:rPr><w:t>{escaped}</w:t></w:r>')
            else:
                runs_xml.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t>{escaped}</w:t></w:r>')
        else:
            runs_xml.append(f'<w:r><w:t>{escaped}</w:t></w:r>')
    return "".join(runs_xml)

def create_apa_table_xml(headers, rows_data, col_widths=None):
    total_w = 9360  # 6.5 in portrait width in dxa
    num_cols = len(headers)
    if col_widths is None:
        col1_w = int(total_w * 0.36)
        rem_w = total_w - col1_w
        sub_w = int(rem_w / (num_cols - 1)) if num_cols > 1 else rem_w
        col_widths = [col1_w] + [sub_w] * (num_cols - 2)
        if num_cols > 1:
            col_widths.append(total_w - sum(col_widths))
        else:
            col_widths = [total_w]

    xml = [f'<w:tbl xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:tblPr><w:tblW w:w="{total_w}" w:type="dxa"/><w:jc w:val="left"/><w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/><w:left w:val="none"/><w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="140" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>']
    for w in col_widths: xml.append(f'<w:gridCol w:w="{w}"/>')
    xml.append('</w:tblGrid>')
    
    # Header Row
    xml.append('<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>')
    for i, h in enumerate(headers):
        align = "left" if i == 0 else "center"
        runs = format_cell_runs(h, is_header=True)
        xml.append(f'<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:tcBorders><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders></w:tcPr><w:p><w:pPr><w:suppressAutoHyphens/><w:spacing w:before="0" w:after="0"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="{align}"/></w:pPr>{runs}</w:p></w:tc>')
    xml.append('</w:tr>')
    
    # Data Rows
    for row in rows_data:
        xml.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>')
        for i, val in enumerate(row):
            w_idx = min(i, len(col_widths) - 1)
            align = "left" if i == 0 else "center"
            runs = format_cell_runs(val, is_header=False)
            no_wrap = "<w:noWrap/>" if i > 0 else ""
            xml.append(f'<w:tc><w:tcPr><w:tcW w:w="{col_widths[w_idx]}" w:type="dxa"/>{no_wrap}</w:tcPr><w:p><w:pPr><w:suppressAutoHyphens/><w:spacing w:before="0" w:after="0"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="{align}"/></w:pPr>{runs}</w:p></w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return "".join(xml)

def generate_table_xmls():
    tables = {}
    h1, r1 = parse_markdown_table("cache/table1_structural_metrics.md")
    if h1 and r1:
        tables["Table 1"] = create_apa_table_xml(h1, r1, [2560, 1360, 1360, 1360, 1360, 1360])

    h2, r2 = parse_markdown_table("cache/table2_cluster_selection.md")
    if h2 and r2:
        tables["Table 2"] = create_apa_table_xml(h2, r2, [2160, 1800, 1800, 1800, 1800])

    h3, r3 = parse_markdown_table("cache/table6_markov_transitions.md")
    if h3 and r3:
        tables["Table 3"] = create_apa_table_xml(h3, r3, [2360, 1400, 1400, 1400, 1400, 1400])

    h4, r4 = parse_markdown_table("cache/table3_demographics.md")
    if h4 and r4:
        tables["Table 4"] = create_apa_table_xml(h4, r4, [2360, 1000, 1000, 1000, 1000, 1000, 1000, 1000])

    h5, r5 = parse_markdown_table("cache/table4_regressions.md")
    if h5 and r5:
        tables["Table 5"] = create_apa_table_xml(h5, r5, [4560, 1600, 1600, 1600])

    h6, r6 = parse_markdown_table("cache/table7_multilevel_categorical.md")
    if h6 and r6:
        tables["Table 6"] = create_apa_table_xml(h6, r6, [4560, 1600, 1600, 1600])

    h7, r7 = parse_markdown_table("cache/table5_big5_regression.md")
    if h7 and r7:
        tables["Table 7"] = create_apa_table_xml(h7, r7, [4560, 1600, 1600, 1600])

    h8, r8 = parse_markdown_table("cache/table8_social_support.md")
    if h8 and r8:
        tables["Table 8"] = create_apa_table_xml(h8, r8, [2560, 1100, 1100, 1100, 1100, 1100, 800, 500])

    return tables

def create_drawing_xml(r_id, image_path):
    pw, ph = get_png_dimensions(image_path)
    cx = 5943600  # 6.5 in portrait width in EMUs
    cy = int(round(5943600 * (ph / pw)))
    
    xml = (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr><w:spacing w:before="60" w:after="120"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="center"/></w:pPr>'
        f'<w:r>'
        f'<w:drawing xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="1" name="Figure"/>'
        f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr>'
        f'<pic:cNvPr id="0" name="Figure"/>'
        f'<pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/></pic:cNvPicPr>'
        f'</pic:nvPicPr>'
        f'<pic:blipFill>'
        f'<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{r_id}"/>'
        f'<a:stretch><a:fillRect/></a:stretch>'
        f'</pic:blipFill>'
        f'<pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'</pic:spPr>'
        f'</pic:pic>'
        f'</a:graphicData>'
        f'</a:graphic>'
        f'</wp:inline>'
        f'</w:drawing>'
        f'</w:r>'
        f'</w:p>'
    )
    return xml

def sync_docx(in_docx, out_docx, inject_tables=False):
    with zipfile.ZipFile(in_docx, "r") as zin:
        xml_bytes = zin.read("word/document.xml")
        rels_bytes = zin.read("word/_rels/document.xml.rels")
        all_files = {item.filename: zin.read(item.filename) for item in zin.infolist()}

    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    ET.register_namespace('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
    ET.register_namespace('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')

    doc_tree = ET.fromstring(xml_bytes)
    root_rels = ET.fromstring(rels_bytes)

    rid_to_target = {e.get('Id'): e.get('Target') for e in root_rels if e.get('Id')}

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'
    }
    body = doc_tree.find('w:body', ns)

    # 11-figure mapping adhering strictly to AGENTS.md Section 4
    figure_map = {
        "Figure 1.": "Plots/fig1_size_distribution.png",
        "Figure 2.": "Plots/fig2_cluster_selection.png",
        "Figure 3.": "Plots/fig3_cluster_profiles.png",
        "Figure 4.": "Plots/fig5_metric_correlations.png",
        "Figure 5.": "Plots/fig6_network_archetypes.png",
        "Figure 6.": "Plots/fig4_decision_tree.png",
        "Figure 7.": "Plots/fig7_comparative_decision_trees.png",
        "Figure 8.": "Plots/fig8_longitudinal_transitions.png",
        "Figure 9.": "Plots/fig9_demographic_dumbbells.png",
        "Figure 10.": "Plots/fig10_personality_profiles.png",
        "Figure 11.": "Plots/fig11_social_support_profiles.png"
    }

    # 1. Caption-Anchored In-Place Figure Update
    body_list = list(body)
    updated_figures = set()

    for i, elem in enumerate(body_list):
        text = ''.join(elem.itertext()).strip()
        for fig_prefix, img_path in figure_map.items():
            if (text.startswith(fig_prefix) or f" {fig_prefix}" in text) and os.path.exists(img_path):
                # Search adjacent elements for existing drawing container (prioritize i-1, i-2, i+1)
                for offset in [-1, -2, 1, 2]:
                    idx = i + offset
                    if 0 <= idx < len(body_list):
                        candidate = body_list[idx]
                        blips = candidate.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
                        if blips:
                            for blip in blips:
                                rid = blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                if rid and rid in rid_to_target:
                                    target_media = "word/" + rid_to_target[rid]
                                    with open(img_path, "rb") as f_img:
                                        all_files[target_media] = f_img.read()
                                    
                                    pw, ph = get_png_dimensions(img_path)
                                    cx = 5943600  # 6.5 in portrait width in EMUs
                                    cy = int(round(5943600 * (ph / pw)))
                                    for wp_ext in candidate.findall('.//wp:extent', ns):
                                        wp_ext.set('cx', str(cx))
                                        wp_ext.set('cy', str(cy))
                                    for a_ext in candidate.findall('.//a:ext', ns):
                                        a_ext.set('cx', str(cx))
                                        a_ext.set('cy', str(cy))
                                    updated_figures.add(fig_prefix)
                                    print(f"  [Figure Update] In-place updated {fig_prefix} -> {target_media} ({pw}x{ph} px, cx={cx}, cy={cy})")
                                    break
                        if fig_prefix in updated_figures:
                            break

    # 2. Fallback: Tag-Based Figure Insertion (if author inserted {{FIGURE_X}} tags)
    figure_tags = {
        "{{FIGURE_1}}": "Plots/fig1_size_distribution.png",
        "{{FIGURE_2}}": "Plots/fig2_cluster_selection.png",
        "{{FIGURE_3}}": "Plots/fig3_cluster_profiles.png",
        "{{FIGURE_4}}": "Plots/fig5_metric_correlations.png",
        "{{FIGURE_5}}": "Plots/fig6_network_archetypes.png",
        "{{FIGURE_6}}": "Plots/fig4_decision_tree.png",
        "{{FIGURE_7}}": "Plots/fig7_comparative_decision_trees.png",
        "{{FIGURE_8}}": "Plots/fig8_longitudinal_transitions.png",
        "{{FIGURE_9}}": "Plots/fig9_demographic_dumbbells.png",
        "{{FIGURE_10}}": "Plots/fig10_personality_profiles.png"
    }

    existing_rids = [e.get('Id') for e in root_rels if e.get('Id', '').startswith('rId')]
    max_rid_num = max([int(r[3:]) for r in existing_rids if r[3:].isdigit()] + [0])
    existing_images = [f for f in all_files.keys() if f.startswith('word/media/image')]
    max_img_num = max([int(re.search(r'image(\d+)', f).group(1)) for f in existing_images if re.search(r'image(\d+)', f)] + [0])

    body_list = list(body)
    for elem in body_list:
        text = ''.join(elem.itertext()).strip()
        for tag, img_path in figure_tags.items():
            if tag in text and os.path.exists(img_path):
                max_rid_num += 1
                max_img_num += 1
                new_rid = f"rId{max_rid_num}"
                img_name = f"image{max_img_num}.png"
                target_media = f"word/media/{img_name}"

                with open(img_path, "rb") as f_img:
                    all_files[target_media] = f_img.read()

                rel_elem = ET.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
                rel_elem.set('Id', new_rid)
                rel_elem.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
                rel_elem.set('Target', f'media/{img_name}')
                root_rels.append(rel_elem)

                draw_p = ET.fromstring(create_drawing_xml(new_rid, img_path))
                idx = list(body).index(elem)
                body.remove(elem)
                body.insert(idx, draw_p)
                print(f"  [Tag Injection] Replaced {tag} with drawing {new_rid} -> {target_media}")
                break

    # 3. Tables Injection (Only if explicit table injection is requested)
    if inject_tables:
        tables = generate_table_xmls()
        table_tags = {
            "{{TABLE_1}}": "Table 1",
            "{{TABLE_2}}": "Table 2",
            "{{TABLE_3}}": "Table 3",
            "{{TABLE_4}}": "Table 4",
            "{{TABLE_5}}": "Table 5",
            "{{TABLE_6}}": "Table 6",
            "{{TABLE_7}}": "Table 7"
        }

        injected_tables = set()
        for elem in list(body):
            text = ''.join(elem.itertext()).strip()
            for tag, tab_key in table_tags.items():
                if tag in text and tab_key in tables:
                    tbl_elem = ET.fromstring(tables[tab_key])
                    idx = list(body).index(elem)
                    body.remove(elem)
                    body.insert(idx, tbl_elem)
                    injected_tables.add(tab_key)
                    print(f"  [Table Tag Injection] Replaced {tag} with {tab_key}")
                    break

        for caption_key, tbl_xml in tables.items():
            if caption_key in injected_tables:
                continue
            body_list = list(body)
            for i, elem in enumerate(body_list):
                text = ''.join(elem.itertext()).strip()
                if text.startswith(caption_key) or f'{caption_key}:' in text or f'{caption_key}.' in text:
                    for j in range(i + 1, min(len(body_list), i + 6)):
                        sibling = body_list[j]
                        if sibling.tag.endswith('tbl'):
                            new_tbl_elem = ET.fromstring(tbl_xml)
                            current_body = list(body)
                            if sibling in current_body:
                                idx_in_body = current_body.index(sibling)
                                body.remove(sibling)
                                body.insert(idx_in_body, new_tbl_elem)
                                injected_tables.add(caption_key)
                                print(f"  [Table Caption Update] In-place updated table adjacent to {caption_key}")
                            break

    # Serialize back cleanly
    all_files["word/document.xml"] = ET.tostring(doc_tree, encoding="utf-8", xml_declaration=True)
    all_files["word/_rels/document.xml.rels"] = ET.tostring(root_rels, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(out_docx, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for fname, data in all_files.items():
            zout.writestr(fname, data)

    print(f"Successfully processed {in_docx} -> {out_docx} (Updated {len(updated_figures)} figures in-place)")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        inject_tbls = "--inject-tables" in sys.argv
        sync_docx(sys.argv[1], sys.argv[2], inject_tables=inject_tbls)
    else:
        print("Usage: python3 sync_manuscript.py input.docx output.docx [--inject-tables]")
