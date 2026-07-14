<template>
  <div class="compare-workspace">
    <form class="compare-brief" :aria-busy="loading" @submit.prevent="handleCompare">
      <span class="compare-brief__rule" aria-hidden="true" />
      <header><div><p>候选名字</p><span>填写 2–5 个名字进行横向评议</span></div><em>{{ validNames.length }} / 5</em></header>
      <div class="candidate-list">
        <div v-for="(candidate, index) in candidates" :key="candidate.id" class="candidate-field">
          <label :for="`candidate-${candidate.id}`">{{ String(index + 1).padStart(2, "0") }}</label>
          <input :id="`candidate-${candidate.id}`" v-model.trim="candidate.value" maxlength="10" :placeholder="`候选名字 ${index + 1}`" :aria-label="`候选名字 ${index + 1}`" :disabled="loading" @keydown.enter.prevent="handleCompare" />
          <button v-if="candidates.length > 2" type="button" :disabled="loading" :aria-label="`移除候选名字 ${index + 1}`" @click="removeCandidate(candidate.id)">
            <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5l10 10M15 5 5 15" /></svg>
          </button>
        </div>
        <button v-if="candidates.length < 5" type="button" class="add-candidate" :disabled="loading" @click="addCandidate">
          <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 4v12M4 10h12" /></svg>添加候选
        </button>
      </div>
      <footer>
        <fieldset :disabled="loading"><legend>性别</legend><div><button v-for="option in genders" :key="option.value" type="button" :class="{ 'is-active': gender === option.value }" :aria-pressed="gender === option.value" @click="gender = option.value">{{ option.label }}</button></div></fieldset>
        <div class="compare-submit"><span v-if="!loading">预计等待 10–20 秒</span><span v-else role="status">正在比较候选名字</span><button type="submit" :disabled="validNames.length < 2 || loading"><i v-if="loading" aria-hidden="true" />{{ loading ? "正在对比" : "开始对比" }}<svg v-if="!loading" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 6l4 4-4 4" /></svg></button></div>
      </footer>
    </form>

    <div v-if="loading" class="compare-skeleton" aria-label="正在比较名字" aria-busy="true"><article v-for="i in 3" :key="i"><b /><i /><span /></article></div>
    <div v-else-if="error" class="compare-state" role="alert"><p>{{ error }}</p><button type="button" @click="handleCompare">重新对比</button></div>

    <section v-else-if="result" class="ranking-list" aria-label="名字对比结果">
      <article v-for="ranking in result.rankings" :key="ranking.full_name" :class="{ 'is-first': ranking.rank === 1 }">
        <span class="ranking-card__rule" aria-hidden="true" />
        <header>
          <div class="ranking-position"><span>RANK</span><strong>{{ String(ranking.rank).padStart(2, "0") }}</strong></div>
          <div class="ranking-name"><p>{{ ranking.rank === 1 ? "首选推荐" : "候选评议" }}</p><h3>{{ ranking.full_name }}</h3></div>
          <div class="ranking-score" :aria-label="`综合评分 ${ranking.score} 分`"><strong>{{ ranking.score }}</strong><span>综合</span></div>
        </header>
        <p class="ranking-summary">{{ ranking.summary }}</p>
        <dl>
          <div v-for="metric in metrics(ranking)" :key="metric.label"><dt><span>{{ metric.label }}</span><em>{{ metric.value }}</em></dt><dd><i :style="{ transform: `scaleX(${metric.ratio})` }" /></dd></div>
        </dl>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { compareNames } from "../api";

interface Candidate { id: number; value: string }
interface Ranking { rank: number; full_name: string; score: number; summary: string; meaning_score: number; sound_score: number; wuxing_score: number; char_score: number }
interface ComparisonResult { rankings: Ranking[] }
const props = defineProps<{ authGuard?: () => boolean }>();
const genders = [{ label: "男", value: "male" }, { label: "女", value: "female" }];
let nextId = 3;
const candidates = ref<Candidate[]>([{ id: 1, value: "" }, { id: 2, value: "" }]);
const gender = ref("male");
const loading = ref(false);
const error = ref("");
const result = ref<ComparisonResult | null>(null);
const validNames = computed(() => candidates.value.map((item) => item.value.trim()).filter(Boolean));

