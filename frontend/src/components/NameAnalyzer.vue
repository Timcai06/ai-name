<template>
  <div class="analysis-workspace">
    <form class="analysis-brief" :aria-busy="loading" @submit.prevent="handleAnalyze">
      <span class="analysis-brief__rule" aria-hidden="true" />
      <div class="analysis-brief__main">
        <label>
          <span class="analysis-label"><span>待鉴姓名</span><em>必填</em></span>
          <input v-model.trim="name" maxlength="10" autocomplete="name" placeholder="输入一个完整名字" :disabled="loading" required />
        </label>
        <fieldset :disabled="loading">
          <legend class="analysis-label"><span>性别</span></legend>
          <div class="analysis-genders">
            <button v-for="option in genders" :key="option.value" type="button" :class="{ 'is-active': gender === option.value }" :aria-pressed="gender === option.value" @click="gender = option.value">
              <span>{{ option.seal }}</span>{{ option.label }}
            </button>
          </div>
        </fieldset>
      </div>
      <footer>
        <p>从寓意、音韵、五行与文化内涵综合解读。</p>
        <button type="submit" :disabled="!name.trim() || loading">
          <span v-if="loading" class="spinner" aria-hidden="true" />
          {{ loading ? "正在分析" : "开始分析" }}
          <svg v-if="!loading" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 6l4 4-4 4" /></svg>
        </button>
      </footer>
    </form>

    <div v-if="loading" class="analysis-skeleton" aria-label="正在分析名字" aria-busy="true"><i /><b /><span /><span /></div>
    <div v-else-if="error" class="analysis-state analysis-state--error" role="alert"><p>{{ error }}</p><button type="button" @click="handleAnalyze">重新分析</button></div>

    <article v-else-if="result" class="analysis-result">
      <span class="analysis-result__rule" aria-hidden="true" />
      <header>
        <div><p>NAME APPRAISAL · 姓名鉴赏</p><h3>{{ name }}</h3></div>
        <div class="analysis-seal" :aria-label="`综合评分 ${result.score} 分`"><strong>{{ result.score }}</strong><span>综合</span></div>
      </header>
      <p class="analysis-summary">{{ result.summary }}</p>
      <dl>
        <div><dt>名字寓意</dt><dd>{{ result.meaning }}</dd></div>
        <div><dt>五行属性</dt><dd>{{ result.wuxing }}</dd></div>
        <div><dt>文化出处</dt><dd>{{ result.source }}</dd></div>
      </dl>
      <div class="analysis-notes">
        <section><p>MERITS</p><h4>可取之处</h4><ul><li v-for="item in result.pros || []" :key="item">{{ item }}</li></ul></section>
        <section><p>CONSIDERATIONS</p><h4>需要留意</h4><ul><li v-for="item in result.cons || []" :key="item">{{ item }}</li><li v-if="!result.cons?.length">整体没有明显需要回避之处。</li></ul></section>
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { analyzeName } from "../api";

interface AnalysisResult { score: number; summary: string; meaning: string; wuxing: string; source: string; pros?: string[]; cons?: string[] }
const props = defineProps<{ authGuard?: () => boolean }>();
const genders = [{ label: "男", seal: "乾", value: "male" }, { label: "女", seal: "坤", value: "female" }];
const name = ref("");
const gender = ref("male");
const loading = ref(false);
const error = ref("");
const result = ref<AnalysisResult | null>(null);

async function handleAnalyze() {
  if (!name.value.trim() || loading.value) return;
  if (props.authGuard && !props.authGuard()) return;
  loading.value = true; error.value = ""; result.value = null;
  try { result.value = await analyzeName(name.value.trim(), gender.value); }
  catch (cause: any) { error.value = cause.response?.data?.detail?.message || cause.message || "分析失败"; }
  finally { loading.value = false; }
}
</script>

