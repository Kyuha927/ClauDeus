---
description: Run all prompts in prompts/ folder natively through Antigravity agent
---

// turbo-all

1. List files in `prompts/` directory.
   ```powershell
   ls prompts/*.md
   ```
2. For each file, read it using `view_file`.
3. Process the content of each file according to its specified model header.
4. Write the results to `.logs/[filename].log` and update `RESULTS_SUMMARY.md`.
5. Notify user with a summary of completion.