function addCandidate() { if (candidates.value.length < 5) candidates.value.push({ id: nextId++, value: "" }); }
function removeCandidate(id: number) { if (candidates.value.length > 2) candidates.value = candidates.value.filter((item) => item.id !== id); }
const scoreRatio = (value: number) => Math.max(0, Math.min(1, Number(value || 0) / 10));
const metrics = (ranking: Ranking) => [
  { label: "寓意", value: ranking.meaning_score, ratio: scoreRatio(ranking.meaning_score) },
  { label: "音韵", value: ranking.sound_score, ratio: scoreRatio(ranking.sound_score) },
  { label: "五行", value: ranking.wuxing_score, ratio: scoreRatio(ranking.wuxing_score) },
  { label: "字形", value: ranking.char_score, ratio: scoreRatio(ranking.char_score) },
];
async function handleCompare() {
  if (validNames.value.length < 2 || loading.value) return;
  if (props.authGuard && !props.authGuard()) return;
  loading.value = true; error.value = ""; result.value = null;
  try { result.value = await compareNames(validNames.value, gender.value); }
  catch (cause: any) { error.value = cause.message || "对比失败"; }
  finally { loading.value = false; }
}
</script>

<style scoped>
.compare-workspace { max-width:820px;margin:0 auto }.compare-brief,.ranking-list article { position:relative;overflow:hidden;border:1px solid rgba(183,161,120,.36);border-radius:25px;background:linear-gradient(138deg,rgba(255,254,249,.92),rgba(244,240,230,.78));box-shadow:0 18px 50px rgba(58,50,38,.06) }.compare-brief__rule,.ranking-card__rule { position:absolute;top:0;left:0;width:66%;height:3px;background:linear-gradient(90deg,#32695d 0 38%,#b7a178 38% 76%,transparent) }.compare-brief>header { display:flex;align-items:flex-start;justify-content:space-between;gap:20px;padding:27px 30px 18px }.compare-brief>header p { font-family:"Songti SC","STSong",serif;font-size:22px }.compare-brief>header span { display:block;margin-top:5px;color:#827c72;font-size:11px }.compare-brief>header em { color:#9a4036;font-family:Georgia,serif;font-size:18px;font-style:normal }.candidate-list { display:grid;grid-template-columns:1fr 1fr;gap:11px;padding:0 30px 27px }.candidate-field { display:grid;grid-template-columns:30px minmax(0,1fr) 44px;min-height:60px;align-items:center;border:1px solid rgba(183,161,120,.34);border-radius:14px;background:rgba(255,255,255,.32);transition:border-color 180ms ease }.candidate-field:focus-within { border-color:#32695d }.candidate-field>label { color:#9d968b;font-family:Georgia,serif;font-size:10px;text-align:center }.candidate-list input { min-width:0;background:transparent;color:#292923;font-family:"Songti SC","STSong",serif;font-size:18px;outline:none }.candidate-list input::placeholder { color:#b4ada2 }.candidate-field button { display:grid;width:44px;height:44px;cursor:pointer;place-items:center;color:#a64235 }.candidate-field svg,.add-candidate svg,.compare-submit svg { width:18px;height:18px;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.5 }.add-candidate { display:flex;min-height:60px;cursor:pointer;align-items:center;justify-content:center;gap:8px;border:1px dashed rgba(50,105,93,.4);border-radius:14px;color:#32695d;font-size:12px }.compare-brief footer { display:flex;align-items:center;justify-content:space-between;gap:24px;border-top:1px solid rgba(183,161,120,.26);padding:20px 30px;background:rgba(235,231,220,.34) }.compare-brief fieldset { display:flex;align-items:center;gap:14px }.compare-brief legend { color:#777168;font-size:11px;float:left;margin-right:12px }.compare-brief fieldset div { display:flex;gap:4px }.compare-brief fieldset button { min-width:48px;min-height:44px;cursor:pointer;border-radius:999px;color:#777168;font-size:12px }.compare-brief fieldset button.is-active { background:rgba(50,105,93,.1);color:#32695d }.compare-submit { display:flex;align-items:center;gap:14px }.compare-submit>span { color:#928c81;font-size:10px }.compare-submit button,.compare-state button { display:inline-flex;min-width:142px;min-height:48px;cursor:pointer;align-items:center;justify-content:center;gap:10px;border-radius:999px;background:#32695d;padding:0 20px;color:white;font-size:13px }.compare-submit button:disabled { cursor:not-allowed;opacity:.42 }.compare-submit i { width:16px;height:16px;border:2px solid rgba(255,255,255,.35);border-top-color:white;border-radius:50%;animation:spin .8s linear infinite }
.compare-skeleton,.ranking-list { display:grid;gap:14px;margin-top:28px }.compare-skeleton article { position:relative;overflow:hidden;height:150px;border:1px solid rgba(183,161,120,.28);border-radius:22px;background:rgba(255,254,249,.7);padding:27px }.compare-skeleton article::after { position:absolute;inset:0;background:linear-gradient(105deg,transparent 30%,rgba(255,255,255,.7) 48%,transparent 65%);content:"";animation:shimmer 1.6s ease-in-out infinite;transform:translateX(-100%) }.compare-skeleton b,.compare-skeleton i,.compare-skeleton span { display:block;border-radius:999px;background:rgba(183,174,157,.26) }.compare-skeleton b { width:130px;height:28px }.compare-skeleton i { width:90%;height:10px;margin-top:22px }.compare-skeleton span { width:62%;height:9px;margin-top:10px }.compare-state { display:grid;min-height:220px;place-items:center;align-content:center;color:#a64235;text-align:center }.compare-state button { margin-top:15px;background:transparent;color:#a64235 }
.ranking-list article { padding:27px 30px 25px }.ranking-list article.is-first { border-color:rgba(50,105,93,.5);box-shadow:0 20px 55px rgba(50,105,93,.09) }.ranking-list header { display:grid;grid-template-columns:58px minmax(0,1fr) 58px;align-items:start;gap:18px }.ranking-position { display:flex;flex-direction:column }.ranking-position span,.ranking-name p { color:#918b80;font-size:8px;letter-spacing:.17em }.ranking-position strong { margin-top:8px;color:#b7a178;font-family:Georgia,serif;font-size:25px;font-weight:400 }.ranking-name h3 { margin-top:8px;font-family:"Songti SC","STSong",serif;font-size:32px;font-weight:400;letter-spacing:.07em }.ranking-score { display:grid;width:56px;height:61px;place-items:center;align-content:center;border:1px solid rgba(166,66,53,.55);color:#9b4035;transform:rotate(2deg) }.ranking-score strong { font-family:Georgia,serif;font-size:21px;font-weight:400 }.ranking-score span { margin-top:3px;font-size:7px;letter-spacing:.18em }.ranking-summary { margin:18px 0;color:#514e46;font-size:13px;line-height:1.8 }.ranking-list dl { display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding-top:17px;border-top:1px solid rgba(183,161,120,.26) }.ranking-list dt { display:flex;justify-content:space-between;color:#777168;font-size:10px }.ranking-list dt em { color:#32695d;font-family:Georgia,serif;font-style:normal }.ranking-list dd { overflow:hidden;height:3px;background:rgba(183,161,120,.22);margin-top:8px }.ranking-list dd i { display:block;width:100%;height:100%;transform-origin:left;background:#32695d }.compare-brief button:focus-visible,.compare-state button:focus-visible { outline:2px solid #32695d;outline-offset:3px }
@keyframes spin { to { transform:rotate(360deg) } }@keyframes shimmer { 55%,100% { transform:translateX(100%) } }
@media(max-width:700px){.candidate-list { grid-template-columns:1fr;padding-inline:20px }.compare-brief>header,.compare-brief footer,.ranking-list article { padding-inline:20px }.compare-brief footer { align-items:stretch;flex-direction:column }.compare-submit { align-items:stretch;flex-direction:column }.compare-submit button { width:100% }.ranking-list dl { grid-template-columns:1fr 1fr }.ranking-list header { grid-template-columns:46px minmax(0,1fr) 52px }.ranking-name h3 { font-size:27px }}
@media(prefers-reduced-motion:reduce){.compare-submit i{animation-duration:1.5s}.compare-skeleton article::after{animation:none}.candidate-field{transition-duration:.01ms!important}}
</style>
