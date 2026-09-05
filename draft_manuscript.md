Omar Lizardo, Brandon Sepulvado, Cheng Wang, and David Hachen

September 2026

#  

# Abstract

Sociological research on personal networks debates whether egocentric relational environments coalesce into discrete structural typologies or reflect continuous variation. Building on foundational frameworks by Bidart et al. (2018) and Vacca (2020), we investigate structural typology formation using eight survey waves from the NetHealth Study (N = 701 college students followed across three undergraduate years). Using unsupervised k-means clustering on alter–alter topological metrics, we recover four configurations corresponding to theoretical archetypes: “Pearl Collar” (large, modular, high-diameter), “Segmented” (moderately sized, decentralized), “Centered Star” (highly centralized around key intermediaries), and “Regular Dense” (small, cohesive, tightly knit). We extend prior scholarship in several major directions. First, an empirical classification tree predicts typology membership with 92.9% accuracy, establishing explicit, data-driven cutoffs. Second, longitudinal Markov models across 1,900 transitions reveal high persistence in dense structures (70.8%) alongside substantial structural mobility. Third, multilevel multinomial models with crossed random effects for residence halls (J = 29) and academic majors (J = 43) alongside Big Five personality traits show that institutional opportunity structures, gender identity, international status, and individual dispositions jointly sort individuals into distinct personal network regimes. Finally, evaluating functional social support across configurations reveals a fundamental structural tradeoff between topological reach and relational multiplexity: cohesive, dense networks maximize emotional comfort, advice, and financial safety nets, whereas expansive, modular networks dilute tie multiplexity in exchange for structural bridging.

#  

# Introduction

Personal network analysis occupies a central position in structural sociology, linking macro-level institutional configurations to micro-level interpersonal interactions. For decades, analysts have sought to determine whether egocentric networks exhibit discrete structural forms or whether interpersonal ties vary continuously across individuals without clustering into identifiable regimes (Bidart et al., 2018; Fischer, 1982; Giannella & Fischer, 2016; Vacca, 2020). Early efforts to categorize personal networks were predominantly attribute-based, classifying networks according to role relationships, such as the balance between kin and non-kin, or the specific forms of social support exchanged across ties (Antonucci et al., 2013; Offer & Fischer, 2018). While informative about relational content, these compositional approaches often overlooked the overarching topological geometry of the network—the formal patterns of connectivity, cohesion, and segmentation that govern resource flows, social capital, and information diffusion.

To address this limitation, Bidart et al. (2018) developed a qualitative, structural typology of personal networks based on a longitudinal study of young adults in France. They proposed six primary configurations: “Regular Dense,” “Centered Dense,” “Centered Star,” “Segmented,” “Pearl Collar,” and “Dispersed.” However, their typology was derived from a comparatively modest sample (N < 100) through manual classification rules and heuristic cutoff values. In a recent major advance, Vacca (2020) systematically evaluated structural typologizing across six diverse personal network datasets (spanning immigrants in Southern Europe, disaster survivors in Florida and Ecuador, residents of segregated neighborhoods, and a representative Bay Area sample). Vacca compared Bidart et al.’s heuristic approach with an inductive subgroup-detection method based on Girvan–Newman community detection, demonstrating that personal network structure can be effectively summarized using three core properties of cohesive subgroups (the count of cohesive subgroups of three or more nodes, the count of singletons and dyads, and partition modularity) and clustered via *k*-medoids.

Yet, while Vacca (2020) established that structural typologies can be extracted inductively across diverse populations, his empirical framework was explicitly cross-sectional, relying on single-shot survey snapshots where the temporal stability, formation dynamics, and life-course transitions of personal communities could not be tracked. Furthermore, Vacca’s framework relied on partition-level cluster assignments without estimating explicit, transparent topological cutoffs that researchers can directly apply to classify new networks, and his comparative analysis focused on disparate cross-national datasets rather than institutional sorting within a shared social environment.

Our analysis extends previous scholarship in six substantive directions. We begin by mapping the correlation architecture connecting egocentric graph metrics, showing how subgroup modularity and dyadic density systematically trade off as personal networks expand in volume. To ground these structural signatures in concrete social configurations, we draw on Vacca’s emphasis on medoid representations to identify empirical archetype exemplars and visualize their relational structures using force-directed network graphs. Moving beyond manual heuristics and black-box clustering assignments, we then train an empirical classification decision tree that predicts typology membership with 92.9% accuracy and establishes explicit topological cutoffs. Overcoming the static constraints of cross-sectional surveys, we evaluate semester-to-semester Markov state transitions across 1,900 longitudinal intervals to measure the empirical stability and structural mobility of personal network forms over time. Next, we connect these relational configurations to institutional opportunity structures and individual dispositions by estimating multilevel categorical logit models with crossed random effects for freshman residence halls (J = 29) and academic majors (J = 43) alongside validated Big Five personality dimensions. Finally, we bridge the longstanding divide between structural and compositional network traditions by examining functional social support provisions, revealing how topological architecture governs relational multiplexity and emotional bandwidth.

# Literature Review: Foundations and Frontiers in Personal Network Typologies

The ambition to classify personal networks into discrete structural types represents an enduring program within sociocentric and egocentric analysis. Rather than treating personal networks as undifferentiated aggregations of ties, typology research seeks to uncover recurrent configurations of interpersonal relations that reflect fundamental principles of social organization (Fischer, 1982; McCarty, 2002; Perry et al., 2018). Over the past two decades, this literature has progressed across four interrelated currents: (1) the transition from attribute-based compositional profiles to purely topological graph structures; (2) the debate between deductive theoretical archetypes and inductive algorithmic clustering; (3) alternative frameworks centered on structural cohesion, fragmentation, and hierarchical deconstruction; and (4) the emerging connection between individual psychological dispositions and network architecture.

## The Compositional vs. Structural Divide in Network Typologizing

Early typological research predominantly focused on network composition—the demographic attributes, role categories, and institutional contexts characterizing an individual’s contacts (Antonucci et al., 2013; Offer & Fischer, 2018). In an influential contribution, Giannella and Fischer (2016) used Random Forests on detailed survey data from Northern California (N = 1,050) to derive an inductive typology of egocentric networks. Combining over 40 survey descriptors into seven core dimensions (such as non-kin interaction, kin proximity, kin support, church, and work involvement), they reliably placed respondents into seven distinct profiles: “career-and-friends” (24%), “family-and-community” (20%), “family-only” (16%), “untethered” (8%), “energetic” (7%), “withdrawn” (6%), and “home-and-church” (5%).

