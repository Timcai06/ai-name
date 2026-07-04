<template>
  <div class="min-h-screen bg-[#f5f5f7]">
    <div class="max-w-[500px] mx-auto px-6 py-16">
      <div class="flex items-center justify-between mb-10">
        <h1 class="text-[32px] font-semibold text-[#1d1d1f]">我的钱包</h1>
        <button class="text-[15px] text-[#0071e3] hover:underline" @click="$router.push('/')">← 返回</button>
      </div>

      <div v-if="msg" class="mb-4 px-4 py-3 rounded-xl text-[14px]" :class="msgType === 'ok' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'">{{ msg }}</div>

      <!-- 余额卡片 -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-[0_2px_12px_rgba(0,0,0,0.03)] mb-6 text-center">
        <p class="text-[13px] text-[#86868b] tracking-wide">当前余额</p>
        <p class="text-[48px] font-semibold text-[#1d1d1f] mt-2">¥{{ balance }}</p>
        <div v-if="vipLevel !== 'free'" class="mt-3">
          <span class="px-3 py-1 rounded-full text-[13px] font-medium"
            :class="vipLevel === 'svip' ? 'bg-yellow-100 text-yellow-700' : 'bg-[#0071e3]/10 text-[#0071e3]'">
            {{ vipLevel.toUpperCase() }}
          </span>
          <p class="text-[13px] text-[#aeaeb2] mt-1">到期 {{ vipExpire?.slice(0, 10) || '' }}</p>
        </div>
      </div>

      <!-- 充值 -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] mb-6">
        <p class="text-[15px] font-medium text-[#1d1d1f] mb-4">充值</p>
        <div class="grid grid-cols-3 gap-3">
          <button v-for="a in [10,20,50]" :key="a" class="py-3 bg-[#f5f5f7] rounded-xl text-[17px] font-medium hover:bg-[#e8e8ed] transition-colors" @click="handleRecharge(a)">¥{{ a }}</button>
        </div>
      </div>

      <!-- 买VIP -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] mb-6">
        <p class="text-[15px] font-medium text-[#1d1d1f] mb-4">开通会员</p>
        <div class="flex gap-3">
          <button class="flex-1 py-3 bg-[#0071e3]/10 text-[#0071e3] rounded-xl font-medium hover:bg-[#0071e3]/20 transition-colors" :disabled="vipLevel==='vip'" @click="handleBuyVip('vip')">
            VIP ¥15/月<br><span class="text-[12px] opacity-60">10次/天</span>
          </button>
          <button class="flex-1 py-3 bg-yellow-100 text-yellow-700 rounded-xl font-medium hover:bg-yellow-200 transition-colors" :disabled="vipLevel==='svip'" @click="handleBuyVip('svip')">
            SVIP ¥30/月<br><span class="text-[12px] opacity-60">30次/天</span>
          </button>
        </div>
      </div>

      <!-- 交易记录 -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)]">
        <p class="text-[15px] font-medium text-[#1d1d1f] mb-4">交易记录</p>
        <div v-if="txs.length===0" class="text-[14px] text-[#aeaeb2] text-center py-4">暂无记录</div>
        <div v-for="t in txs" :key="t.id" class="flex justify-between py-2 border-b border-[#d2d2d7]/20 last:border-0">
          <div><span class="text-[14px] text-[#1d1d1f]">{{ t.detail }}</span><span class="ml-2 text-[13px] text-[#aeaeb2]">{{ formatTime(t.created_at) }}</span></div>
          <span class="text-[14px] font-medium" :class="t.amount>0?'text-green-600':'text-[#1d1d1f]'">{{ t.amount>0?'+':'' }}{{ t.amount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getBalance, recharge, buyVip, getTransactions } from '../api'

const balance = ref(0)
const vipLevel = ref('free')
const vipExpire = ref<string|null>(null)
const txs = ref<any[]>([])
const msg = ref('')
const msgType = ref('ok')
let msgTimer: any = null

function show(msgTxt: string, type: string) { msg.value=msgTxt; msgType.value=type; clearTimeout(msgTimer); msgTimer=setTimeout(()=>msg.value='',5000) }
function formatTime(s:string){return s?.replace('T',' ').slice(0,16)||''}

async function load() {
  try { const b:any = await getBalance(); balance.value=b.balance; vipLevel.value=b.vip_level; vipExpire.value=b.vip_expire_at } catch(e:any){}
  try { const t:any = await getTransactions(); txs.value = t.items } catch(e:any){}
}
async function handleRecharge(a:number) { try { const r:any = await recharge(a); balance.value=r.balance; show('充值成功','ok'); load() } catch(e:any){ show(e.message,'err') } }
async function handleBuyVip(lvl:string) { try { const r:any = await buyVip(lvl); balance.value=r.balance; vipLevel.value=lvl; vipExpire.value=r.vip_expire_at; show('开通成功','ok'); load() } catch(e:any){ show(e.message,'err') } }

onMounted(load)
</script>
