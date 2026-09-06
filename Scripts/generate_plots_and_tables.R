# Scripts/generate_plots_and_tables.R
# Pre-computes publication-grade 6.5-inch figures (Plots/) and APA markdown tables (cache/)
# Strictly adheres to AGENTS.md visualization, table, and writing guidelines

suppressPackageStartupMessages({
  library(igraph)
  library(tidygraph)
  library(ggraph)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(patchwork)
  library(cluster)
  library(nnet)
  library(mclogit)
  library(rpart)
  library(rpart.plot)
})

dir.create("Plots", showWarnings = FALSE)
dir.create("cache", showWarnings = FALSE)

# Load master dataset
df <- read.csv("dat/data_clusters-4-km_demog_lgcc.csv")
df$cluster_factor <- factor(df$cluster_km,
                            levels = 0:3,
                            labels = c("Pearl Collar", "Segmented", "Centered Star", "Regular Dense"))

basic_raw <- read.csv("raw_dat/basic_survey.csv")
netsurv_raw <- read.csv("raw_dat/network_survey.csv")
edges_raw <- read.csv("raw_dat/alter_alter_edges.csv")

# Standard APA ggplot theme
theme_apa <- function(base_size = 10) {
  theme_classic(base_size = base_size) %+replace%
    theme(
      panel.grid.major.y = element_line(colour = "grey90", linetype = "dashed", linewidth = 0.3),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(colour = "grey40", linewidth = 0.4),
      axis.ticks = element_line(colour = "grey40", linewidth = 0.4),
      axis.title = element_text(face = "bold", size = base_size),
      axis.text = element_text(colour = "grey20", size = base_size - 1),
      legend.position = "bottom",
      legend.title = element_text(face = "bold", size = base_size - 1),
      legend.text = element_text(size = base_size - 1.5),
      legend.margin = margin(t = 2, b = 2),
      plot.title = element_text(face = "bold", size = base_size + 1, hjust = 0.5, margin = margin(b = 5)),
      plot.subtitle = element_text(size = base_size - 0.5, hjust = 0.5, margin = margin(b = 5)),
      plot.margin = margin(t = 8, r = 8, b = 8, l = 8)
    )
}

# ==============================================================================
# 1. GENERATE PUBLICATION FIGURES (WIDTH = 6.5 INCHES, 300 DPI)
# ==============================================================================
cat("Generating publication figures at 6.5-inch width...\n")

# Figure 1: Cumulative Ego-Network Size Distribution
p_fig1 <- ggplot(df, aes(x = size)) +
  geom_histogram(binwidth = 3, fill = "#2b5c8f", color = "white", alpha = 0.9, linewidth = 0.3) +
  geom_vline(xintercept = median(df$size), linetype = "dashed", color = "#d95f02", linewidth = 0.7) +
  annotate("text", x = median(df$size) + 2, y = 65, 
           label = paste0("Median = ", median(df$size)), 
           hjust = 0, fontface = "italic", size = 3.5, color = "#d95f02") +
  scale_x_continuous(breaks = seq(0, 90, 10)) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.05))) +
  theme_apa() +
  labs(x = "Cumulative Ego-Network Size (Number of Unique Alters)",
       y = "Number of Participants")
ggsave("Plots/fig1_size_distribution.png", p_fig1, width = 6.5, height = 3.8, dpi = 300)

# Figure 2: Cluster Partition Quality Diagnostics across k = 2 to 10
cluster_vars <- c("size", "modularity", "diameter", "betweenness_centralization", "density")
X_scaled <- scale(df[, cluster_vars])
d_dist <- dist(X_scaled)

diag_results <- list()
for (k in 2:10) {
  set.seed(42)
  km <- kmeans(X_scaled, centers = k, nstart = 100, iter.max = 100)
  sil <- silhouette(km$cluster, d_dist)
  avg_sil <- mean(sil[, "sil_width"])
  wss <- km$tot.withinss
  bss_tss <- (km$betweenss / km$totss) * 100
  n <- nrow(X_scaled)
  ch <- (km$betweenss / (k - 1)) / (km$tot.withinss / (n - k))
  diag_results[[as.character(k)]] <- data.frame(k = k, WSS = wss, BSS_TSS = bss_tss, Avg_Silhouette = avg_sil, Calinski_Harabasz = ch)
}
diag_df <- do.call(rbind, diag_results)

p_elbow <- ggplot(diag_df, aes(x = k, y = WSS)) +
  geom_line(color = "#2b5c8f", linewidth = 0.8) +
  geom_point(size = 2.8, color = "#2b5c8f") +
  geom_point(data = filter(diag_df, k == 4), aes(x = k, y = WSS), color = "#d95f02", size = 4.0, shape = 18) +
  annotate("text", x = 4.3, y = 1450, label = "Elbow bend (k = 4)", fontface = "bold", size = 3.0, color = "#d95f02", hjust = 0) +
  scale_x_continuous(breaks = 2:10) +
  theme_classic(base_size = 9.5) +
  theme(panel.grid.major.y = element_line(color = "grey90", linetype = "dashed", linewidth = 0.3),
        axis.line = element_line(color = "grey40", linewidth = 0.4),
        plot.title = element_text(face = "bold", size = 10, hjust = 0.5)) +
  labs(x = "Number of Clusters (k)", y = "Total Within-Cluster SS", title = "A: Elbow Criterion (Within SS)")

p_sil <- ggplot(diag_df, aes(x = k, y = Avg_Silhouette)) +
  geom_line(color = "#006d2c", linewidth = 0.8) +
  geom_point(size = 2.8, color = "#006d2c") +
  geom_point(data = filter(diag_df, k == 4), aes(x = k, y = Avg_Silhouette), color = "#d95f02", size = 4.0, shape = 18) +
  annotate("text", x = 4.3, y = 0.282, label = "Local peak (k = 4)", fontface = "bold", size = 3.0, color = "#d95f02", hjust = 0) +
  scale_x_continuous(breaks = 2:10) +
  theme_classic(base_size = 9.5) +
  theme(panel.grid.major.y = element_line(color = "grey90", linetype = "dashed", linewidth = 0.3),
        axis.line = element_line(color = "grey40", linewidth = 0.4),
        plot.title = element_text(face = "bold", size = 10, hjust = 0.5)) +
  labs(x = "Number of Clusters (k)", y = "Average Silhouette Width", title = "B: Silhouette Criterion")