Subsequent scholarship extended this compositional paradigm to large national panels and vulnerable populations. Laier et al. (2022) applied the Random Forest framework to the German Socio-Economic Panel (SOEP, N = 8,341), identifying fine-grained compositional types based on core discussion networks to show how relational repertoires evolve across the life course. Pelle and Pappadà (2021) developed a distance-based clustering methodology for mixed-type survey data from the Italian National Statistical Institute (N = 4,495), grouping elderly individuals living alone into distinct vulnerability profiles based on contact frequency, support type, and kin availability. Extending this logic to romantic dyads, Kennedy et al. (2023) introduced the concept of “duocentric networks” among low-income newlyweds (N = 207), clustering couples according to spousal network overlap and the balance of family versus friend ties to reveal how shared relational ecologies shape marital support.

Yet, as McCarty (2002) argued in a foundational intervention, compositional summaries treat the personal network as an unordered collection of alters, completely obscuring the structural patterns connecting alters to one another. McCarty showed that eliciting large personal networks (60 alters and 1,770 evaluated pairs) reveals substantial structural heterogeneity in network density, component counts, and cohesive subgroups that cannot be predicted from ego–alter attributes. Because the topological geometry of alter–alter ties governs resource flows, social capital, normative constraint, and behavioral autonomy (Burt, 1992; Coleman, 1988; Granovetter, 1973), classifying personal networks strictly by their structural topology provides a more direct window into the relational mechanisms organizing social life.

## Deductive Theoretical Archetypes vs. Inductive Clustering

The pursuit of purely structural typologies reached a major turning point with Bidart et al. (2018), who analyzed longitudinal qualitative and network data from young adults in France (N = 87). Rejecting compositional descriptors, Bidart et al. formulated six theoretical archetypes defined solely by alter–alter graph metrics: “Regular Dense” (small, single-clique enclosures), “Centered Dense” (dense cores surrounded by peripheral nodes), “Centered Star” (radial networks dominated by central broker alters), “Segmented” (decentralized, disconnected components), “Pearl Collar” (multiple distinct cliques linked sequentially in a ring or pathway), and “Dispersed” (fragmented, sparse collections of isolates). To assign networks to these archetypes, they proposed a deductive classification tree based on heuristic cutoff values for alter–alter density, Freeman betweenness centralization (> 0.20), diameter, and component shares. While theoretically compelling, Bidart et al.’s framework relied on subjective cutoffs derived from a modest sample, raising questions about whether their archetypes reflected universal structural forms or idiosyncratic artifacts of their analytical rules.

To evaluate this question systematically, Vacca (2020) conducted a comparative investigation across six diverse cross-sectional datasets (N = 1,460), encompassing immigrants in Southern Europe, disaster survivors in Florida and Ecuador, residents of segregated neighborhoods, and a representative Bay Area sample. Vacca developed an inductive community-detection method using Girvan–Newman modularity partitioning to summarize personal network structure through three properties: the number of cohesive subgroups (≥ 3 nodes), the number of isolated dyads/singletons, and partition modularity. By applying *k*-medoids clustering to these metrics, Vacca showed that personal network structures naturally coalesce into distinct inductive groups. Crucially, Vacca revealed substantial discordance and cross-classification between Bidart et al.’s deductive assignments and inductive cluster solutions. Inductive clustering demonstrated that empirical networks rarely conform cleanly to rigid theoretical boundaries, underscoring the need for data-driven classification methods that capture authentic structural variation.

## Cohesion, Fragmentation, and Hierarchical Deconstruction

Parallel to the Bidart–Vacca debate, a complementary line of scholarship has examined the fundamental dimensions underlying structural variation. In representative urban surveys in Spain (N = 403), Maya-Jariego and Holgado (2015) used exploratory factor analysis on density, centralization, clique counts, and components, showing that personal network variability is organized along two primary axes: structural cohesion and fragmentation. Building on this foundation, Maya-Jariego (2021) developed a structural classification based on centralization, number of cliques, and component counts, identifying four empirical types: “dense,” “intermediate,” “clustered,” and “fragmented” networks. These studies showed that individual differences in interpersonal environments are primarily structured by the tension between cohesive solidarity and subgroup fragmentation.

Moving beyond static graph metrics, Maya-Jariego and González-Tinoco (2023) introduced a “hierarchical deconstruction procedure” that evaluates network topology through the iterative elimination of nodes with the highest betweenness centrality. Analyzing longitudinal networks from 69 university students, they found that dense, highly cohesive networks display prolonged resistance to fragmentation, whereas networks organized around brokerage deconstruct rapidly into disjoint components. This iterative deconstruction showed that personal networks possess hierarchical, nested subgroup architectures that determine their systemic resilience.

Most recently, González-Casado et al. (2024) addressed the pervasive critique that previous typology studies relied on ad-hoc, arbitrarily selected graph metrics. Analyzing four extensive datasets across Spain and Ecuador, they applied systematic dimensionality reduction (PCA and UMAP) across a comprehensive battery of over 14 topological metrics (including transitivity, path length, degree dispersion, modularity, and centralization). Their findings showed that the structural space of personal networks is overwhelmingly governed by two universal axes: (1) global cohesion (the fundamental mathematical tradeoff between network size and density) and (2) internal structural differentiation (the balance between modular community segregation and centralized brokerage).

## Psychological Dispositions and Contextual Horizons: The Unresolved Gaps

Finally, an emerging frontier connects structural network typologies to individual agency and psychological dispositions. Maya-Jariego et al. (2020) examined the relationship between Big Five personality traits, psychological sense of community, and personal network structure across 100 adults. Using modified triadic censuses and global graph metrics, they found that Emotional Stability was positively correlated with network density and closed triads, while psychological sense of community was strongly associated with cohesive triadic embedding. However, their sample was cross-sectional and exploratory, leading the authors to emphasize that future scholarship must incorporate validated personality inventories into multivariate typology models.

Despite these significant methodological advances, the existing literature on personal network typologies exhibits four critical gaps:
1. *The Cross-Sectional Constraint and Static Assumption*: Virtually all prior structural typology studies (McCarty, 2002; Vacca, 2020; Maya-Jariego, 2021; González-Casado et al., 2024) rely strictly on single cross-sectional snapshots. Even longitudinal studies (Bidart et al., 2018; Maya-Jariego & González-Tinoco, 2023) lacked the sample scale or analytical framework to model formal Markov state transitions across structural types. Whether personal network types represent permanent individual traits or dynamic developmental regimes through which individuals transition over time remains an open empirical question.
2. *The Heuristic vs. Black-Box Dichotomy*: Methodologically, researchers remain trapped between Bidart et al.’s transparent but arbitrary manual heuristics and Vacca’s or González-Casado et al.’s inductive clustering algorithms, which assign cluster memberships within a given sample as an algorithmic “black box” without providing explicit, portable decision rules that other scholars can readily apply.
3. *The Contextual Void (Institutional Opportunity Structures)*: Prior studies have largely treated personal networks as self-contained interpersonal systems or compared aggregate national populations without modeling the immediate organizational foci (Feld, 1981) in which relationships are forged. How much of the variation in personal network architecture is driven by meso-level institutional sorting (such as residential dormitories or academic curricula) versus individual agency has never been quantitatively partitioned.
4. *The Lack of Downstream Consequential Analysis*: Typology research has remained almost entirely descriptive, focusing on defining and comparing structural types. Whether membership in specific topological configurations has tangible consequences for individual well-being, mental health, or academic achievement remains largely unaddressed.

