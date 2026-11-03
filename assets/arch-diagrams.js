(function(){
'use strict';
var LAYER_COLORS={
  authority:'#495057',orchestrator:'#2f9e44',worker:'#2f9e44',checker:'#e8590c',
  roles:'#7048e8',ops:'#1c7ed6',id:'#c2255c'
};
function qs(sel,root){return (root||document).querySelector(sel)}
function qsa(sel,root){return [].slice.call((root||document).querySelectorAll(sel))}
function el(tag,attrs,kids){
  var n=document.createElement(tag);
  if(attrs)Object.keys(attrs).forEach(function(k){
    if(k==='text')n.textContent=attrs[k];
    else if(k==='html')n.innerHTML=attrs[k];
    else if(k==='className')n.className=attrs[k];
    else n.setAttribute(k,attrs[k]);
  });
  (kids||[]).forEach(function(c){if(c)n.appendChild(c)});
  return n;
}
function svgEl(tag,attrs){
  var n=document.createElementNS('http://www.w3.org/2000/svg',tag);
  if(attrs)Object.keys(attrs).forEach(function(k){n.setAttribute(k,attrs[k])});
  return n;
}
function dataUrl(){
  var base=document.documentElement.getAttribute('data-asset-base')||'';
  return base+'data/architecture.json';
}

function buildHierarchy(host, data){
  var wrap=el('div',{className:'arch-canvas'});
  var tip=el('div',{className:'arch-tooltip',role:'tooltip','aria-hidden':'true'});
  var expand=el('div',{className:'arch-expand',hidden:'hidden','aria-live':'polite'});
  var W=900,H=420;
  var svg=svgEl('svg',{class:'arch-svg',viewBox:'0 0 '+W+' '+H,role:'img','aria-label':data.title});
  var defs=svgEl('defs');
  var marker=svgEl('marker',{id:'arch-arrow',viewBox:'0 0 10 10',refX:'9',refY:'5',markerWidth:'7',markerHeight:'7',orient:'auto'});
  marker.appendChild(svgEl('path',{d:'M0,0L10,5L0,10z',fill:'#868e96'}));
  defs.appendChild(marker);svg.appendChild(defs);

  var layout={
    gem:[380,16,140,48],
    explorer:[370,90,160,56],
    emissary:[40,90,150,56],engineer:[200,90,150,56],
    imitator:[690,90,170,56],
    safeguard:[40,220,160,56],scrutineer:[220,220,160,56],
    architect:[400,220,150,56],archivist:[570,220,150,56],
    investigator:[690,220,170,56],
    mender:[200,330,200,48],arbiter:[450,330,200,48],inferer:[690,330,170,48]
  };
  var byId={};(data.nodes||[]).forEach(function(n){byId[n.id]=n});
  (data.edges||[]).forEach(function(e){
    var a=layout[e.from],b=layout[e.to];if(!a||!b)return;
    var x1=a[0]+a[2]/2,y1=a[1]+a[3],x2=b[0]+b[2]/2,y2=b[1];
    if(y2<y1){y1=a[1];y2=b[1]+b[3]}
    var path=svgEl('path',{class:'arch-edge',d:'M'+x1+' '+y1+' L'+x2+' '+y2});
    svg.appendChild(path);
  });
  Object.keys(layout).forEach(function(id){
    var n=byId[id];if(!n)return;
    var box=layout[id],g=svgEl('g',{class:'arch-node',tabindex:'0',role:'button','aria-label':n.label+', '+n.role,'data-id':id});
    var color=LAYER_COLORS[n.layer]||'#495057';
    var rect=svgEl('rect',{x:box[0],y:box[1],width:box[2],height:box[3],rx:'12',fill:color});
    var t1=svgEl('text',{x:box[0]+box[2]/2,y:box[1]+22,'text-anchor':'middle'});t1.textContent=n.label;
    var t2=svgEl('text',{x:box[0]+box[2]/2,y:box[1]+40,'text-anchor':'middle',class:'sub'});t2.textContent=n.role;
    g.appendChild(rect);g.appendChild(t1);g.appendChild(t2);
    function open(){
      qsa('.arch-node',svg).forEach(function(x){x.removeAttribute('data-expanded')});
      g.setAttribute('data-expanded','true');
      tip.innerHTML='<strong>'+n.label+'</strong>'+(n.tooltip||n.role);
      tip.setAttribute('data-open','true');tip.setAttribute('aria-hidden','false');
      tip.style.left=Math.min(box[0]+20, wrap.clientWidth-200)+'px';
      tip.style.top=(box[1]+box[3]+8)+'px';
      expand.hidden=false;
      expand.innerHTML='<strong>'+n.label+'</strong> · '+(n.group||n.layer)+'<p>'+(n.tooltip||'')+'</p>'+
        (n.children&&n.children.length?'<p class="muted">Expands to: '+n.children.map(function(c){return (byId[c]||{}).label||c}).join(', ')+'</p>':'');
    }
    g.addEventListener('click',open);
    g.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();open()}});
    g.addEventListener('mouseenter',function(){
      tip.innerHTML='<strong>'+n.label+'</strong>'+(n.tooltip||'');
      tip.setAttribute('data-open','true');
      tip.style.left=Math.min(box[0]+20, wrap.clientWidth-200)+'px';
      tip.style.top=(box[1]+box[3]+8)+'px';
    });
    g.addEventListener('mouseleave',function(){if(g.getAttribute('data-expanded')!=='true'){tip.removeAttribute('data-open')}});
    svg.appendChild(g);
  });
  wrap.appendChild(svg);wrap.appendChild(tip);
  host.appendChild(el('p',{className:'arch-blurb',text:data.blurb}));
  host.appendChild(wrap);host.appendChild(expand);
  var legend=el('div',{className:'arch-legend'});
  [['authority','Authority'],['orchestrator','Orchestrator / Work'],['checker','Checks'],['roles','Roles'],['ops','Ops'],['id','ID']].forEach(function(pair){
    legend.appendChild(el('span',null,[
      el('i',{className:'arch-swatch',style:'background:'+LAYER_COLORS[pair[0]]}),
      document.createTextNode(pair[1])
    ]));
  });
  host.appendChild(legend);
}

