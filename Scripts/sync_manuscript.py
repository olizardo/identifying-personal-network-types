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
    headers = [c.strip().strip('*').strip() for c in table_lines[0].strip("|").split("|")]
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

def text_to_runs(text):
    tokens = re.split(r'(\*[^*]+\*)', text)
    runs = []
    for token in tokens:
        if not token: continue
        if token.startswith('*') and token.endswith('*') and len(token) > 2:
            escaped = xml_escape(token[1:-1])
            runs.append(f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{escaped}</w:t></w:r>')
        else:
            escaped = xml_escape(token)
            runs.append(f'<w:r><w:t xml:space="preserve">{escaped}</w:t></w:r>')
    return ''.join(runs)

def make_heading_p(text, level=1):
    style = f"Heading{level}"
    before = "300" if level == 1 else "200"
    escaped = xml_escape(text)
    xml = (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr><w:pStyle w:val="{style}"/><w:suppressAutoHyphens/><w:spacing w:before="{before}" w:after="60"/>'
        f'<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="left"/></w:pPr>'
        f'<w:r><w:t>{escaped}</w:t></w:r>'
        f'</w:p>'
    )
    return ET.fromstring(xml)

def make_body_p(text):
    runs = text_to_runs(text)
    xml = (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr><w:pStyle w:val="Normal"/><w:suppressAutoHyphens/><w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/>'
        f'<w:ind w:left="0" w:right="0" w:firstLine="720"/><w:jc w:val="both"/></w:pPr>'
        f'{runs}'
        f'</w:p>'
    )
    return ET.fromstring(xml)

def make_ref_p(text):
    runs = text_to_runs(text)
    xml = (
        f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:pPr><w:suppressAutoHyphens/><w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="60"/>'
        f'<w:ind w:left="720" w:right="0" w:hanging="720"/><w:jc w:val="left"/></w:pPr>'
        f'{runs}'
        f'</w:p>'
    )
    return ET.fromstring(xml)

def inject_literature_review_and_intro(body, ns):
    trans_p_text = (
        "The present study addresses each of these four limitations by leveraging the longitudinal design, institutional setting, and relational depth of the NetHealth Study. "
        "First, to overcome the cross-sectional constraint, we analyze eight waves of survey data tracking an undergraduate cohort across their first three collegiate years. "
        "This multi-wave architecture allows us to examine both cumulative relational capital accumulated across college (N = 701) and semester-to-semester Markov state transitions (N = 1,900 intervals), directly evaluating the empirical persistence versus structural mobility of personal network regimes over time. "
        "Second, to resolve the dilemma between arbitrary heuristics and uninterpretable algorithmic clustering, we train an empirical classification decision tree that reproduces unsupervised cluster assignments with 92.9% accuracy. "
        "This model yields explicit, data-driven cutoffs—identifying alter–alter density as the primary structural boundary in dense collegiate environments—offering transparent and portable decision criteria that can be applied in comparative research. "
        "Third, to address the contextual void, we embed personal networks within their meso-level organizational settings (Feld, 1981), estimating multilevel categorical logit models with crossed random effects for freshman residence halls (J = 29) and academic majors (J = 43). "
        "By partitioning institutional sorting alongside validated Big Five personality dimensions, we quantitatively assess how organizational opportunity structures and individual dispositions jointly shape personal network geometry. "
        "Finally, to connect abstract topology to substantive social capital, we evaluate alter-level functional support provision across four key domains (social companionship, informational advice, emotional comfort, and financial assistance) alongside composite measures of support multiplexity, relational closeness, and interpersonal trust (N = 580). "
        "In doing so, we bridge the compositional and structural traditions, showing how distinct topological configurations embody systematic tradeoffs between broad informational reach and dense, high-bandwidth emotional solidarity."
    )

    body_children = list(body)
    gaps_idx = None
    data_idx = None

    for idx, elem in enumerate(body_children):
        t = ''.join(elem.itertext()).strip()
        if t.startswith("Despite these significant methodological advances"):
            if gaps_idx is None:
                gaps_idx = idx
        elif t.startswith("Data and Analytical Sample"):
            data_idx = idx
            break

    # If the four gaps paragraph and Data heading are found:
    if gaps_idx is not None and data_idx is not None:
        elements_between = body_children[gaps_idx + 1 : data_idx]
        if len(elements_between) == 1 and "The present study addresses each of these four limitations" in ''.join(elements_between[0].itertext()):
            print("  [Lit Review] Transitional paragraph already perfectly in place. Skipping.")
            return

        # Purge any duplicate/stray elements between gaps_idx and data_idx
        for elem in elements_between:
            body.remove(elem)

        # Insert exactly the transitional paragraph
        body.insert(gaps_idx + 1, make_body_p(trans_p_text))
        print(f"  [Lit Review] Successfully placed transitional paragraph after four gaps paragraph (element {gaps_idx}).")
        return

    intro_last_idx = None
    for idx, elem in enumerate(body_children):
        t = ''.join(elem.itertext()).strip()
        if t.startswith("Our analysis extends"):
            intro_last_idx = idx
        elif t.startswith("Data and Analytical Sample"):
            data_idx = idx
            break

    if data_idx is None:
        print("  [Lit Review Warning] Could not find 'Data and Analytical Sample' heading.")
        return

    # Update paragraph 14 of introduction to reflect all 6 contributions
    intro_updated_text = (
        "Our analysis extends previous scholarship in six substantive directions. "
        "We begin by mapping the correlation architecture connecting egocentric graph metrics, showing how subgroup modularity and dyadic density systematically trade off as personal networks expand in volume. "
        "To ground these structural signatures in concrete social configurations, we draw on Vacca’s emphasis on medoid representations to identify empirical archetype exemplars and visualize their relational structures using force-directed network graphs. "
        "Moving beyond manual heuristics and black-box clustering assignments, we then train an empirical classification decision tree that predicts typology membership with 92.9% accuracy and establishes explicit topological cutoffs. "
        "Overcoming the static constraints of cross-sectional surveys, we evaluate semester-to-semester Markov state transitions across 1,900 longitudinal intervals to measure the empirical stability and structural mobility of personal network forms over time. "
        "Next, we connect these relational configurations to institutional opportunity structures and individual dispositions by estimating multilevel categorical logit models with crossed random effects for freshman residence halls (J = 29) and academic majors (J = 43) alongside validated Big Five personality dimensions. "
        "Finally, we bridge the longstanding divide between structural and compositional network traditions by examining functional social support provisions, revealing how topological architecture governs relational multiplexity and emotional bandwidth."
    )
    if intro_last_idx is not None:
        body.remove(body_children[intro_last_idx])
        body.insert(intro_last_idx, make_body_p(intro_updated_text))
        body_children = list(body)
        for idx, elem in enumerate(body_children):
            t = ''.join(elem.itertext()).strip()
            if t.startswith("Data and Analytical Sample"):
                data_idx = idx
                break

    lit_elems = []
    lit_elems.append(make_heading_p("Recent Developments in Personal Network Typologies", 1))
    lit_elems.append(make_body_p(
        "The ambition to classify personal networks into discrete structural types represents an enduring program within sociocentric and egocentric analysis. "
        "Rather than treating personal networks as undifferentiated aggregations of ties, typology research seeks to uncover recurrent configurations of interpersonal relations that reflect fundamental principles of social organization (Fischer, 1982; McCarty, 2002; Perry et al., 2018). "
        "Over the past two decades, this literature has progressed across four interrelated currents: (1) the transition from attribute-based compositional profiles to purely topological graph structures; "
        "(2) the debate between deductive theoretical archetypes and inductive algorithmic clustering; "
        "(3) alternative frameworks centered on structural cohesion, fragmentation, and hierarchical deconstruction; and "
        "(4) the emerging connection between individual psychological dispositions and network architecture."
    ))

    # Subsection 1
    lit_elems.append(make_heading_p("The Compositional vs. Structural Divide in Network Typologizing", 2))
    lit_elems.append(make_body_p(
        "Early typological research predominantly focused on network composition—the demographic attributes, role categories, and institutional contexts characterizing an individual’s contacts (Antonucci et al., 2013; Offer & Fischer, 2018). "
        "In an influential contribution, Giannella and Fischer (2016) used Random Forests on detailed survey data from Northern California (N = 1,050) to derive an inductive typology of egocentric networks. "
        "Combining over 40 survey descriptors into seven core dimensions (such as non-kin interaction, kin proximity, kin support, church, and work involvement), they reliably placed respondents into seven distinct profiles: “career-and-friends” (24%), “family-and-community” (20%), “family-only” (16%), “untethered” (8%), “energetic” (7%), “withdrawn” (6%), and “home-and-church” (5%)."
    ))
    lit_elems.append(make_body_p(
        "Subsequent scholarship extended this compositional paradigm to large national panels and vulnerable populations. "
        "Laier et al. (2022) applied the Random Forest framework to the German Socio-Economic Panel (SOEP, N = 8,341), identifying fine-grained compositional types based on core discussion networks to show how relational repertoires evolve across the life course. "
        "Pelle and Pappadà (2021) developed a distance-based clustering methodology for mixed-type survey data from the Italian National Statistical Institute (N = 4,495), grouping elderly individuals living alone into distinct vulnerability profiles based on contact frequency, support type, and kin availability. "
        "Extending this logic to romantic dyads, Kennedy et al. (2023) introduced the concept of “duocentric networks” among low-income newlyweds (N = 207), clustering couples according to spousal network overlap and the balance of family versus friend ties to reveal how shared relational ecologies shape marital support."
    ))
    lit_elems.append(make_body_p(
        "Yet, as McCarty (2002) argued in an early intervention, compositional summaries treat the personal network as an unordered collection of alters, completely obscuring the structural patterns connecting alters to one another. "
        "McCarty showed that eliciting large personal networks (60 alters and 1,770 evaluated pairs) reveals substantial structural heterogeneity in network density, component counts, and cohesive subgroups that cannot be predicted from ego–alter attributes. "
        "Because the topological geometry of alter–alter ties governs resource flows, social capital, normative constraints, and behavioral autonomy (Burt, 1992; Coleman, 1988; Granovetter, 1973), classifying personal networks strictly by their structural topology provides a more direct window into the relational mechanisms that organize social life."
    ))

    # Subsection 2
    lit_elems.append(make_heading_p("Deductive Theoretical Archetypes vs. Inductive Clustering", 2))
    lit_elems.append(make_body_p(
        "The pursuit of purely structural typologies reached a major turning point with Bidart et al. (2018), who analyzed longitudinal qualitative and network data from young adults in France (N = 87). "
        "Rejecting compositional descriptors, Bidart et al. formulated six theoretical archetypes defined solely by alter–alter graph metrics: “Regular Dense” (small, single-clique enclosures), “Centered Dense” (dense cores surrounded by peripheral nodes), “Centered Star” (radial networks dominated by central broker alters), “Segmented” (decentralized, disconnected components), “Pearl Collar” (multiple distinct cliques linked sequentially in a ring or pathway), and “Dispersed” (fragmented, sparse collections of isolates). "
        "To assign networks to these archetypes, they proposed a deductive classification tree based on heuristic cutoff values for alter–alter density, Freeman betweenness centralization (> 0.20), diameter, and component shares. "
        "While theoretically compelling, Bidart et al.’s framework relied on subjective cutoffs derived from a modest sample, raising questions about whether their archetypes reflected universal structural forms or idiosyncratic artifacts of their analytical rules."
    ))
    lit_elems.append(make_body_p(
        "To evaluate this question systematically, Vacca (2020) conducted a comparative investigation across six diverse cross-sectional datasets (N = 1,460), encompassing immigrants in Southern Europe, disaster survivors in Florida and Ecuador, residents of segregated neighborhoods, and a representative Bay Area sample. "
        "Vacca developed an inductive community-detection method using Girvan–Newman modularity partitioning to summarize personal network structure through three properties: the number of cohesive subgroups (≥ 3 nodes), the number of isolated dyads/singletons, and partition modularity. "
        "By applying *k*-medoids clustering to these metrics, Vacca showed that personal network structures naturally coalesce into distinct inductive groups. "
        "Crucially, Vacca revealed substantial discordance and cross-classification between Bidart et al.’s deductive assignments and inductive cluster solutions. "
        "Inductive clustering demonstrated that empirical networks rarely conform cleanly to rigid theoretical boundaries, underscoring the need for data-driven classification methods that capture authentic structural variation."
    ))

    # Subsection 3
    lit_elems.append(make_heading_p("Cohesion, Fragmentation, and Hierarchical Deconstruction", 2))
    lit_elems.append(make_body_p(
        "Parallel to the Bidart–Vacca contributions, a complementary line of scholarship has examined the fundamental dimensions underlying structural variation. "
        "In representative urban surveys in Spain (N = 403), Maya-Jariego and Holgado (2015) used exploratory factor analysis on density, centralization, clique counts, and components, showing that personal network variability is organized along two primary axes: structural cohesion and fragmentation. "
        "Building on this foundation, Maya-Jariego (2021) developed a structural classification based on centralization, number of cliques, and component counts, identifying four empirical ego-network types: “dense,” “intermediate,” “clustered,” and “fragmented” networks. "
        "These studies showed that individual differences in interpersonal environments are primarily structured by the tension between cohesive solidarity and subgroup fragmentation."
    ))
    lit_elems.append(make_body_p(
        "Moving beyond static graph metrics, Maya-Jariego and González-Tinoco (2023) introduced a “hierarchical deconstruction procedure” that evaluates network topology through the iterative elimination of nodes with the highest betweenness centrality. "
        "Analyzing longitudinal networks from 69 university students, they found that dense, highly cohesive networks display prolonged resistance to fragmentation, whereas networks organized around brokerage deconstruct rapidly into disjoint components. "
        "This iterative deconstruction showed that personal networks possess hierarchical, nested subgroup architectures that determine their resilience to disruption."
    ))
    lit_elems.append(make_body_p(
        "Most recently, González-Casado et al. (2024) addressed the pervasive critique that previous typology studies relied on ad-hoc, arbitrarily selected graph metrics. "
        "Analyzing four extensive datasets across Spain and Ecuador, they applied systematic dimensionality reduction (PCA and UMAP) across a comprehensive battery of over 14 topological metrics (including transitivity, path length, degree dispersion, modularity, and centralization). "
        "Their findings showed that the structural space of personal networks is overwhelmingly governed by two universal axes: (1) global cohesion (the fundamental mathematical tradeoff between network size and density) and (2) internal structural differentiation (the balance between modular community segregation and centralized brokerage)."
    ))

    # Subsection 4
    lit_elems.append(make_heading_p("Psychological Dispositions and Contextual Horizons: The Unresolved Gaps", 2))
    lit_elems.append(make_body_p(
        "Finally, an emerging line of work connects structural network typologies to individual agency and psychological dispositions. "
        "Maya-Jariego et al. (2020) examined the relationship between Big Five personality traits, psychological sense of community, and personal network structure across 100 adults. "
        "Using modified triadic censuses and global graph metrics, they found that Emotional Stability was positively correlated with network density and closed triads, while psychological sense of community was strongly associated with cohesive triadic embedding. "
        "However, their sample was cross-sectional and exploratory, leading the authors to emphasize that future scholarship must incorporate validated personality inventories into multivariate typology models."
    ))
    lit_elems.append(make_body_p(
        "Despite these significant methodological advances, the existing literature on personal network typologies exhibits four critical gaps: "
        "First, virtually all prior structural typology studies (González-Casado et al., 2024; Maya-Jariego, 2021; McCarty, 2002; Vacca, 2020) rely strictly on single cross-sectional snapshots. Even longitudinal studies (Bidart et al., 2018; Maya-Jariego & González-Tinoco, 2023) lacked the sample scale or analytical framework to model possible state transitions across structural types. Accordingly, whether personal network types represent permanent individual traits or dynamic developmental regimes through which individuals transition over time remains an open empirical question. "
        "Second, methodologically, researchers remain trapped between Bidart et al.’s transparent but arbitrary manual heuristics and Vacca’s or González-Casado et al.’s inductive clustering algorithms, which assign cluster memberships within a given sample as an algorithmic “black box” without providing explicit, portable decision rules that other scholars can readily apply. "
        "Thirdly, prior studies have largely treated personal networks as self-contained interpersonal systems or compared aggregate national populations without modeling the immediate organizational foci (Feld, 1981) in which relationships are forged. How much of the variation in personal network architecture is driven by meso-level institutional sorting (such as residential dormitories or academic curricula) versus individual tendencies to select particular types of alters is still not known. "
        "Finally, typological research has remained almost entirely structural and descriptive, focusing on defining and comparing topological forms without examining how different network structures systematically shape substantive social support, relational multiplexity, and affective tie closeness."
    ))
    lit_elems.append(make_body_p(trans_p_text))

    for offset, elem in enumerate(lit_elems):
        body.insert(data_idx + offset, elem)

    print(f"  [Lit Review] Successfully injected {len(lit_elems)} elements before 'Data and Analytical Sample'.")

    for offset, elem in enumerate(lit_elems):
        body.insert(data_idx + offset, elem)

    print(f"  [Lit Review] Successfully injected {len(lit_elems)} elements before 'Data and Analytical Sample'.")

def update_references_if_needed(body, ns):
    complete_references = [
        "Antonucci, T. C., Ajrouch, K. J., & Birditt, K. S. (2013). The convoy model: Explaining social relations from a multidisciplinary perspective. *The Gerontologist*, 54(1), 82–92. https://doi.org/10.1093/geront/gnt118",
        "Bidart, C., Degenne, A., & Grossetti, M. (2018). Personal network typologies: A structural approach. *Social Networks*, 54, 1–11. https://doi.org/10.1016/j.socnet.2017.11.003",
        "Breiman, L., Friedman, J. H., Olshen, R. A., & Stone, C. J. (1984). *Classification and regression trees*. Wadsworth & Brooks/Cole.",
        "Burt, R. S. (1992). *Structural holes: The social structure of competition*. Harvard University Press.",
        "Coleman, J. S. (1988). Social capital in the creation of human capital. *American Journal of Sociology*, 94, S95–S120. https://doi.org/10.1086/228943",
        "Feld, S. L. (1981). The focused organization of social ties. *American Journal of Sociology*, 86(5), 1015–1035. https://doi.org/10.1086/227352",
        "Fischer, C. S. (1982). *To dwell among friends: Personal networks in town and city*. University of Chicago Press.",
        "Giannella, E., & Fischer, C. S. (2016). An inductive typology of egocentric networks. *Social Networks*, 47, 15–23. https://doi.org/10.1016/j.socnet.2016.04.003",
        "González-Casado, M. A., Gonzales, G., Molina, J. L., & Sánchez, A. (2024). Towards a general method to classify personal network structures. *Social Networks*, 78, 265–278. https://doi.org/10.1016/j.socnet.2024.01.002",
        "Granovetter, M. S. (1973). The strength of weak ties. *American Journal of Sociology*, 78(6), 1360–1380. https://doi.org/10.1086/225469",
        "Kennedy, D. P., Bradbury, T. N., & Karney, B. R. (2023). Typologies of duocentric networks among low-income newlywed couples. *Network Science*, 11(4), 632–656. https://doi.org/10.1017/nws.2023.16",
        "Laier, B., Hennig, M., & Hundsdorfer, S. (2022). An inductive typology of egocentric networks with data from the Socio-Economic Panel. *Social Networks*, 71, 131–142. https://doi.org/10.1016/j.socnet.2022.07.001",
        "Lin, N. (2001). *Social capital: A theory of social structure and action*. Cambridge University Press. https://doi.org/10.1017/CBO9780511815447",
        "Liu, S., Hachen, D., Lizardo, O., Poellabauer, C., Striegel, A., & Milenković, T. (2018). Network analysis of the NetHealth data: Exploring co-evolution of individuals’ social network positions and physical activities. *Applied Network Science*, 3(1), 45. https://doi.org/10.1007/s41109-018-0103-2",
        "Marsden, P. V. (1987). Core discussion networks of Americans. *American Sociological Review*, 52(1), 122–131. https://doi.org/10.2307/2095397",
        "Maya-Jariego, I. (2021). Building a structural typology of personal networks: Individual differences in the cohesion of interpersonal environment. *Social Networks*, 64, 173–180. https://doi.org/10.1016/j.socnet.2020.09.004",
        "Maya-Jariego, I., & González-Tinoco, E. (2023). Use of a hierarchical deconstruction procedure for the classification of personal networks: Exploring nested groups around you. *Social Networks*, 73, 20–29. https://doi.org/10.1016/j.socnet.2022.12.003",
        "Maya-Jariego, I., & Holgado, D. (2015). Living in the metropolitan area: Correlation of interurban mobility with the structural cohesion of personal networks and the originative sense of community. *Psychosocial Intervention*, 24(3), 185–190. https://doi.org/10.1016/j.psi.2015.09.001",
        "Maya-Jariego, I., Letina, S., & González Tinoco, E. (2020). Personal networks and psychological attributes: Exploring individual differences in personality and sense of community and their relationship to the structure of personal networks. *Network Science*, 8(2), 168–188. https://doi.org/10.1017/nws.2019.15",
        "McCarty, C. (2002). Structure in personal networks. *Journal of Social Structure*, 3(1).",
        "Offer, S., & Fischer, C. S. (2018). Does help discussion build closer ties? In J. Youm, E. O. Laumann, & K. Lee (Eds.), *Social networks and the life course* (pp. 45–68). Springer. https://doi.org/10.1007/978-3-319-71544-5_3",
        "Pelle, E., & Pappadà, R. (2021). A clustering procedure for mixed-type data to explore ego network typologies: An application to elderly people living alone in Italy. *Statistical Methods & Applications*, 30(5), 1507–1533. https://doi.org/10.1007/s10260-021-00591-5",
        "Perry, B. L., Pescosolido, B. A., & Borgatti, S. P. (2018). *Egocentric network analysis: Foundations, methods, and models*. Cambridge University Press. https://doi.org/10.1017/9781316443255",
        "Sepulvado, B., Wood, M., Wang, C., Fridmanski, E., Chandler, M., Lizardo, O., & Hachen, D. (2020). Predicting homophily and social network connectivity from dyadic behavioral similarity trajectory clusters. *Social Science Computer Review*, 40(1), 186–205. https://doi.org/10.1177/0894439320923123",
        "Smith, M. L. (2020). Introduction to the special issue on ego networks. *Network Science*, 8(2), 139–141. https://doi.org/10.1017/nws.2020.17",
        "Vacca, R. (2020). Structure in personal networks: Constructing and comparing typologies. *Network Science*, 8(2), 142–167. https://doi.org/10.1017/nws.2019.29",
        "Wang, C., Lizardo, O., & Hachen, D. S. (2020). Neither influence nor selection: Examining co-evolution of political orientation and social networks in the NetSense and NetHealth studies. *PLOS ONE*, 15(5), e0233458. https://doi.org/10.1371/journal.pone.0233458"
    ]

    ref_idx = None
    body_list = list(body)
    for idx, elem in enumerate(body_list):
        t = ''.join(elem.itertext()).strip()
        if t == "References":
            ref_idx = idx
            break

    if ref_idx is not None:
        for elem in body_list[ref_idx + 1:]:
            body.remove(elem)
        for r_text in complete_references:
            body.append(make_ref_p(r_text))
        print(f"  [References] Replaced references with {len(complete_references)} APA entries.")

def inject_support_section_if_missing(body, root_rels, all_files, ns, tables):
    # Check if section is already present in the body
    for elem in body:
        text = ''.join(elem.itertext()).strip()
        if "Functional Social Support" in text or "Figure 11." in text or "Table 8." in text:
            print("  [Support Section] Section already present in document. Skipping structural injection.")
            return

    # Find insertion point: immediately before "Discussion and Conclusion"
    target_idx = None
    body_children = list(body)
    for i, elem in enumerate(body_children):
        text = ''.join(elem.itertext()).strip()
        if text.startswith("Discussion and Conclusion") or text == "Discussion and Conclusion":
            target_idx = i
            break

    if target_idx is None:
        print("  [Support Section Warning] Could not find 'Discussion and Conclusion' heading to insert before.")
        return

    print(f"  [Support Section] Inserting Section 8 (Functional Support), Table 8, and Figure 11 at element index {target_idx}...")

    # Ensure Table 8 is generated
    if "Table 8" not in tables:
        h8, r8 = parse_markdown_table("cache/table8_social_support.md")
        if h8 and r8:
            tables["Table 8"] = create_apa_table_xml(h8, r8, [2560, 1100, 1100, 1100, 1100, 1100, 800, 500])

    fig11_path = "Plots/fig11_social_support_profiles.png"
    if not os.path.exists(fig11_path):
        print(f"  [Support Section Error] {fig11_path} not found.")
        return

    existing_rids = [e.get('Id') for e in root_rels if e.get('Id', '').startswith('rId')]
    max_rid_num = max([int(r[3:]) for r in existing_rids if r[3:].isdigit()] + [0])
    existing_images = [f for f in all_files.keys() if f.startswith('word/media/image')]
    max_img_num = max([int(re.search(r'image(\d+)', f).group(1)) for f in existing_images if re.search(r'image(\d+)', f)] + [0])

    new_rid_num = max_rid_num + 1
    new_img_num = max_img_num + 1
    new_rid = f"rId{new_rid_num}"
    img_name = f"image{new_img_num}.png"
    target_media = f"word/media/{img_name}"

    with open(fig11_path, "rb") as f_img:
        all_files[target_media] = f_img.read()

    rel_elem = ET.Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
    rel_elem.set('Id', new_rid)
    rel_elem.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    rel_elem.set('Target', f'media/{img_name}')
    root_rels.append(rel_elem)

    elems_to_insert = []

    # 1. Heading 1
    h1_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Heading1"/><w:suppressAutoHyphens/><w:spacing w:before="300" w:after="60"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="left"/></w:pPr>'
        '<w:r><w:t>Functional Social Support and Relational Multiplexity Across Typologies</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(h1_xml))

    # 2. Intro paragraph
    p1_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Normal"/><w:suppressAutoHyphens/><w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/><w:ind w:left="0" w:right="0" w:firstLine="720"/><w:jc w:val="both"/></w:pPr>'
        '<w:r><w:t>A foundational divide in egocentric research separates the compositional tradition—which focuses on relational content, functional aid, and social support (Giannella &amp; Fischer, 2016; Laier et al., 2022; Pelle &amp; Pappadà, 2021)—from the purely structural tradition (Bidart et al., 2018; González-Casado et al., 2024; McCarty, 2002; Vacca, 2020). By examining alter-level support evaluations within our analytic sample (N = 580 participants with complete support records), we directly bridge this gap, evaluating whether distinct topological configurations systematically shape relational multiplexity and functional support bandwidth. Table 8 reports descriptive statistics and analysis of variance across network typologies for eight support and relationship characteristics. Figure 11 visualizes these functional support profiles and the structural multiplexity gradient.</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(p1_xml))

    # 3. Table 8 Caption
    t8_cap_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:suppressAutoHyphens/><w:spacing w:before="120" w:after="60"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="left"/></w:pPr>'
        '<w:r><w:rPr><w:b/></w:rPr><w:t>Table 8. Social Support Provision and Functional Multiplexity Across Personal Network Typologies</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(t8_cap_xml))

    # 4. Table 8 table
    if "Table 8" in tables:
        elems_to_insert.append(ET.fromstring(tables["Table 8"]))

    # 5. Table 8 Note
    t8_note_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Heading4"/><w:suppressAutoHyphens/><w:spacing w:before="60" w:after="120"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="left"/></w:pPr>'
        '<w:r><w:rPr><w:b/></w:rPr><w:t>Note: </w:t></w:r>'
        '<w:r><w:t>Sample restricted to N = 580 participants with complete alter support evaluations across Waves 2 through 8. Standard deviations are reported in parentheses. Support Multiplexity Index reflects the average count of functional support types (socializing, advice, emotional comfort, financial assistance) provided per alter (0 to 4 scale). High-multiplex alters represent the percentage of alters providing three or more distinct support functions. F-statistics and p-values are derived from one-way analysis of variance across network typologies.</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(t8_note_xml))

    # 6. Figure 11 Drawing
    draw_xml = create_drawing_xml(new_rid, fig11_path)
    elems_to_insert.append(ET.fromstring(draw_xml))

    # 7. Figure 11 Caption
    f11_cap_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:suppressAutoHyphens/><w:spacing w:before="60" w:after="60"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="left"/></w:pPr>'
        '<w:r><w:rPr><w:b/></w:rPr><w:t>Figure 11. Functional Social Support Profiles and Multiplexity Gradient Across Personal Network Typologies.</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(f11_cap_xml))

    # 8. Figure 11 Note
    f11_note_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Heading4"/><w:suppressAutoHyphens/><w:spacing w:before="60" w:after="120"/><w:ind w:left="0" w:right="0" w:firstLine="0" w:hanging="0"/><w:jc w:val="left"/></w:pPr>'
        '<w:r><w:rPr><w:b/></w:rPr><w:t>Note: </w:t></w:r>'
        '<w:r><w:t>Panel A displays the percentage of nominated alters providing specific functional support types across personal network typologies with 95% confidence interval error bars. Panel B displays the monotonic progression of high-multiplex alters (≥ 3 support types) and tie closeness (% especially close alters) across network configurations.</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(f11_note_xml))

    # 9. Discussion paragraph 1
    p2_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Normal"/><w:suppressAutoHyphens/><w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/><w:ind w:left="0" w:right="0" w:firstLine="720"/><w:jc w:val="both"/></w:pPr>'
        '<w:r><w:t>Table 8 and Figure 11 show that while social companionship (hanging out) represents a universal baseline of collegiate sociability (~88% to 93% across all configurations), substantive functional support exhibits a pronounced, monotonic structural gradient across typologies. Informational advice rises systematically from the expansive Pearl Collar configuration (61.6%) and Segmented networks (63.6%) to Centered Stars (70.5%) and reaches its peak in Regular Dense networks (78.0%; F = 8.47, p &lt; 0.001). Emotional comfort exhibits an identical progression, rising from 55.3% in Pearl Collar networks to 72.5% in Regular Dense networks (F = 5.46, p = 0.001), while financial assistance displays a matching concentration (14.2% in Pearl Collar vs. 23.7% in Regular Dense; F = 5.79, p &lt; 0.001).</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(p2_xml))

    # 10. Discussion paragraph 2
    p3_xml = (
        '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:pPr><w:pStyle w:val="Normal"/><w:suppressAutoHyphens/><w:spacing w:line="360" w:lineRule="auto" w:before="0" w:after="0"/><w:ind w:left="0" w:right="0" w:firstLine="720"/><w:jc w:val="both"/></w:pPr>'
        '<w:r><w:t>Crucially, this functional gradient reflects a fundamental structural tradeoff between topological reach and relational bandwidth. As shown in Panel B of Figure 11, the Support Multiplexity Index—measuring the average number of functional supports provided per alter—increases monotonically from 2.24 in Pearl Collar networks to 2.62 in Regular Dense networks (F = 6.90, p &lt; 0.001). Similarly, the share of “high-multiplex” alters providing three or more distinct forms of support rises from 47.9% to 65.6% (F = 6.24, p &lt; 0.001). This functional concentration is underpinned by emotional intimacy: alters classified as “especially close” account for only 60.5% of contacts in Pearl Collar networks, but surge to 82.9% in Regular Dense networks (F = 14.28, p &lt; 0.001), accompanied by elevated interpersonal trust (F = 5.28, p = 0.001). Expansive, chained network configurations like the Pearl Collar maximize structural breadth and bridge across modular student worlds, but they do so by diluting the proportion of multiplex, emotionally intensive, and financially supportive ties. Conversely, small, cohesive cliques sacrifice structural reach and external bridging in order to maximize dense mutual trust, emotional solidarity, and multi-functional safety nets.</w:t></w:r>'
        '</w:p>'
    )
    elems_to_insert.append(ET.fromstring(p3_xml))

    for offset, new_elem in enumerate(elems_to_insert):
        body.insert(target_idx + offset, new_elem)

    print(f"  [Support Section] Successfully inserted {len(elems_to_insert)} elements before 'Discussion and Conclusion'.")

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

    # 1. Pre-load table XMLs and check for structural additions
    tables = generate_table_xmls()
    inject_literature_review_and_intro(body, ns)
    update_references_if_needed(body, ns)
    inject_support_section_if_missing(body, root_rels, all_files, ns, tables)

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
        "{{FIGURE_10}}": "Plots/fig10_personality_profiles.png",
        "{{FIGURE_11}}": "Plots/fig11_social_support_profiles.png"
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
            "{{TABLE_7}}": "Table 7",
            "{{TABLE_8}}": "Table 8"
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