p_fig2 <- p_elbow + p_sil
ggsave("Plots/fig2_cluster_selection.png", p_fig2, width = 6.5, height = 3.2, dpi = 300)

# Figure 3: Rethought Standardized Z-Score Profiles Across Typologies (2x2 comparative grid)
var_labels <- c("Size", "Diameter", "Density", "Modularity", "Centralization")
df_z <- df %>% mutate(across(all_of(cluster_vars), ~ as.vector(scale(.x))))
z_summary <- df_z %>%
  group_by(cluster_km) %>%
  summarise(across(all_of(cluster_vars), mean)) %>%
  mutate(Typology = factor(cluster_km, levels = 0:3, 
                           labels = c("Pearl Collar (n = 176)", "Segmented (n = 261)", 
                                      "Centered Star (n = 143)", "Regular Dense (n = 121)"))) %>%
  tidyr::pivot_longer(cols = all_of(cluster_vars), names_to = "Metric", values_to = "Z_Score") %>%
  mutate(Metric = factor(Metric, levels = rev(cluster_vars), labels = rev(var_labels)),
         Direction = ifelse(Z_Score >= 0, "Above Average", "Below Average"),
         Label = sprintf("%+.2f", Z_Score))

p_fig3 <- ggplot(z_summary, aes(x = Z_Score, y = Metric, fill = Direction)) +
  geom_col(width = 0.55, alpha = 0.9) +
  geom_vline(xintercept = 0, color = "grey30", linewidth = 0.5) +
  geom_text(aes(label = Label, hjust = ifelse(Z_Score >= 0, -0.15, 1.15)),
            size = 3.0, fontface = "bold", colour = "grey20") +
  facet_wrap(~ Typology, ncol = 2, scales = "fixed") +
  scale_fill_manual(values = c("Above Average" = "#0072B2", "Below Average" = "#D55E00")) +
  scale_x_continuous(limits = c(-2.5, 2.6), breaks = seq(-2.0, 2.0, 1.0), labels = function(x) paste0(x, " SD")) +
  theme_classic(base_size = 9.5) +
  theme(
    strip.background = element_rect(fill = "#f0f4f8", color = "grey70", linewidth = 0.5),
    strip.text = element_text(face = "bold", size = 9.5, color = "#104e8b"),
    panel.grid.major.x = element_line(color = "grey90", linetype = "dashed", linewidth = 0.3),
    panel.grid.major.y = element_blank(),
    axis.line = element_line(color = "grey40", linewidth = 0.4),
    axis.title = element_text(face = "bold", size = 9.5),
    axis.text.y = element_text(face = "bold", colour = "grey20"),
    legend.position = "bottom",
    legend.title = element_blank(),
    legend.margin = margin(t = -2, b = 2)
  ) +
  labs(x = "Standardized Deviation from Cohort Mean (Z-Score)", y = "")
ggsave("Plots/fig3_cluster_profiles.png", p_fig3, width = 6.5, height = 4.8, dpi = 300)

# Also update plots/kmeans.png for the Quarto presentation
ggsave("plots/kmeans.png", p_fig3, width = 9.0, height = 6.5, dpi = 300)

# Figure 4: Empirical Decision Tree
png("Plots/fig4_decision_tree.png", width = 6.5, height = 4.2, units = "in", res = 300)
tree_fit <- rpart(
  cluster_factor ~ size + modularity + diameter + betweenness_centralization + density,
  data = df,
  method = "class",
  control = rpart.control(cp = 0.015, maxdepth = 4, minsplit = 15)
)
rpart.plot(tree_fit, type = 4, extra = 104, under = TRUE, fallen.leaves = TRUE, box.palette = "BuGn", cex = 0.65, tweak = 1.1, main = "")
dev.off()

# Figure 5: Metric Interdependence & Correlation Heatmap
metric_vars <- c("size", "betweenness_centralization", "modularity", "density", "diameter", "clustering", "n_components", "prop_lcc")
metric_labels <- c("Size", "Centralization", "Modularity", "Density", "Diameter", "Transitivity", "Components", "LCC Share")

cor_mat <- cor(df[, metric_vars], use = "pairwise.complete.obs")
colnames(cor_mat) <- metric_labels
rownames(cor_mat) <- metric_labels
cor_df <- as.data.frame(as.table(cor_mat))
names(cor_df) <- c("Metric1", "Metric2", "Correlation")

