/* Cache tiny PNG frames from the actual logo; only the solar crescent rotates. */
(() => {
  const icon=document.querySelector('link[rel="icon"]');
  if(!icon)return;
  const fallback={href:icon.getAttribute('href'),type:icon.getAttribute('type'),sizes:icon.getAttribute('sizes')};
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  const period=8000,count=48;
  let frames=[],timer=null,loading=false,failed=false;
  function stop(){clearTimeout(timer);timer=null;}
  function restore(){
    for(const [key,value] of Object.entries(fallback)){
      if(value===null)icon.removeAttribute(key);else icon.setAttribute(key,value);
    }
  }
  function tick(){
    if(document.hidden || motion.matches){sync();return;}
    icon.type='image/png';icon.sizes='64x64';
    icon.href=frames[Math.floor((Date.now()%period)/period*count)];
    timer=setTimeout(tick,period/count);
  }
  async function layer(svg,remove){
    const copy=svg.cloneNode(true);
    for(const selector of remove)copy.querySelector(selector)?.remove();
    copy.setAttribute('width','64');copy.setAttribute('height','64');
    const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(copy)],{type:'image/svg+xml'}));
    try{const image=new Image();image.src=url;await image.decode();return image;}
    finally{URL.revokeObjectURL(url);}
  }
  async function prepare(){
    loading=true;
    try{
      const response=await fetch(fallback.href);
      if(!response.ok)throw Error(response.status);
      const svg=new DOMParser().parseFromString(await response.text(),'image/svg+xml').documentElement;
      if(!svg.querySelector('#solar-orbit') || !svg.querySelector('#solar-letter'))throw Error('Logo layers missing');
      const [base,orbit]=await Promise.all([layer(svg,['#solar-orbit']),layer(svg,['#solar-letter','rect'])]);
      const canvas=document.createElement('canvas');canvas.width=canvas.height=64;
      const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvas unavailable');
      for(let frame=0;frame<count;frame++){
        ctx.clearRect(0,0,64,64);ctx.drawImage(base,0,0);
        ctx.save();ctx.translate(32,32);ctx.rotate(frame/count*Math.PI*2);
        ctx.drawImage(orbit,-32,-32);ctx.restore();
        frames.push(canvas.toDataURL('image/png'));
      }
    }catch(_){failed=true;frames=[];restore();}
    finally{loading=false;sync();}
  }
  function sync(){
    stop();
    if(motion.matches || failed){restore();return;}
    if(document.hidden)return;
    if(frames.length===count)tick();else if(!loading)prepare();
  }
  document.addEventListener('visibilitychange',sync);
  motion.addEventListener('change',sync);
  addEventListener('pagehide',()=>{stop();restore();});
  addEventListener('pageshow',sync);
  sync();
})();
