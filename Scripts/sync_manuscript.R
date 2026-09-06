#!/usr/bin/env Rscript
# Scripts/sync_manuscript.R
# Master R driver for Google Drive manuscript synchronization
# Adheres strictly to AGENTS.md Turnkey Setup and Intermediate File Cleanup standards

suppressPackageStartupMessages({
  library(googledrive)
})

# 1. Configuration: Note document ID from Google Doc URL
doc_id <- "1vtRoaJQ1FTEfpEj-PVMBFuBoxN0cCWt8VNuAfiTm304"
live_docx <- "draft_live.docx"
updated_docx <- "draft_updated.docx"

# Automated cleanup handler (AGENTS.md Section 6)
on.exit({
  unlink(Sys.glob("draft_*.docx"))
  unlink(Sys.glob("draft_*.txt"))
  unlink(Sys.glob("*.tmp"))
  unlink("replacements.json")
}, add = TRUE)

message("[1/4] Ensuring table summaries and publication figures are up to date...")
if (file.exists("Scripts/generate_plots_and_tables.R")) {
  source("Scripts/generate_plots_and_tables.R")
}

message("[2/4] Downloading live manuscript from Google Drive (preserving all author formatting)...")
drive_auth(email = "omarlizardo@gmail.com")
drive_download(as_id(doc_id), path = live_docx, overwrite = TRUE)

message("[3/4] Performing in-place XML injection of tables and figures...")
exit_code <- system2("python3", args = c("Scripts/sync_manuscript.py", live_docx, updated_docx))
if (exit_code != 0) {
  stop("Error during in-place XML injection.")
}

message("  Formatting manuscript typography and layout...")
system2("python3", args = c("Scripts/format_manuscript.py", updated_docx, updated_docx))

# Update local markdown mirror from the updated docx
system2("pandoc", args = c("-f", "docx", "-t", "gfm", "--wrap=none", updated_docx, "-o", "draft_manuscript.md"))

message("[4/4] Uploading updated manuscript back to Google Drive...")
drive_update(as_id(doc_id), media = updated_docx)

message("Synchronization complete! Google Doc updated successfully.")
message("Google Doc URL: https://docs.google.com/document/d/", doc_id)
