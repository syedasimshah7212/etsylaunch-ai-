"""MallOfAmericans Etsy Studio | Run: streamlit run app.py"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid
import zipfile

import streamlit as st
from engine.research import research_ideas, find_competitors, IDEAS
from engine.ai import generate_blueprint, generate_seo
from engine.product import build_product, create_previews, validate_blueprint
from engine.seo import draft_seo, write_seo, clean_tags
from engine.package import make_packages, IMAGE_NAMES, VIDEO_NAMES

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='MallOfAmericans | Etsy Launch Studio',page_icon='🛍️',layout='wide')
st.markdown('''<style>.block-container{max-width:1200px;padding-top:1.6rem}.hero{background:linear-gradient(100deg,#203c43,#335e5d);border-radius:18px;color:white;padding:27px;margin-bottom:13px}.hero h1{margin:0;color:white}.hero p{color:#e6eeee;margin:8px 0 0}.muted{color:#66747a;font-size:0.9rem}</style>''',unsafe_allow_html=True)
st.markdown('''<div class="hero"><h1>🛍️ MallOfAmericans — Etsy AI Launch Studio</h1><p>US digital product research · actual printable & fillable PDFs · 10 true mockups · 2 silent 15-second videos · SEO · tested ZIPs</p></div>''',unsafe_allow_html=True)


def setting(name):
    try:return str(st.secrets.get(name,'')).strip() or str(os.environ.get(name,'')).strip()
    except Exception:return str(os.environ.get(name,'')).strip()

with st.sidebar:
    st.markdown('### 🔐 API settings')
    st.caption('Optional. Keys entered here are session-only and never written to project files.')
    claude_key=st.text_input('Anthropic API key',value=setting('ANTHROPIC_API_KEY'),type='password',help='Required for generating new, custom product blueprint & AI SEO')
    brave_key=st.text_input('Brave Search API key',value=setting('BRAVE_SEARCH_API_KEY'),type='password',help='Required for live public search-result research')
    model=st.text_input('Claude model ID',value='claude-sonnet-4-5',help='Use a model available to your Anthropic account; change if necessary.')
    st.divider()
    st.write('**Store:** [MallOfAmericans](https://www.etsy.com/shop/MallOfAmericans)')
    st.caption('Without search API: discovery ideas remain UNVERIFIED. Without Claude API: only the explicitly labeled built-in sample product is available.')
    st.caption('Hosting: Streamlit Community Cloud or any Python server. GitHub Pages alone cannot execute Python.')

if 'ideas' not in st.session_state:st.session_state.ideas=[]
if 'competitors' not in st.session_state:st.session_state.competitors=[]
if 'generated' not in st.session_state:st.session_state.generated=None

tab1,tab2,tab3,tab4=st.tabs(['1 · US Research','2 · Competitor audit','3 · Product + SEO','4 · Build & Downloads'])
with tab1:
    st.subheader('Discover 10 targeted US digital product niches')
    st.caption('Directional opportunity scoring is NOT proof of sales, exact demand, or low competition. Seller-only analytics cannot be retrieved from search results.')
    left,right=st.columns([1,2])
    with left:
        if st.button('🔎 Run opportunity research',use_container_width=True):
            with st.spinner('Checking public search results (or preparing unverified ideas)...'):
                try:st.session_state.ideas=research_ideas(brave_key,max_calls=10)
                except Exception as exc:st.error(f'Public search temporarily unavailable: {type(exc).__name__}: {exc}')
    with right:
        st.info('Select the product you want to build. For niches other than the built-in demonstration template, provide your own Anthropic API key so content can be custom-designed.')
    if st.session_state.ideas:
        rows=[]
        for r in st.session_state.ideas:
            rows.append({'Opportunity':r['name'],'Buyer':r['buyer'],'Directional score / 5':r['weighted_score'],
                         'Public listing links':len(r['sources']),'Evidence':r['evidence_status']})
        st.dataframe(rows,use_container_width=True,hide_index=True)
        st.caption('Scores use transparent subjective priors plus search-result coverage, not Etsy sales/volume. Competitor gaps need manual evaluation.')
    selected=st.selectbox('Product opportunity to develop',[i[0] for i in IDEAS],key='product_selected')
    buyer=next((i[2] for i in IDEAS if i[0]==selected),'US customers')
    st.text_input('Target customer',value=buyer,key='buyer_selected')

with tab2:
    st.subheader('Five-source, transparent competitor audit')
    keyword=next((x[1] for x in IDEAS if x[0]==st.session_state.product_selected),st.session_state.product_selected)
    q=st.text_input('Research keyword',value=keyword)
    urls=st.text_area('Optional: competitor Etsy listing URLs (one per line)',placeholder='https://www.etsy.com/listing/...\nhttps://www.etsy.com/listing/...',height=110)
    if st.button('🧾 Find up to 5 public competitors'):
        try:st.session_state.competitors=find_competitors(q,brave_key,manual_urls=[u.strip() for u in urls.splitlines() if u.strip()])
        except Exception as exc:st.error(str(exc))
    competitors=st.session_state.competitors
    if competitors:
        st.write('Public snippets are limited. You can manually add price and description observations from the linked live pages.')
        editable=[{'Public search title':c.get('title',''), 'Listing URL':c.get('url',''),
                  'Price observed by seller':c.get('user_observed_price',''),
                  'Description themes / public keywords (seller notes)':c.get('seller_description_notes','')}
                 for c in competitors]
        enriched=st.data_editor(editable,use_container_width=True,hide_index=True,num_rows='fixed',key='competitor_notes_editor',
               disabled=['Listing URL'])
        if st.button('💾 Save competitor observations'):
            for original,updated in zip(st.session_state.competitors,enriched):
                original['user_observed_price']=str(updated.get('Price observed by seller',''))
                original['seller_description_notes']=str(updated.get('Description themes / public keywords (seller notes)',''))
                original['seller_notes_provenance']='User-supplied observations (not independently verified by app)'
            st.success('Saved competitor notes for the SEO and research report.')
        for idx,c in enumerate(st.session_state.competitors,1):
            st.caption(f"{idx}. {c.get('snippet','')} | Source: {c['source_type']} | Checked: {c['checked']}")
        st.caption('Only actually observed words are attributed. User-added price/description information is labeled seller-supplied; private tags, precise sales and revenue remain unknown.')
    else:
        st.warning('No verified competitor listing data in this session. Add listing URLs or a Brave key. The tool will never invent five competitors.')

with tab3:
    st.subheader('Original buyer-ready PDF + Etsy listing text')
    st.write(f"**Selected:** {st.session_state.product_selected}")
    sample=(st.session_state.product_selected=='Multi-Pet Sitter Handoff Kit')
    mode=st.radio('Content creation mode',["Use built-in original sample" if sample else 'Build custom product with Claude API','Build custom product with Claude API'] if sample else ['Build custom product with Claude API'],horizontal=True)
    price=st.number_input('Suggested asking price (USD)',min_value=6.01,value=12.95,step=1.00,format='%.2f')
    if st.button('✨ Prepare product blueprint and SEO'):
        try:
            if mode.startswith('Use built-in'):
                bp=json.loads((ROOT/'templates/pet_sitter.json').read_text(encoding='utf-8'))
            else:
                if not claude_key:raise ValueError('Provide ANTHROPIC_API_KEY to design a new custom product.')
                with st.spinner('Claude is designing original product pages...'):
                    bp=generate_blueprint(claude_key,st.session_state.product_selected,st.session_state.buyer_selected,competitors)
            validate_blueprint(bp)
            if claude_key:
                with st.spinner('Claude is drafting 13 tags and complete listing copy...'):
                    seo=generate_seo(claude_key,bp,competitors)
            else:seo=draft_seo(bp,price)
            seo['price_usd']=float(price)
            clean_tags(seo['tags'])
            st.session_state.blueprint=bp;st.session_state.seo=seo
            st.success(f"Blueprint prepared: {len(bp['pages'])} useful printable pages | exactly 13 SEO tags")
        except Exception as exc:st.error(f'Could not prepare: {type(exc).__name__}: {exc}')
    if st.session_state.get('blueprint'):
        bp=st.session_state.blueprint
        st.markdown(f"**Product:** {bp['name']} — {len(bp['pages'])} pages")
        st.dataframe([{'Page':i+1,'Page title':p['title'],'Sections':len(p['sections'])} for i,p in enumerate(bp['pages'])],hide_index=True,use_container_width=True)
        st.markdown('**SEO title:** '+st.session_state.seo['title'])
        st.code(', '.join(st.session_state.seo['tags']),language=None)
        with st.expander('Preview the customer-facing description'):
            st.text(st.session_state.seo['description'])
        st.download_button('Download blueprint JSON',json.dumps(bp,indent=2).encode(),file_name='product_blueprint.json',mime='application/json')
        st.download_button('Download SEO JSON',json.dumps(st.session_state.seo,indent=2).encode(),file_name='etsy_seo.json',mime='application/json')

with tab4:
    st.subheader('Create actual files: PDF → page previews → 10 JPGs → 2 MP4s → ZIP')
    st.write('The renderer only uses **screenshots of the actual completed product**. It will not show fictional pages, fake customer reviews or fabricated sales.')
    st.caption('Media rendering requires ffmpeg/ffprobe. 10 full-resolution JPEGs and two HD videos take time and server CPU; check Streamlit Cloud resource limits.')
    enable_video=st.checkbox('Render both silent 15-second MP4s (requires ffmpeg)',value=True)
    if st.button('🚀 Generate complete launch package',type='primary',disabled=not bool(st.session_state.get('blueprint'))):
        bp=st.session_state.blueprint;seo=st.session_state.seo
        slug=re.sub(r'[^A-Za-z0-9]+','_',bp['name']).strip('_')[:52]
        path=Path(tempfile.gettempdir())/'moa_etsy_outputs'/f'{slug}_{uuid.uuid4().hex[:8]}'
        path.mkdir(parents=True,exist_ok=True)
        project=path/f'Etsy_Launch_{slug}';project.mkdir()
        try:
            with st.status('Creating assets...',expanded=True) as status:
                st.write('Step 1 / 5 — Building real printable and fillable PDF product...')
                meta=build_product(bp,project/'02_Buyer_Downloads')
                previews=create_previews(project/'02_Buyer_Downloads'/meta['files'][0],project/'_previews',max_pages=10)
                st.write(f"Created {meta['pages']} US Letter pages with {meta['fillable_fields']} fillable fields.")
                st.write('Step 2 / 5 — Writing final SEO and report...')
                write_seo(seo,project/'05_SEO')
                research={'opportunities':st.session_state.ideas,'competitors':competitors,
                          'note':'Unverified demand/competitive gaps must not be represented as confirmed.'}
                if not competitors:st.warning('No competitor data: seller report explicitly labels this research gap.')
                st.write('Step 3 / 5 — Rendering ten 2400×1800 JPG mockups from real pages...')
                labels=[
                    [bp['name'],f'{meta["pages"]} real pages to organize your routines'],
                    ['What is included',f'{meta["pages"]}-page printable & fillable PDFs'],
                    ['Less confusion, more clarity',bp.get('benefits',['Organize the next step'])[0]],
                    ['See the real pages','Actual content from your download'],
                    ['Prepare. Use. Repeat.','Clear sections you can complete'],
                    ['Print or type','US Letter | fillable & printable PDFs'],
                    ['Designed for real life',bp.get('benefits',['Useful details'])[1 if len(bp.get('benefits',[]))>1 else 0]],
                    ['A better handoff','Organize what matters to you'],
                    ['One useful toolkit',f'{meta["pages"]} original pages, two PDF formats'],
                    ['Instant digital download','No physical product is shipped'],
                ]
                labels_path=path/'labels.json';labels_path.write_text(json.dumps(labels),encoding='utf-8')
                args=[sys.executable,str(ROOT/'scripts/asset_factory.py'),
                      '--preview-dir',str(project/'_previews'),'--output-dir',str(project),'--title',bp['name'],
                      '--subtitle',bp.get('subtitle','A practical printable and fillable kit'),
                      '--features','|'.join(bp.get('benefits',[])[:3]),'--labels-json',str(labels_path)]
                if not enable_video:
                    # Current factory generates videos as part of one call; videos are mandatory for full completion.
                    # To support manual mode, the script has --skip-videos CLI flag.
                    args.append('--skip-videos')
                output=subprocess.run(args,capture_output=True,text=True,timeout=1100)
                if output.returncode!=0:raise RuntimeError('Media renderer failed: '+(output.stderr or output.stdout)[-3000:])
                st.write('Step 4 / 5 — Inspecting dimensions, PDF and MP4 durations...')
                qa,buyer,seller=make_packages(project,path,meta,research)
                if qa['complete']:status.update(label='Complete: all requested assets verified',state='complete')
                else:status.update(label='Partial: one or more assets missing/failed checks',state='error')
                st.write('Step 5 / 5 — Two downloadable ZIP packages created.')
            st.session_state.generated={'project':str(project),'qa':qa,'buyer':str(buyer),'seller':str(seller),'meta':meta}
        except Exception as exc:
            st.error(f'Launch generation failed: {type(exc).__name__}: {exc}')
            st.write('No success is claimed until all required files pass QA. You can inspect server logs and retry with ffmpeg installed.')
    g=st.session_state.generated
    if g:
        if g['qa']['complete']:st.success('✅ Complete launch package: 10 JPGs + 2 validated 15-second MP4s + buyer PDFs.')
        else:st.warning('⚠ Partial launch package; check manifest before selling.')
        c1,c2=st.columns(2)
        for col,key,filename in [(c1,'seller','Full_Seller_Launch.zip'),(c2,'buyer','Buyer_Download.zip')]:
            with col:
                f=Path(g[key]);st.download_button(f'⬇️ Download {"seller" if key=="seller" else "buyer"} ZIP',f.read_bytes(),file_name=filename,mime='application/zip',use_container_width=True)
        st.dataframe(g['qa']['files'],use_container_width=True,hide_index=True)
        p=Path(g['project']);pics=sorted((p/'03_Etsy_Mockups').glob('*.jpg'))
        if pics:
            st.subheader('Actual preview of finished images');st.image(str(pics[0]),caption='01_hero.jpg',use_container_width=True)
        for fn in VIDEO_NAMES:
            video=p/'04_Etsy_Videos'/fn
            if video.is_file():
                with st.expander(f'Watch {fn}'):
                    st.video(video.read_bytes())

st.divider()
st.caption('Tool does not publish to Etsy or scrape blocked/private Etsy data. Verify up-to-date policies and preview files before listing. All digital products must be original and comply with applicable Etsy rules. Not a guarantee of sales or search rank.')
