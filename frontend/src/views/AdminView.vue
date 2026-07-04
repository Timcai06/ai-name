<template>
  <div class="min-h-screen bg-[#f5f5f7]">
    <div class="max-w-[1100px] mx-auto px-6 py-12">
      <!-- 头部 -->
      <div class="flex items-center justify-between mb-10">
        <div>
          <h1 class="text-[32px] font-semibold text-[#1d1d1f] tracking-tight">
            管理后台
          </h1>
          <p class="mt-1 text-[15px] text-[#86868b]">
            {{ authStore.username }} · 管理员
          </p>
        </div>
        <div class="flex gap-4">
          <button
            class="text-[14px] text-[#0071e3] hover:underline transition-colors"
            @click="$router.push('/')"
          >
            ← 返回主页
          </button>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-3 gap-4 mb-10">
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] cursor-pointer hover:shadow-[0_4px_20px_rgba(0,0,0,0.08)] hover:-translate-y-[1px] transition-all" @click="showUserModal('all')">
          <p class="text-[13px] text-[#86868b] tracking-wide">总用户数</p>
          <p class="text-[32px] font-semibold text-[#0071e3] mt-1">{{ stats.users }}</p>
        </div>
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)]">
          <p class="text-[13px] text-[#86868b] tracking-wide">取名次数</p>
          <p class="text-[32px] font-semibold text-[#1d1d1f] mt-1">{{ stats.namings }}</p>
        </div>
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] cursor-pointer hover:shadow-[0_4px_20px_rgba(0,0,0,0.08)] hover:-translate-y-[1px] transition-all" @click="showUserModal('active')">
          <p class="text-[13px] text-[#86868b] tracking-wide">今日活跃</p>
          <p class="text-[32px] font-semibold text-[#0071e3] mt-1">{{ stats.todayActive }}</p>
        </div>
      </div>

      <!-- 用户列表弹窗 -->
      <div v-if="userModal" class="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center" @click.self="userModal = null">
        <div class="bg-white rounded-2xl p-8 w-full max-w-[640px] max-h-[80vh] overflow-y-auto mx-4 shadow-xl">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-[22px] font-semibold text-[#1d1d1f]">
              {{ userModal === 'all' ? '全部用户' : '今日活跃用户' }}
            </h2>
            <button class="text-[#86868b] hover:text-[#1d1d1f] text-[20px] transition-colors" @click="userModal = null">✕</button>
          </div>
          <div v-if="modalLoading" class="text-center py-10 text-[15px] text-[#86868b]">加载中…</div>
          <div v-else-if="modalUsers.length === 0" class="text-center py-10 text-[15px] text-[#86868b]">暂无数据</div>
          <div v-else class="space-y-2">
            <div v-for="u in modalUsers" :key="u.id" class="flex items-center justify-between py-3 px-4 bg-[#f5f5f7] rounded-xl">
              <div>
                <span class="text-[15px] font-medium text-[#1d1d1f]">{{ u.username }}</span>
                <span v-if="u.email" class="ml-3 text-[14px] text-[#86868b]">{{ u.email }}</span>
                <span v-if="u.role === 'admin'" class="ml-2 px-2 py-0.5 rounded-full bg-[#0071e3]/10 text-[#0071e3] text-[12px] font-medium">管理员</span>
                <span v-if="u.is_deleted" class="ml-2 px-2 py-0.5 rounded-full bg-red-100 text-red-600 text-[12px] font-medium">已注销</span>
              </div>
              <div class="flex items-center gap-3" :class="u.is_deleted ? 'opacity-50' : ''">
                <span class="text-[13px] text-[#aeaeb2]">取名 {{ u.naming_count }} 次</span>
                <span class="text-[13px] text-[#aeaeb2]">{{ formatTime(u.created_at).slice(0, 10) }}</span>
                <button class="text-[13px] text-[#ff3b30] hover:underline transition-colors" @click.stop="handleResetPw(u)">重置密码</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab 切换 -->
      <div class="flex gap-6 mb-6 border-b border-[#d2d2d7]/40 pb-3">
        <button
          v-for="tab in tabs" :key="tab.key"
          class="text-[15px] transition-colors pb-2 -mb-[13px] border-b-2"
          :class="activeTab === tab.key
            ? 'text-[#1d1d1f] border-[#1d1d1f] font-medium'
            : 'text-[#86868b] border-transparent hover:text-[#1d1d1f]'"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- 认证日志 -->
      <div v-if="activeTab === 'logs'" class="space-y-2">
        <div v-if="logsLoading" class="text-center py-16 text-[15px] text-[#86868b]">
          加载中…
        </div>
        <div v-else-if="logs.length === 0" class="text-center py-16 text-[15px] text-[#86868b]">
          暂无日志
        </div>
        <div v-else class="bg-white/80 backdrop-blur-xl rounded-2xl overflow-hidden
                        shadow-[0_2px_12px_rgba(0,0,0,0.03)]">
          <table class="w-full">
            <thead>
              <tr class="border-b border-[#d2d2d7]/30">
                <th class="text-left text-[13px] font-medium text-[#86868b] px-6 py-3 tracking-wide">用户名</th>
                <th class="text-left text-[13px] font-medium text-[#86868b] px-6 py-3 tracking-wide">操作</th>
                <th class="text-left text-[13px] font-medium text-[#86868b] px-6 py-3 tracking-wide">IP 地址</th>
                <th class="text-left text-[13px] font-medium text-[#86868b] px-6 py-3 tracking-wide">时间</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="log in logs" :key="log.id"
                class="border-b border-[#d2d2d7]/20 last:border-0 hover:bg-[#f5f5f7]/50 transition-colors"
              >
                <td class="px-6 py-3 text-[15px] text-[#1d1d1f]">{{ log.username }}</td>
                <td class="px-6 py-3">
                  <span
                    class="inline-block px-2.5 py-0.5 rounded-full text-[13px] font-medium"
                    :class="actionClass(log.action)"
                  >
                    {{ actionLabel(log.action) }}
                  </span>
                </td>
                <td class="px-6 py-3 text-[14px] text-[#86868b] font-mono">{{ log.ip_address }}</td>
                <td class="px-6 py-3 text-[14px] text-[#86868b]">{{ formatTime(log.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 取名记录 -->
      <div v-if="activeTab === 'namings'" class="space-y-2">
        <div v-if="namingsLoading" class="text-center py-16 text-[15px] text-[#86868b]">
          加载中…
        </div>
        <div v-else-if="namings.length === 0" class="text-center py-16 text-[15px] text-[#86868b]">
          暂无取名记录
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="n in namings" :key="n.id"
            class="bg-white/80 backdrop-blur-xl rounded-xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.03)]
                   flex items-center justify-between"
            :class="n.is_deleted ? 'opacity-50' : ''"
          >
            <div class="flex items-center gap-3">
              <span class="text-[15px] font-medium"
                :class="n.is_deleted ? 'text-[#86868b] line-through' : 'text-[#1d1d1f]'">
                {{ n.username }} · {{ n.surname }} · {{ n.gender === 'male' ? '男' : '女' }}
              </span>
              <span class="text-[14px]" :class="n.is_deleted ? 'text-[#aeaeb2]' : 'text-[#86868b]'">
                {{ n.names_count }} 个名字
              </span>
              <span
                v-if="n.is_deleted"
                class="inline-block px-2 py-0.5 rounded-full text-[12px] font-medium
                       bg-red-100 text-red-600"
              >
                已删除
              </span>
            </div>
            <span class="text-[13px] text-[#aeaeb2]">{{ formatTime(n.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getAuthLogs, getAllNamings, getAllUsers, getActiveUsers, adminResetPassword } from '../api'

const router = useRouter()
const authStore = useAuthStore()

const tabs = [
  { key: 'logs', label: '认证日志' },
  { key: 'namings', label: '取名记录' },
]
const activeTab = ref('logs')

const logs = ref<any[]>([])
const logsLoading = ref(true)
const namings = ref<any[]>([])
const namingsLoading = ref(true)

const stats = reactive({ users: 0, namings: 0, todayActive: 0 })
const userModal = ref<string | null>(null)
const modalUsers = ref<any[]>([])
const modalLoading = ref(false)

function formatTime(iso: string): string {
  if (!iso) return ''
  return iso.replace('T', ' ').slice(0, 19)
}

function actionLabel(action: string): string {
  const map: Record<string, string> = { register: '注册', login: '登录', logout: '登出', delete_account: '注销账号' }
  return map[action] || action
}

function actionClass(action: string): string {
  const map: Record<string, string> = {
    register: 'bg-green-100 text-green-700',
    login: 'bg-blue-100 text-blue-700',
    logout: 'bg-gray-100 text-gray-600',
    delete_account: 'bg-red-100 text-red-600',
  }
  return map[action] || 'bg-gray-100 text-gray-600'
}

async function loadLogs() {
  logsLoading.value = true
  try {
    const [logRes, userRes] = await Promise.all([getAuthLogs(), getAllUsers()])
    logs.value = logRes.items
    stats.users = userRes.total
    stats.todayActive = new Set(
      logRes.items
        .filter((l: any) => l.created_at?.startsWith(new Date().toISOString().slice(0, 10)))
        .map((l: any) => l.username)
    ).size
  } catch (e: any) {
    if (e.response?.status === 403) router.push('/')
  } finally {
    logsLoading.value = false
  }
}

async function loadNamings() {
  namingsLoading.value = true
  try {
    const res = await getAllNamings()
    namings.value = res.items
    stats.namings = res.total
  } catch {
    // handled by axios interceptor
  } finally {
    namingsLoading.value = false
  }
}

async function handleResetPw(user: any) {
  const newPw = prompt(`重置 ${user.username} 的密码，输入新密码（至少6位）：`)
  if (!newPw || newPw.length < 6) return
  try {
    await adminResetPassword(user.id, newPw)
    alert(`已重置 ${user.username} 的密码为：${newPw}`)
  } catch (e: any) { alert(e.message || '重置失败') }
}

async function showUserModal(type: string) {
  userModal.value = type
  modalLoading.value = true
  modalUsers.value = []
  try {
    const res = type === 'all' ? await getAllUsers() : await getActiveUsers()
    modalUsers.value = res.items
  } catch { /* handled */ } finally { modalLoading.value = false }
}

onMounted(async () => {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  await Promise.all([loadLogs(), loadNamings()])
})
</script>