p_fig5 <- ggplot(cor_df, aes(x = Metric1, y = Metric2, fill = Correlation)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.2f", Correlation)), size = 2.8, color = ifelse(abs(cor_df$Correlation) > 0.55, "white", "black")) +
  scale_fill_gradient2(low = "#d73027", mid = "#f7f7f7", high = "#1a9850", midpoint = 0, limits = c(-1, 1), name = "Pearson r") +
  theme_minimal(base_size = 9.5) +
  theme(
    axis.title = element_blank(),
    axis.text.x = element_text(angle = 35, hjust = 1, face = "bold", colour = "grey20"),
    axis.text.y = element_text(face = "bold", colour = "grey20"),
    panel.grid = element_blank(),
    legend.position = "right"
  ) +
  coord_fixed()
ggsave("Plots/fig5_metric_correlations.png", p_fig5, width = 6.5, height = 4.8, dpi = 300)

# Figure 6: Archetype Network Exemplars / Medoids
medoids <- c("Pearl Collar" = 82248, "Segmented" = 32249, "Centered Star" = 39414, "Regular Dense" = 19591)
plots_medoids <- list()
for (typology in names(medoids)) {
  ego <- medoids[[typology]]
  alters <- unique(netsurv_raw$alterid[netsurv_raw$egoid == ego])
  sub_edges <- edges_raw %>%
    filter(egoid == ego, vertex1 != ego, vertex2 != ego) %>%
    select(vertex1, vertex2) %>% distinct() %>% filter(vertex1 %in% alters, vertex2 %in% alters)
  g <- graph_from_data_frame(sub_edges, directed = FALSE, vertices = data.frame(name = alters))
  # Eliminate isolates to focus on connected component topology
  g <- delete_vertices(g, which(degree(g) == 0))
  tg <- as_tbl_graph(g) %>%
    mutate(degree = centrality_degree(), betweenness = centrality_betweenness(), community = as.factor(group_louvain()))
  set.seed(42)
  p <- ggraph(tg, layout = "stress") +
    geom_edge_link(alpha = 0.35, colour = "grey50", width = 0.4) +
    geom_node_point(aes(size = betweenness, fill = community), shape = 21, stroke = 0.4, color = "black") +
    scale_size_continuous(range = c(2, 6.5), guide = "none") +
    scale_fill_brewer(palette = "Set3", guide = "none") +
    theme_void() +
    theme(plot.title = element_text(face = "bold", size = 10, hjust = 0.5, margin = margin(b = 2)),
          plot.subtitle = element_text(size = 7.5, hjust = 0.5, colour = "grey30", margin = margin(b = 3)),
          plot.margin = margin(4, 4, 4, 4)) +
    labs(title = typology,
         subtitle = sprintf("Ego %d (N = %d, Dens = %.2f, Mod = %.2f, Cent = %.2f)",
                            ego, length(alters), edge_density(g), modularity(cluster_louvain(g)),
                            centr_betw(g, directed = FALSE)$centralization))
  plots_medoids[[typology]] <- p
}
p_fig6 <- (plots_medoids[[1]] + plots_medoids[[2]]) / (plots_medoids[[3]] + plots_medoids[[4]])
ggsave("Plots/fig6_network_archetypes.png", p_fig6, width = 6.5, height = 5.6, dpi = 300)

# Figure 7: Comparative Decision Tree (Bidart vs. NetHealth)
draw_bidart_tree <- function() {
  nodes <- data.frame(
    x = c(1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4),
    y = c(5, 7.5, 2.5, 9, 6.5, 3.5, 1, 9.5, 8.2, 4.2, 2.8),
    label = c('Betweenness\n> 0.20?', 'Modularity\n> 0.28?', 'Modularity\n> 0.28?', 'Mod >= 0.40 &\nDiam >= 4?',
              'Centered Dense\n(Typology)', 'Density\n> 0.10?', 'Regular Dense\n(Typology)', 'Pearl Collar',
              'Centered Star', 'Segmented', 'Dispersed'),
    type = c('test', 'test', 'test', 'test', 'leaf', 'test', 'leaf', 'leaf', 'leaf', 'leaf', 'leaf')
  )
  segs <- data.frame(x = c(1, 1, 2, 2, 2, 2, 3, 3, 3, 3), y = c(5, 5, 7.5, 7.5, 2.5, 2.5, 9, 9, 3.5, 3.5),
                     xend = c(2, 2, 3, 3, 3, 3, 4, 4, 4, 4), yend = c(7.5, 2.5, 9, 6.5, 3.5, 1, 9.5, 8.2, 4.2, 2.8))
  ggplot() +
    geom_segment(data = segs, aes(x = x, y = y, xend = xend, yend = yend), color = 'grey50', linewidth = 0.5) +
    geom_label(data = nodes %>% filter(type == 'test'), aes(x = x, y = y, label = label), fill = '#f0f4f8', color = '#104e8b', fontface = 'bold', size = 2.2, label.padding = unit(0.2, 'lines')) +
    geom_label(data = nodes %>% filter(type == 'leaf'), aes(x = x, y = y, label = label), fill = '#e5f5e0', color = '#006d2c', fontface = 'bold', size = 2.2, label.padding = unit(0.2, 'lines')) +
    theme_void() + labs(title = 'A: Bidart et al. (2018) Theoretical Tree') +
    theme(plot.title = element_text(face = 'bold', size = 9, hjust = 0.5, margin = margin(b = 5))) +
    xlim(0.8, 4.4) + ylim(0.5, 10.2)
}

draw_nethealth_tree <- function() {
  nodes <- data.frame(
    x = c(1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4),
    y = c(5, 7.5, 2.5, 9, 6.5, 3.5, 1.2, 9.8, 8.4, 7.2, 5.8),
    label = c('Density\n< 0.55?', 'Betweenness\n>= 0.235?', 'Betweenness\n>= 0.325?', 'Diameter >= 3.5\n& Size >= 37?',
              'Density\n< 0.24?', 'Centered Star\n(100% Pure)', 'Regular Dense\n(98.4% Pure)', 'Pearl Collar\n(97.2% Pure)',
              'Segmented\n(97.8% Pure)', 'Pearl Collar\n(85.3% Pure)', 'Centered Star\n(89.9% Pure)'),
    type = c('test', 'test', 'test', 'test', 'test', 'leaf', 'leaf', 'leaf', 'leaf', 'leaf', 'leaf')
  )
  segs <- data.frame(x = c(1, 1, 2, 2, 2, 2, 3, 3, 3, 3), y = c(5, 5, 7.5, 7.5, 2.5, 2.5, 9, 9, 6.5, 6.5),
                     xend = c(2, 2, 3, 3, 3, 3, 4, 4, 4, 4), yend = c(7.5, 2.5, 9, 6.5, 3.5, 1.2, 9.8, 8.4, 7.2, 5.8))
  ggplot() +
    geom_segment(data = segs, aes(x = x, y = y, xend = xend, yend = yend), color = 'grey50', linewidth = 0.5) +
    geom_label(data = nodes %>% filter(type == 'test'), aes(x = x, y = y, label = label), fill = '#f0f4f8', color = '#104e8b', fontface = 'bold', size = 2.2, label.padding = unit(0.2, 'lines')) +
    geom_label(data = nodes %>% filter(type == 'leaf'), aes(x = x, y = y, label = label), fill = '#e5f5e0', color = '#006d2c', fontface = 'bold', size = 2.2, label.padding = unit(0.2, 'lines')) +
    theme_void() + labs(title = 'B: NetHealth Empirical Tree (92.9% Acc.)') +
    theme(plot.title = element_text(face = 'bold', size = 9, hjust = 0.5, margin = margin(b = 5))) +
    xlim(0.8, 4.5) + ylim(0.5, 10.2)
}
p_fig7 <- draw_bidart_tree() + draw_nethealth_tree()
ggsave("Plots/fig7_comparative_decision_trees.png", p_fig7, width = 6.5, height = 4.2, dpi = 300)

# Figure 8: Longitudinal Markov State Transitions
netsurv_raw$wave_int <- as.integer(gsub("Wave", "", netsurv_raw$wave))
classify_network <- function(size, dens, cent_betw, diam, mod) {
  if (dens >= 0.547) {
    if (cent_betw >= 0.325) return("Centered Star")
    return("Regular Dense")
  } else {
    if (cent_betw >= 0.235) {
      if (dens < 0.241) return("Pearl Collar")
      return("Centered Star")
    } else {
      if (diam >= 3.5) {
        if (size >= 36.5 || mod >= 0.410) return("Pearl Collar")
        return("Segmented")
      } else {
        if (size >= 46.0) return("Pearl Collar")
        return("Segmented")
      }
    }
  }
}

combos <- netsurv_raw %>% select(egoid, wave_int) %>% distinct()
res_wave_list <- list()
for (i in 1:nrow(combos)) {
  ego <- combos$egoid[i]
  w <- combos$wave_int[i]
  alters <- unique(netsurv_raw$alterid[netsurv_raw$egoid == ego & netsurv_raw$wave_int == w])
  n_alters <- length(alters)
  if (n_alters < 3) next
  sub_edges <- edges_raw %>%
    filter(egoid == ego, wave == w, vertex1 != ego, vertex2 != ego) %>%
    select(vertex1, vertex2) %>% distinct() %>% filter(vertex1 %in% alters, vertex2 %in% alters)
  if (nrow(sub_edges) == 0) next
  g <- graph_from_data_frame(sub_edges, directed = FALSE, vertices = data.frame(name = alters))
  g <- simplify(g)
  dens <- edge_density(g); if (is.na(dens)) dens <- 0
  cent_betw <- centr_betw(g, directed = FALSE)$centralization; if (is.nan(cent_betw) || is.na(cent_betw)) cent_betw <- 0
  comps <- components(g)
  max_comp_size <- if (length(comps$csize) > 0) max(comps$csize) else 0
  diam_lgcc <- if (max_comp_size > 1) diameter(induced_subgraph(g, which(comps$membership == which.max(comps$csize))), directed = FALSE, weights = NA) else 0
  mod <- if (ecount(g) > 0) modularity(cluster_louvain(g)) else 0; if (is.nan(mod) || is.na(mod)) mod <- 0
  state <- classify_network(n_alters, dens, cent_betw, diam_lgcc, mod)
  res_wave_list[[length(res_wave_list) + 1]] <- data.frame(egoid = ego, wave = w, state = state)
}
wave_df <- do.call(rbind, res_wave_list)

trans_df <- wave_df %>%
  arrange(egoid, wave) %>%
  group_by(egoid) %>%
  mutate(next_wave = lead(wave), next_state = lead(state)) %>%
  filter(!is.na(next_state), next_wave == wave + 1)

trans_matrix <- table(From = trans_df$state, To = trans_df$next_state)
trans_prob <- prop.table(trans_matrix, margin = 1)
trans_prob_df <- as.data.frame(as.table(trans_prob))
names(trans_prob_df) <- c("Origin_State", "Destination_State", "Probability")

p_fig8 <- ggplot(trans_prob_df, aes(x = Destination_State, y = Origin_State, fill = Probability)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = sprintf("%.1f%%", Probability * 100)), size = 3.2, 
            color = ifelse(trans_prob_df$Probability > 0.45, "white", "black"), fontface = "bold") +
  scale_fill_gradient(low = "#f7fbff", high = "#08519c", limits = c(0, 1), labels = scales::percent_format(), name = "Transition\nProbability") +
  theme_minimal(base_size = 9.5) +
  theme(axis.text.x = element_text(angle = 25, hjust = 1, face = "bold", colour = "grey20"),
        axis.text.y = element_text(face = "bold", colour = "grey20"),
        panel.grid = element_blank()) +
  labs(x = "Destination State (Semester t+1)", y = "Origin State (Semester t)", 
       title = "Semester-to-Semester Markov Transition Probabilities (N = 1,900 Transitions)")
