Omar Lizardo, Brandon Sepulvado, Cheng Wang, and David Hachen

September 2026

#  

# Abstract

Building on foundational work by Bidart et al. (2018) and Vacca (2020), we investigate whether ego networks can be classified into discrete types based on their structural signatures using eight survey waves from the NetHealth Study (N = 701). Using unsupervised *k*-means clustering on ego-network topological metrics, we recover four configurations corresponding to types discussed in previous work: “Pearl Collar Networks” (large, modular, high-diameter), “Segmented Networks” (moderately sized, decentralized), “Centered Star Networks” (highly centralized around key intermediaries), and “Regular Dense Networks” (small, cohesive, tightly knit). With this classification in hand, we extend prior scholarship in three major directions. First, we use empirical classification trees to predict individual membership in each ego-network type with 92.9% accuracy, while establishing explicit, data-driven cutoffs for values of each structural signature to determine membership in each type. Second, we use longitudinal Markov models across 1,900 transitions to examine the dynamic evolution of individuals across types, revealing high persistence in regular dense network structures (70.8%) alongside substantial structural mobility across the other types. Third, we evaluate alter-level functional support provision across four domains (companionship, advice, emotional comfort, and financial assistance) alongside tie multiplexity and interpersonal trust (N = 580), showing how topological structure systematically governs relational bandwidth and emotional solidarity.

#  

# Introduction

The study of ego networks occupies a central position in network analysis, linking macro-level institutional configurations to micro-level interpersonal interactions (Smith 2020; Perry et al. 2018). Early efforts to categorize personal networks were predominantly attribute-based, classifying networks according to role relationships, such as the balance between kin and non-kin, or the specific forms of social support exchanged across ties (Antonucci et al., 2013; Offer & Fischer, 2018). While informative about relational content, these compositional approaches often overlooked the overarching topological geometry of the ego network—the formal patterns of connectivity, cohesion, and segmentation that govern resource flows, social capital, and information diffusion among alters and ego and alter. When structural signatures were used, they were limited to basic network statistics such as size and clustering (Burt 1992; Marsden 1987). More recent work has gone beyond this approach, using a richer set of structural signatures, built from alter-to-alter patterns of connectivity, to develop data-driven typologies that classify ego-networks into theoretically meaningful types (Bidart et al., 2018; Giannella & Fischer, 2016; Vacca, 2020).

Our analysis extends previous scholarship in several substantive directions. We begin by mapping the correlation matrix of egocentric graph metrics, showing how subgroup modularity and dyadic density systematically trade off as personal networks expand in volume. To ground these structural signatures in concrete social configurations, we draw on Vacca’s emphasis on medoid representations to identify empirical archetype exemplars and visualize their relational structures using force-directed network graphs. Moving beyond manual heuristics and black-box clustering assignments, we then train an empirical classification decision tree that predicts typology membership with 92.9% accuracy and establishes explicit topological cutoffs. Overcoming the static constraints of cross-sectional surveys, we evaluate semester-to-semester Markov state transitions across 1,900 longitudinal intervals to measure the empirical stability and structural mobility of personal network forms over time. Finally, we bridge the longstanding divide between structural and compositional network traditions by examining functional social support provisions, revealing how topological structure governs relational multiplexity and emotional bandwidth.

# Recent Developments in Personal Network Typologies

The ambition to classify personal networks into discrete structural types represents an enduring program within sociocentric and egocentric analysis. Rather than treating personal networks as undifferentiated aggregations of ties, typology research seeks to uncover recurrent configurations of interpersonal relations that reflect fundamental principles of social organization (Fischer, 1982; McCarty, 2002; Perry et al., 2018). Over the past two decades, this literature has progressed across three interrelated currents: (1) the transition from attribute-based compositional profiles to purely topological graph structures; (2) the debate between deductive theoretical archetypes and inductive algorithmic clustering; and (3) alternative frameworks centered on structural cohesion, fragmentation, and hierarchical deconstruction.

## The Compositional vs. Structural Divide in Network Typologizing

Early typological research predominantly focused on network composition—the demographic attributes, role categories, and institutional contexts characterizing an individual’s contacts (Antonucci et al., 2013; Offer & Fischer, 2018). In an influential contribution, Giannella and Fischer (2016) used Random Forests on detailed survey data from Northern California (N = 1,050) to derive an inductive typology of egocentric networks. Combining over 40 survey descriptors into seven core dimensions (such as non-kin interaction, kin proximity, kin support, church, and work involvement), they reliably placed respondents into seven distinct profiles: “career-and-friends” (24%), “family-and-community” (20%), “family-only” (16%), “untethered” (8%), “energetic” (7%), “withdrawn” (6%), and “home-and-church” (5%).

