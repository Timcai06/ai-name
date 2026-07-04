<template>
  <div class="w-full max-w-[680px] mx-auto">
    <div v-if="state==='idle'" class="text-center py-20"><p class="text-[17px] text-[#aeaeb2]">输入信息后点击「生成名字」</p></div>

    <div v-if="state==='loading'" class="space-y-4">
      <div v-for="i in 3" :key="i" class="bg-white/80 rounded-2xl p-6 animate-pulse"><div class="h-7 w-24 bg-[#e8e8ed] rounded mb-3"/><div class="h-4 w-full bg-[#e8e8ed] rounded mb-2"/><div class="h-4 w-2/3 bg-[#e8e8ed] rounded"/></div>
    </div>

    <div v-if="state==='empty'" class="text-center py-16"><p class="text-[17px] text-[#86868b]">暂未生成到合适的名字</p></div>
    <div v-if="state==='error'" class="text-center py-16"><p class="text-[17px] text-[#ff3b30] mb-3">{{errorMessage}}</p><button class="text-[15px] text-[#0071e3] hover:underline" @click="emit('retry')">重试</button></div>

    <TransitionGroup v-if="state==='success'" name="card" tag="div" class="space-y-4" appear>
      <div v-for="(name, idx) in names" :key="name.full_name"
        class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] border border-[#d2d2d7]/30"
        :style="{ transitionDelay: `${idx * 0.1}s` }">
        <!-- 头部 -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-[28px] font-semibold text-[#1d1d1f]">{{ name.full_name }}</h3>
          <button class="text-[14px] text-[#aeaeb2] hover:text-[#0071e3] transition-colors" @click="emit('favorite', name)">收藏</button>
        </div>

        <!-- 寓意 -->
        <p class="text-[15px] text-[#3a3a3c] leading-relaxed mb-4">{{ name.meaning }}</p>

        <!-- 属性标签 -->
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="px-3 py-1 bg-[#f5f5f7] rounded-full text-[13px] text-[#86868b]">五行 {{ name.wuxing }}</span>
          <span class="px-3 py-1 bg-[#f5f5f7] rounded-full text-[13px] text-[#86868b]">出处 {{ name.source }}</span>
          <span v-if="name.sound_analysis" class="px-3 py-1 bg-[#f5f5f7] rounded-full text-[13px] text-[#86868b]">音律分析</span>
          <span v-if="name.char_analysis" class="px-3 py-1 bg-[#f5f5f7] rounded-full text-[13px] text-[#86868b]">字形分析</span>
          <span class="px-3 py-1 rounded-full text-[13px] font-medium"
            :class="(name.popularity||'').includes('低') ? 'bg-green-100 text-green-700' : (name.popularity||'').includes('高') ? 'bg-red-100 text-red-600' : 'bg-yellow-100 text-yellow-700'">
            重名{{ name.popularity || '未知' }}
          </span>
        </div>

        <!-- 八字 -->
        <div v-if="name.bazi" class="bg-[#f5f5f7] rounded-xl p-4 mb-3">
          <p class="text-[13px] font-medium text-[#86868b] mb-1">八字分析</p>
          <p class="text-[14px] text-[#3a3a3c] leading-relaxed">{{ name.bazi }}</p>
        </div>

        <!-- 音律 -->
        <div v-if="name.sound_analysis" class="bg-[#f5f5f7] rounded-xl p-4 mb-3">
          <p class="text-[13px] font-medium text-[#86868b] mb-1">音律分析</p>
          <p class="text-[14px] text-[#3a3a3c] leading-relaxed">{{ name.sound_analysis }}</p>
        </div>

        <!-- 字形 -->
        <div v-if="name.char_analysis" class="bg-[#f5f5f7] rounded-xl p-4 mb-3">
          <p class="text-[13px] font-medium text-[#86868b] mb-1">字形分析</p>
          <p class="text-[14px] text-[#3a3a3c] leading-relaxed">{{ name.char_analysis }}</p>
        </div>

        <!-- 命名故事 -->
        <div v-if="name.story" class="bg-gradient-to-r from-[#f5f5f7] to-white rounded-xl p-4 border border-[#0071e3]/10">
          <p class="text-[13px] font-medium text-[#0071e3] mb-1">命名故事</p>
          <p class="text-[14px] text-[#3a3a3c] leading-relaxed italic">{{ name.story }}</p>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import type { LoadState, NameItem } from '../types'

defineProps<{ names: NameItem[]; state: LoadState; errorMessage: string }>()
const emit = defineEmits<{ retry: []; favorite: [name: NameItem] }>()
</script>

<style scoped>
.card-enter-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.card-enter-from { opacity: 0; transform: translateY(8px); }
</style>