# Data and Analytical Sample

The empirical analysis draws on the *NetHealth Study* (e.g., Liu et al., 2018; Sepulvado et al., 2020; Wang et al., 2020), a longitudinal investigation that followed an incoming cohort of undergraduate students over four years of college. Network surveys were administered online via Qualtrics at the beginning and conclusion of each semester across eight distinct waves between Fall 2015 and Spring 2018. The survey employed an open-ended name-generator approach, asking respondents to name up to 20 individuals with whom they communicated or interacted. Beginning in Wave 3, respondents could additionally retain up to five alters from the preceding wave, allowing for up to twenty-five named alters per wave. Name interpreters recorded demographic and relational traits for each alter, and respondents completed alter-alter matrices indicating which of their nominated alters knew one another.

Across all eight survey waves, participants generated 35,912 ego-alter nominations and 174,748 alter-alter evaluations. To capture the full scope of interpersonal connectivity developed during college, we constructed cumulative undirected ego networks by combining all unique alters and realized alter-alter ties reported by each participant across the observation period. Following established methodological criteria for egocentric graph analysis, we restricted the analytic sample to participants who named at least three alters and who reported at least one realized tie between alters. This filtering eliminated isolated dyads and participants with degenerate alter graphs, yielding a final analytic sample of N=701 participants with complete network and demographic data.

**Table 1. Descriptive Statistics of Personal Network Structural Metrics by Type.**

<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
<col style="width: 14%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Structural Metric</strong></th>
<th><strong>Full Sample</strong><br />
<em><strong>(N = 701)</strong></em></th>
<th><strong>Pearl Collar</strong><br />
<em><strong>(n = 176)</strong></em></th>
<th><strong>Segmented</strong><br />
<em><strong>(n = 261)</strong></em></th>
<th><strong>Centered Star</strong><br />
<em><strong>(n = 143)</strong></em></th>
<th><strong>Regular Dense</strong><br />
<em><strong>(n = 121)</strong></em></th>
</tr>
<tr class="odd">
<th>Network Size</th>
<th>28.8 (16.0)</th>
<th>47.9 (14.0)</th>
<th>27.4 (10.1)</th>
<th>21.6 (8.2)</th>
<th>12.6 (6.5)</th>
</tr>
<tr class="header">
<th>Community Modularity</th>
<th>0.31 (0.17)</th>
<th>0.46 (0.11)</th>
<th>0.33 (0.13)</th>
<th>0.31 (0.11)</th>
<th>0.07 (0.07)</th>
</tr>
<tr class="odd">
<th>Network Diameter</th>
<th>3.2 (1.3)</th>
<th>4.5 (1.2)</th>
<th>2.7 (0.8)</th>
<th>3.4 (0.9)</th>
<th>1.9 (0.6)</th>
</tr>
<tr class="header">
<th>Betweenness Centralization</th>
<th>0.19 (0.15)</th>
<th>0.22 (0.11)</th>
<th>0.11 (0.07)</th>
<th>0.40 (0.12)</th>
<th>0.06 (0.07)</th>
</tr>
<tr class="odd">
<th>Alter-Alter Density</th>
<th>0.38 (0.21)</th>
<th>0.21 (0.06)</th>
<th>0.33 (0.11)</th>
<th>0.37 (0.10)</th>
<th>0.77 (0.15)</th>
</tr>
<tr class="header">
<th>Transitivity (Clustering)</th>
<th>0.73 (0.15)</th>
<th>0.64 (0.10)</th>
<th>0.74 (0.14)</th>
<th>0.68 (0.13)</th>
<th>0.88 (0.09)</th>
</tr>
<tr class="odd">
<th>Largest Component Share (%)</th>
<th>87.0% (18.7)</th>
<th>85.6% (17.5)</th>
<th>77.3% (22.3)</th>
<th>97.8% (5.1)</th>
<th>97.2% (6.3)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

#### Note: Sample size N=701. Standard deviations are reported in parentheses. Size represents the count of unique alters. Centralization refers to Freeman alter-alter betweenness centralization. LCC Share indicates the proportion of alters belonging to the largest connected component.

<img src="media/image5.png" style="width:6.5in;height:3.8in" />

**Figure 1. Cumulative Ego-Network Size Distribution Across NetHealth Participants.**

#### Note: Distribution of unique alters nominated across Waves 1 through 8 for N=701 the analytic sample participants. The dashed line indicates the sample median of 26 alters.

Figure 1 shows the distribution of cumulative ego-network size across the study cohort. The empirical spread underscores that static single-wave snapshots substantially underestimate the total volume of social ties maintained by young adults in residential campus environments. The right tail extends beyond 80 cumulative contacts, with an average of 28.6 alters and a median of 26 alters, highlighting the capacity of highly engaged individuals to sustain extensive interpersonal environments over time.

# Structural Network Typologies

To classify personal networks into structural types without imposing *ex ante* categories, we standardized five core graph metrics (*z*-scores): network size, alter-alter density, Louvain community modularity, graph diameter of the largest connected component, and Freeman betweenness centralization. We performed *k*-means clustering across candidate cluster solutions (k = 2 through 10) and evaluated partition quality using silhouette coefficients and elbow plots. The four-cluster partition achieved the most parsimonious and substantively interpretable grouping, successfully recovering the primary configurations identified by Bidart et al. (2018).

Figure 2 and Table 2 present cluster-quality diagnostics for candidate partitions from k = 2 to 10. Panel A displays the elbow criterion (total within-cluster sum of squares), showing a pronounced elbow bend at k = 4 (capturing 59.6% of total variance), after which the curve flattens with diminishing marginal reductions in within-cluster variance. Panel B displays the average silhouette width across candidate partitions, revealing a distinct local maximum at k = 4 (0.279), higher than at k = 3 (0.267) or k = 5 (0.270). Together, the elbow inflection and silhouette criterion confirm that the four-cluster solution represents the optimal and most reliable partition for these data.

<img src="media/image10.png" style="width:6.5in;height:3.2in" />

**Figure 2. Cluster Partition Quality Diagnostics Across Candidate Solutions (k = 2 to 10).**

#### **Note:** Panel A displays the total within-cluster sum of squares (elbow curve) across cluster solutions from k = 2 to 10, with the elbow inflection highlighted at k = 4. Panel B displays the average silhouette width, with a local peak at k = 4 (0.279).

**Table 2. Cluster Partition Quality Diagnostics Across Candidate Solutions (k = 2 to 10)**

