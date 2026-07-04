<template>
  <div class="min-h-screen bg-[#f5f5f7]">
    <div class="max-w-[680px] mx-auto px-6 py-16">
      <div class="flex items-center justify-between mb-10">
        <h1 class="text-[32px] font-semibold text-[#1d1d1f]">收藏夹</h1>
        <button class="text-[15px] text-[#0071e3] hover:underline" @click="$router.push('/')">← 返回</button>
      </div>

      <div v-if="loading" class="text-center py-10 text-[15px] text-[#86868b]">加载中…</div>
      <div v-else-if="items.length===0" class="text-center py-20">
        <p class="text-[17px] text-[#86868b]">还没有收藏</p>
      </div>
      <div v-else class="space-y-3">
        <div v-for="f in items" :key="f.id" class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] flex items-center justify-between">
          <div>
            <h3 class="text-[20px] font-semibold text-[#1d1d1f]">{{ f.full_name }}</h3>
            <p class="text-[14px] text-[#86868b] mt-1">{{ f.name_data?.meaning || '' }}</p>
            <p class="text-[13px] text-[#aeaeb2] mt-1">五行 {{ f.name_data?.wuxing }} · 出处 {{ f.name_data?.source }}</p>
          </div>
          <button class="text-[#ff3b30] text-[14px] hover:underline shrink-0" @click="handleRemove(f.id)">取消收藏</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFavorites, removeFavorite } from '../api'

const items = ref<any[]>([])
const loading = ref(true)

async function load() { try { const r:any = await getFavorites(); items.value=r.items } catch{} finally{loading.value=false} }
async function handleRemove(id:number) { try { await removeFavorite(id); items.value=items.value.filter(i=>i.id!==id) } catch{} }

onMounted(load)
</script>