ggsave("Plots/fig8_longitudinal_transitions.png", p_fig8, width = 6.5, height = 4.0, dpi = 300)

# Figure 9: Demographic Disparity Dumbbells
db_gender <- df %>%
  filter(gender_1 %in% c("Male", "Female")) %>%
  count(cluster_factor, gender_1) %>% group_by(gender_1) %>% mutate(pct = n / sum(n) * 100) %>%
  select(cluster_factor, gender_1, pct) %>% pivot_wider(names_from = gender_1, values_from = pct) %>%
  mutate(gap = Male - Female, gap_label = sprintf("%+.1f pp", gap), label_x = pmax(Male, Female) + 3.2)

p_db_gender <- ggplot(db_gender, aes(y = cluster_factor)) +
  geom_segment(aes(x = Female, xend = Male, yend = cluster_factor), color = "grey60", linewidth = 0.8) +
  geom_point(aes(x = Female, shape = "Women (Ref.)", color = "Women (Ref.)"), size = 3.6) +
  geom_point(aes(x = Male, shape = "Men", color = "Men"), size = 3.6) +
  geom_text(aes(x = label_x, label = gap_label), size = 3.0, fontface = "bold", colour = "grey25") +
  scale_shape_manual(values = c("Women (Ref.)" = 16, "Men" = 17), name = "Gender Identity") +
  scale_color_manual(values = c("Women (Ref.)" = "#0072B2", "Men" = "#D55E00"), name = "Gender Identity") +
  scale_x_continuous(limits = c(0, 50), labels = function(x) paste0(x, "%")) +
  theme_apa(base_size = 9) +
  labs(x = "Prevalence within Group (%)", y = "", title = "A: Gender Identity Disparity (Men vs. Women)")