Subsequent scholarship extended this compositional paradigm to large national panels and vulnerable populations. Laier et al. (2022) applied the Random Forest framework to the German Socio-Economic Panel (SOEP, N = 8,341), identifying fine-grained compositional types based on core discussion networks to show how relational repertoires evolve across the life course. Pelle and Pappadà (2021) developed a distance-based clustering methodology for mixed-type survey data from the Italian National Statistical Institute (N = 4,495), grouping elderly individuals living alone into distinct vulnerability profiles based on contact frequency, support type, and kin availability. Extending this logic to romantic dyads, Kennedy et al. (2023) introduced the concept of “duocentric networks” among low-income newlyweds (N = 207), clustering couples according to spousal network overlap and the balance of family versus friend ties to reveal how shared relational ecologies shape marital support.

Yet, as McCarty (2002) argued in an early intervention, compositional summaries treat the personal network as an unordered collection of alters, completely obscuring the structural patterns connecting alters to one another. McCarty showed that eliciting large personal networks (60 alters and 1,770 evaluated pairs) reveals substantial structural heterogeneity in network density, component counts, and cohesive subgroups that cannot be predicted from ego–alter attributes. Because the topological geometry of alter–alter ties governs resource flows, social capital, normative constraints, and behavioral autonomy (Burt, 1992; Coleman, 1988; Granovetter, 1973), classifying personal networks strictly by their structural topology provides a more direct window into the relational mechanisms that organize social life.

## Deductive Theoretical Archetypes vs. Inductive Clustering

The pursuit of purely structural typologies reached a major turning point with Bidart et al. (2018), who analyzed longitudinal qualitative and network data from young adults in France (N = 87). Rejecting compositional descriptors, Bidart et al. formulated six theoretical archetypes defined solely by alter–alter graph metrics: “Regular Dense” (small, single-clique enclosures), “Centered Dense” (dense cores surrounded by peripheral nodes), “Centered Star” (radial networks dominated by central broker alters), “Segmented” (decentralized, disconnected components), “Pearl Collar” (multiple distinct cliques linked sequentially in a ring or pathway), and “Dispersed” (fragmented, sparse collections of isolates). To assign networks to these archetypes, they proposed a deductive classification tree based on heuristic cutoff values for alter–alter density, Freeman betweenness centralization (\> 0.20), diameter, and component shares. While theoretically compelling, Bidart et al.’s framework relied on subjective cutoffs derived from a modest sample, raising questions about whether their archetypes reflected universal structural forms or idiosyncratic artifacts of their analytical rules.

To evaluate this question systematically, Vacca (2020) conducted a comparative investigation across six diverse cross-sectional datasets (N = 1,460), encompassing immigrants in Southern Europe, disaster survivors in Florida and Ecuador, residents of segregated neighborhoods, and a representative Bay Area sample. Vacca developed an inductive community-detection method using Girvan–Newman modularity partitioning to summarize personal network structure through three properties: the number of cohesive subgroups (≥ 3 nodes), the number of isolated dyads/singletons, and partition modularity. By applying *k*-medoids clustering to these metrics, Vacca showed that personal network structures naturally coalesce into distinct inductive groups. Crucially, Vacca revealed substantial discordance and cross-classification between Bidart et al.’s deductive assignments and inductive cluster solutions. Inductive clustering demonstrated that empirical networks rarely conform cleanly to rigid theoretical boundaries, underscoring the need for data-driven classification methods that capture authentic structural variation.

## Cohesion, Fragmentation, and Hierarchical Deconstruction

Parallel to the Bidart–Vacca contributions, a complementary line of scholarship has examined the fundamental dimensions underlying structural variation. In representative urban surveys in Spain (N = 403), Maya-Jariego and Holgado (2015) used exploratory factor analysis on density, centralization, clique counts, and components, showing that personal network variability is organized along two primary axes: structural cohesion and fragmentation. Building on this foundation, Maya-Jariego (2021) developed a structural classification based on centralization, number of cliques, and component counts, identifying four empirical ego-network types: “dense,” “intermediate,” “clustered,” and “fragmented” networks. These studies showed that individual differences in interpersonal environments are primarily structured by the tension between cohesive solidarity and subgroup fragmentation.

Moving beyond static graph metrics, Maya-Jariego and González-Tinoco (2023) introduced a “hierarchical deconstruction procedure” that evaluates network topology through the iterative elimination of nodes with the highest betweenness centrality. Analyzing longitudinal networks from 69 university students, they found that dense, highly cohesive networks display prolonged resistance to fragmentation, whereas networks organized around brokerage deconstruct rapidly into disjoint components. This iterative deconstruction showed that personal networks possess hierarchical, nested subgroup structures that determine their resilience to disruption.