<style scoped>
.analysis-workspace { max-width: 820px; margin: 0 auto; }.analysis-brief,.analysis-result { position: relative; overflow: hidden; border: 1px solid rgba(183,161,120,.36); border-radius: 25px; background: linear-gradient(138deg,rgba(255,254,249,.92),rgba(244,240,230,.78)); box-shadow: 0 18px 50px rgba(58,50,38,.06); }.analysis-brief__rule,.analysis-result__rule { position: absolute; top: 0; left: 0; width: 66%; height: 3px; background: linear-gradient(90deg,#32695d 0 38%,#b7a178 38% 76%,transparent); }.analysis-brief__main { display: grid; grid-template-columns: minmax(0,1.4fr) minmax(230px,.7fr); }.analysis-brief__main > label,.analysis-brief fieldset { padding: 28px 30px; }.analysis-brief fieldset { border-left: 1px solid rgba(183,161,120,.26); }.analysis-label { display: flex; align-items: center; justify-content: space-between; color: #5e5a52; font-size: 12px; letter-spacing: .08em; }.analysis-label em { color: #9a9489; font-size: 9px; font-style: normal; }.analysis-brief input { width: 100%; border-bottom: 1px solid rgba(50,105,93,.34); background: transparent; margin-top: 13px; padding: 2px 0 10px; color: #191916; font-family: "Songti SC","STSong",serif; font-size: clamp(30px,4vw,43px); letter-spacing: .07em; outline: none; }.analysis-brief input::placeholder { color: #bdb6aa; }.analysis-brief input:focus { border-color: #32695d; }.analysis-genders { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }.analysis-genders button { display: flex; min-height: 58px; cursor: pointer; align-items: center; justify-content: center; gap: 9px; border: 1px solid rgba(183,161,120,.38); border-radius: 14px; color: #68635a; transition: border-color 180ms ease,background-color 180ms ease,color 180ms ease; }.analysis-genders button span { display: grid; width: 25px; height: 29px; place-items: center; border: 1px solid currentColor; font-family: "STKaiti","KaiTi",serif; font-size: 11px; }.analysis-genders button.is-active { border-color: #32695d; background: rgba(50,105,93,.08); color: #32695d; }.analysis-brief footer { display: flex; align-items: center; justify-content: space-between; gap: 20px; border-top: 1px solid rgba(183,161,120,.26); padding: 20px 30px; background: rgba(235,231,220,.34); }.analysis-brief footer p { color: #777168; font-size: 12px; }.analysis-brief footer button,.analysis-state button { display: inline-flex; min-width: 142px; min-height: 48px; cursor: pointer; align-items: center; justify-content: center; gap: 10px; border-radius: 999px; background: #32695d; padding: 0 20px; color: white; font-size: 13px; }.analysis-brief footer button:disabled { cursor: not-allowed; opacity: .42; }.analysis-brief footer svg { width: 18px; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.5; }.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.35); border-top-color: white; border-radius: 50%; animation: spin .8s linear infinite; }
.analysis-skeleton { position: relative; overflow: hidden; height: 310px; border: 1px solid rgba(183,161,120,.3); border-radius: 25px; background: rgba(255,254,249,.7); margin-top: 28px; padding: 34px; }.analysis-skeleton::after { position: absolute; inset: 0; background: linear-gradient(105deg,transparent 30%,rgba(255,255,255,.7) 48%,transparent 65%); content: ""; animation: shimmer 1.6s ease-in-out infinite; transform: translateX(-100%); }.analysis-skeleton i,.analysis-skeleton b,.analysis-skeleton span { display: block; border-radius: 999px; background: rgba(183,174,157,.26); }.analysis-skeleton i { width: 130px; height: 8px; }.analysis-skeleton b { width: 190px; height: 45px; margin-top: 18px; border-radius: 5px; }.analysis-skeleton span { width: 100%; height: 12px; margin-top: 28px; }.analysis-skeleton span:last-child { width: 70%; margin-top: 10px; }
.analysis-result { margin-top: 28px; padding: 31px 32px 28px; }.analysis-result header { display: flex; align-items: flex-start; justify-content: space-between; gap: 22px; }.analysis-result header p { color: #817b71; font-size: 9px; letter-spacing: .16em; }.analysis-result h3 { margin-top: 12px; font-family: "Songti SC","STSong",serif; font-size: clamp(39px,5vw,54px); font-weight: 400; letter-spacing: .08em; }.analysis-seal { position: relative; display: grid; width: 59px; height: 65px; place-items: center; align-content: center; border: 1px solid rgba(166,66,53,.58); color: #9b4035; transform: rotate(2deg); }.analysis-seal strong { font-family: Georgia,serif; font-size: 23px; font-weight: 400; }.analysis-seal span { margin-top: 3px; font-size: 8px; letter-spacing: .18em; }.analysis-summary { max-width: 680px; margin-top: 21px; color: #49473f; font-size: 15px; line-height: 1.9; }.analysis-result dl { display: grid; grid-template-columns: 1.2fr .7fr 1.2fr; gap: 16px; margin-top: 23px; padding: 18px 0; border-block: 1px solid rgba(183,161,120,.28); }.analysis-result dt { color: #918b80; font-size: 9px; letter-spacing: .15em; }.analysis-result dd { margin-top: 6px; color: #292923; font-family: "Songti SC","STSong",serif; font-size: 14px; line-height: 1.6; }.analysis-notes { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 18px; }.analysis-notes section { border-left: 2px solid rgba(50,105,93,.28); background: rgba(235,231,220,.56); padding: 16px; }.analysis-notes section > p { color: #918b80; font-size: 8px; letter-spacing: .17em; }.analysis-notes h4 { margin-top: 7px; font-family: "Songti SC","STSong",serif; font-size: 17px; font-weight: 400; }.analysis-notes ul { display: grid; gap: 5px; margin-top: 9px; color: #5d5950; font-size: 12px; line-height: 1.7; }.analysis-notes li::before { margin-right: 7px; color: #32695d; content: "—"; }.analysis-state { display: grid; min-height: 220px; place-items: center; align-content: center; margin-top: 28px; text-align: center; }.analysis-state--error { color: #a64235; }.analysis-state button { min-width: 120px; margin-top: 15px; background: transparent; color: #a64235; }.analysis-brief button:focus-visible,.analysis-state button:focus-visible { outline: 2px solid #32695d; outline-offset: 3px; }
@keyframes spin { to { transform: rotate(360deg); } }@keyframes shimmer { 55%,100% { transform: translateX(100%); } }
@media (max-width:700px) { .analysis-brief__main { grid-template-columns: 1fr; }.analysis-brief fieldset { border-top: 1px solid rgba(183,161,120,.26); border-left: 0; }.analysis-brief__main > label,.analysis-brief fieldset,.analysis-brief footer,.analysis-result { padding-inline: 20px; }.analysis-brief footer { align-items: stretch; flex-direction: column; }.analysis-brief footer button { width: 100%; }.analysis-result dl,.analysis-notes { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion:reduce) { .spinner { animation-duration: 1.5s; }.analysis-skeleton::after { animation:none; }.analysis-genders button { transition-duration:.01ms!important; } }
</style>
