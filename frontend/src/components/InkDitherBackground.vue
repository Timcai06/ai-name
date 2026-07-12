<template><div ref="mount" class="absolute inset-0" aria-hidden="true" /></template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as THREE from 'three'

const mount=ref<HTMLElement>()
let cleanup:()=>void=()=>{}
const vertex=`precision highp float;attribute vec3 position;void main(){gl_Position=vec4(position,1.0);}`
const fragment=`
#ifdef GL_ES
precision highp float;
#endif
uniform float iTime;uniform vec2 iResolution;uniform vec3 uColorLow;uniform vec3 uColorHigh;uniform float uColorSteps;uniform float uScale;uniform float uSpeed;uniform float uPixelSize;uniform float uFade;
float hash(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+34.123);return fract(p.x*p.y);}
float vnoise(vec2 p){vec2 i=floor(p),f=fract(p);float a=hash(i),b=hash(i+vec2(1.,0.)),c=hash(i+vec2(0.,1.)),d=hash(i+vec2(1.,1.));vec2 u=f*f*(3.-2.*f);return mix(mix(a,b,u.x),mix(c,d,u.x),u.y);}
float fbm(vec2 p){float v=0.,amp=.5;mat2 m=mat2(.8,.6,-.6,.8);for(int i=0;i<5;i++){v+=amp*vnoise(p);p=m*p*2.+11.;amp*=.5;}return v;}
float Bayer2(vec2 a){a=floor(a);return fract(a.x*.5+a.y*a.y*.75);}
#define Bayer4(a) (Bayer2(.5*(a))*.25+Bayer2(a))
#define Bayer8(a) (Bayer4(.5*(a))*.25+Bayer2(a))
void main(){vec2 block=floor(gl_FragCoord.xy/uPixelSize);vec2 frag=block*uPixelSize;vec2 uv=frag/iResolution.xy;vec2 p=uv*uScale;p.x*=iResolution.x/max(iResolution.y,1.);float t=iTime*uSpeed;float n=fbm(p+vec2(t*.15,t*.08)+fbm(p-t*.05));n=n*.72+.28*(.5+.5*sin((uv.x+uv.y)*3.-t*.6));n=clamp(n,0.,1.);float ramp=pow(n,1.72);float threshold=Bayer8(block)-.5;ramp=clamp(ramp+threshold/uColorSteps,0.,1.);ramp=floor(ramp*(uColorSteps-1.)+.5)/(uColorSteps-1.);vec3 col=mix(uColorLow,uColorHigh,ramp);col=mix(uColorLow,col,uFade);gl_FragColor=vec4(col,1.);}`

onMounted(()=>{
  const host=mount.value
  if(!host||matchMedia('(prefers-reduced-motion: reduce)').matches)return
  const renderer=new THREE.WebGLRenderer({antialias:false,alpha:false,depth:false,stencil:false,powerPreference:'high-performance',premultipliedAlpha:false,preserveDrawingBuffer:false})
  const dpr=Math.min(devicePixelRatio||1,1.5);renderer.setPixelRatio(dpr);renderer.setClearColor(0xeee9dd,1)
  const canvas=renderer.domElement;canvas.style.cssText='width:100%;height:100%;display:block';host.appendChild(canvas)
  const scene=new THREE.Scene();const camera=new THREE.OrthographicCamera(-1,1,1,-1,0,1);const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.BufferAttribute(new Float32Array([-1,-1,0,3,-1,0,-1,3,0]),3))
  const uniforms={iTime:{value:0},iResolution:{value:new THREE.Vector2(1,1)},uColorLow:{value:new THREE.Vector3(.93,.91,.86)},uColorHigh:{value:new THREE.Vector3(.12,.17,.14)},uColorSteps:{value:6},uScale:{value:3.05},uSpeed:{value:.34},uPixelSize:{value:Math.max(1,2.5*dpr)},uFade:{value:0}}
  const material=new THREE.RawShaderMaterial({vertexShader:vertex,fragmentShader:fragment,uniforms,depthTest:false,depthWrite:false});const mesh=new THREE.Mesh(geometry,material);mesh.frustumCulled=false;scene.add(mesh)
  const setSize=()=>{const w=host.clientWidth||1,h=host.clientHeight||1;renderer.setSize(w,h,false);uniforms.iResolution.value.set(w*dpr,h*dpr)};setSize();const ro=new ResizeObserver(setSize);ro.observe(host)
  let paused=false,raf=0,fade=0;const startedAt=performance.now();const onVisibility=()=>paused=document.hidden;document.addEventListener('visibilitychange',onVisibility,{passive:true})
  const animate=()=>{raf=requestAnimationFrame(animate);if(paused)return;uniforms.iTime.value=(performance.now()-startedAt)/1000;if(fade<1){fade=Math.min(1,fade+1/60);uniforms.uFade.value=fade}renderer.render(scene,camera)};animate()
  cleanup=()=>{cancelAnimationFrame(raf);ro.disconnect();document.removeEventListener('visibilitychange',onVisibility);geometry.dispose();material.dispose();renderer.dispose();renderer.forceContextLoss();if(host.contains(canvas))host.removeChild(canvas)}
})
onBeforeUnmount(()=>cleanup())
</script>
