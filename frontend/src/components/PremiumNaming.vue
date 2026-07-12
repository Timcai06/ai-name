<template>
  <div class="w-full max-w-[820px] mx-auto">
    <NameForm v-model="form" :loading="loading" :disabled="loading" estimate="10-15" @submit="handleSubmit" />
    <section v-if="showResults" class="mt-10">
      <PremiumResults :names="names" :state="state" :error-message="error" @retry="handleSubmit(form)" @favorite="handleFavorite" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import type { GenerateRequest, NameItem, LoadState } from '../types'
import { premiumNaming, addFavorite } from '../api'
import NameForm from './NameForm.vue'
import PremiumResults from './PremiumResults.vue'

const props = defineProps<{ authGuard?: () => boolean }>()

const form = reactive<GenerateRequest>({ surname:'', gender:'male', birthday:'', birth_time:'', style:'', expectations:'' })
const names = ref<NameItem[]>([])
const state = ref<LoadState>('idle')
const error = ref('')
const loading = ref(false)
const showResults = computed(() => state.value !== 'idle')

async function handleSubmit(data: GenerateRequest) {
  Object.assign(form, data)
  if (props.authGuard && !props.authGuard()) return
  loading.value=true; state.value='loading'; names.value=[]; error.value=''
  try { const r = await premiumNaming(data); names.value=r.names; state.value=r.names.length?'success':'empty' } catch(e:any){ error.value=e.message; state.value='error' } finally{loading.value=false}
}

async function handleFavorite(name: any) {
  try { await addFavorite(name.full_name, name) } catch(e:any){}
}
</script>
