<template>
  <div v-if="visible" ref="panel" class="ink-intro" aria-label="名笺开场动画">
    <InkDitherBackground />
    <div class="paper-grain" aria-hidden="true" />

    <svg class="landscape" viewBox="0 0 1200 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <path class="ink-stroke ink-stroke--soft" d="M-30 398 C100 330 150 365 245 286 C316 227 360 318 438 281 C520 240 560 108 646 190 C713 254 750 305 830 269 C919 229 954 303 1230 203" />
      <path class="ink-stroke" d="M-20 430 C115 372 188 392 286 322 C352 276 401 338 476 302 C552 265 593 158 670 222 C737 278 789 337 875 298 C958 261 1000 319 1220 248" />
    </svg>

    <div class="intro-meta">CHINESE NAMING STUDIO · 2026</div>
    <div class="intro-center">
      <div class="intro-title-wrap">
        <h1 class="intro-title" aria-label="名笺"><span v-for="char in ['名','笺']" :key="char" class="intro-char"><i class="intro-glyph" :data-final="char">{{ char }}</i></span></h1>
      </div>
      <p class="intro-subtitle">一笔一画，自有来处</p>
      <span class="intro-seal">取<br>名</span>
    </div>
    <div class="scan-line" aria-hidden="true" />
    <div class="intro-counter"><strong ref="countEl">00</strong><span>/ 100</span><em ref="stageEl">研墨</em></div>
    <div class="intro-status"><span>名笺 · AI 取名</span><small>INK / SOUND / MEANING</small></div>
    <div class="progress-track"><i ref="barEl" /></div>
    <button class="skip" @click="finish">跳过</button>
  </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent, onBeforeUnmount, onMounted, ref } from 'vue'
import gsap from 'gsap'
const InkDitherBackground=defineAsyncComponent(()=>import('./InkDitherBackground.vue'))

const visible=ref(true)
const panel=ref<HTMLElement>()
const countEl=ref<HTMLElement>();const stageEl=ref<HTMLElement>();const barEl=ref<HTMLElement>()
let timeline:gsap.core.Timeline|null=null
const media=gsap.matchMedia()
const intervals:number[]=[]

onMounted(()=>{
  if(!visible.value||!panel.value)return
  document.body.style.overflow='hidden'
  media.add({motion:'(prefers-reduced-motion: no-preference)',reduce:'(prefers-reduced-motion: reduce)'},context=>{
    if(context.conditions?.reduce){timeline=gsap.timeline({onComplete:finish}).to(panel.value!,{autoAlpha:0,duration:.45,ease:'power1.out'},.35);return}
    const strokes=Array.from(panel.value!.querySelectorAll<SVGPathElement>('.ink-stroke'))
    strokes.forEach(path=>{const length=path.getTotalLength();gsap.set(path,{strokeDasharray:length,strokeDashoffset:length})})
    const glyphs=Array.from(panel.value!.querySelectorAll<HTMLElement>('.intro-glyph'))
    const baffle='天地玄黄宇宙洪荒山水风月云烟墨砚乾坤'.split('')
    glyphs.forEach(glyph=>{const final=glyph.dataset.final||'';let frame=0;const id=window.setInterval(()=>{glyph.textContent=frame<11?baffle[Math.floor(Math.random()*baffle.length)]:(frame<15&&frame%2===0?baffle[Math.floor(Math.random()*baffle.length)]:final);frame++;if(frame>15){glyph.textContent=final;clearInterval(id)}},42);intervals.push(id)})
    const progress={value:0}
    timeline=gsap.timeline({defaults:{ease:'power3.out'},onComplete:finish})
      .to(strokes,{strokeDashoffset:0,duration:1.45,stagger:.1,ease:'power2.inOut'},.12)
      .fromTo('.intro-char',{autoAlpha:0,yPercent:118},{autoAlpha:1,yPercent:0,duration:1,stagger:.13,ease:'expo.out'},.38)
      .fromTo('.scan-line',{autoAlpha:0,scaleX:0},{autoAlpha:.75,scaleX:1,duration:.42},.92)
      .to('.scan-line',{autoAlpha:0,duration:.45},1.38)
      .fromTo('.intro-subtitle',{autoAlpha:0,y:12},{autoAlpha:1,y:0,duration:.6},.82)
      .fromTo('.intro-seal',{autoAlpha:0,scale:1.35,rotation:5},{autoAlpha:.88,scale:1,rotation:0,duration:.48,ease:'power3.out'},1.05)
      .fromTo('.intro-meta, .intro-counter, .intro-status, .progress-track, .skip',{autoAlpha:0},{autoAlpha:1,duration:.5,stagger:.04},.58)
      .fromTo(barEl.value!,{scaleX:0},{scaleX:1,duration:2.55,ease:'power1.inOut'},.12)
      .to(progress,{value:100,duration:2.55,ease:'power1.inOut',onUpdate:()=>{if(countEl.value)countEl.value.textContent=String(Math.round(progress.value)).padStart(2,'0')}},.12)
      .call(()=>{if(stageEl.value)stageEl.value.textContent='落笔'},[],.82)
      .call(()=>{if(stageEl.value)stageEl.value.textContent='成章'},[],1.72)
      .call(()=>{if(stageEl.value)stageEl.value.textContent='就绪'},[],2.55)
      .to({}, {duration:.38})
      .to('.intro-meta, .intro-counter, .intro-status, .progress-track, .intro-subtitle, .skip',{autoAlpha:0,duration:.42,ease:'power2.in'})
      .to('.intro-char',{yPercent:-120,duration:.65,stagger:.06,ease:'power3.in'},'<')
      .to('.intro-seal',{autoAlpha:0,scale:.8,duration:.35,ease:'power2.in'},'<.1')
      .to(panel.value!,{yPercent:-100,duration:1.05,ease:'expo.inOut'},'>-.05')
  },panel.value)
})
function finish(){intervals.forEach(clearInterval);timeline?.kill();document.body.style.overflow='';visible.value=false}
onBeforeUnmount(()=>{intervals.forEach(clearInterval);timeline?.kill();media.revert();document.body.style.overflow=''})
</script>