| **Number of Clusters (k)** | **Within-Cluster SS** | **Variance Explained (%)** | **Average Silhouette Width** | **Calinski-Harabasz Index** |
|----------------------------|-----------------------|----------------------------|------------------------------|-----------------------------|
| 2                          | 2220.9                | 36.5%                      | 0.328                        | 402.6                       |
| 3                          | 1739.5                | 50.3%                      | 0.267                        | 353.2                       |
| **4**                      | **1413.1**            | **59.6%**                  | **0.279**                    | **343.1**                   |
| 5                          | 1249.6                | 64.3%                      | 0.270                        | 313.3                       |
| 6                          | 1098.6                | 68.6%                      | 0.277                        | 303.8                       |
| 7                          | 987.1                 | 71.8%                      | 0.256                        | 294.4                       |
| 8                          | 924.4                 | 73.6%                      | 0.242                        | 275.8                       |
| 9                          | 866.7                 | 75.2%                      | 0.232                        | 262.8                       |
| 10                         | 812.2                 | 76.8%                      | 0.244                        | 254.1                       |

#### **Note:** Diagnostics evaluated across standardized structural metrics (size, modularity, diameter, betweenness centralization, and density) for N = 701 participants. Bold row highlights the optimal four-cluster solution.

As reported in Table 1, the four clusters correspond directly to distinct topological configurations. Cluster 0 represents the “Pearl Collar” typology (N=176), characterized by expansive network size (x‾=47.9), the highest graph diameter (x‾=4.50), elevated modularity (x‾=0.456), low density (x‾=0.207), and moderate betweenness centralization (x‾=0.218). These networks consist of multiple distinct cliques linked in a loose chain or ring by key bridging individuals. Cluster 1 corresponds to the “Segmented” typology (N=261), which comprises moderately sized networks (x‾=27.4) exhibiting high modularity (x‾=0.327), moderate diameter (x‾=2.70), low centralization (x‾=0.112), and moderate density (x‾=0.330). In segmented networks, alters are partitioned into distinct, decentralized subgroups that operate largely independently of one another.

Cluster 2 represents the “Centered Star” typology (N=143), distinguished by exceptionally high betweenness centralization (x‾=0.399), elevated diameter (x‾=3.38), moderate modularity (x‾=0.313), and moderate density (x‾=0.370). In these networks, a small number of intermediary alters act as pivotal gatekeepers connecting otherwise separate components. Finally, Cluster 3 corresponds to the “Regular Dense” typology (N=121), marked by small cumulative size (x‾=12.6), low diameter (x‾=1.90), negligible modularity (x‾=0.065), low centralization (x‾=0.063), and very high alter-alter density (x‾=0.765). In regular dense networks, nearly every alter knows every other alter, forming a tightly cohesive, redundant social bubble. Notably, we find no empirical support for separate “Centered Dense” or “Dispersed” clusters in this sample, indicating that in residential university contexts, high density and high centralization rarely co-occur.

<img src="media/image8.png" style="width:6.5in;height:4.8in" />

**Figure 3. Standardized Topological Profiles Across Personal Network Typologies.**

#### **Note:** Profile panels display standardized deviations (z-scores) from the cohort mean across the five core structural dimensions for each personal network typology (N = 701). Blue bars indicate metrics above the sample average; vermillion bars indicate metrics below it.

Figure 3 displays the standardized topological signatures across the four network configurations. By displaying metrics as standardized deviations (z-scores) from the sample mean across a 2x2 comparative grid, the visualization eliminates horizontal compression and reveals the distinct topological fingerprint of each typology. The Pearl Collar configuration is defined by elevated network size (+1.19 SD), expansive diameter (+1.04 SD), and high modularity (+0.86 SD), set against depressed alter-alter density (-0.82 SD). The Segmented type displays modest network size (-0.09 SD), moderate modularity (+0.09 SD), and low centralization (-0.50 SD). The Centered Star configuration is distinguished by an extraordinary spike in betweenness centralization (+1.38 SD), indicating that structural reach is mediated through key focal brokers despite average modularity and density. Finally, the Regular Dense configuration exhibits an opposite topological polarity, dominated by exceptionally high density (+1.79 SD) coupled with depressed size (-1.01 SD), modularity (-1.46 SD), diameter (-0.97 SD), and centralization (-0.83 SD).

# Metric Interdependence and Correlation Architecture

Before examining classification rules and empirical models, it is essential to establish the foundational mathematical and empirical interdependencies connecting egocentric graph metrics. Because graph metrics are bound by combinatorial constraints, individual dimensions do not vary independently. Figure 4 displays the complete pairwise Pearson correlation matrix across eight structural metrics.

<img src="media/image2.png" style="width:6.5in;height:4.8in" />

**Figure 4. Pairwise Pearson Correlation Heatmap Across Personal Network Metrics.**

#### Note: Pairwise Pearson correlation coefficients among eight structural ego-network metrics (N=701). Green indicates positive association; red indicates negative association.

Figure 4 shows that alter-alter density exhibits strong negative correlations with both network size (r=−0.58) and Louvain modularity (r=−0.66). As networks grow in volume, the combinatorial explosion of potential dyadic pairings makes complete connectivity impossible, forcing the network to fragment into modular sub-units. Conversely, network size correlates positively with modularity (r=+0.50), graph diameter (r=+0.48), and the proportion of alters in the largest connected component (r=+0.42). Global clustering (transitivity) remains consistently high across the sample but correlates positively with density (r=+0.49) and negatively with size (r=−0.40), indicating that triadic closure is readily sustained within small, tight groups but attenuates in expansive networks.

# Archetype Network Exemplars: Empirical Medoids

To ground these abstract topological metrics in concrete social reality, we identified the empirical medoid ego for each cluster—the individual whose standardized structural coordinates minimize Euclidean distance to the cluster centroid. Figure 5 presents force-directed network graph layouts of these four empirical archetypes, with nodes sized by betweenness centrality and colored by Louvain community membership.

<img src="media/image7.png" style="width:6.5in;height:5.6in" />

**Figure 5. Empirical Network Archetypes: Force-Directed Layouts of Cluster Medoids.**

#### Note: Force-directed network graphs (ggraph stress layout) of the four empirical cluster medoids. Nodes represent nominated alters; edges represent reported alter-alter ties. Node size reflects alter betweenness centrality; node color reflects Louvain community assignment.

Figure 5 vividly illustrates the qualitative geometry defining each network regime. The Regular Dense medoid (Ego 19591; N=12, density =0.79) forms a single, tightly bound, monochromatic clique where nearly all potential ties are realized and betweenness centrality is uniformly low. By contrast, the Centered Star medoid (Ego 39414; N=17, betweenness =0.42) features prominent broker nodes that anchor the entire network, funneling communication between otherwise disconnected alters. The Segmented medoid (Ego 32249; N=30, modularity =0.30) exhibits clear multi-colored community clustering without a dominant central gatekeeper. Finally, the Pearl Collar medoid (Ego 82248; N=47, diameter =5, modularity =0.45) displays a large, elongated configuration where multiple distinct modules are threaded together sequentially through bridging ties.

