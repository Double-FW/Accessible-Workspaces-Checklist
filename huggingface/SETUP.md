# Accessible Workspace Design — weekly publishing

Source: [Double-FW/Accessible-Workspaces-Checklist](https://github.com/Double-FW/Accessible-Workspaces-Checklist). Destination: [GarethFW/Accessible_Workspace_Design](https://huggingface.co/datasets/GarethFW/Accessible_Workspace_Design).

## First setup

1. At [Hugging Face access tokens](https://huggingface.co/settings/tokens), create a fine-grained token (Custom if presets are shown), select only `GarethFW/Accessible_Workspace_Design` under repository permissions and enable **Write contents/settings of selected repos**. Read/access-request permissions may be selected automatically. Leave unrelated user/org permissions off. Copy the generated token privately; never put it in a file, chat or ordinary variable.
2. Open [GitHub Actions repository secrets](https://github.com/Double-FW/Accessible-Workspaces-Checklist/settings/secrets/actions). Choose **New repository secret**, name it `HF_TOKEN` (underscore), paste the token in Secret and save. If it exists, update its value.
3. The destination is already built into the workflow. No variable is required. If an existing `HF_DATASET_ID` variable is present at [Actions variables](https://github.com/Double-FW/Accessible-Workspaces-Checklist/settings/variables/actions), its value must be exactly `GarethFW/Accessible_Workspace_Design`, without a URL or trailing slash. This is a public name, never the token.
4. Open [the sync workflow](https://github.com/Double-FW/Accessible-Workspaces-Checklist/actions/workflows/huggingface-sync.yml), choose **Run workflow**, keep the default branch selected and click the green **Run workflow** button. Wait for completion and open the newest run. Green success is required; a configured secret alone does not mean an upload happened.
5. Review [dataset files](https://huggingface.co/datasets/GarethFW/Accessible_Workspace_Design/tree/main). The managed files are README.md, LICENSE, NOTICE.md, documents.jsonl, checklist_items.jsonl, record_resources.jsonl, provenance.json and record_schema.json. Compare provenance source_commit with the successful workflow's commit. `.gitattributes` is expected and remains untouched.

## Coverage and boundaries

The explicit [inventory](export-config.json) covers all ten original content files: seven Markdown documents, the finding schema, blank example and licence. The schema and example are retained as complete text in record_resources.jsonl, not as observed findings. The whole checklist is in documents.jsonl; 21 full AW prompts with shared context are a separate overlapping retrieval view. Do not train as if the two views are independent evidence. Implementation code, configuration, setup instructions and regression tests are not training content.

Folder nesting does not prevent inclusion. Add reviewed new substantive paths to source_files and document_files in the inventory; any unclassified committed content outside `.github/`, `scripts/`, `tests/` and `huggingface/` stops publication. JSON record resources have fixed roles. New sensitive or real case records must not be added to this public source or dataset. Linked external bodies are never automatically downloaded.

Runs are weekly Monday at **11:07 UTC** (11:07 UK winter / 12:07 UK summer). GitHub schedules can be delayed. Manual runs are available. The publisher verifies public source visibility, rebuilds against committed bytes, checks the fixed destination and updates only changed managed files atomically using the destination's parent revision. Concurrent destination edits cause failure rather than a blind overwrite; inspect and rerun. Unrelated dataset files and visibility are preserved. Rotate/revoke tokens in Hugging Face and replace the GitHub secret if credentials are lost or compromised.

## Local maintenance

Use Python 3.12 and install `python -m pip install -r huggingface/requirements.txt`. After committing source edits, run `python scripts/export_huggingface.py --check-only`, `python -m unittest discover -s tests -v` and `python scripts/export_huggingface.py --output /tmp/workspace-dataset-preview`. Output must be outside the source checkout. No audit or test report is committed or published. Structural validation with date checking does not establish truth, site safety, legal compliance or actual human approval.