Most recently, González-Casado et al. (2024) addressed the pervasive critique that previous typology studies relied on ad-hoc, arbitrarily selected graph metrics. Analyzing four extensive datasets across Spain and Ecuador, they applied systematic dimensionality reduction (PCA and UMAP) across a comprehensive battery of over 14 topological metrics (including transitivity, path length, degree dispersion, modularity, and centralization). Their findings showed that the structural space of personal networks is overwhelmingly governed by two universal axes: (1) global cohesion (the fundamental mathematical tradeoff between network size and density) and (2) internal structural differentiation (the balance between modular community segregation and centralized brokerage).

## Extant Gaps in the Current Literature

Despite these significant methodological advances, the existing literature on personal network typologies exhibits three critical gaps: First, virtually all prior structural typology studies (González-Casado et al., 2024; Maya-Jariego, 2021; McCarty, 2002; Vacca, 2020) rely strictly on single cross-sectional snapshots. Even longitudinal studies (Bidart et al., 2005, 2018; Maya-Jariego & González-Tinoco, 2023) lacked the sample scale or analytical framework to model possible state transitions across structural types. Accordingly, whether personal network types represent permanent individual traits or dynamic developmental regimes through which individuals transition over time remains an open empirical question. Second, methodologically, researchers remain trapped between Bidart et al.’s transparent but arbitrary manual heuristics and Vacca’s or González-Casado et al.’s inductive clustering algorithms, which assign cluster memberships within a given sample as an algorithmic “black box” without providing explicit, portable decision rules that other scholars can readily apply. Finally, typological research has remained almost entirely structural and descriptive, focusing on defining and comparing topological forms without examining how different network structures systematically shape substantive social support, relational multiplexity, and affective tie closeness.

The present study addresses each of these three limitations by leveraging the *NetHealth* Study's longitudinal design, institutional setting, and relational depth. First, to overcome the cross-sectional constraint, we analyze eight waves of survey data tracking an undergraduate cohort across their first three collegiate years. This multi-wave design allows us to examine both cumulative relational capital accumulated across college (N = 701) and semester-to-semester Markov state transitions (N = 1,900 intervals), directly evaluating the empirical persistence versus structural mobility of personal network regimes over time. Second, to resolve the dilemma between arbitrary heuristics and uninterpretable algorithmic clustering, we train an empirical classification decision tree that reproduces unsupervised cluster assignments with 92.9% accuracy. This model yields explicit, data-driven cutoffs—identifying alter–alter density as the primary structural boundary in dense collegiate environments—offering transparent and portable decision criteria that can be applied in comparative research. Finally, to connect abstract topology to substantive social capital, we evaluate alter-level functional support provision across four key domains (social companionship, informational advice, emotional comfort, and financial assistance) alongside composite measures of support multiplexity, relational closeness, and interpersonal trust (N = 580). In doing so, we bridge the compositional and structural traditions of ego-network typologizing, showing how distinct topological configurations embody systematic tradeoffs between broad informational reach and dense, high-bandwidth emotional solidarity.

# Data and Analytical Sample

The empirical analysis draws on the *NetHealth Study* (e.g., Liu et al., 2018; Sepulvado et al., 2020; Wang et al., 2020), a longitudinal investigation that followed an incoming cohort of undergraduate students over four years of college. Network surveys were administered online via *Qualtrics* at the beginning and conclusion of each semester across eight distinct waves between Fall 2015 and Spring 2018. The survey used an open-ended name-generator approach, asking respondents to name up to 20 individuals with whom they communicated or interacted. Beginning in Wave 3, respondents could additionally retain up to five alters from the preceding wave, allowing for up to twenty-five named alters per wave. Name interpreters recorded demographic and relational traits for each alter, and respondents completed alter-alter matrices indicating which of their nominated alters knew one another.

Across all eight survey waves, participants generated 35,912 ego-alter nominations and 174,748 alter-alter evaluations. To capture the full scope of interpersonal connectivity realized during college, we constructed cumulative undirected ego networks by combining all unique alters and realized alter-alter ties reported by each participant across the observation period. Following established methodological criteria for egocentric graph analysis, we restricted the analytic sample to participants who named at least three alters and who reported at least one realized tie between alters. This filtering eliminated isolated dyads and participants with degenerate alter graphs, yielding a final analytic sample of N=701 participants with complete network and demographic data.

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

<img src="media/image6.png" style="width:6.5in;height:3.8in" />

**Figure 1. Cumulative Ego-Network Size Distribution Across NetHealth Participants.**

