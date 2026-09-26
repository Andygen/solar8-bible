// SOLAR 8: Canvas 2D reference for the top-down manipulator prototype.
// Source coordinates and limits are documented in rig.json.
const D = Math.PI / 180;
const sourceSize = 1254;
const forearmAngle = Math.atan2(4, 843);
const files = Object.fromEntries(['base', 'upper', 'forearm', 'gripper'].map(
  part => [part, `rig/assembler-gripper/assembler-gripper-${part}.png`]
));

export function demoAngles(progress) {
  const w = Math.sin(2 * Math.PI * progress);
  return { shoulderDeg: -105 + 20*w, elbowDeg: 70 + 35*w, wristDeg: -15 + 20*w };
}

export async function createAssemblerGripper(assetBase = new URL('../../assets/', import.meta.url)) {
  const entries = await Promise.all(Object.entries(files).map(async ([id, path]) => {
    const url = new URL(path, assetBase).href;
    const img = await new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = () => reject(new Error(`Cannot load ${url}`));
      image.src = url;
    });
    return [id, img];
  }));
  const images = Object.fromEntries(entries);
  return {
    draw(ctx, { x = 0, y = 0, scale = 1, shoulderDeg = -105, elbowDeg = 70, wristDeg = -15 } = {}) {
      if (![x,y,scale,shoulderDeg,elbowDeg,wristDeg].every(Number.isFinite) || scale <= 0)
        throw new TypeError('Finite transforms and positive scale are required');
      const a = shoulderDeg*D, b = elbowDeg*D, c = wristDeg*D;
      const elbow = { x:260*Math.cos(a), y:260*Math.sin(a) };
      const wrist = { x:elbow.x+220*Math.cos(a+b), y:elbow.y+220*Math.sin(a+b) };
      const sprite = (id, px, py, angle, s, pivotX, pivotY) => {
        ctx.save(); ctx.translate(px,py); ctx.rotate(angle); ctx.scale(s,s);
        ctx.drawImage(images[id],-pivotX,-pivotY,sourceSize,sourceSize); ctx.restore();
      };
      ctx.save(); ctx.translate(x,y); ctx.scale(scale,scale);
      sprite('base',0,0,0,.16,627,604);
      sprite('upper',0,0,a,260/829,210,620);
      sprite('base',0,0,0,.030,627,604);
      sprite('forearm',elbow.x,elbow.y,a+b-forearmAngle,220/Math.hypot(843,4),235,620);
      sprite('base',elbow.x,elbow.y,0,.034,627,604);
      sprite('gripper',wrist.x,wrist.y,a+b+c+Math.PI/2,.12,626,893);
      ctx.restore();
      return {
        shoulder: {x,y},
        elbow: {x:x+elbow.x*scale,y:y+elbow.y*scale},
        wrist: {x:x+wrist.x*scale,y:y+wrist.y*scale}
      };
    }
  };
}
