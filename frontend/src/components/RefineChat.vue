<template>
  <div class="w-full max-w-[680px] mx-auto">
    <!-- 对话气泡 -->
    <TransitionGroup
      name="bubble"
      tag="div"
      class="space-y-3 mb-5 max-h-[280px] overflow-y-auto scrollbar-thin"
      appear
    >
      <div
        v-for="(msg, idx) in history"
        :key="idx"
        class="flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="max-w-[80%] px-4 py-2.5 rounded-2xl text-[15px] leading-relaxed
                 transition-all duration-300"
          :class="msg.role === 'user'
            ? 'bg-[#0071e3] text-white rounded-br-md'
            : 'bg-[#e8e8ed] text-[#1d1d1f] rounded-bl-md'"
        >
          {{ msg.content }}
        </div>
      </div>
    </TransitionGroup>

    <!-- 输入区 -->
    <div
      class="flex items-center gap-3 bg-white/80 backdrop-blur-xl rounded-2xl
             shadow-[0_2px_12px_rgba(0,0,0,0.03)] border border-[#d2d2d7]/30
             px-5 py-3 transition-all duration-300
             focus-within:shadow-[0_4px_20px_rgba(0,0,0,0.06)]"
    >
      <span class="text-[15px] text-[#86868b] shrink-0">
        不满意？
      </span>
      <input
        v-model="feedback"
        type="text"
        maxlength="500"
        placeholder="说说你的想法…"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] placeholder-[#aeaeb2]
               outline-none"
        :disabled="disabled"
        @keydown.enter="handleSend"
      />
      <button
        type="button"
        class="shrink-0 w-9 h-9 flex items-center justify-center rounded-full
               transition-all duration-200"
        :class="canSend
          ? 'bg-[#0071e3] text-white hover:scale-105'
          : 'bg-[#e8e8ed] text-[#aeaeb2] cursor-not-allowed'"
        :disabled="!canSend || disabled"
        @click="handleSend"
      >
        <svg v-if="!loading" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
        </svg>
        <span v-else class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { ChatMessage } from '../types'

const props = defineProps<{
  history: ChatMessage[]
  loading: boolean
  disabled: boolean
}>()

const emit = defineEmits<{
  send: [feedback: string]
}>()

const feedback = ref('')

const canSend = computed(() => feedback.value.trim().length > 0 && !props.loading)

function handleSend() {
  if (!canSend.value) return
  emit('send', feedback.value.trim())
  feedback.value = ''
}
</script>

<style scoped>
.bubble-enter-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.bubble-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
</style>