#### Note: Distribution of unique alters nominated across Waves 1 through 8 for analytic-sample participants. The dashed line indicates the sample median of 26 alters.

Figure 1 shows the distribution of cumulative ego-network size across the study cohort. The empirical spread underscores that static single-wave snapshots substantially underestimate the total volume of social ties maintained by young adults in residential campus environments. The right tail extends beyond 80 cumulative contacts, with an average of 28.6 alters and a median of 26 alters, highlighting the capacity of highly engaged individuals to sustain extensive interpersonal environments over time.

# Results

## Structural Network Typologies

To classify personal networks into structural types without imposing *ex ante* categories, we standardized five core graph metrics (*z*-scores): network size, density, Louvain community modularity, graph diameter of the largest connected component, and Freeman betweenness centralization. The correlation between these ego-network features is shown in Figure 4, revealing that alter-alter density exhibits strong negative correlations with both network size (*r* = -0.58) and Louvain modularity (*r* = -0.66). As networks grow in volume, the combinatorial explosion of potential dyadic pairings makes complete connectivity impossible, forcing the network to fragment into modular sub-units. Conversely, network size correlates positively with modularity (*r* = +0.50), graph diameter (*r* = +0.48), and the proportion of alters in the largest connected component (*r* = +0.42). Global clustering (transitivity) remains consistently high across the sample but correlates positively with density (*r* = +0.49) and negatively with size (*r* = −0.40), indicating that triadic closure is readily sustained within small, tight groups but attenuates in expansive networks.

<img src="media/image4.png" style="width:6.5in;height:4.8in" />

**Figure 4. Pairwise Pearson Correlation Heatmap Across Personal Network Metrics.**

#### Note: Pairwise Pearson correlation coefficients among eight structural ego-network metrics (N=701). Green indicates positive association; red indicates negative association.

Using these features, we performed *k*-means clustering across candidate values of k (*k* = 2 through 10) and evaluated partition quality using silhouette coefficients and elbow plots. The four-cluster partition achieved the most parsimonious and substantively interpretable grouping, successfully recovering the primary configurations identified by Bidart et al. (2018). Figure 2 and Table 2 present cluster-quality diagnostics for candidate partitions from k = 2 to 10. Panel A displays the elbow criterion (total within-cluster sum of squares), showing a pronounced elbow bend at k = 4 (capturing 59.6% of total variance), after which the curve flattens with diminishing marginal reductions in within-cluster variance. Panel B displays the average silhouette width across candidate partitions, revealing a distinct local maximum at k = 4 (0.279), higher than at k = 3 (0.267) or k = 5 (0.270). Together, the elbow inflection and silhouette criterion confirm that the four-cluster solution represents the optimal and most reliable partition for these data.

<img src="media/image1.png" style="width:6.5in;height:3.2in" />

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

As shown in Table 1, the four clusters correspond to some of the distinct topological configurations identified by Bidart et al. 2018. Cluster 1 represents the “Pearl Collar” typology (N=176), characterized by expansive network size (x‾=47.9), the highest graph diameter (x‾=4.50), elevated modularity (x‾=0.456), low density (x‾=0.207), and moderate betweenness centralization (x‾=0.218). These networks consist of multiple distinct cliques linked in a loose chain or ring by key bridging individuals.

Cluster 2 corresponds to the “Segmented” typology (N=261), which comprises moderately sized networks (x‾=27.4) exhibiting high modularity (x‾=0.327), moderate diameter (x‾=2.70), low centralization (x‾=0.112), and moderate densit (x‾=0.330). In segmented networks, alters are partitioned into distinct, decentralized subgroups that operate largely independently of one another. Cluster 3 represents the “Centered Star” typology (N=143), distinguished by exceptionally high betweenness centralization (x‾=0.399), elevated diameter (x‾=3.38), moderate modularity (x‾=0.313), and moderate density (x‾=0.370). In these networks, a small number of intermediary alters act as pivotal gatekeepers connecting otherwise separate components.

Finally, Cluster 4 corresponds to the “Regular Dense” typology (N=121), characterized by small cumulative size (x̄=12.6), low diameter (x̄=1.90), negligible modularity (x̄=0.065), low centralization (x̄=0.063), and very high alter-alter density (x̄=0.765). In regular dense networks, nearly every alter knows every other alter, forming a tightly cohesive, redundant social bubble. Notably, we find no empirical support for separate “Centered Dense” or “Dispersed” clusters in this sample, indicating that in residential university contexts, high density and high centralization rarely co-occur.

<img src="media/image2.png" style="width:6.5in;height:4.8in" />

**Figure 3. Standardized Topological Profiles Across Personal Network Typologies.**

