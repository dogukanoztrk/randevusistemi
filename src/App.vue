<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { useAppointmentStore } from '@/stores/appointment'
import Toast from '@/components/Toast.vue'
import { onMounted, computed, ref } from 'vue'
import { User, LogOut, Menu as MenuIcon, X, Loader2, CheckCircle2, Sun, Moon, Download } from 'lucide-vue-next'

const store = useAppointmentStore()
const router = useRouter()

// Theme & PWA Logic
const isDark = ref(true)
const deferredPrompt = ref<any>(null)

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.remove('light')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.add('light')
    localStorage.setItem('theme', 'light')
  }
}

const installPWA = async () => {
  if (deferredPrompt.value) {
    deferredPrompt.value.prompt()
    const { outcome } = await deferredPrompt.value.userChoice
    if (outcome === 'accepted') {
      deferredPrompt.value = null
    }
  }
}

onMounted(async () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'light') {
    isDark.value = false
    document.documentElement.classList.add('light')
  }
  
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt.value = e
  })

  await store.fetchInitialData()
})


const logoutCustomer = async () => {
  store.triggerAuthOverlay('Çıkış yapılıyor...', 'loading')
  
  setTimeout(() => {
    // Clear Auth Tokens
    localStorage.removeItem('dita_customer_token')
    localStorage.removeItem('dita_customer_user')
    localStorage.removeItem('dita_user_phone')
    sessionStorage.removeItem('dita_customer_token')
    sessionStorage.removeItem('dita_customer_user')
    
    // Clear Pinia State
    store.myAppointments = []
    store.customerPhone = null
    store.customerName = null
    store.setCurrentUser(null)
    
    store.triggerAuthOverlay('Çıkış yapıldı', 'success')
    router.push('/')
  }, 1000)
}
</script>