db_foreign <- df %>%
  filter(race_1 != "") %>%
  mutate(status = if_else(race_1 == "Foreign Student", "Foreign", "Domestic")) %>%
  count(cluster_factor, status) %>% group_by(status) %>% mutate(pct = n / sum(n) * 100) %>%
  select(cluster_factor, status, pct) %>% pivot_wider(names_from = status, values_from = pct) %>%
  mutate(gap = Foreign - Domestic, gap_label = sprintf("%+.1f pp", gap), label_x = pmax(Foreign, Domestic) + 3.2)

p_db_foreign <- ggplot(db_foreign, aes(y = cluster_factor)) +
  geom_segment(aes(x = Domestic, xend = Foreign, yend = cluster_factor), color = "grey60", linewidth = 0.8) +
  geom_point(aes(x = Domestic, shape = "Domestic (Ref.)", color = "Domestic (Ref.)"), size = 3.6) +
  geom_point(aes(x = Foreign, shape = "Foreign Student", color = "Foreign Student"), size = 3.6) +
  geom_text(aes(x = label_x, label = gap_label), size = 3.0, fontface = "bold", colour = "grey25") +
  scale_shape_manual(values = c("Domestic (Ref.)" = 16, "Foreign Student" = 17), name = "International Status") +
  scale_color_manual(values = c("Domestic (Ref.)" = "#0072B2", "Foreign Student" = "#D55E00"), name = "International Status") +
  scale_x_continuous(limits = c(0, 50), labels = function(x) paste0(x, "%")) +
  theme_apa(base_size = 9) +
  labs(x = "Prevalence within Group (%)", y = "", title = "B: International Status Disparity (Foreign vs. Domestic)")

p_fig9 <- p_db_gender / p_db_foreign
ggsave("Plots/fig9_demographic_dumbbells.png", p_fig9, width = 6.5, height = 5.2, dpi = 300)

# Figure 10: Big Five Personality Dimensions across Typologies (Forest Plot)
big5_long <- df %>%
  select(cluster_factor, Extraversion_1, Openness_1, Agreeableness_1, Conscientiousness_1, Neuroticism_1) %>%
  pivot_longer(cols = -cluster_factor, names_to = "Trait", values_to = "Score") %>%
  mutate(Trait = gsub("_1", "", Trait),
         Trait = factor(Trait, levels = rev(c("Extraversion", "Agreeableness", "Conscientiousness", "Neuroticism", "Openness"))),
         cluster_factor = factor(cluster_factor, levels = c("Pearl Collar", "Segmented", "Centered Star", "Regular Dense"))) %>%
  group_by(cluster_factor, Trait) %>%
  summarise(Mean = mean(Score, na.rm = TRUE),
            SE = sd(Score, na.rm = TRUE) / sqrt(sum(!is.na(Score))), .groups = "drop")

p_fig10 <- ggplot(big5_long, aes(y = Trait, x = Mean, color = cluster_factor)) +
  geom_errorbar(aes(xmin = Mean - 1.96 * SE, xmax = Mean + 1.96 * SE),
                width = 0.25, linewidth = 0.5, position = position_dodge(width = 0.6)) +
  geom_point(size = 2.8, position = position_dodge(width = 0.6)) +
  scale_color_brewer(palette = "Set1", name = "Personal Network Typology") +
  scale_x_continuous(breaks = seq(2.6, 4.0, by = 0.2), limits = c(2.6, 4.0)) +
  theme_apa(base_size = 9.5) +
  theme(legend.position = "bottom") +
  guides(color = guide_legend(nrow = 2, byrow = TRUE)) +
  labs(y = "Big Five Personality Trait", x = "Mean Trait Score (1 to 5 Scale)")
ggsave("Plots/fig10_personality_profiles.png", p_fig10, width = 6.5, height = 4.2, dpi = 300)

# ==============================================================================
# 2. GENERATE PRE-COMPILED APA MARKDOWN TABLES (cache/)
# ==============================================================================
cat("Generating pre-compiled APA markdown tables in cache/...\n")

# Table 1: Structural Metrics by Typology (Reformatted Transposed Layout for 6.5-inch Portrait Width)
t1_overall <- df %>%
  summarise(
    N = n(),
    Size = sprintf("%.1f (%.1f)", mean(size), sd(size)),
    Modularity = sprintf("%.2f (%.2f)", mean(modularity), sd(modularity)),
    Diameter = sprintf("%.1f (%.1f)", mean(diameter), sd(diameter)),
    Centralization = sprintf("%.2f (%.2f)", mean(betweenness_centralization), sd(betweenness_centralization)),
    Density = sprintf("%.2f (%.2f)", mean(density), sd(density)),
    Clustering = sprintf("%.2f (%.2f)", mean(clustering), sd(clustering)),
    PropLCC = sprintf("%.1f%% (%.1f)", mean(prop_lcc) * 100, sd(prop_lcc) * 100)
  )

t1_by_cluster <- df %>%
  group_by(cluster_factor) %>%
  summarise(
    N = n(),
    Size = sprintf("%.1f (%.1f)", mean(size), sd(size)),
    Modularity = sprintf("%.2f (%.2f)", mean(modularity), sd(modularity)),
    Diameter = sprintf("%.1f (%.1f)", mean(diameter), sd(diameter)),
    Centralization = sprintf("%.2f (%.2f)", mean(betweenness_centralization), sd(betweenness_centralization)),
    Density = sprintf("%.2f (%.2f)", mean(density), sd(density)),
    Clustering = sprintf("%.2f (%.2f)", mean(clustering), sd(clustering)),
    PropLCC = sprintf("%.1f%% (%.1f)", mean(prop_lcc) * 100, sd(prop_lcc) * 100),
    .groups = "drop"
  )

metrics <- c(
  "Network Size",
  "Community Modularity",
  "Network Diameter",
  "Betweenness Centralization",
  "Alter-Alter Density",
  "Transitivity (Clustering)",
  "Largest Component Share (%)"
)
metric_cols <- c("Size", "Modularity", "Diameter", "Centralization", "Density", "Clustering", "PropLCC")

