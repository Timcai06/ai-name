<template>
  <div class="skeleton-list" aria-label="正在生成推荐名字" aria-busy="true">
    <article v-for="item in count" :key="item" class="skeleton-card">
      <span class="skeleton-card__rule" />
      <div class="skeleton-card__header">
        <div>
          <i class="skeleton-line skeleton-line--eyebrow" />
          <i class="skeleton-line skeleton-line--name" />
        </div>
        <i class="skeleton-seal" />
      </div>
      <div class="skeleton-copy">
        <i class="skeleton-line" />
        <i class="skeleton-line skeleton-line--short" />
      </div>
      <div class="skeleton-meta">
        <i /><i /><i />
      </div>
    </article>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ count?: number }>(), { count: 3 });
</script>

<style scoped>
.skeleton-list { display: grid; gap: 20px; }
.skeleton-card { position: relative; overflow: hidden; border: 1px solid rgba(183, 161, 120, 0.3); border-radius: 28px; background: linear-gradient(138deg, rgba(255, 254, 249, 0.88), rgba(245, 241, 231, 0.82)); padding: 30px 32px 24px; }
.skeleton-card::after { position: absolute; inset: 0; background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,.7) 46%, transparent 62%); content: ""; transform: translateX(-100%); animation: paper-shimmer 1.65s ease-in-out infinite; }
.skeleton-card__rule { position: absolute; top: 0; left: 0; width: 64%; height: 3px; background: linear-gradient(90deg, rgba(50,105,93,.62) 0 38%, rgba(183,161,120,.5) 38% 100%); }
.skeleton-card__header { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; }
.skeleton-card__header > div { flex: 1; }
.skeleton-line, .skeleton-meta i, .skeleton-seal { display: block; border-radius: 999px; background: rgba(183, 174, 157, 0.26); }
.skeleton-line { width: 100%; height: 12px; }
.skeleton-line--eyebrow { width: 132px; height: 8px; }
.skeleton-line--name { width: 170px; height: 42px; margin-top: 17px; border-radius: 5px; }
.skeleton-seal { flex: 0 0 58px; height: 64px; border-radius: 0; background: rgba(166, 66, 53, 0.1); }
.skeleton-copy { display: grid; gap: 10px; margin-top: 24px; }
.skeleton-line--short { width: 68%; }
.skeleton-meta { display: grid; grid-template-columns: .65fr 1.7fr .55fr; gap: 16px; margin-top: 24px; padding: 19px 0 4px; border-top: 1px solid rgba(183,161,120,.24); }
.skeleton-meta i { height: 30px; border-radius: 4px; }
@keyframes paper-shimmer { 55%, 100% { transform: translateX(100%); } }
@media (max-width: 640px) {
  .skeleton-card { border-radius: 20px; padding: 24px 20px 20px; }
  .skeleton-line--name { width: 140px; height: 36px; }
  .skeleton-seal { flex-basis: 50px; height: 56px; }
  .skeleton-meta { grid-template-columns: 1fr 1fr; }
  .skeleton-meta i:nth-child(2) { grid-column: 1 / -1; grid-row: 2; }
}
@media (prefers-reduced-motion: reduce) { .skeleton-card::after { animation: none; } }
</style>