function buildBots(host, data){
  host.appendChild(el('p',{className:'arch-blurb',text:data.blurb}));
  var list=el('div',{className:'arch-group-list'});
  (data.groups||[]).forEach(function(g){
    var box=el('div',{className:'arch-group'});
    var btn=el('button',{type:'button','aria-expanded':'false',html:
      '<span><span class="arch-swatch" style="background:'+g.color+';margin-right:.4rem"></span>'+g.label+' · '+(g.bots||[]).length+' bots</span><span aria-hidden="true">+</span>'});
    var bots=el('div',{className:'bots'});
    (g.bots||[]).forEach(function(b){
      var card=el('div',{className:'arch-bot',tabindex:'0',role:'button','aria-label':b.name});
      card.appendChild(el('span',{className:'phase',text:b.phase}));
      card.appendChild(el('span',{className:'name',text:b.name}));
      card.appendChild(el('span',{className:'duty',text:b.duty}));
      card.title=b.duty;
      bots.appendChild(card);
    });
    btn.addEventListener('click',function(){
      var open=box.getAttribute('data-open')==='true';
      box.setAttribute('data-open', open?'false':'true');
      btn.setAttribute('aria-expanded', open?'false':'true');
      btn.querySelector('span[aria-hidden]').textContent=open?'+':'−';
    });
    box.appendChild(btn);box.appendChild(bots);list.appendChild(box);
  });
  host.appendChild(list);
}

function buildGovernance(host, data){
  host.appendChild(el('p',{className:'arch-blurb',text:data.blurb}));
  var flow=el('div',{className:'arch-flow',role:'list'});
  (data.steps||[]).forEach(function(s,i){
    var btn=el('button',{className:'arch-step',type:'button',role:'listitem','aria-expanded':'false'});
    btn.appendChild(el('span',{className:'n',text:'Step '+(i+1)}));
    btn.appendChild(el('span',{className:'l',text:s.label}));
    var d=el('span',{className:'d'});
    d.textContent=s.detail+(s.source?' · Source: '+s.source:'');
    btn.appendChild(d);
    btn.title=s.detail;
    btn.addEventListener('click',function(){
      var on=btn.getAttribute('aria-expanded')==='true';
      qsa('.arch-step',flow).forEach(function(x){x.setAttribute('aria-expanded','false')});
      btn.setAttribute('aria-expanded', on?'false':'true');
    });
    flow.appendChild(btn);
    if(i<data.steps.length-1)flow.appendChild(el('span',{className:'muted','aria-hidden':'true',text:'→'}));
  });
  host.appendChild(flow);
}