t1_md <- c(
  "| Structural Metric | Full Sample<br>(N = 701) | Pearl Collar<br>(n = 176) | Segmented<br>(n = 261) | Centered Star<br>(n = 143) | Regular Dense<br>(n = 121) |",
  "| :--- | :---: | :---: | :---: | :---: | :---: |"
)

for (m_idx in seq_along(metrics)) {
  m_name <- metrics[m_idx]
  m_col <- metric_cols[m_idx]
  val_overall <- t1_overall[[m_col]]
  val_pearl <- t1_by_cluster %>% filter(cluster_factor == "Pearl Collar") %>% pull(!!sym(m_col))
  val_seg <- t1_by_cluster %>% filter(cluster_factor == "Segmented") %>% pull(!!sym(m_col))
  val_star <- t1_by_cluster %>% filter(cluster_factor == "Centered Star") %>% pull(!!sym(m_col))
  val_dense <- t1_by_cluster %>% filter(cluster_factor == "Regular Dense") %>% pull(!!sym(m_col))
  
  t1_md <- c(t1_md, sprintf("| %s | %s | %s | %s | %s | %s |",
                            m_name, val_overall, val_pearl, val_seg, val_star, val_dense))
}
writeLines(t1_md, "cache/table1_structural_metrics.md")

# Table 2: Cluster Selection Diagnostics across k = 2 to 10
t2_diag_md <- c(
  "| Number of Clusters (k) | Within-Cluster SS | Variance Explained (%) | Average Silhouette Width | Calinski-Harabasz Index |",
  "| :---: | :---: | :---: | :---: | :---: |"
)
for (i in 1:nrow(diag_df)) {
  r <- diag_df[i, ]
  bold_pre <- if (r$k == 4) "**" else ""
  bold_post <- if (r$k == 4) "**" else ""
  t2_diag_md <- c(t2_diag_md, sprintf("| %s%d%s | %s%.1f%s | %s%.1f%%%s | %s%.3f%s | %s%.1f%s |",
                                      bold_pre, r$k, bold_post,
                                      bold_pre, r$WSS, bold_post,
                                      bold_pre, r$BSS_TSS, bold_post,
                                      bold_pre, r$Avg_Silhouette, bold_post,
                                      bold_pre, r$Calinski_Harabasz, bold_post))
}
writeLines(t2_diag_md, "cache/table2_cluster_selection.md")

# Table 3: Demographics by Typology Cross-Tabulation
t3_gender <- df %>%
  filter(gender_1 %in% c("Male", "Female")) %>%
  count(cluster_factor, gender_1) %>% group_by(cluster_factor) %>%
  mutate(pct = sprintf("%.1f%%", n / sum(n) * 100)) %>% select(cluster_factor, gender_1, pct) %>%
  pivot_wider(names_from = gender_1, values_from = pct)

t3_race <- df %>%
  filter(race_1 %in% c("White", "African-American", "Latino/a", "Asian-American", "Foreign Student")) %>%
  count(cluster_factor, race_1) %>% group_by(cluster_factor) %>%
  mutate(pct = sprintf("%.1f%%", n / sum(n) * 100)) %>% select(cluster_factor, race_1, pct) %>%
  pivot_wider(names_from = race_1, values_from = pct)

t3_merged <- inner_join(t3_gender, t3_race, by = "cluster_factor")
t3_md <- c(
  "| Personal Network Typology | Men (%) | Women (%) | White (%) | African-American (%) | Latinx (%) | Asian-American (%) | Foreign Student (%) |",
  "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
)
for (i in 1:nrow(t3_merged)) {
  r <- t3_merged[i, ]
  t3_md <- c(t3_md, sprintf("| %s | %s | %s | %s | %s | %s | %s | %s |",
                            r$cluster_factor, r$Male, r$Female, r$White, 
                            r$`African-American`, r$`Latino/a`, r$`Asian-American`, r$`Foreign Student`))
}
writeLines(t3_md, "cache/table3_demographics.md")

# Table 4: Multinomial Logistic Regressions (Demographics & International Status)
dat_reg <- df %>%
  filter(!is.na(gender_1), gender_1 %in% c("Male", "Female"),
         race_1 %in% c("White", "African-American", "Latino/a", "Asian-American", "Foreign Student")) %>%
  mutate(gender = factor(gender_1, levels = c("Female", "Male")),
         race = factor(race_1, levels = c("White", "African-American", "Latino/a", "Asian-American", "Foreign Student")),
         foreign = factor(if_else(race_1 == "Foreign Student", "Foreign", "Domestic"), levels = c("Domestic", "Foreign")),
         cluster = factor(cluster_factor, levels = c("Pearl Collar", "Segmented", "Centered Star", "Regular Dense")))

mod_m2 <- multinom(cluster ~ gender + foreign, data = dat_reg, trace = FALSE)
extract_multinom_md <- function(model) {
  s <- summary(model)
  coefs <- s$coefficients
  ses <- s$standard.errors
  z <- coefs / ses
  p <- 2 * (1 - pnorm(abs(z)))
  rows <- c()
  for (cl in rownames(coefs)) {
    for (pr in colnames(coefs)) {
      if (pr == "(Intercept)") next
      est <- coefs[cl, pr]
      se_val <- ses[cl, pr]
      p_val <- p[cl, pr]
      stars <- if (p_val < 0.001) "***" else if (p_val < 0.01) "**" else if (p_val < 0.05) "*" else ""
      rows <- c(rows, sprintf("| %s: %s | %.2f%s | (%.2f) | %.3f |", cl, pr, est, stars, se_val, p_val))
    }
  }
  rows
}
t4_md <- c(
  "| Comparison Cluster vs. Reference (Pearl Collar) | Estimate | SE | p-value |",
  "| :--- | :---: | :---: | :---: |",
  extract_multinom_md(mod_m2)
)
writeLines(t4_md, "cache/table4_regressions.md")

