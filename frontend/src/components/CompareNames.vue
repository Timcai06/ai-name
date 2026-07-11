<template>
  <div class="w-full max-w-[820px] mx-auto">
    <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_4px_24px_rgba(0,0,0,0.04)] mb-8">
      <div class="flex gap-2 flex-wrap mb-4">
        <div v-for="(n,i) in names" :key="i" class="flex items-center gap-1 bg-[#f5f5f7] rounded-full px-3 py-1.5">
          <input v-model="names[i]" maxlength="10" class="w-20 bg-transparent text-[15px] outline-none" :placeholder="'名字'+(i+1)" :disabled="loading" @keydown.enter="handleCompare" />
          <button v-if="names.length>2" class="text-[#aeaeb2] hover:text-[#ff3b30] text-[14px]" @click="names.splice(i,1)">×</button>
        </div>
        <button v-if="names.length<5" class="text-[14px] text-[#0071e3] hover:underline" @click="names.push('')">+ 添加</button>
      </div>
      <div class="flex items-center justify-between">
        <div class="flex gap-3">
          <button v-for="g in [{v:'male',l:'男'},{v:'female',l:'女'}]" :key="g.v" class="text-[15px]" :class="gender===g.v?'text-[#0071e3] font-medium':'text-[#86868b]'" @click="gender=g.v">{{ g.l }}</button>
        </div>
        <div class="flex flex-col items-center">
          <button class="px-6 py-2.5 bg-[#0071e3] text-white rounded-full font-medium hover:scale-[1.02] transition-all disabled:opacity-50" :disabled="names.filter(n=>n.trim()).length<2||loading" @click="handleCompare">{{loading?'对比中…':'开始对比'}}</button>
          <p v-if="!loading" class="text-[12px] text-[#aeaeb2] mt-1">预计 10-20 秒</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="bg-white/80 rounded-2xl p-8 animate-pulse"><div class="h-8 w-32 bg-[#e8e8ed] rounded mb-4"/></div>
    <div v-else-if="error" class="text-center py-10"><p class="text-[#ff3b30]">{{error}}</p></div>
    <div v-else-if="result" class="space-y-3">
      <div v-for="r in result.rankings" :key="r.full_name" class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] flex items-center gap-5">
        <div class="text-center shrink-0 w-16">
          <p class="text-[32px] font-semibold text-[#0071e3]">{{ r.score }}</p>
          <p class="text-[12px] text-[#86868b]">#{{ r.rank }}</p>
        </div>
        <div class="flex-1">
          <h3 class="text-[20px] font-semibold text-[#1d1d1f]">{{ r.full_name }}</h3>
          <p class="text-[14px] text-[#3a3a3c] mt-1">{{ r.summary }}</p>
          <div class="flex gap-4 mt-2 text-[13px] text-[#aeaeb2]">
            <span>寓意 {{ r.meaning_score }}</span><span>音韵 {{ r.sound_score }}</span><span>五行 {{ r.wuxing_score }}</span><span>字形 {{ r.char_score }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { compareNames } from '../api'

const props = defineProps<{ authGuard?: () => boolean }>()

const names = ref(['',''])
const gender = ref('male')
const loading = ref(false)
const error = ref('')
const result = ref<any>(null)

async function handleCompare() {
  const list = names.value.map(n=>n.trim()).filter(Boolean)
  if (list.length<2) return
  if (props.authGuard && !props.authGuard()) return
  loading.value=true; error.value=''; result.value=null
  try { result.value = await compareNames(list, gender.value) } catch(e:any){ error.value=e.message } finally{loading.value=false}
}
</script>
