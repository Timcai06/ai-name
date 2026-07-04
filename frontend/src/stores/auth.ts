import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const TOKEN_KEY = 'ai_naming_token'
const USERNAME_KEY = 'ai_naming_username'
const ROLE_KEY = 'ai_naming_role'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem(TOKEN_KEY) || '')
  const username = ref<string>(localStorage.getItem(USERNAME_KEY) || '')
  const role = ref<string>(localStorage.getItem(ROLE_KEY) || 'user')

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => role.value === 'admin')

  function setAuth(newToken: string, newUsername: string, newRole: string = 'user') {
    token.value = newToken
    username.value = newUsername
    role.value = newRole
    localStorage.setItem(TOKEN_KEY, newToken)
    localStorage.setItem(USERNAME_KEY, newUsername)
    localStorage.setItem(ROLE_KEY, newRole)
  }

  function clearAuth() {
    token.value = ''
    username.value = ''
    role.value = 'user'
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USERNAME_KEY)
    localStorage.removeItem(ROLE_KEY)
  }

  return { token, username, role, isLoggedIn, isAdmin, setAuth, clearAuth }
})
