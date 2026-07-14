<template>
  <WorkspaceDrawer
    :open="open"
    title="取名历史"
    kicker="NAMING ARCHIVE"
    :description="`共 ${total} 条记录`"
    width="700px"
    @close="emit('close')"
  >
    <div class="archive-shell">
      <div class="archive-toolbar">
        <label>
          <span class="sr-only">筛选记录类型</span>
          <select v-model="filter" aria-label="筛选记录类型" @change="load">
            <option value="">全部类型</option>
            <option value="naming">取名</option>
            <option value="analyze">分析</option>
            <option value="compare">对比</option>
            <option value="premium">精品</option>
          </select>
        </label>
        <div class="archive-actions">
          <button v-if="items.length && !batchMode" type="button" @click="batchMode = true">批量选择</button>
          <button v-if="batchMode" type="button" class="danger" :disabled="!selected.length || batchBusy" @click="batchDelete">
            {{ batchBusy ? "正在删除…" : `删除所选 ${selected.length}` }}
          </button>
          <button v-if="batchMode" type="button" @click="cancelBatch">取消</button>
          <button v-if="items.length && !batchMode" type="button" class="danger" :disabled="clearBusy" @click="clear">
            {{ clearBusy ? "正在清空…" : "清空全部" }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="archive-loading" aria-label="正在整理名笺" aria-busy="true">
        <article v-for="i in 3" :key="i"><i /><b /><span /></article>
      </div>
      <div v-else-if="error" class="archive-state archive-state--error" role="alert">
        <p>{{ error }}</p><button type="button" @click="load">重新加载</button>
      </div>
      <div v-else-if="!items.length" class="archive-state">
        <svg viewBox="0 0 48 48" aria-hidden="true"><path d="M13 8h19l5 5v27H13V8Z"/><path d="M32 8v6h6M19 22h12M19 28h9"/></svg>
        <h3>还没有取名记录</h3>
        <p>完成一次取名后，结果会收进这里。</p>
        <button type="button" @click="emit('close')">返回工作台</button>
      </div>

      <div v-else class="archive-list">
        <article
          v-for="item in items"
          :key="item.id"
          class="archive-card"
          :class="{ 'archive-card--selected': selected.includes(item.id) }"
        >
          <span class="archive-card__rule" aria-hidden="true" />
          <div class="archive-card__top">
            <button
              v-if="batchMode"
              type="button"
              class="archive-check"
              :class="{ 'is-selected': selected.includes(item.id) }"
              :aria-pressed="selected.includes(item.id)"
              :aria-label="`${selected.includes(item.id) ? '取消选择' : '选择'} ${item.surname} 的记录`"
              @click="toggleSelect(item.id)"
            >
              <svg viewBox="0 0 20 20" aria-hidden="true"><path d="m5 10 3 3 7-7" /></svg>
            </button>

            <button
              type="button"
              class="archive-card__toggle"
              :aria-expanded="expanded === item.id"
              :aria-controls="`history-detail-${item.id}`"
              @click="expanded = expanded === item.id ? null : item.id"
            >
              <span class="archive-card__copy">
                <span class="archive-card__eyebrow">{{ recordLabel(item.record_type) }} · {{ formatTime(item.created_at) }}</span>
                <strong>{{ item.surname }}</strong>
                <span class="archive-card__meta">{{ item.gender === "male" ? "男" : "女" }} · {{ item.names.length }} 个推荐名字</span>
              </span>
              <svg class="archive-chevron" :class="{ 'is-open': expanded === item.id }" viewBox="0 0 20 20" aria-hidden="true"><path d="m5.5 7.5 4.5 4.5 4.5-4.5" /></svg>
            </button>

            <button
              v-if="!batchMode"
              type="button"
              class="archive-remove"
              :disabled="deleting.includes(item.id)"
              :aria-label="`删除 ${item.surname} 的历史记录`"
              @click="remove(item.id)"
            >
              <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 6h12M8 3h4l1 3H7l1-3ZM6 6l1 11h6l1-11M9 9v5M11 9v5" /></svg>
            </button>
          </div>

          <Transition name="archive-detail">
            <div v-if="expanded === item.id" :id="`history-detail-${item.id}`" class="archive-card__details">
              <section v-for="(name, index) in item.names" :key="name.full_name">
                <span>{{ String(index + 1).padStart(2, "0") }}</span>
                <div><h4>{{ name.full_name }}</h4><p>{{ name.meaning }}</p></div>
                <strong v-if="name.score" :aria-label="`评分 ${name.score}`">{{ name.score }}</strong>
              </section>
            </div>
          </Transition>
        </article>
      </div>
    </div>
  </WorkspaceDrawer>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import WorkspaceDrawer from "./WorkspaceDrawer.vue";
import { batchDeleteHistory, clearAllHistory, deleteHistory, getHistory } from "../api";
import type { HistoryItem } from "../types";

const props = defineProps<{ open: boolean }>();
const emit = defineEmits<{ close: [] }>();
const items = ref<HistoryItem[]>([]);
const total = ref(0);
const loading = ref(true);
const error = ref("");
const filter = ref("");
const expanded = ref<number | null>(null);
const batchMode = ref(false);
const selected = ref<number[]>([]);
const deleting = ref<number[]>([]);
const batchBusy = ref(false);
const clearBusy = ref(false);

watch(() => props.open, (value) => { if (value) load(); }, { immediate: true });

const formatTime = (value: string) => value?.replace("T", " ").slice(0, 16) || "";
const recordLabel = (value: string) => ({ naming: "智能取名", analyze: "名字分析", compare: "名字对比", premium: "精品取名" }[value] || "取名记录");
function toggleSelect(id: number) { const index = selected.value.indexOf(id); index >= 0 ? selected.value.splice(index, 1) : selected.value.push(id); }
function cancelBatch() { batchMode.value = false; selected.value = []; }
async function load() {
  loading.value = true; error.value = ""; expanded.value = null;
  try { const result = await getHistory(0, 50, filter.value || undefined); items.value = result.items; total.value = result.total; }
  catch (cause: any) { error.value = cause.message || "历史记录加载失败"; }
  finally { loading.value = false; }
}
async function remove(id: number) {
  if (deleting.value.includes(id)) return;
  deleting.value = [...deleting.value, id]; error.value = "";
  try { await deleteHistory(id); items.value = items.value.filter((item) => item.id !== id); total.value = Math.max(0, total.value - 1); }
  catch (cause: any) { error.value = cause.message || "删除失败"; }
  finally { deleting.value = deleting.value.filter((value) => value !== id); }
}
async function clear() {
  if (!confirm("确定清空全部历史吗？")) return;
  clearBusy.value = true; error.value = "";
  try { await clearAllHistory(); items.value = []; total.value = 0; }
  catch (cause: any) { error.value = cause.message || "清空失败"; }
  finally { clearBusy.value = false; }
}
async function batchDelete() {
  if (!selected.value.length || batchBusy.value) return;
  batchBusy.value = true; error.value = ""; const count = selected.value.length;
  try { await batchDeleteHistory(selected.value); items.value = items.value.filter((item) => !selected.value.includes(item.id)); total.value = Math.max(0, total.value - count); cancelBatch(); }
  catch (cause: any) { error.value = cause.message || "批量删除失败"; }
  finally { batchBusy.value = false; }
}
</script>

<style scoped>
.archive-shell { min-height: 480px; }
.archive-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin-bottom: 22px; }
.archive-toolbar select { min-height: 44px; cursor: pointer; border: 1px solid #d9d1c3; border-radius: 999px; background: rgba(255,255,255,.55); padding: 0 38px 0 16px; color: #4f4c45; font-size: 13px; outline: none; }
.archive-toolbar select:focus-visible, .archive-actions button:focus-visible, .archive-card button:focus-visible, .archive-state button:focus-visible { outline: 2px solid #32695d; outline-offset: 3px; }
.archive-actions { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 2px; }
.archive-actions button { min-height: 44px; cursor: pointer; padding: 0 10px; color: #666158; font-size: 12px; }
.archive-actions button.danger { color: #a64235; }
.archive-actions button:disabled, .archive-remove:disabled { cursor: wait; opacity: .45; }
.archive-list, .archive-loading { display: grid; gap: 12px; }
.archive-card { position: relative; overflow: hidden; border: 1px solid rgba(183,161,120,.34); border-radius: 20px; background: linear-gradient(135deg,rgba(255,254,249,.9),rgba(242,238,228,.72)); transition: border-color 180ms ease, box-shadow 180ms ease; }
.archive-card:hover, .archive-card--selected { border-color: rgba(50,105,93,.45); box-shadow: 0 12px 30px rgba(58,50,38,.07); }
.archive-card__rule { position: absolute; top: 0; left: 0; width: 90px; height: 2px; background: #32695d; }
.archive-card__top { display: flex; align-items: center; gap: 6px; padding: 12px 12px 12px 18px; }
.archive-card__toggle { display: flex; min-width: 0; min-height: 64px; flex: 1; cursor: pointer; align-items: center; justify-content: space-between; gap: 14px; text-align: left; }
.archive-card__copy { display: flex; min-width: 0; flex-direction: column; }
.archive-card__eyebrow { color: #8e887e; font-size: 9px; letter-spacing: .13em; }
.archive-card__copy strong { margin-top: 7px; font-family: "Songti SC","STSong",serif; font-size: 25px; font-weight: 400; letter-spacing: .06em; }
.archive-card__meta { margin-top: 4px; color: #77736a; font-size: 11px; }
.archive-chevron { width: 18px; height: 18px; flex: 0 0 auto; fill: none; stroke: #77736a; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.5; transition: transform 180ms ease; }
.archive-chevron.is-open { transform: rotate(180deg); }
.archive-check, .archive-remove { display: grid; width: 44px; height: 44px; flex: 0 0 44px; cursor: pointer; place-items: center; border-radius: 50%; }
.archive-check { border: 1px solid #c8c0b2; color: transparent; }
.archive-check.is-selected { border-color: #32695d; background: #32695d; color: white; }
.archive-check svg, .archive-remove svg { width: 18px; height: 18px; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.5; }
.archive-remove { color: #a64235; transition: background-color 180ms ease; }
.archive-remove:hover { background: rgba(166,66,53,.08); }
.archive-card__details { margin: 0 18px; padding: 2px 0 18px; border-top: 1px solid rgba(183,161,120,.25); }
.archive-card__details section { display: grid; grid-template-columns: 28px minmax(0,1fr) auto; gap: 12px; padding-top: 16px; }
.archive-card__details section > span { padding-top: 4px; color: #aaa296; font-family: Georgia,serif; font-size: 10px; }
.archive-card__details h4 { font-family: "Songti SC","STSong",serif; font-size: 20px; font-weight: 400; }
.archive-card__details p { margin-top: 4px; color: #69645b; font-size: 12px; line-height: 1.7; }
.archive-card__details section > strong { color: #32695d; font-family: Georgia,serif; font-size: 20px; font-weight: 400; }
.archive-loading article { position: relative; overflow: hidden; height: 104px; border: 1px solid rgba(183,161,120,.25); border-radius: 20px; background: rgba(255,255,255,.42); padding: 23px; }
.archive-loading article::after { position: absolute; inset: 0; background: linear-gradient(105deg,transparent 30%,rgba(255,255,255,.65) 48%,transparent 65%); content: ""; animation: archive-shimmer 1.6s ease-in-out infinite; transform: translateX(-100%); }
.archive-loading i, .archive-loading b, .archive-loading span { display: block; border-radius: 999px; background: rgba(183,174,157,.27); }
.archive-loading i { width: 130px; height: 8px; }.archive-loading b { width: 100px; height: 23px; margin-top: 12px; }.archive-loading span { width: 180px; height: 8px; margin-top: 9px; }
.archive-state { display: grid; min-height: 300px; place-items: center; align-content: center; text-align: center; }
.archive-state svg { width: 46px; height: 46px; fill: none; stroke: #b7a178; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.2; }
.archive-state h3 { margin-top: 18px; font-family: "Songti SC","STSong",serif; font-size: 24px; font-weight: 400; }.archive-state p { margin-top: 7px; color: #77736a; font-size: 13px; }.archive-state button { min-height: 44px; margin-top: 18px; cursor: pointer; color: #32695d; font-size: 13px; }
.archive-state--error { color: #a64235; }.archive-state--error button { color: #a64235; }
.archive-detail-enter-active,.archive-detail-leave-active { transition: opacity 180ms ease,transform 180ms ease; }.archive-detail-enter-from,.archive-detail-leave-to { opacity: 0; transform: translateY(-5px); }
@keyframes archive-shimmer { 55%,100% { transform: translateX(100%); } }
@media (max-width: 640px) { .archive-toolbar { align-items: stretch; flex-direction: column; }.archive-actions { justify-content: flex-start; }.archive-card__top { padding-left: 12px; }.archive-card__copy strong { font-size: 22px; } }
@media (prefers-reduced-motion: reduce) { .archive-loading article::after { animation: none; }.archive-card,.archive-chevron,.archive-detail-enter-active,.archive-detail-leave-active { transition-duration: .01ms !important; } }
</style>