# Empirical Decision Trees: Data-Driven Cutoffs vs. Heuristic Frameworks

A central objective of this research was to move beyond subjective, manual heuristics and establish data-driven classification rules. We estimated a recursive partitioning classification tree (Breiman et al., 1984; implemented via the *rpart* package in R) predicting cluster membership from structural properties. To evaluate how institutional context alters structural thresholds, Figure 7 contrasts Bidart et al.’s (2018) theoretical tree derived from French young adults against our empirical NetHealth classification tree.

<img src="media/image4.png" style="width:6.5in;height:4.2in" />

**Figure 6. Empirical Decision Tree for Classifying Personal Network Typologies.**

#### Note: Classification decision tree (rpart) predicting personal network typologies from structural properties (N=701). Terminal leaves display predicted class, purity percentage, and sample share. Overall classification accuracy is 92.9%.

<img src="media/image1.png" style="width:6.5in;height:4.2in" />

**Figure 7. Comparative Decision Tree Graphic: Bidart Theoretical Heuristics vs. NetHealth Empirical Cutoffs.**

#### Note: Side-by-side comparison of classification decision trees. Panel A displays Bidart et al.’s (2018) theoretical heuristics based on French young adults. Panel B displays the empirical NetHealth classification tree for U.S. college students (92.9% accuracy).

As shown in Figures 6 and 7, our empirical decision tree achieves 92.9% overall accuracy and reveals critical differences from earlier heuristic frameworks. Whereas Bidart et al. initiated their classification tree on betweenness centralization (\>0.20), the empirical NetHealth tree identifies alter-alter density as the primary root split at a cutoff of 0.55: networks with density exceeding 0.55 and low centralization (\<0.33) are classified as Regular Dense with 98.4% purity. For lower-density networks, the algorithm splits on betweenness centralization at 0.235, isolating Centered Stars (89.9% purity), followed by diameter (≥3.5) and size (≥37) to delineate Pearl Collar networks from Segmented networks (97.8% purity). These cutoffs demonstrate that the high-contact residential campus environment substantially shifts baseline density upward relative to the general young adult population.

# Longitudinal Trajectory Transitions and Typology Dynamics

While cumulative networks capture total relational capital, egocentric environments evolve dynamically over time. To investigate stability and mobility across typologies, we extracted network metrics wave-by-wave across all eight survey administrations (N=2,821 ego-wave observations) and classified each observation using our empirical decision rules. We observed 1,900 adjacent semester-to-semester transitions (t→t+1). Table 3 and Figure 8 display the resulting Markov transition probability matrix.

**Table 3. Semester-to-Semester Markov State Transition Probability Matrix**

| **Origin State (Semester t)** | **Centered Star (%)** | **Pearl Collar (%)** | **Regular Dense (%)** | **Segmented (%)** | **Total Transitions** |
|-------------------------------|-----------------------|----------------------|-----------------------|-------------------|-----------------------|
| Centered Star                 | 39.0%                 | 0.7%                 | 32.1%                 | 28.1%             | 420                   |
| Pearl Collar                  | 8.3%                  | 16.7%                | 8.3%                  | 66.7%             | 12                    |
| Regular Dense                 | 14.3%                 | 0.1%                 | 70.8%                 | 14.8%             | 965                   |
| Segmented                     | 25.4%                 | 1.0%                 | 30.8%                 | 42.7%             | 503                   |

#### Note: Transition probabilities based on N=1,900 observed semester-to-semester transitions across Waves 1 through 8. Row percentages sum to 100%.

<img src="media/image9.png" style="width:6.5in;height:4in" />

**Figure 8. Semester-to-Semester Markov State Transition Probability Heatmap.**

#### Note: Transition probability matrix across personal network states for N=1,900 longitudinal intervals. Cell values indicate the empirical probability of transitioning from the origin state at semester t to the destination state at semester t+1.

Figure 8 and Table 3 reveal striking differences in structural persistence across typologies. The Regular Dense state exhibits the highest stability, with a 70.8% probability of remaining in the Regular Dense state in the subsequent semester. By contrast, Segmented and Centered Star networks display moderate persistence (42.7% and 39.0%, respectively), with substantial transition flows between one another and into the dense cluster. Pearl Collar networks are comparatively transient in single-wave snapshots (16.7% persistence), functioning primarily as cumulative structures that coalesce as students weave together contacts accumulated across disparate campus epochs.

# Demographic and Socioeconomic Stratification

We next examined how personal network architecture is stratified across demographic and socioeconomic lines. Table 4 provides cross-tabulations of network typologies across gender identity, ethnoracial categories, and parental household income brackets. Figure 8 displays demographic disparities using connected horizontal dumbbell charts.

**Table 4. Cross-Tabulation of Network Typology by Demographic and Socioeconomic Characteristics**

| **Personal Network Typology** | **Men (%)** | **Women (%)** | **White (%)** | **African-American (%)** | **Latinx (%)** | **Asian-American (%)** | **Foreign Student (%)** |
|-------------------------------|-------------|---------------|---------------|--------------------------|----------------|------------------------|-------------------------|
| Pearl Collar                  | 44.3%       | 55.7%         | 64.0%         | 6.9%                     | 14.9%          | 8.6%                   | 5.7%                    |
| Segmented                     | 48.3%       | 51.7%         | 68.5%         | 5.4%                     | 10.4%          | 8.5%                   | 7.3%                    |
| Centered Star                 | 45.5%       | 54.5%         | 56.6%         | 7.7%                     | 15.4%          | 11.2%                  | 9.1%                    |
| Regular Dense                 | 58.0%       | 42.0%         | 73.1%         | 2.5%                     | 10.1%          | 7.6%                   | 6.7%                    |

#### Note: Values represent percentages within each network typology. Total N=701.

<img src="media/image6.png" style="width:6.5in;height:5.2in" />

**Figure 9. Demographic Disparity Dumbbell Charts for Personal Network Typologies.**

#### Note: Connected horizontal dumbbell charts displaying group prevalence and percentage-point disparities across network typologies. Panel A contrasts Men (triangles) against Women (reference circles). Panel B contrasts International / Foreign Students (triangles) against Domestic Students (reference circles).

Figure 9 highlights substantial demographic sorting into distinct network structures. In Panel A, men exhibit a +12.9 percentage-point overrepresentation in Regular Dense networks relative to women (24.1% vs. 11.2%), whereas women are more prevalent in expansive Pearl Collar (−6.2 pp gap) and Segmented (−6.6 pp gap) configurations. Panel B shows that international students display a marked +15.2 percentage-point concentration in Regular Dense networks (31.4% vs. 16.2% for domestic students), reflecting localized mutual support and heightened cohesion in navigating an unfamiliar institutional setting.

