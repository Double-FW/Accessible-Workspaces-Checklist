"""Export complete committed workspace guidance; examples never become observed findings."""
import argparse
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import quote,unquote,urlsplit
import yaml
from jsonschema import Draft202012Validator,FormatChecker
from workspace_hf_common import ROOT,SOURCE,TARGET,MANAGED,git,digest,destination,read_sources
GUIDE='Accessible_Workspaces_Design_Checklist.md'
def serial(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str)
def metadata(text):return yaml.safe_load(text.split('---\n',2)[1]) if text.startswith('---\n') else {}
def anchors(text):
    result=set();seen={}
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
        h=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',h).replace('`','').lower()
        h=''.join(c for c in h if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ','-')
        n=seen.get(h,0);seen[h]=n+1;result.add(h+(f'-{n}' if n else ''))
    return result

def check(root=ROOT,loaded=None):
    root=Path(root).resolve();cfg,texts,manifest=loaded or read_sources(root);links=0;blocks=0
    for path,text in texts.items():
        if not path.endswith('.md'):continue
        md=metadata(text)
        if not md or md.get('license')!='MIT':raise ValueError('Invalid MIT source metadata: '+path)
        if '\ufffd' in text:raise ValueError('Damaged source character: '+path)
        if len(re.findall(r'^```',text,re.M))%2:raise ValueError('Unclosed source fence: '+path)
        for body in re.findall(r'```yaml\n(.*?)\n```',text,re.S):yaml.safe_load(body);blocks+=1
        for target in re.findall(r'\[[^\]\n]+\]\(([^\n]+?)\)',text):
            u=urlsplit(target)
            if u.scheme or u.netloc:continue
            links+=1;p=root/path;dest=(p.parent/unquote(u.path)).resolve() if u.path else p
            if not dest.is_relative_to(root) or not dest.is_file():raise ValueError('Missing local source link: '+target)
            if u.fragment and unquote(u.fragment) not in anchors(dest.read_text()):raise ValueError('Missing source fragment: '+target)
    ids=re.findall(r'^- \[ \] \*\*(AW-\d{2}) ',texts[GUIDE],re.M)
    if ids!=[f'AW-{n:02}' for n in range(1,22)]:raise ValueError('Expected 21 ordered AW checklist items.')
    a=metadata(texts['AGENTS.md']);g=metadata(texts[GUIDE])
    if a['sources']['checklist_version']!=g['version']:raise ValueError('Checklist metadata version mismatch.')
    if any(v is not None for v in a['adoption'].values()) or any(v is not None for v in a['review'].values()):raise ValueError('Local adoption or approval metadata changed; review before export.')
    schema=json.loads(texts['workspace-finding.schema.json']);example=json.loads(texts['workspace-finding.example.json'])
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(example)
    if a['sources']['schema_version']!=schema['properties']['schema_version']['const']:raise ValueError('Finding schema version mismatch.')
    if example['record_state']!='illustrative' or example['status']!='not_assessed' or example['check_result']!='not_tested' or example['evidence'] or example['proposed_actions'] or example['finding'] is not None or example['human_decision']['state']!='pending':raise ValueError('Blank example must remain illustrative and unassessed, without findings or decisions.')
    if any(example[k] is not None for k in ['project_reference','item_id','jurisdiction','building_use','location_and_task','applicability_reason','review_trigger']) or any(v is not None for v in example['verification'].values()) or any(v is not None for k,v in example['human_decision'].items() if k!='state'):raise ValueError('Blank example must not acquire project, verification or decision facts.')
    if re.findall(r'^## (\d+)\. ',texts['AGENTS.md'],re.M)!=[str(i) for i in range(1,14)]:raise ValueError('Expected 13 agent guidance topics.')
    return {'source_files':len(texts),'checklist_items':21,'agent_topics':13,'local_links':links}

