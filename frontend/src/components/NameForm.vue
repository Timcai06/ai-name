<template>
  <div
    class="w-full max-w-[680px] mx-auto bg-white/80 backdrop-blur-xl rounded-2xl
           shadow-[0_4px_24px_rgba(0,0,0,0.04)] border border-[#d2d2d7]/30
           transition-all duration-500"
  >
    <!-- 姓氏 -->
    <div class="flex items-center px-6 py-5 border-b border-[#d2d2d7]/40">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide">
        姓氏
      </label>
      <input
        v-model="form.surname"
        type="text"
        maxlength="5"
        placeholder="请输入姓氏"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] placeholder-[#aeaeb2]
               outline-none"
        :disabled="disabled"
        @input="emit('update:modelValue', { ...form })"
      />
    </div>

    <!-- 性别 -->
    <div class="flex items-center px-6 py-5 border-b border-[#d2d2d7]/40">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide">
        性别
      </label>
      <div class="flex gap-6">
        <button
          v-for="opt in genderOptions"
          :key="opt.value"
          type="button"
          class="flex items-center gap-2 text-[17px] transition-colors duration-200"
          :class="form.gender === opt.value ? 'text-[#0071e3]' : 'text-[#1d1d1f]'"
          :disabled="disabled"
          @click="selectGender(opt.value)"
        >
          <span
            class="w-[18px] h-[18px] rounded-full border-2 flex items-center justify-center
                   transition-all duration-200"
            :class="form.gender === opt.value
              ? 'border-[#0071e3] bg-[#0071e3]'
              : 'border-[#d2d2d7]'"
          >
            <span
              v-if="form.gender === opt.value"
              class="w-[6px] h-[6px] rounded-full bg-white"
            />
          </span>
          {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- 生日 -->
    <div class="flex items-center px-6 py-5 border-b border-[#d2d2d7]/40">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide">
        生日
      </label>
      <input
        v-model="form.birthday"
        type="date"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] outline-none
               [color-scheme:light]"
        :disabled="disabled"
        @input="emit('update:modelValue', { ...form })"
      />
    </div>

    <!-- 时辰 -->
    <div class="flex items-center px-6 py-5 border-b border-[#d2d2d7]/40">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide">
        时辰
      </label>
      <select
        v-model="form.birth_time"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] outline-none cursor-pointer
               appearance-none"
        :disabled="disabled"
        @change="emit('update:modelValue', { ...form })"
      >
        <option value="" class="text-[#aeaeb2]">请选择（可选）</option>
        <option v-for="t in timeOptions" :key="t" :value="t">{{ t }}</option>
      </select>
    </div>

    <!-- 期望风格 -->
    <div class="flex items-center px-6 py-5 border-b border-[#d2d2d7]/40">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide">
        风格
      </label>
      <input
        v-model="form.style"
        type="text"
        maxlength="50"
        placeholder="如：文雅书香、大气磅礴（可选）"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] placeholder-[#aeaeb2]
               outline-none"
        :disabled="disabled"
        @input="emit('update:modelValue', { ...form })"
      />
    </div>

    <!-- 更多期望 -->
    <div class="flex items-start px-6 py-5">
      <label class="w-[100px] shrink-0 text-[13px] font-medium text-[#86868b] tracking-wide mt-1">
        期望
      </label>
      <textarea
        v-model="form.expectations"
        maxlength="200"
        rows="3"
        placeholder="说说你对名字的期望，如寓意、字数、避讳字等（可选）"
        class="flex-1 bg-transparent text-[17px] text-[#1d1d1f] placeholder-[#aeaeb2]
               outline-none resize-none leading-relaxed"
        :disabled="disabled"
        @input="emit('update:modelValue', { ...form })"
      />
    </div>

    <!-- 提交按钮 -->
    <div class="px-6 py-5 flex flex-col items-center gap-2">
      <button
        type="button"
        class="px-10 py-3 bg-[#0071e3] text-white text-[17px] font-medium
               rounded-full transition-all duration-300
               hover:scale-[1.02] hover:shadow-[0_4px_16px_rgba(0,113,227,0.35)]
               active:scale-[0.98]
               disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100
               disabled:hover:shadow-none"
        :disabled="disabled || !canSubmit"
        @click="handleSubmit"
      >
        <span v-if="!loading">生成名字</span>
        <span v-else class="flex items-center gap-2">
          <span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full
                       animate-spin" />
          生成中…
        </span>
      </button>
      <p v-if="!loading" class="text-[13px] text-[#aeaeb2]">预计等待 {{ estimate || '5-10' }} 秒</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import type { Gender, GenerateRequest } from '../types'

const props = defineProps<{
  modelValue: GenerateRequest
  loading: boolean
  disabled: boolean
  estimate?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: GenerateRequest]
  submit: [value: GenerateRequest]
}>()

const genderOptions = [
  { label: '男', value: 'male' as Gender },
  { label: '女', value: 'female' as Gender },
]

const timeOptions = [
  '子时', '丑时', '寅时', '卯时', '辰时', '巳时',
  '午时', '未时', '申时', '酉时', '戌时', '亥时',
]

const form = reactive<GenerateRequest>({ ...props.modelValue })

const canSubmit = computed(() => form.surname.trim().length > 0 && form.gender)

function selectGender(g: Gender) {
  form.gender = g
  emit('update:modelValue', { ...form })
}

function handleSubmit() {
  if (canSubmit.value) {
    emit('submit', { ...form })
  }
}
</script>
