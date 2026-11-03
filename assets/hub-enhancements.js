(function(){
'use strict';
var LABEL_KEY='swarm-hub-always-labels';
var COACH_KEY='swarm-hub-coach-seen-v1';

function asOfMap(){
  return {
    'governance-master':{label:'Governance master',asOf:'2026-11-03',rev:'live shared'},
    'governance-r054':{label:'R-054',asOf:'2026-10-22',rev:'R-054 in force'},
    'governance-rulings':{label:'Rulings in force',asOf:'2026-11-03',rev:'catalogue'},
    'governance-annex':{label:'Annex',asOf:'2026-11-03',rev:'historical'},
    'bots-rolemap':{label:'Role map',asOf:'2026-11-03',rev:'interactive'},
    'observatory-overview':{label:'Observatory overview',asOf:'2026-11-03',rev:'embed'},
    'observatory-evidence':{label:'Evidence',asOf:'2026-11-03',rev:'embed'},
    'observatory-authority':{label:'Authority model',asOf:'2026-11-03',rev:'embed'},
    'observatory-ledger':{label:'Ledger contract',asOf:'2026-11-03',rev:'embed'},
    'observatory-graph':{label:'Relationships',asOf:'2026-11-03',rev:'embed'},
    'observatory-conflicts':{label:'Open questions',asOf:'2026-11-03',rev:'embed'},
    'workspace':{label:'Workspace map',asOf:'2026-11-03',rev:'snapshot'},
    'workspace-summary':{label:'Workspace summary',asOf:'2026-11-03',rev:'summary'}
  };
}

function updateTitle(){
  var h=(location.hash||'#').slice(1)||'overview';
  var parts=[];
  var top=document.querySelector('#top-tabs [aria-selected=true]');
  if(top)parts.push(top.getAttribute('data-tab-name')||top.textContent.trim());
  var nest=document.querySelector('[data-nest] [aria-selected=true]');
  if(nest && top && (top.getAttribute('aria-controls')==='governance'||top.getAttribute('aria-controls')==='bots'||top.getAttribute('aria-controls')==='observatory')){
    var nestName=nest.getAttribute('data-tab-name')||nest.textContent.trim();
    if(nestName && parts[0]!==nestName)parts.push(nestName);
  }
  if(!parts.length)parts.push(h);
  document.title=parts.join(' · ')+' · Swarm';
}

function setupLabels(){
  var prefs=document.getElementById('hub-prefs');
  if(!prefs)return;
  var box=document.getElementById('always-labels');
  if(!box)return;
  try{box.checked=localStorage.getItem(LABEL_KEY)==='1'}catch(e){}
  function apply(){document.body.classList.toggle('labels-always', !!box.checked)}
  apply();
  box.addEventListener('change',function(){
    try{localStorage.setItem(LABEL_KEY, box.checked?'1':'0')}catch(e){}
    apply();
  });
}

function setupCoach(){
  var seen=false;
  try{seen=localStorage.getItem(COACH_KEY)==='1'}catch(e){}
  if(seen||window.matchMedia('(min-width:901px)').matches)return;
  var mark=document.createElement('div');
  mark.className='coach-mark';mark.setAttribute('role','status');
  mark.innerHTML='<strong>Tip:</strong> Press and hold a tab for its guide, or tap the <strong>?</strong> control for the same content in a dialog.<div class="actions"><button type="button" class="btn" id="coach-dismiss">Got it</button></div>';
  document.body.appendChild(mark);
  document.getElementById('coach-dismiss').addEventListener('click',function(){
    mark.hidden=true;
    try{localStorage.setItem(COACH_KEY,'1')}catch(e){}
  });
}

function setupTipDialog(){
  var dlg=document.getElementById('tab-tip-dialog');
  var openBtn=document.getElementById('open-tab-guide');
  if(!dlg||!openBtn)return;
  openBtn.addEventListener('click',function(){
    var tab=document.querySelector('[role=tablist] [role=tab][aria-selected=true]')||document.querySelector('#top-tabs [role=tab]');
    var tip=tab&&tab.querySelector('.tab-tip');
    var inner=dlg.querySelector('.inner');
    if(tip&&inner){
      inner.innerHTML='<h2>'+(tab.getAttribute('data-tab-name')||'Tab guide')+'</h2>'+tip.innerHTML+
        '<p class="muted" style="margin-top:.75rem">On phones, press and hold any tab icon for this guide.</p>';
    }
    if(typeof dlg.showModal==='function')dlg.showModal();
    else dlg.setAttribute('open','');
  });
  var close=dlg.querySelector('[data-close]');
  if(close)close.addEventListener('click',function(){
    if(typeof dlg.close==='function')dlg.close(); else dlg.removeAttribute('open');
  });
}

function setupAsOf(){
  var map=asOfMap();
  Object.keys(map).forEach(function(id){
    var panel=document.getElementById(id);
    if(!panel)return;
    var wrap=panel.querySelector('.frame-wrap');
    if(!wrap||panel.querySelector('.frame-meta'))return;
    var meta=document.createElement('div');
    meta.className='frame-meta';
    meta.innerHTML='<span><strong>'+map[id].label+'</strong></span><span>As-of <time datetime="'+map[id].asOf+'">'+map[id].asOf+'</time> (Australia/Brisbane)</span><span>Source revision: '+map[id].rev+'</span>';
    wrap.parentNode.insertBefore(meta, wrap);
    wrap.classList.add('has-meta');
  });
}

function setupLazyFrames(){
  var frames=[].slice.call(document.querySelectorAll('.frame-wrap iframe[data-src], .frame-wrap iframe[src]'));
  frames.forEach(function(f){
    if(!f.getAttribute('data-src')){
      var s=f.getAttribute('src');
      if(s){f.setAttribute('data-src',s);f.removeAttribute('src')}
    }
  });
  function activate(panel){
    if(!panel)return;
    panel.querySelectorAll('iframe[data-src]').forEach(function(f){
      if(!f.getAttribute('src'))f.setAttribute('src',f.getAttribute('data-src'));
    });
  }
  function onShow(){
    var top=document.querySelector('#top-tabs [aria-selected=true]');
    if(!top)return;
    var panel=document.getElementById(top.getAttribute('aria-controls'));
    if(!panel||panel.hidden)return;
    var nested=panel.querySelector('.nest-panel:not([hidden])')||panel;
    activate(nested);
    // park hidden frames on small screens
    if(window.matchMedia('(max-width:700px)').matches){
      document.querySelectorAll('.nest-panel[hidden] iframe[src], #workspace[hidden] iframe[src], #observatory[hidden] iframe[src], #governance[hidden] iframe[src]').forEach(function(f){
        if(f.getAttribute('data-src'))f.removeAttribute('src');
      });
    }
  }
  window.addEventListener('hashchange',function(){setTimeout(onShow,0)});
  document.querySelectorAll('[role=tab]').forEach(function(t){
    t.addEventListener('click',function(){setTimeout(onShow,0)});
  });
  onShow();
}

function setupResizeObserver(){
  if(typeof ResizeObserver==='undefined')return;
  document.querySelectorAll('.frame-wrap iframe').forEach(function(iframe){
    function fit(){
      try{
        var doc=iframe.contentDocument||iframe.contentWindow.document;
        if(!doc||!doc.body)return;
        var h=Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight, 420);
        iframe.style.height=Math.min(h, Math.floor(window.innerHeight*0.92))+'px';
      }catch(e){/* cross-origin or not ready */}
    }
    iframe.addEventListener('load',function(){
      fit();
      try{
        var doc=iframe.contentDocument;
        if(doc&&doc.body){
          var ro=new ResizeObserver(fit);
          ro.observe(doc.body);
        }
      }catch(e){}
    });
  });
}

function boot(){
  setupLabels();
  setupCoach();
  setupTipDialog();
  setupAsOf();
  setupLazyFrames();
  setupResizeObserver();
  updateTitle();
  window.addEventListener('hashchange',updateTitle);
  document.querySelectorAll('[role=tab]').forEach(function(t){
    t.addEventListener('click',function(){setTimeout(updateTitle,0)});
  });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);
else boot();
})();