#### **Note:** Profile panels display standardized deviations (z-scores) from the cohort mean across the five core structural dimensions for each personal network typology (N = 701). Blue bars indicate metrics above the sample average; vermillion bars indicate metrics below it.

Figure 3 displays the standardized topological signatures (z-scores) across the five core structural metrics for each personal network typology, illustrating how each configuration departs from the cohort mean. In the top-left panel, the Pearl Collar configuration (n = 176) is defined by four above-average metrics: expansive network size (+1.19 SD), the highest graph diameter in the cohort (+1.04 SD), elevated community modularity (+0.86 SD), and slightly elevated betweenness centralization (+0.19 SD). These positive features are counterbalanced by a single, pronounced negative dimension: alter–alter density (-0.82 SD), capturing the sequential chaining of distinct modular cliques across bridging pathways.

In the top-right panel, the Segmented configuration (n = 261) presents a decentralized, compact profile in which four of the five dimensions fall below the cohort average. Its primary defining feature is low betweenness centralization (-0.50 SD), accompanied by below-average graph diameter (-0.35 SD) and below-average density (-0.25 SD). Network size sits close to the cohort mean (-0.09 SD), while community modularity is slightly positive (+0.09 SD), indicating that segmentation in these networks reflects localized subgroup autonomy rather than chain-like modular bridging.

In the bottom-left panel, the Centered Star configuration (n = 143) is dominated by a substantial spike in betweenness centralization (+1.38 SD)—the largest positive deviation observed for any metric outside of regular density. Crucially, this focal brokerage pattern operates within relatively compact networks: network size is distinctly below average (-0.45 SD; x̄ = 21.6 alters), while alter–alter density (-0.06 SD) and community modularity (+0.01 SD) hover near the sample mean, and diameter is modestly elevated (+0.18 SD).

Finally, in the bottom-right panel, the Regular Dense configuration (n = 121) exhibits an inverse structural polarity. It is anchored by an extreme concentration in alter–alter density (+1.79 SD), while all other four structural dimensions are strongly suppressed: community modularity (-1.46 SD), network size (-1.01 SD), graph diameter (-0.97 SD), and betweenness centralization (-0.83 SD). In this regime, interpersonal ties coalesce into a small, tightly knit, and redundant social enclave where virtually all alters are directly connected.

## Archetype Network Exemplars: Empirical Medoids

To ground the four-fold typology more concretely, we identified the empirical medoid ego for each cluster—the individual whose standardized structural coordinates minimize Euclidean distance to the cluster centroid. Figure 5 presents force-directed network graph layouts of these four empirical archetypes, with nodes sized by betweenness centrality and colored by Louvain community membership.

<img src="media/image11.png" style="width:6.5in;height:5.6in" />

**Figure 5. Empirical Network Archetypes: Force-Directed Layouts of Cluster Medoids.**

#### Note: Force-directed network graphs (ggraph stress layout) of the four empirical cluster medoids. Nodes represent nominated alters; edges represent reported alter-alter ties. Node size reflects alter betweenness centrality; node color reflects Louvain community assignment.

Figure 5 illustrates the structural signatures defining each network regime. The Regular Dense medoid (Ego 19591; N=12, density =0.79) forms a single, tightly bound, cluster in which nearly all potential ties are realized and betweenness centrality is uniformly low. By contrast, the Centered Star medoid (Ego 39414; N=17, betweenness =0.42) features prominent broker nodes that anchor the entire network, funneling communication between otherwise disconnected alters. The Segmented medoid (Ego 32249; N=30, modularity =0.30) exhibits clear multi-colored community clustering without a dominant central gatekeeper. Finally, the Pearl Collar medoid (Ego 82248; N=47, diameter = 5, modularity = 0.45) displays a large, elongated configuration in which multiple distinct modules are threaded together sequentially via bridging ties.

## Empirical Decision Trees: Data-Driven Cutoffs vs. Heuristic Frameworks

A central objective of this research was to move beyond subjective, manual heuristics and establish data-driven classification rules. We estimated a recursive partitioning classification tree (Breiman et al., 1984; implemented via the *rpart* package in R) predicting cluster membership from structural properties. To evaluate how institutional context alters structural thresholds, Figure 7 contrasts Bidart et al.’s (2018) theoretical tree derived from French young adults against our empirical NetHealth classification tree.

<img src="media/image10.png" style="width:6.5in;height:4.2in" />

**Figure 6. Empirical Decision Tree for Classifying Personal Network Typologies.**

#### Note: Classification decision tree (rpart) predicting personal network typologies from structural properties (N=701). Terminal leaves display predicted class, classification accuracy, and sample share. Overall classification accuracy is 92.9%.

<img src="media/image9.png" style="width:6.5in;height:4.2in" />