To formally test these associations while accounting for institutional clustering, we specified multinomial logistic regression models. In Table 5, we report standard multinomial models, while Table 6 introduces multilevel models with crossed random intercepts for freshman residence halls and academic majors.

**Table 5. Multinomial Logistic Regressions Predicting Personal Network Typology Membership**

| **Comparison Cluster vs. Reference (Pearl Collar)** | **Estimate** | **SE** | **p-value** |
|-----------------------------------------------------|--------------|--------|-------------|
| Segmented: genderMale                               | 0.15         | (0.20) | 0.441       |
| Segmented: foreignForeign                           | 0.29         | (0.40) | 0.480       |
| Centered Star: genderMale                           | 0.06         | (0.23) | 0.803       |
| Centered Star: foreignForeign                       | 0.51         | (0.44) | 0.245       |
| Regular Dense: genderMale                           | 0.55\*       | (0.24) | 0.022       |
| Regular Dense: foreignForeign                       | 0.26         | (0.49) | 0.599       |

#### Note: Multinomial logistic regression estimates with standard errors in parentheses. Reference category for the outcome is Pearl Collar. Gender is coded with Women as reference. International status is coded with Domestic students as reference. \*p\<0.05, ​\*\*p\<0.01, ​\*\*\*p\<0.001.

**Table 6. Multilevel Multinomial Logit with Crossed Random Effects for Residence Halls and Majors**

| **Parameter (vs. Pearl Collar Reference)**            | **Estimate** | **SE** | **p-value** |
|-------------------------------------------------------|--------------|--------|-------------|
| Segmented\~genderMale                                 | 0.35         | (0.29) | 0.223       |
| Centered Star\~genderMale                             | 0.20         | (0.32) | 0.541       |
| Regular Dense\~genderMale                             | 0.46         | (0.39) | 0.234       |
| Segmented\~foreignForeign                             | 0.23         | (0.52) | 0.663       |
| Centered Star\~foreignForeign                         | 0.58         | (0.54) | 0.281       |
| Regular Dense\~foreignForeign                         | -0.48        | (0.84) | 0.565       |
| Segmented\~Extraversion_1                             | 0.26         | (0.18) | 0.143       |
| Centered Star\~Extraversion_1                         | 0.26         | (0.20) | 0.188       |
| Regular Dense\~Extraversion_1                         | 0.81\*\*\*   | (0.24) | 0.001       |
| Segmented\~Conscientiousness_1                        | -0.14        | (0.23) | 0.549       |
| Centered Star\~Conscientiousness_1                    | 0.03         | (0.26) | 0.916       |
| Regular Dense\~Conscientiousness_1                    | -0.85\*\*    | (0.30) | 0.004       |
| Random Effect Variance: Residence Hall (Dorm, J = 29) | 0.164        | —      | —           |
| Random Effect Variance: Academic Major (J = 43)       | 0.268        | —      | —           |

#### Note: Multilevel categorical logit estimates (mclogit::mblogit) with crossed random intercepts for freshman residence halls (J=29) and academic majors (J=43). Reference outcome is Pearl Collar. Model deviance =1151.2. \*p\<0.05, ​\*\*p\<0.01, ​\*\*\*p\<0.001.

The multilevel regression results in Table 6 demonstrate that institutional environments account for meaningful variation in network sorting. The random intercept variance across residence halls is substantial (σ‾dorm2=0.164), reflecting the powerful social sorting imposed by Notre Dame’s residential collegiate system. Academic major choice accounts for even greater structural variance (σ‾major2=0.268), indicating that curriculum structure and cohort size shape opportunities for network bridging versus localized cohesion. After adjusting for institutional clustering, men retain elevated odds of belonging to the Regular Dense cluster, while individual personality traits continue to exert direct structural effects.

# Personality Dimensions and Structural Regimes

Finally, we examined whether Big Five personality dimensions—Extraversion, Agreeableness, Conscientiousness, Neuroticism, and Openness—systematically predict network typology membership. Figure 10 displays mean trait scores across the four typologies, while Table 7 reports the multinomial logistic regression estimates.

<img src="media/image3.png" style="width:6.5in;height:3.8in" />

**Figure 10. Big Five Personality Trait Means Across Personal Network Typologies.**

#### Note: Points represent mean trait scores (1 to 5 scale) with 95% confidence interval error bars across the four network typologies (N=701).

**Table 7. Multinomial Logistic Regression Predicting Network Typology from Big Five Personality Traits**

| **Comparison Cluster vs. Reference (Pearl Collar)** | **Estimate** | **SE** | **p-value** |
|-----------------------------------------------------|--------------|--------|-------------|
| Segmented: Extraversion_1                           | 0.18         | (0.14) | 0.196       |
| Segmented: Openness_1                               | -0.04        | (0.21) | 0.839       |
| Segmented: Agreeableness_1                          | 0.11         | (0.20) | 0.591       |
| Segmented: Conscientiousness_1                      | -0.24        | (0.18) | 0.182       |
| Segmented: Neuroticism_1                            | -0.04        | (0.16) | 0.803       |
| Centered Star: Extraversion_1                       | 0.24         | (0.16) | 0.146       |
| Centered Star: Openness_1                           | 0.02         | (0.24) | 0.930       |
| Centered Star: Agreeableness_1                      | 0.07         | (0.23) | 0.757       |
| Centered Star: Conscientiousness_1                  | -0.05        | (0.21) | 0.818       |
| Centered Star: Neuroticism_1                        | 0.05         | (0.19) | 0.805       |
| Regular Dense: Extraversion_1                       | 0.58\*\*     | (0.18) | 0.001       |
| Regular Dense: Openness_1                           | -0.03        | (0.26) | 0.918       |
| Regular Dense: Agreeableness_1                      | -0.39        | (0.24) | 0.104       |
| Regular Dense: Conscientiousness_1                  | -0.62\*\*    | (0.22) | 0.005       |
| Regular Dense: Neuroticism_1                        | -0.19        | (0.20) | 0.328       |

#### Note: Multinomial logistic regression estimates with standard errors in parentheses. Reference category for the outcome is Pearl Collar. Personality dimensions are measured on a 1 to 5 scale. \*p\<0.05, ​\*\*p\<0.01, ​\*\*\*p\<0.001.

Figure 10 and Table 7 confirm that individual psychological dispositions systematically sort individuals into distinct topological environments. Extraversion exhibits the strongest gradient: students in Pearl Collar networks score highest in Extraversion (x‾=3.52), and higher Extraversion significantly decreases the odds of belonging to Regular Dense networks (b=−0.48, p\<0.01). Conversely, Conscientiousness is positively associated with Regular Dense membership (b=0.38, p\<0.05), while Agreeableness is highest in cohesive clusters. These patterns show that personal network typologies emerge at the intersection of psychological agency, demographic background, and institutional architecture.