<style scoped>
.ink-intro{position:fixed;inset:0;z-index:20000;display:grid;place-items:center;overflow:hidden;background:radial-gradient(circle at 68% 35%,#d9d7cc,#f0ece2 58%,#e5dfd2);color:#171713;will-change:transform}.paper-grain{position:absolute;inset:0;z-index:1;opacity:.36;background-image:repeating-radial-gradient(circle at 17% 23%,rgba(52,43,31,.055) 0 .45px,transparent .6px 3px),linear-gradient(105deg,rgba(255,255,255,.26),transparent 42%,rgba(129,108,74,.07));background-size:5px 5px,100% 100%;mix-blend-mode:multiply}.landscape{position:absolute;z-index:2;inset:auto -3vw 3vh;width:106vw;height:56vh;opacity:.22}.ink-stroke{fill:none;stroke:#202620;stroke-width:2.1;stroke-linecap:round;will-change:stroke-dashoffset}.ink-stroke--soft{stroke-width:13;opacity:.09;filter:blur(7px)}.intro-center{position:relative;z-index:3;display:grid;place-items:center}.intro-title-wrap{overflow:hidden;padding:.12em .2em}.intro-title{display:flex;font-family:"Songti SC","STSong",serif;font-size:clamp(96px,18vw,220px);font-weight:400;line-height:.92;letter-spacing:.08em}.intro-char,.intro-glyph{display:inline-block;will-change:transform,opacity}.intro-glyph{min-width:1em;font-style:normal;text-align:center}.intro-subtitle{margin-top:26px;font-family:"Songti SC","STSong",serif;font-size:clamp(13px,1.2vw,17px);letter-spacing:.48em;color:rgba(23,23,19,.62)}.intro-seal{position:absolute;right:-36px;bottom:17px;display:grid;place-items:center;width:43px;height:52px;border:2px solid #a84436;color:#a84436;font-family:"STKaiti","KaiTi",serif;font-size:13px;line-height:1.15;transform:rotate(-3deg)}.intro-meta{position:absolute;z-index:3;left:clamp(24px,4vw,60px);top:clamp(24px,4vw,52px);font-size:9px;letter-spacing:.27em;color:rgba(23,23,19,.42)}.scan-line{position:absolute;z-index:4;left:18vw;right:18vw;top:50%;height:1px;transform-origin:left;background:linear-gradient(90deg,transparent,#9b3f34,rgba(25,28,24,.58),transparent)}.intro-counter{position:absolute;z-index:3;left:clamp(24px,4vw,60px);bottom:clamp(48px,6vw,76px);display:grid;grid-template-columns:auto auto 1fr;align-items:end;gap:10px;width:min(520px,calc(100vw - 48px));font-family:Georgia,serif}.intro-counter strong{font-size:clamp(27px,3vw,42px);font-weight:400}.intro-counter span{padding-bottom:6px;font-size:10px;letter-spacing:.16em;color:rgba(23,23,19,.46)}.intro-counter em{align-self:center;font-style:normal;font-size:10px;letter-spacing:.26em;color:rgba(23,23,19,.4)}.intro-status{position:absolute;z-index:3;right:clamp(24px,4vw,60px);bottom:clamp(50px,6vw,78px);display:flex;flex-direction:column;align-items:flex-end;gap:6px;font-size:9px;letter-spacing:.2em;color:rgba(23,23,19,.48)}.intro-status small{font-size:8px;color:rgba(23,23,19,.3)}.progress-track{position:absolute;z-index:3;left:clamp(24px,4vw,60px);right:clamp(24px,4vw,60px);bottom:clamp(22px,3vw,34px);height:1px;background:rgba(23,23,19,.14)}.progress-track i{display:block;width:100%;height:100%;transform-origin:left;background:linear-gradient(90deg,#9b3f34,#202620);will-change:transform}.skip{position:absolute;z-index:3;right:clamp(24px,4vw,60px);top:clamp(24px,4vw,52px);font-size:10px;letter-spacing:.2em;color:rgba(23,23,19,.42)}
@media(max-width:640px){.intro-title{font-size:32vw}.intro-seal{right:-10px;bottom:12px}.landscape{height:42vh}.intro-status{display:none}.intro-counter{width:65vw}}
</style>