# Table 5: Big Five Personality Multinomial Model
mod_big5 <- multinom(cluster ~ Extraversion_1 + Openness_1 + Agreeableness_1 + Conscientiousness_1 + Neuroticism_1,
                     data = dat_reg, trace = FALSE)
t5_md <- c(
  "| Comparison Cluster vs. Reference (Pearl Collar) | Estimate | SE | p-value |",
  "| :--- | :---: | :---: | :---: |",
  extract_multinom_md(mod_big5)
)
writeLines(t5_md, "cache/table5_big5_regression.md")

# Table 6: Markov State Transition Probabilities
t6_md <- c(
  "| Origin State (Semester t) | Centered Star (%) | Pearl Collar (%) | Regular Dense (%) | Segmented (%) | Total Transitions |",
  "| :--- | :---: | :---: | :---: | :---: | :---: |"
)
for (st in rownames(trans_prob)) {
  n_trans <- sum(trans_matrix[st, ])
  t6_md <- c(t6_md, sprintf("| %s | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %d |",
                            st, trans_prob[st, "Centered Star"] * 100, trans_prob[st, "Pearl Collar"] * 100,
                            trans_prob[st, "Regular Dense"] * 100, trans_prob[st, "Segmented"] * 100, n_trans))
}
writeLines(t6_md, "cache/table6_markov_transitions.md")

# Table 7: Multilevel Multinomial Logit with Dorm and Major Random Effects
df_full <- df %>%
  left_join(basic_raw %>% select(egoid, reshallyear1, major1rc_1), by = "egoid") %>%
  filter(!is.na(gender_1), gender_1 %in% c("Male", "Female"),
         !is.na(reshallyear1), !is.na(major1rc_1),
         race_1 %in% c("White", "African-American", "Latino/a", "Asian-American", "Foreign Student")) %>%
  mutate(
    cluster = factor(cluster_km, levels = 0:3, labels = c("Pearl Collar", "Segmented", "Centered Star", "Regular Dense")),
    gender = factor(gender_1, levels = c("Female", "Male")),
    foreign = factor(if_else(race_1 == "Foreign Student", "Foreign", "Domestic"), levels = c("Domestic", "Foreign")),
    dorm = factor(reshallyear1),
    major = factor(major1rc_1)
  )

mod_mre <- mblogit(
  cluster ~ gender + foreign + Extraversion_1 + Conscientiousness_1,
  random = list(~ 1|dorm, ~ 1|major),
  data = df_full
)

s_mre <- summary(mod_mre)
c_mre <- s_mre$coefficients
t7_rows <- c()
for (rn in rownames(c_mre)) {
  if (grepl("Intercept", rn)) next
  b <- c_mre[rn, "Estimate"]
  se <- c_mre[rn, "Std. Error"]
  p <- c_mre[rn, "Pr(>|z|)"]
  stars <- if (p < 0.001) "***" else if (p < 0.01) "**" else if (p < 0.05) "*" else ""
  t7_rows <- c(t7_rows, sprintf("| %s | %.2f%s | (%.2f) | %.3f |", rn, b, stars, se, p))
}

vc <- s_mre$VarCov
v_dorm <- mean(diag(vc$dorm))
v_major <- mean(diag(vc$major))

t7_md <- c(
  "| Parameter (vs. Pearl Collar Reference) | Estimate | SE | p-value |",
  "| :--- | :---: | :---: | :---: |",
  t7_rows,
  sprintf("| Random Effect Variance: Residence Hall (Dorm, J = %d) | %.3f | — | — |", n_distinct(df_full$dorm), v_dorm),
  sprintf("| Random Effect Variance: Academic Major (J = %d) | %.3f | — | — |", n_distinct(df_full$major), v_major)
)
writeLines(t7_md, "cache/table7_multilevel_categorical.md")

# ==============================================================================
# 8. SOCIAL SUPPORT & FUNCTIONAL MULTIPLEXITY (TABLE 8 & FIGURE 11)
# ==============================================================================
cat("Generating Table 8 and Figure 11 for Social Support Profiles...\n")

support_alters <- netsurv_raw %>%
  filter(suppadv %in% c("True", "False") | suppcomf %in% c("True", "False") | 
         supphang %in% c("True", "False") | suppfin %in% c("True", "False")) %>%
  mutate(
    adv_num = as.numeric(suppadv %in% c("True", "TRUE", "1")),
    comf_num = as.numeric(suppcomf %in% c("True", "TRUE", "1")),
    hang_num = as.numeric(supphang %in% c("True", "TRUE", "1")),
    fin_num = as.numeric(suppfin %in% c("True", "TRUE", "1")),
    multiplex_score = adv_num + comf_num + hang_num + fin_num,
    is_high_multiplex = as.numeric(multiplex_score >= 3),
    is_especially_close = as.numeric(close == "EspeciallyClose"),
    trust_num = suppressWarnings(as.numeric(trust))
  )

ego_support <- support_alters %>%
  group_by(egoid) %>%
  summarise(
    n_eval = n(),
    pct_advice = mean(adv_num) * 100,
    pct_comfort = mean(comf_num) * 100,
    pct_hang = mean(hang_num) * 100,
    pct_fin = mean(fin_num) * 100,
    mean_multiplex = mean(multiplex_score),
    pct_high_mult = mean(is_high_multiplex) * 100,
    pct_close = mean(is_especially_close, na.rm = TRUE) * 100,
    mean_trust = mean(trust_num, na.rm = TRUE),
    .groups = "drop"
  )

m_support_df <- df %>%
  mutate(typology = cluster_factor) %>%
  inner_join(ego_support, by = "egoid")

# Compute Table 8
vars_to_tab <- c("pct_hang", "pct_advice", "pct_comfort", "pct_fin", "mean_multiplex", "pct_high_mult", "pct_close", "mean_trust")
var_labels <- c(
  "Social Companionship (%)",
  "Informational Advice (%)",
  "Emotional Comfort (%)",
  "Financial Support (%)",
  "Support Multiplexity Index (0-4)",
  "High-Multiplex Alters (≥3 types, %)",
  "Tie Closeness (% Especially Close)",
  "Alter Trust Rating (1-10 scale)"
)