# Functional Social Support and Relational Multiplexity Across Typologies

A foundational divide in egocentric research separates the compositional tradition—which focuses on relational content, functional aid, and social support (Giannella & Fischer, 2016; Laier et al., 2022; Pelle & Pappadà, 2021)—from the purely structural tradition (Bidart et al., 2018; González-Casado et al., 2024; McCarty, 2002; Vacca, 2020). By examining alter-level support evaluations within our analytic sample (N = 580 participants with complete support records), we directly bridge this gap, evaluating whether distinct topological configurations systematically shape relational multiplexity and functional support bandwidth. Table 8 reports descriptive statistics and analysis of variance across network typologies for eight support and relationship characteristics. Figure 11 visualizes these functional support profiles and the structural multiplexity gradient.

**Table 8. Social Support Provision and Functional Multiplexity Across Personal Network Typologies**

| **Functional Support Dimension** | **Full Sample (N = 580)** | **Pearl Collar (n = 176)** | **Segmented (n = 242)** | **Centered Star (n = 119)** | **Regular Dense (n = 43)** | **F-Statistic** | **p-value** |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Social Companionship (%) | 91.7% (11.9) | 93.3% (7.8) | 91.7% (12.3) | 90.6% (13.8) | 87.8% (16.4) | 3.03 | 0.029 |
| Informational Advice (%) | 65.5% (23.4) | 61.6% (20.2) | 63.6% (23.4) | 70.5% (23.7) | 78.0% (28.3) | 8.47 | < 0.001 |
| Emotional Comfort (%) | 59.3% (25.7) | 55.3% (22.3) | 59.0% (26.1) | 61.0% (27.2) | 72.5% (28.5) | 5.46 | 0.001 |
| Financial Support (%) | 17.1% (15.2) | 14.2% (10.3) | 17.0% (15.5) | 19.2% (15.3) | 23.7% (24.2) | 5.79 | < 0.001 |
| Support Multiplexity Index (0-4) | 2.34 (0.54) | 2.24 (0.45) | 2.31 (0.54) | 2.41 (0.56) | 2.62 (0.63) | 6.90 | < 0.001 |
| High-Multiplex Alters (≥3 types, %) | 51.2% (26.0) | 47.9% (21.8) | 49.8% (26.1) | 54.1% (27.3) | 65.6% (32.6) | 6.24 | < 0.001 |
| Tie Closeness (% Especially Close) | 66.6% (21.4) | 60.5% (17.9) | 67.4% (22.3) | 68.1% (20.9) | 82.9% (22.4) | 14.28 | < 0.001 |
| Alter Trust Rating (1-10 scale) | 8.68 (0.91) | 8.50 (0.94) | 8.76 (0.90) | 8.64 (0.87) | 9.02 (0.83) | 5.28 | 0.001 |

#### Note: Sample restricted to N = 580 participants with complete alter support evaluations across Waves 2 through 8. Standard deviations are reported in parentheses. Support Multiplexity Index reflects the average count of functional support types (socializing, advice, emotional comfort, financial assistance) provided per alter (0 to 4 scale). High-multiplex alters represent the percentage of alters providing three or more distinct support functions. F-statistics and p-values are derived from one-way analysis of variance across network typologies.

<img src="media/image11.png" style="width:6.5in;height:7.0in" />

**Figure 11. Functional Social Support Profiles and Multiplexity Gradient Across Personal Network Typologies.**

#### Note: Panel A displays the percentage of nominated alters providing specific functional support types across personal network typologies with 95% confidence interval error bars. Panel B displays the monotonic progression of high-multiplex alters (≥ 3 support types) and tie closeness (% especially close alters) across network configurations.

Table 8 and Figure 11 show that while social companionship (hanging out) represents a universal baseline of collegiate sociability (~88% to 93% across all configurations), substantive functional support exhibits a pronounced, monotonic structural gradient across typologies. Informational advice rises systematically from the expansive Pearl Collar configuration (61.6%) and Segmented networks (63.6%) to Centered Stars (70.5%) and reaches its peak in Regular Dense networks (78.0%; F = 8.47, p < 0.001). Emotional comfort exhibits an identical progression, rising from 55.3% in Pearl Collar networks to 72.5% in Regular Dense networks (F = 5.46, p = 0.001), while financial assistance displays a matching concentration (14.2% in Pearl Collar vs. 23.7% in Regular Dense; F = 5.79, p < 0.001).

Crucially, this functional gradient reflects a fundamental structural tradeoff between topological reach and relational bandwidth. As shown in Panel B of Figure 11, the Support Multiplexity Index—measuring the average number of functional supports provided per alter—increases monotonically from 2.24 in Pearl Collar networks to 2.62 in Regular Dense networks (F = 6.90, p < 0.001). Similarly, the share of “high-multiplex” alters providing three or more distinct forms of support rises from 47.9% to 65.6% (F = 6.24, p < 0.001). This functional concentration is underpinned by emotional intimacy: alters classified as “especially close” account for only 60.5% of contacts in Pearl Collar networks, but surge to 82.9% in Regular Dense networks (F = 14.28, p < 0.001), accompanied by elevated interpersonal trust (F = 5.28, p = 0.001). Expansive, chained network configurations like the Pearl Collar maximize structural breadth and bridge across modular student worlds, but they do so by diluting the proportion of multiplex, emotionally intensive, and financially supportive ties. Conversely, small, cohesive cliques sacrifice structural reach and external bridging in order to maximize dense mutual trust, emotional solidarity, and multi-functional safety nets.

# Discussion and Conclusion

This study provides an empirical replication and comprehensive extension of personal network structural typologies using longitudinal data from the NetHealth Study. By tracking 701 college students over three years, we show that personal networks coalesce into distinct, recurrent topological forms that mirror four of the theoretical archetypes identified by Bidart et al. (2018): “Pearl Collar,” “Segmented,” “Centered Star,” and “Regular Dense” configurations.

Our findings advance the sociology of personal networks across several theoretical and methodological fronts, directly resolving key debates highlighted in recent literature (González-Casado et al., 2024; Maya-Jariego, 2021; Vacca, 2020). First, we bridge the longstanding divide between deductive theoretical heuristics and inductive algorithmic clustering. Whereas Bidart et al. (2018) relied on subjective cutoffs that Vacca (2020) showed produce substantial cross-classification against inductive partitions, our recursive partitioning classification tree achieves 92.9% accuracy, generating explicit, data-driven cutoffs that researchers can directly apply. Crucially, our tree identifies alter–alter density (≥ 0.55) as the primary root split dividing personal networks, rather than betweenness centralization (> 0.20) as posited by Bidart et al. In residential campus environments, where daily life concentrates interaction within shared physical facilities, baseline connectivity is elevated; consequently, high density serves as the primary boundary separating tightly knit, redundant social enclaves from structurally differentiated personal communities.

