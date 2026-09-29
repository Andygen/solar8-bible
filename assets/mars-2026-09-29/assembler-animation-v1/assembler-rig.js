/* Canvas 2D rig, x right/y down. Dimensions are pixels of the original PNGs.
   This file is also embedded unchanged in the preview for identical rendering. */
function makeAssemblerRig(images) {
  const D=Math.PI/180;
  const sockets=[[207,188],[1047,188],[207,925],[1047,925]];
  function draw(ctx,{phase=1,t=0,opening=0,joints=false,jointColor='currentColor'}={}) {
    const poses=[];
    const sprite=(id,x,y,a,s,px,py,mirror=1)=>{
      const im=images[id];ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.scale(s*mirror,s);
      ctx.drawImage(im,-px,-py,im.sourceWidth||im.width,im.sourceHeight||im.height);ctx.restore();
    };
    sprite('chassis',550,535,0,.5,627,627);
    // Core is only exposed in the third visual state.
    if(opening>35)sprite('core',550,490,0,.20,627,627);
    const slide=opening;
    sprite('hatch',506-slide,490,0,.14,444,887);
    sprite('hatch',594+slide,490,0,.14,444,887,-1);
    const reveal=Math.max(0,Math.min(1,(opening-35)/63));
    const pressY=411-87*reveal+12*Math.sin(t*2*Math.PI)*(1-reveal);
    sprite('press',550,pressY,0,.14,627,627);
    for(let i=0;i<4;i++) {
      const side=i%2===0?-1:1;
      const bottom=i>1;
      const w=Math.sin(t*2*Math.PI+i*.6);
      const s={x:550+(sockets[i][0]-627)*.5,y:535+(sockets[i][1]-627)*.5};
      const a=((bottom?(side<0?150:30):(side<0?-150:-30))+side*8*w)*D;
      const b=(bottom?(side<0?-60:60):(side<0?-90:90))*D+side*12*w*D;
      const e={x:s.x+125*Math.cos(a),y:s.y+125*Math.sin(a)};
      const v={x:e.x+105*Math.cos(a+b),y:e.y+105*Math.sin(a+b)};
      sprite('base',s.x,s.y,0,.085,627,604);
      sprite('upper',s.x,s.y,a,125/829,210,620);
      sprite('base',s.x,s.y,0,.015,627,604);
      sprite('forearm',e.x,e.y,a+b-Math.atan2(4,843),105/Math.hypot(843,4),235,620);
      sprite('base',e.x,e.y,0,.019,627,604);
      const direction=a+b+Math.PI/2;
      if(i===1) {
        sprite('drill',v.x,v.y,direction,.105,627,967);
      } else if(i===2) {
        sprite('saw',v.x,v.y,t*Math.PI*8,.105,627,612);
        sprite('base',v.x,v.y,0,.021,627,604);
      } else {
        sprite('base',v.x,v.y,direction,.059,627,604);
        ctx.save();ctx.translate(v.x,v.y);ctx.rotate(direction);
        const spread=(8+14*(.5+.5*Math.sin(t*2*Math.PI+i)))*D;
        sprite('jaw',-20,-5,-spread,.074,599,951);
        sprite('jaw',20,-5,spread,.074,599,951,-1);
        ctx.restore();
      }
      poses.push({shoulder:s,elbow:e,wrist:v});
    }
    if(joints){ctx.strokeStyle=jointColor;ctx.lineWidth=2;
      for(const arm of poses)for(const p of Object.values(arm)){
        ctx.beginPath();ctx.arc(p.x,p.y,8,0,Math.PI*2);ctx.stroke();
      }
    }
    return poses;
  }
  return {draw};
}
if(typeof module!=='undefined')module.exports={makeAssemblerRig};