**Figure 7. Comparative Decision Tree Graphic: Bidart Theoretical Heuristics vs. NetHealth Empirical Cutoffs.**

#### Note: Side-by-side comparison of classification decision trees. Panel A displays Bidart et al.’s (2018) theoretical heuristics based on French young adults. Panel B displays the empirical NetHealth classification tree for U.S. college students (92.9% accuracy).

As shown in Figures 6 and 7, our empirical decision tree achieves 92.9% overall accuracy and reveals critical differences from earlier heuristic frameworks. Whereas Bidart et al. initiated their classification tree on betweenness centralization (\>0.20), the empirical *NetHealth* tree identifies alter-alter density as the primary root split at a cutoff of 0.55: networks with density exceeding 0.55 and low centralization (\<0.33) are classified as Regular Dense with 98.4% accuracy. For lower-density networks, the algorithm splits on betweenness centralization at 0.235, isolating Centered Stars (89.9% classification accuracy), followed by diameter (≥3.5) and size (≥37) to delineate Pearl Collar networks from Segmented networks (97.8% classification accuracy). These cutoffs demonstrate that the high-contact residential campus environment substantially shifts baseline density upward relative to the general young adult population.

## Longitudinal Trajectory Transitions and Typology Dynamics

While cumulative networks capture total relational capital, egocentric environments evolve dynamically over time. To investigate stability and mobility across typologies, we extracted network metrics wave-by-wave across all eight survey administrations (N=2,821 ego-wave observations) and classified each observation using our empirical decision rules. We observed 1,900 adjacent semester-to-semester transitions (t→t+1). Table 3 and Figure 8 display the resulting Markov transition probability matrix.

**Table 3. Semester-to-Semester Markov State Transition Probability Matrix**

| **Origin State (Semester t)** | **Centered Star (%)** | **Pearl Collar (%)** | **Regular Dense (%)** | **Segmented (%)** | **Total Transitions** |
|-------------------------------|-----------------------|----------------------|-----------------------|-------------------|-----------------------|
| Centered Star                 | 39.0%                 | 0.7%                 | 32.1%                 | 28.1%             | 420                   |
| Pearl Collar                  | 8.3%                  | 16.7%                | 8.3%                  | 66.7%             | 12                    |
| Regular Dense                 | 14.3%                 | 0.1%                 | 70.8%                 | 14.8%             | 965                   |
| Segmented                     | 25.4%                 | 1.0%                 | 30.8%                 | 42.7%             | 503                   |

#### Note: Transition probabilities based on N=1,900 observed semester-to-semester transitions across Waves 1 through 8. Row percentages sum to 100%.

<img src="media/image7.png" style="width:6.5in;height:4in" />

**Figure 8. Semester-to-Semester Markov State Transition Probability Heatmap.**

#### Note: Transition probability matrix across personal network states for N=1,900 longitudinal intervals. Cell values indicate the empirical probability of transitioning from the origin state at semester t to the destination state at semester t+1.

Figure 8 and Table 3 reveal striking differences in structural persistence across typologies. The Regular Dense state exhibits the highest stability, with a 70.8% probability of remaining in the Regular Dense state in the subsequent semester. By contrast, Segmented and Centered Star networks display moderate persistence (42.7% and 39.0%, respectively), with substantial transition flows between one another and into the dense cluster. Pearl Collar networks are comparatively transient in single-wave snapshots (16.7% persistence), functioning primarily as cumulative structures that coalesce as students weave together contacts accumulated across disparate campus epochs.

## Functional Social Support and Relational Multiplexity Across Typologies

A foundational divide in egocentric research separates the compositional tradition—which focuses on relational content, functional aid, and social support (Giannella & Fischer, 2016; Laier et al., 2022; Pelle & Pappadà, 2021)—from the purely structural tradition (Bidart et al., 2018; González-Casado et al., 2024; McCarty, 2002; Vacca, 2020). By examining alter-level support evaluations within our analytic sample (N = 580 participants with complete support records), we directly bridge this gap, evaluating whether distinct topological configurations systematically shape relational multiplexity and functional support bandwidth. Table 4 reports descriptive statistics and analysis of variance across network typologies for eight support and relationship characteristics. Figure 9 visualizes these functional support profiles and the structural multiplexity gradient.

**Table 4. Social Support Provision and Functional Multiplexity Across Personal Network Typologies**