<template>
  <div class="min-h-screen bg-app text-main flex flex-col font-sans relative">
    
    <!-- Auth Overlay (New) -->
    <Teleport to="body">
      <transition name="fade-overlay">
        <div v-if="store.authOverlay.visible" class="fixed inset-0 z-[1000] flex items-center justify-center bg-app/95 backdrop-blur-xl">
          <div class="flex flex-col items-center gap-6 animate-scale-in">
            <div v-if="store.authOverlay.type === 'loading'" class="w-16 h-16 border-4 border-[#C5A059]/20 border-t-[#C5A059] rounded-full animate-spin"></div>
            <div v-else class="w-16 h-16 bg-[#34d399]/10 rounded-full flex items-center justify-center text-[#34d399] border border-[#34d399]/20">
              <CheckCircle2 class="w-8 h-8" />
            </div>
            <p class="text-xl font-heading font-bold text-main tracking-tight">{{ store.authOverlay.message }}</p>
          </div>
        </div>
      </transition>
    </Teleport>
    
    <!-- Subtle Background Accent -->
    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-[#C5A059]/5 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <!-- Premium Global Header -->
    <header class="sticky top-0 z-[100] bg-surface/80 backdrop-blur-2xl border-b border-main/10 h-20 flex items-center px-4 md:px-8 shadow-sm">
      <div class="max-w-7xl mx-auto w-full flex justify-between items-center relative z-10">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group relative">
          <div class="w-10 h-10 bg-surface-elevated border border-main/10 rounded-xl flex items-center justify-center text-[#C5A059] font-black text-xl group-hover:scale-105 transition-all shadow-[0_0_15px_rgba(197,160,89,0.2)]">
            D
          </div>
          <div class="flex flex-col">
            <span class="font-heading font-black text-2xl tracking-[0.2em] text-main leading-none">DiTA</span>
            <span class="text-[8px] uppercase tracking-[0.4em] font-bold text-[#C5A059]/70 mt-1">Appointment</span>
          </div>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="hidden lg:flex items-center gap-10">
          <button v-if="deferredPrompt" @click="installPWA" class="flex items-center gap-2 px-4 py-1.5 bg-[#C5A059]/10 text-[#C5A059] border border-[#C5A059]/20 font-bold text-[10px] uppercase tracking-widest rounded-full hover:bg-[#C5A059] hover:text-[#0a0a0a] transition-all">
            <Download class="w-3.5 h-3.5" />
            İndir
          </button>
          
          <button @click="toggleTheme" class="w-8 h-8 rounded-full bg-surface-elevated border border-main/10 flex items-center justify-center text-[#C5A059] hover:bg-[#C5A059] hover:text-[#0a0a0a] transition-all shadow-inner">
            <Sun v-if="isDark" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>

          <router-link to="/" class="text-xs font-bold uppercase tracking-widest text-main/50 hover:text-main transition-colors">Ana Sayfa</router-link>
          <router-link to="/my-appointments" class="text-xs font-bold uppercase tracking-widest text-main/50 hover:text-main transition-colors">Randevularım</router-link>
          
          <div class="h-6 w-px bg-main/10 mx-2"></div>
          
          <template v-if="store.currentUser">
            <div class="flex items-center gap-4">
              <div class="flex flex-col items-end">
                <span class="text-xs font-bold text-main/90">{{ store.currentUser.name }}</span>
                <button @click="logoutCustomer" class="text-[9px] font-black uppercase tracking-widest text-rose-400 hover:text-rose-300 transition-colors mt-0.5">Çıkış Yap</button>
              </div>
              <div class="w-10 h-10 rounded-full bg-surface-elevated border border-main/10 flex items-center justify-center text-[#C5A059] shadow-inner">
                <User class="w-4 h-4" />
              </div>
            </div>
          </template>
          <template v-else>
            <router-link to="/auth" class="px-6 py-3 bg-[#C5A059] text-[#0a0a0a] rounded-xl text-xs font-black uppercase tracking-widest hover:bg-[#d4b06a] hover:scale-105 transition-all shadow-[0_0_20px_rgba(197,160,89,0.3)] active:scale-95">
              Giriş / Kayıt
            </router-link>
          </template>
        </nav>

        <!-- Mobile Menu Trigger -->
        <div class="flex items-center gap-4 lg:hidden">
          <button v-if="deferredPrompt" @click="installPWA" class="text-[#C5A059]">
            <Download class="w-5 h-5" />
          </button>
          <button @click="toggleTheme" class="text-[#C5A059]">
            <Sun v-if="isDark" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
          </button>
          <button class="p-2 text-main/50 hover:text-main transition-colors">
            <MenuIcon class="w-6 h-6" />
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow relative z-10">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Simple Footer -->
    <footer class="py-12 border-t border-main/10 bg-surface relative z-10">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-8">
        <router-link to="/" class="flex items-center gap-3 opacity-50 hover:opacity-100 transition-opacity">
          <div class="w-8 h-8 bg-surface-elevated border border-main/10 rounded-lg flex items-center justify-center text-[#C5A059] font-black text-lg">D</div>
          <span class="font-heading font-black text-xl tracking-[0.2em] text-main">DiTA</span>
        </router-link>
        <p class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30">© 2026 DiTA Appointment Platform. All rights reserved.</p>
        <div class="flex gap-6">
          <router-link to="/terms" class="text-[9px] font-black uppercase tracking-widest text-main/30 hover:text-main/60 transition-colors">Kullanım Koşulları</router-link>
          <router-link to="/privacy" class="text-[9px] font-black uppercase tracking-widest text-main/30 hover:text-main/60 transition-colors">Gizlilik Politikası</router-link>
        </div>
      </div>
    </footer>

    <!-- Global Toast Notifications -->
    <Toast />
  </div>
</template>

<style>
/* App-wide styles are handled in index.css */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-overlay-enter-active,
.fade-overlay-leave-active {
  transition: opacity 0.5s ease;
}

.fade-overlay-enter-from,
.fade-overlay-leave-to {
  opacity: 0;
}

.animate-scale-in {
  animation: scale-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes scale-in {
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>