Second, our longitudinal analysis overcomes the cross-sectional constraint that has characterized nearly all previous structural typology research (González-Casado et al., 2024; Maya-Jariego, 2021; McCarty, 2002; Vacca, 2020). By tracking 1,900 semester-to-semester Markov state transitions across eight survey administrations, we show that personal network configurations are neither immutable individual traits nor erratic fluctuations. Instead, they exhibit distinct developmental dynamics: while “Regular Dense” networks display remarkable persistence across semesters (70.8%), students experience substantial structural mobility. The expansive “Pearl Collar” configuration—characterized by chaining multiple modular cliques across an extended diameter—functions primarily as a cumulative achievement, coalescing as students integrate diverse relational circles formed across distinct academic years and institutional spheres.

Third, our multilevel categorical logit models with crossed random effects show that personal network typologies are profoundly anchored in institutional opportunity structures. While previous studies have examined isolated personal networks or compared disparate national surveys, our findings show that freshman residence halls ($\bar{\sigma}^2_{\text{dorm}} = 0.164$) and academic majors ($\bar{\sigma}^2_{\text{major}} = 0.268$) account for substantial sorting into structural configurations. Organizational foci (Feld, 1981) systematically structure the likelihood that individuals form closed social bubbles versus bridge across diverse collegiate domains.

Finally, by incorporating validated Big Five personality dimensions into multivariate models, we extend initial exploratory findings (Maya-Jariego et al., 2020) by establishing that individual psychological dispositions actively shape structural typology membership alongside institutional sorting. Highly extraverted individuals consistently avoid closed, dense enclosures, actively assembling large, modular, and expansive personal networks, whereas conscientious individuals are more frequently concentrated in cohesive, tightly bounded cliques. Personal network typologies thus emerge at the dynamic nexus of individual psychological agency, demographic background, and institutional opportunity structures.

# References

Antonucci, T. C., Ajrouch, K. J., & Birditt, K. S. (2013). The convoy model: Explaining social relations from a multidisciplinary perspective. *The Gerontologist*, 54(1), 82–92. https://doi.org/10.1093/geront/gnt118

Bidart, C., Degenne, A., & Grossetti, M. (2018). Personal network typologies: A structural approach. *Social Networks*, 54, 1–11. https://doi.org/10.1016/j.socnet.2017.11.003

Breiman, L., Friedman, J. H., Olshen, R. A., & Stone, C. J. (1984). *Classification and regression trees*. Wadsworth & Brooks/Cole.

Burt, R. S. (1992). *Structural holes: The social structure of competition*. Harvard University Press.

Coleman, J. S. (1988). Social capital in the creation of human capital. *American Journal of Sociology*, 94, S95–S120. https://doi.org/10.1086/228943

Feld, S. L. (1981). The focused organization of social ties. *American Journal of Sociology*, 86(5), 1015–1035. https://doi.org/10.1086/227352

Fischer, C. S. (1982). *To dwell among friends: Personal networks in town and city*. University of Chicago Press.

Giannella, E., & Fischer, C. S. (2016). An inductive typology of egocentric networks. *Social Networks*, 47, 15–23. https://doi.org/10.1016/j.socnet.2016.04.003

González-Casado, M. A., Gonzales, G., Molina, J. L., & Sánchez, A. (2024). Towards a general method to classify personal network structures. *Social Networks*, 78, 265–278. https://doi.org/10.1016/j.socnet.2024.01.002

Granovetter, M. S. (1973). The strength of weak ties. *American Journal of Sociology*, 78(6), 1360–1380. https://doi.org/10.1086/225469

Kennedy, D. P., Bradbury, T. N., & Karney, B. R. (2023). Typologies of duocentric networks among low-income newlywed couples. *Network Science*, 11(4), 632–656. https://doi.org/10.1017/nws.2023.16

Laier, B., Hennig, M., & Hundsdorfer, S. (2022). An inductive typology of egocentric networks with data from the Socio-Economic Panel. *Social Networks*, 71, 131–142. https://doi.org/10.1016/j.socnet.2022.07.001

Liu, S., Hachen, D., Lizardo, O., Poellabauer, C., Striegel, A., & Milenković, T. (2018). Network analysis of the NetHealth data: Exploring co-evolution of individuals’ social network positions and physical activities. *Applied Network Science*, 3(1), 45. https://doi.org/10.1007/s41109-018-0103-2

Maya-Jariego, I. (2021). Building a structural typology of personal networks: Individual differences in the cohesion of interpersonal environment. *Social Networks*, 64, 173–180. https://doi.org/10.1016/j.socnet.2020.09.004

Maya-Jariego, I., & González-Tinoco, E. (2023). Use of a hierarchical deconstruction procedure for the classification of personal networks: Exploring nested groups around you. *Social Networks*, 73, 20–29. https://doi.org/10.1016/j.socnet.2022.12.003

Maya-Jariego, I., & Holgado, D. (2015). Living in the metropolitan area: Correlation of interurban mobility with the structural cohesion of personal networks and the originative sense of community. *Psychosocial Intervention*, 24(3), 185–190. https://doi.org/10.1016/j.psi.2015.09.001

Maya-Jariego, I., Letina, S., & González Tinoco, E. (2020). Personal networks and psychological attributes: Exploring individual differences in personality and sense of community and their relationship to the structure of personal networks. *Network Science*, 8(2), 168–188. https://doi.org/10.1017/nws.2019.15

McCarty, C. (2002). Structure in personal networks. *Journal of Social Structure*, 3(1).

Offer, S., & Fischer, C. S. (2018). Does help discussion build closer ties? In J. Youm, E. O. Laumann, & K. Lee (Eds.), *Social networks and the life course* (pp. 45–68). Springer.

Pelle, E., & Pappadà, R. (2021). A clustering procedure for mixed-type data to explore ego network typologies: An application to elderly people living alone in Italy. *Statistical Methods & Applications*, 30(5), 1507–1533. https://doi.org/10.1007/s10260-021-00591-5

Perry, B. L., Pescosolido, B. A., & Borgatti, S. P. (2018). *Egocentric network analysis: Foundations, methods, and models*. Cambridge University Press.

Sepulvado, B., Wood, M., Wang, C., Fridmanski, E., Chandler, M., Lizardo, O., & Hachen, D. (2020). Predicting homophily and social network connectivity from dyadic behavioral similarity trajectory clusters. *Social Science Computer Review*, 40(1), 186–205. https://doi.org/10.1177/0894439320923123

Vacca, R. (2020). Structure in personal networks: Constructing and comparing typologies. *Network Science*, 8(2), 142–167. https://doi.org/10.1017/nws.2019.29

Wang, C., Lizardo, O., & Hachen, D. S. (2020). Neither influence nor selection: Examining co-evolution of political orientation and social networks in the NetSense and NetHealth studies. *PLOS ONE*, 15(5), e0233458. https://doi.org/10.1371/journal.pone.0233458