| **Functional Support Dimension**    | **Full Sample (N = 580)** | **Pearl Collar (n = 176)** | **Segmented (n = 242)** | **Centered Star (n = 119)** | **Regular Dense (n = 43)** | **F-Statistic** | **p-value** |
|-------------------------------------|---------------------------|----------------------------|-------------------------|-----------------------------|----------------------------|-----------------|-------------|
| Social Companionship (%)            | 91.7% (11.9)              | 93.3% (7.8)                | 91.7% (12.3)            | 90.6% (13.8)                | 87.8% (16.4)               | 3.03            | 0.029       |
| Informational Advice (%)            | 65.5% (23.4)              | 61.6% (20.2)               | 63.6% (23.4)            | 70.5% (23.7)                | 78.0% (28.3)               | 8.47            | \< 0.001    |
| Emotional Comfort (%)               | 59.3% (25.7)              | 55.3% (22.3)               | 59.0% (26.1)            | 61.0% (27.2)                | 72.5% (28.5)               | 5.46            | 0.001       |
| Financial Support (%)               | 17.1% (15.2)              | 14.2% (10.3)               | 17.0% (15.5)            | 19.2% (15.3)                | 23.7% (24.2)               | 5.79            | \< 0.001    |
| Support Multiplexity Index (0-4)    | 2.34 (0.54)               | 2.24 (0.45)                | 2.31 (0.54)             | 2.41 (0.56)                 | 2.62 (0.63)                | 6.90            | \< 0.001    |
| High-Multiplex Alters (≥3 types, %) | 51.2% (26.0)              | 47.9% (21.8)               | 49.8% (26.1)            | 54.1% (27.3)                | 65.6% (32.6)               | 6.24            | \< 0.001    |
| Tie Closeness (% Especially Close)  | 66.5% (21.5)              | 60.4% (18.0)               | 67.4% (22.3)            | 68.1% (20.9)                | 82.9% (22.4)               | 14.35           | \< 0.001    |
| Alter Trust Rating (1-10 scale)     | 8.68 (0.91)               | 8.50 (0.94)                | 8.76 (0.90)             | 8.64 (0.87)                 | 9.02 (0.83)                | 5.28            | 0.001       |

#### **Note:** Sample restricted to N = 580 participants with complete alter support evaluations across Waves 2 through 8. Standard deviations are reported in parentheses. Support Multiplexity Index reflects the average count of functional support types (socializing, advice, emotional comfort, financial assistance) provided per alter (0 to 4 scale). High-multiplex alters represent the percentage of alters providing three or more distinct support functions. F-statistics and p-values are derived from one-way analysis of variance across network typologies.

<img src="media/image3.png" style="width:6.5in;height:7in" />

**Figure 9. Functional Social Support Profiles and Multiplexity Gradient Across Personal Network Typologies.**

#### **Note:** Panel A displays the percentage of nominated alters providing specific functional support types across personal network typologies with 95% confidence interval error bars. Panel B displays the monotonic progression of high-multiplex alters (≥ 3 support types) and tie closeness (% especially close alters) across network configurations.

Table 4 and Figure 9 show that while social companionship (hanging out) represents a universal baseline of collegiate sociability (\~88% to 93% across all configurations), substantive functional support exhibits a pronounced, monotonic structural gradient across typologies. Informational advice rises systematically from the expansive Pearl Collar configuration (61.6%) and Segmented networks (63.6%) to Centered Stars (70.5%) and reaches its peak in Regular Dense networks (78.0%; F = 8.47, p \< 0.001). Emotional comfort exhibits an identical progression, rising from 55.3% in Pearl Collar networks to 72.5% in Regular Dense networks (F = 5.46, p = 0.001), while financial assistance displays a matching concentration (14.2% in Pearl Collar vs. 23.7% in Regular Dense; F = 5.79, p \< 0.001).

Crucially, this functional gradient reflects a fundamental structural tradeoff between topological reach and relational bandwidth. As shown in Panel B of Figure 9, the Support Multiplexity Index—measuring the average number of functional supports provided per alter—increases monotonically from 2.24 in Pearl Collar networks to 2.62 in Regular Dense networks (F = 6.90, p \< 0.001). Similarly, the share of “high-multiplex” alters providing three or more distinct forms of support rises from 47.9% to 65.6% (F = 6.24, p \< 0.001). This functional concentration is underpinned by emotional intimacy: alters classified as “especially close” account for only 60.5% of contacts in Pearl Collar networks, but surge to 82.9% in Regular Dense networks (F = 14.28, p \< 0.001), accompanied by elevated interpersonal trust (F = 5.28, p = 0.001). Expansive, chained network configurations like the Pearl Collar maximize structural breadth and bridge across modular student worlds, but they do so by diluting the proportion of multiplex, emotionally intensive, and financially supportive ties. Conversely, small, cohesive cliques sacrifice structural reach and external bridging in order to maximize dense mutual trust, emotional solidarity, and multi-functional safety nets.

# Discussion and Conclusion