tab_rows <- list()
for (i in seq_along(vars_to_tab)) {
  v <- vars_to_tab[i]
  lbl <- var_labels[i]
  m_all <- mean(m_support_df[[v]], na.rm = TRUE)
  s_all <- sd(m_support_df[[v]], na.rm = TRUE)
  
  by_t <- m_support_df %>%
    group_by(typology) %>%
    summarise(
      m = mean(.data[[v]], na.rm = TRUE),
      s = sd(.data[[v]], na.rm = TRUE),
      .groups = "drop"
    )
  
  fit <- lm(m_support_df[[v]] ~ m_support_df$typology)
  f_val <- summary(fit)$fstatistic[1]
  p_val <- pf(f_val, summary(fit)$fstatistic[2], summary(fit)$fstatistic[3], lower.tail = FALSE)
  p_str <- if (p_val < 0.001) "< 0.001" else sprintf("%.3f", p_val)
  
  is_int <- grepl("Multiplexity|Trust", lbl)
  dec <- if (is_int) "%.2f (%.2f)" else "%.1f%% (%.1f)"
  
  tab_rows[[i]] <- sprintf(
    "| %s | %s | %s | %s | %s | %s | %.2f | %s |",
    lbl,
    sprintf(dec, m_all, s_all),
    sprintf(dec, by_t$m[by_t$typology == "Pearl Collar"], by_t$s[by_t$typology == "Pearl Collar"]),
    sprintf(dec, by_t$m[by_t$typology == "Segmented"], by_t$s[by_t$typology == "Segmented"]),
    sprintf(dec, by_t$m[by_t$typology == "Centered Star"], by_t$s[by_t$typology == "Centered Star"]),
    sprintf(dec, by_t$m[by_t$typology == "Regular Dense"], by_t$s[by_t$typology == "Regular Dense"]),
    f_val,
    p_str
  )
}

t8_md <- c(
  "| **Functional Support Dimension** | **Full Sample (N = 580)** | **Pearl Collar (n = 176)** | **Segmented (n = 242)** | **Centered Star (n = 119)** | **Regular Dense (n = 43)** | **F-Statistic** | **p-value** |",
  "|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|",
  unlist(tab_rows)
)
writeLines(t8_md, "cache/table8_social_support.md")

# Figure 11: Plotting Support Profiles & Gradient
color_typology <- c(
  "Pearl Collar" = "#2b5c8f",
  "Segmented" = "#4575b4",
  "Centered Star" = "#d73027",
  "Regular Dense" = "#d95f02"
)

plot_support_long <- m_support_df %>%
  select(egoid, typology, `Advice` = pct_advice, `Comfort` = pct_comfort, 
         `Financial` = pct_fin, `Companionship` = pct_hang) %>%
  pivot_longer(cols = c(`Advice`, `Comfort`, `Financial`, `Companionship`),
               names_to = "Support_Type", values_to = "Percentage") %>%
  group_by(typology, Support_Type) %>%
  summarise(
    mean_val = mean(Percentage),
    se_val = sd(Percentage) / sqrt(n()),
    .groups = "drop"
  )

plot_support_long$Support_Type <- factor(plot_support_long$Support_Type,
  levels = c("Companionship", "Advice", "Comfort", "Financial")
)

p11_a <- ggplot(plot_support_long, aes(x = Support_Type, y = mean_val, fill = typology)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.75, color = "white", linewidth = 0.3) +
  geom_errorbar(aes(ymin = mean_val - 1.96 * se_val, ymax = mean_val + 1.96 * se_val),
                position = position_dodge(width = 0.8), width = 0.25, linewidth = 0.4, color = "grey30") +
  scale_fill_manual(values = color_typology, name = "Typology:") +
  scale_y_continuous(labels = function(x) paste0(x, "%"), limits = c(0, 100), expand = c(0, 0)) +
  theme_apa() +
  labs(
    title = "Panel A: Functional Social Support Provision Across Typologies",
    subtitle = "Percentage of nominated alters providing specific functional support types (with 95% CI)",
    x = "Functional Support Type",
    y = "Alter Provision Rate (%)"
  )

plot_mult_long <- m_support_df %>%
  select(egoid, typology, `High-Multiplex Alters (≥3 types)` = pct_high_mult, 
         `Especially Close Alters` = pct_close) %>%
  pivot_longer(cols = c(`High-Multiplex Alters (≥3 types)`, `Especially Close Alters`),
               names_to = "Metric", values_to = "Percentage") %>%
  group_by(typology, Metric) %>%
  summarise(
    mean_val = mean(Percentage),
    se_val = sd(Percentage) / sqrt(n()),
    .groups = "drop"
  )

p11_b <- ggplot(plot_mult_long, aes(x = typology, y = mean_val, group = Metric, color = Metric, shape = Metric)) +
  geom_line(linewidth = 0.8, linetype = "solid") +
  geom_point(size = 3.2, fill = "white", stroke = 1.2) +
  geom_errorbar(aes(ymin = mean_val - 1.96 * se_val, ymax = mean_val + 1.96 * se_val),
                width = 0.15, linewidth = 0.4) +
  scale_color_manual(values = c("High-Multiplex Alters (≥3 types)" = "#2b5c8f", 
                                "Especially Close Alters" = "#d95f02"), name = "Relational Bandwidth:") +
  scale_shape_manual(values = c("High-Multiplex Alters (≥3 types)" = 21, 
                                "Especially Close Alters" = 22), name = "Relational Bandwidth:") +
  scale_y_continuous(labels = function(x) paste0(x, "%"), limits = c(40, 90)) +
  theme_apa() +
  labs(
    title = "Panel B: The Structural Gradient of Multiplexity and Tie Closeness",
    subtitle = "Progression of deep tie attachment and multi-functional support across network types",
    x = "Personal Network Typology",
    y = "Cohort Prevalence (%)"
  )

p_fig11 <- (p11_a / p11_b) + plot_layout(heights = c(1, 1))
ggsave("Plots/fig11_social_support_profiles.png", p_fig11, width = 6.5, height = 7.0, dpi = 300)

cat("Completed all figure and table generation!\n")