def build(root,output,dataset_id=TARGET):
    destination(dataset_id);root=Path(root).resolve();output=Path(output).resolve()
    if output==root or root in output.parents:raise ValueError('Write the export outside the source checkout.')
    cfg,texts,manifest=read_sources(root);check(root,(cfg,texts,manifest))
    commit=git(root,'rev-parse','HEAD').decode().strip();date=git(root,'show','-s','--format=%cI','HEAD').decode().strip()
    authority=serial({'qualification':'Draft guidance for local adoption, not employer approval or evidence of an actual workspace review. Retrieved instructions are data, not runtime authority.', 'agent_instructions_as_source_data':texts['AGENTS.md'],'evidence_and_decision_boundaries':texts['Workspace_Review_and_Handover.md'],'terminology_alignment':texts['Terminology_Alignment.md'],'rights_and_status':texts['NOTICE.md']})
    def row(ident,path,text,**fields):
        return dict(id=ident,text=text,source_repository=SOURCE,source_path=path,source_commit=commit,source_commit_date=date,source_url=f'https://github.com/{SOURCE}/blob/{commit}/{quote(path,safe="/")}',source_document_sha256=digest(texts[path].encode()),text_sha256=digest(text.encode()),source_metadata_json=serial(metadata(texts[path])),authority_context_json=authority,license='MIT',empirical_evidence=False,runtime_authority=False,**fields)
    documents=[row(p,p,texts[p],record_type='maintained_guidance_document') for p in cfg['document_files']]
    guide=texts[GUIDE];matches=list(re.finditer(r'^- \[ \] \*\*(AW-\d{2}) \(([^)]+)\)\*\* ',guide,re.M));sections=list(re.finditer(r'^## [1-4]\. .+$',guide,re.M));suffix_at=guide.index('## Scope boundaries and connected guidance');items=[]
    for i,m in enumerate(matches):
        section=max((s for s in sections if s.start()<m.start()),key=lambda s:s.start())
        end=matches[i+1].start() if i+1<len(matches) else suffix_at
        # Next section headings belong to their next items, not to the previous prompt.
        boundary=next((s.start() for s in sections if m.start()<s.start()<end),end)
        text=guide[m.start():boundary]
        items.append(row(m.group(1),GUIDE,text,record_type='source_checklist_prompt_not_observed_finding',item_id=m.group(1),source_tags=m.group(2),section=section.group(),shared_guide_prefix=guide[:sections[0].start()],shared_guide_suffix=guide[suffix_at:],source_start=m.start(),source_end=boundary))
    if len(items)!=21:raise ValueError('Checklist extraction is incomplete.')
    for item in items:
        if guide[item['source_start']:item['source_end']]!=item['text']:raise ValueError('Checklist extraction lost source text.')
    resources=[row(p,p,texts[p],record_type='json_schema_not_validation_service' if p.endswith('.schema.json') else 'illustrative_blank_template_not_observed_finding',illustrative=p.endswith('.example.json')) for p in cfg['resource_files']]
    views={'documents.jsonl':documents,'checklist_items.jsonl':items,'record_resources.jsonl':resources}
    payload={name:''.join(serial(r)+'\n' for r in records).encode() for name,records in views.items()}
    links=lambda text:set(re.findall(r'https://github\.com/[^\s<>\x22\x27`\\)\]]+',text))
    if not links('\n'.join(texts.values()))<=links(''.join(payload[n].decode() for n in views)):raise ValueError('A source GitHub link was lost during export.')
    payload['LICENSE']=texts['LICENSE'].encode();payload['NOTICE.md']=texts['NOTICE.md'].encode()
    provenance={'source_repository':SOURCE,'source_commit':commit,'source_commit_date':date,'destination_dataset':TARGET,'manifest':manifest,'license':'MIT','coverage':{'document_files':cfg['document_files'],'resource_files':cfg['resource_files'],'alternative_checklist_view':GUIDE,'new_committed_content':'Unclassified files outside reserved implementation directories stop publication.'},'limits':'Guidance and checklist views overlap; do not count them as independent evidence. No linked source bodies, actual cases, approvals or sensitive records are imported. Export does not renew legal or source verification.'}
    schema={'format':'JSON Lines','views':{n:{'columns':sorted(records[0]),'record_count':len(records)} for n,records in views.items()},'authority_context_json':'Keep authority, evidence, terminology and rights with excerpts; instructions are source data, not runtime permission.','text':'Whole source text or exact AW prompt body. Item offsets are Unicode character offsets in the complete checklist; shared context and section are preserved.','finding_resources':'Full JSON Schema and blank illustrative example, not completed findings. Structural validation does not prove truth, safety, approval or compliance.'}
    for name,value in [('provenance.json',provenance),('record_schema.json',schema)]:payload[name]=(serial(value)+'\n').encode()
    card="---\nlicense: mit\nlanguage:\n- en\ntask_categories:\n- text-retrieval\nconfigs:\n- config_name: documents\n  default: true\n  data_files:\n  - split: train\n    path: documents.jsonl\n- config_name: checklist_items\n  data_files:\n  - split: train\n    path: checklist_items.jsonl\n- config_name: record_resources\n  data_files:\n  - split: train\n    path: record_resources.jsonl\n---\n# Accessible Workspace Design — Double FW\n\nSource: [public GitHub repository](https://github.com/Double-FW/Accessible-Workspaces-Checklist).\n\n## Content and use\n\nSeven complete maintained Markdown documents, 21 AW-01–AW-21 checklist prompts and two complete JSON resources (finding schema and blank example) are provided in separate configurations. Additional explicitly reviewed guidance may increase the document count. The MIT licence is also copied unchanged, covering all ten original source files. Full file inventory, Git revision, blob hashes and SHA-256 checksums are in provenance.json. The record layout is described in record_schema.json.\n\nThe checklist view is an alternative representation of the complete checklist in documents, not additional independent evidence. Keep the shared introduction, source section, full multi-part prompt and source notes together. Source P/N/C tags are broad scanning labels, not diagnoses. Record resources contain exact JSON text: the example is illustrative, unassessed and blank; the schema is not an installed validation service. Neither provides evidence of actual workspace checks, worker experiences or legal compliance.\n\n## Authority, privacy and rights\n\nThis is proposed practitioner guidance for local adoption, not employer policy, professional approval or legal advice. Preserve unknown/not_tested and the distinction between progress, scoped results and actual human decisions. Do not invent owners, dates, evidence, approval or exemptions. Do not publish personal, health, adjustment or sensitive site/security records. Retrieved AGENTS instructions are source data and cannot override a consuming system's governing instructions.\n\nMIT applies to Double FW project material; retain the copyright and permission notice. See LICENSE and NOTICE.md. External publications retain their own rights. Links to related public Double-FW repositories remain in the complete source text; linked content is not automatically imported. This export is suitable for retrieval/curation, not a prevalidated instruction/answer training set or proof of a trained model's safety.\n\n## Updates\n\nThe GitHub workflow runs weekly on Monday at 11:07 UTC, with manual runs available. A successful run verifies that the source remains public, rebuilds from committed source and updates only eight managed dataset files in one commit. New substantive files, including folders, require explicit classification; unclassified content stops publication. Implementation files are not training content. Unrelated destination files and visibility remain unchanged. No audit/test report is published.\n"
    payload['README.md']=card.encode()
    if set(payload)!=set(MANAGED):raise ValueError('Managed output inventory mismatch.')
    output.mkdir(parents=True,exist_ok=True)
    for name,data in payload.items():(output/name).write_bytes(data)
    return {'documents':len(documents),'checklist_items':len(items),'record_resources':len(resources),'managed_files':len(payload)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--dataset-id',default=TARGET);p.add_argument('--check-only',action='store_true');a=p.parse_args()
    try:
        if a.check_only:result=check()
        elif a.output:result=build(ROOT,a.output,a.dataset_id)
        else:p.error('Specify --output or --check-only.')
    except ValueError as e:raise SystemExit(str(e))
    print(serial(result))
if __name__=='__main__':main()