This study provides an empirical replication and comprehensive extension of personal network structural typologies using longitudinal data from the NetHealth Study. By tracking 701 college students over three years, we demonstrate that personal networks coalesce into distinct, recurrent topological forms that mirror the theoretical archetypes identified by Bidart et al. (2018): Pearl Collar, Segmented, Centered Star, and Regular Dense configurations.

Our findings advance the sociology of personal networks across several theoretical and methodological fronts. First, our empirical decision tree establishes objective, data-driven cutoffs that classify network forms with 92.9% accuracy, offering concrete operational guidance for future research. Second, our wave-by-wave Markov transition models show that while small, cohesive networks exhibit remarkable persistence across college semesters (70.8%), students experience substantial structural mobility, with expansive Pearl Collar configurations emerging cumulatively across academic years. Third, our analysis of functional social support bridges the longstanding divide between compositional and topological traditions, showing that expansive, modular configurations like the Pearl Collar trade off tie multiplexity and emotional solidarity in exchange for broad structural reach, whereas dense enclaves maximize mutual trust and high-bandwidth emotional safety nets. Future research should leverage these empirical typologies to investigate downstream consequences for academic performance, mental health, and early occupational trajectories.

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

Lin, N. (2001). *Social capital: A theory of social structure and action*. Cambridge University Press. https://doi.org/10.1017/CBO9780511815447

Liu, S., Hachen, D., Lizardo, O., Poellabauer, C., Striegel, A., & Milenković, T. (2018). Network analysis of the NetHealth data: Exploring co-evolution of individuals’ social network positions and physical activities. *Applied Network Science*, 3(1), 45. https://doi.org/10.1007/s41109-018-0103-2

Marsden, P. V. (1987). Core discussion networks of Americans. *American Sociological Review*, 52(1), 122–131. https://doi.org/10.2307/2095397

Maya-Jariego, I. (2021). Building a structural typology of personal networks: Individual differences in the cohesion of interpersonal environment. *Social Networks*, 64, 173–180. https://doi.org/10.1016/j.socnet.2020.09.004

Maya-Jariego, I., & González-Tinoco, E. (2023). Use of a hierarchical deconstruction procedure for the classification of personal networks: Exploring nested groups around you. *Social Networks*, 73, 20–29. https://doi.org/10.1016/j.socnet.2022.12.003

Maya-Jariego, I., & Holgado, D. (2015). Living in the metropolitan area: Correlation of interurban mobility with the structural cohesion of personal networks and the originative sense of community. *Psychosocial Intervention*, 24(3), 185–190. https://doi.org/10.1016/j.psi.2015.09.001

Maya-Jariego, I., Letina, S., & González Tinoco, E. (2020). Personal networks and psychological attributes: Exploring individual differences in personality and sense of community and their relationship to the structure of personal networks. *Network Science*, 8(2), 168–188. https://doi.org/10.1017/nws.2019.15

McCarty, C. (2002). Structure in personal networks. *Journal of Social Structure*, 3(1).

Offer, S., & Fischer, C. S. (2018). Does help discussion build closer ties? In J. Youm, E. O. Laumann, & K. Lee (Eds.), *Social networks and the life course* (pp. 45–68). Springer. https://doi.org/10.1007/978-3-319-71544-5_3

Pelle, E., & Pappadà, R. (2021). A clustering procedure for mixed-type data to explore ego network typologies: An application to elderly people living alone in Italy. *Statistical Methods & Applications*, 30(5), 1507–1533. https://doi.org/10.1007/s10260-021-00591-5

Perry, B. L., Pescosolido, B. A., & Borgatti, S. P. (2018). *Egocentric network analysis: Foundations, methods, and models*. Cambridge University Press. https://doi.org/10.1017/9781316443255

Sepulvado, B., Wood, M., Wang, C., Fridmanski, E., Chandler, M., Lizardo, O., & Hachen, D. (2020). Predicting homophily and social network connectivity from dyadic behavioral similarity trajectory clusters. *Social Science Computer Review*, 40(1), 186–205. https://doi.org/10.1177/0894439320923123

Smith, M. L. (2020). Introduction to the special issue on ego networks. *Network Science*, 8(2), 139–141. https://doi.org/10.1017/nws.2020.17

Vacca, R. (2020). Structure in personal networks: Constructing and comparing typologies. *Network Science*, 8(2), 142–167. https://doi.org/10.1017/nws.2019.29

Wang, C., Lizardo, O., & Hachen, D. S. (2020). Neither influence nor selection: Examining co-evolution of political orientation and social networks in the NetSense and NetHealth studies. *PLOS ONE*, 15(5), e0233458. https://doi.org/10.1371/journal.pone.0233458