function buildPipelines(host, data){
  host.appendChild(el('p',{className:'arch-blurb',text:data.blurb}));
  var grid=el('div',{className:'arch-pipe-grid'});
  (data.nodes||[]).forEach(function(n){
    var btn=el('button',{className:'arch-pipe',type:'button','aria-expanded':'false'});
    btn.appendChild(el('strong',{text:n.label}));
    btn.appendChild(el('div',{className:'path',text:n.path}));
    var detail=el('div',{className:'detail'});
    detail.textContent=(n.detail||'')+' Owner: '+(n.owner||'—');
    btn.appendChild(detail);
    btn.title=n.detail||n.label;
    btn.addEventListener('click',function(){
      var on=btn.getAttribute('aria-expanded')==='true';
      btn.setAttribute('aria-expanded', on?'false':'true');
    });
    grid.appendChild(btn);
  });
  host.appendChild(grid);
  if(data.edges&&data.edges.length){
    var edges=el('p',{className:'muted',style:'margin-top:.75rem;font-size:.85rem'});
    edges.textContent='Flows: '+data.edges.map(function(e){return e.from+' → '+e.to+(e.label?' ('+e.label+')':'')}).join(' · ');
    host.appendChild(edges);
  }
}

function mount(root){
  var suite=el('section',{className:'arch-suite','aria-label':'Interactive architecture diagrams'});
  var head=el('header',null,[
    el('h3',{text:'Architecture diagrams'}),
    el('p',{className:'muted',style:'margin:0;font-size:.85rem',text:'Click or tap a node to expand. Tooltips on hover / focus. Data-driven from architecture.json.'})
  ]);
  var tabs=el('div',{className:'arch-tabs',role:'tablist','aria-label':'Architecture views'});
  var panels=el('div');
  suite.appendChild(head);suite.appendChild(tabs);suite.appendChild(panels);
  root.appendChild(suite);

  fetch(dataUrl(),{cache:'no-store'}).then(function(r){
    if(!r.ok)throw new Error('architecture '+r.status);
    return r.json();
  }).then(function(payload){
    var diagrams=payload.diagrams||{};
    var order=[
      ['hierarchy','Hierarchy',buildHierarchy],
      ['bots','Bots & roles',buildBots],
      ['governance','Governance flow',buildGovernance],
      ['pipelines','Data & automation',buildPipelines]
    ];
    var panelEls=[];
    order.forEach(function(item,idx){
      var key=item[0],label=item[1],builder=item[2];
      var data=diagrams[key];if(!data)return;
      var tab=el('button',{type:'button',role:'tab',id:'arch-tab-'+key,'aria-controls':'arch-panel-'+key,'aria-selected':idx===0?'true':'false',text:label});
      var panel=el('div',{className:'arch-panel',role:'tabpanel',id:'arch-panel-'+key,'aria-labelledby':'arch-tab-'+key});
      if(idx!==0)panel.hidden=true;
      builder(panel,data);
      tab.addEventListener('click',function(){
        panelEls.forEach(function(p){p.panel.hidden=true;p.tab.setAttribute('aria-selected','false')});
        panel.hidden=false;tab.setAttribute('aria-selected','true');
      });
      tabs.appendChild(tab);panels.appendChild(panel);
      panelEls.push({tab:tab,panel:panel});
    });
    if(payload.asOf){
      suite.appendChild(el('p',{className:'muted',style:'font-size:.8rem;margin:.5rem 0 0',text:'Diagram data as-of '+payload.asOf+' ('+(payload.timezone||'Australia/Brisbane')+').'}));
    }
  }).catch(function(err){
    suite.appendChild(el('div',{className:'callout',text:'Architecture diagrams unavailable: '+(err&&err.message||err)}));
  });
}

function boot(){
  var host=document.getElementById('arch-diagrams-root');
  if(host)mount(host);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
else boot();
})();
