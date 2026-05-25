<template>
  <div class="min-h-screen bg-[#050505] text-main font-sans selection:bg-[#C5A059]/30">
    <!-- Login Screen -->
    <div v-if="!isAuthenticated" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-[#050505]">
      <div class="w-full max-w-md animate-fade-in-up">
        <div class="bg-surface/80 backdrop-blur-2xl border border-main/10 rounded-[2.5rem] p-10 shadow-2xl">
          <div class="text-center mb-10">
            <div class="w-16 h-16 bg-[#C5A059]/10 rounded-2xl flex items-center justify-center border border-[#C5A059]/20 mx-auto mb-6">
              <ShieldCheck class="w-8 h-8 text-[#C5A059]" />
            </div>
            <h2 class="text-3xl font-serif text-main mb-2">Personel Paneli</h2>
            <p class="text-main/40 text-sm font-medium">Hizmet vermeye başlamak için giriş yapın</p>
          </div>

          <div class="space-y-5">
            <div class="group">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 block mb-2 ml-1 group-focus-within:text-[#C5A059] transition-colors">Personel Kodu</label>
              <div class="relative">
                <UserCircle class="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-main/20 group-focus-within:text-[#C5A059] transition-colors" />
                <input v-model="staffCode" type="text" placeholder="Örn: KAAN01" 
                       class="w-full bg-main/[0.03] border border-main/10 rounded-2xl py-4 pl-14 pr-6 text-main placeholder:text-main/10 focus:outline-none focus:border-[#C5A059]/50 focus:bg-main/[0.05] transition-all" />
              </div>
            </div>

            <div class="group">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 block mb-2 ml-1 group-focus-within:text-[#C5A059] transition-colors">Şifre</label>
              <div class="relative">
                <Lock class="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-main/20 group-focus-within:text-[#C5A059] transition-colors" />
                <input v-model="password" type="password" placeholder="••••••••" 
                       class="w-full bg-main/[0.03] border border-main/10 rounded-2xl py-4 pl-14 pr-6 text-main placeholder:text-main/10 focus:outline-none focus:border-[#C5A059]/50 focus:bg-main/[0.05] transition-all" />
              </div>
            </div>

            <div v-if="error" class="bg-rose-500/10 border border-rose-500/20 rounded-2xl p-4 flex items-center gap-3 animate-shake">
              <AlertCircle class="w-5 h-5 text-rose-500 shrink-0" />
              <p class="text-xs text-rose-200 font-medium leading-relaxed">{{ error }}</p>
            </div>

            <button @click="handleLogin" :disabled="isLoading"
                    class="w-full bg-[#C5A059] hover:bg-[#D5B069] disabled:opacity-50 disabled:cursor-not-allowed text-black font-black uppercase tracking-widest py-5 rounded-2xl transition-all shadow-xl shadow-[#C5A059]/10 flex items-center justify-center gap-3 mt-4">
              <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
              <span v-else>Giriş Yap</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="max-w-7xl mx-auto px-6 py-12 md:py-20 animate-fade-in">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-8 mb-16">
        <div class="space-y-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-main/5 rounded-2xl flex items-center justify-center border border-main/10">
              <UserCircle class="w-6 h-6 text-main/40" />
            </div>
            <div>
              <p class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 mb-0.5">Hoş Geldiniz</p>
              <h1 class="text-3xl font-serif text-main">{{ staffInfo?.name }}</h1>
            </div>
          </div>
        </div>

        <button @click="handleLogout" 
                class="flex items-center gap-3 px-6 py-3 rounded-2xl border border-main/10 hover:bg-main/5 transition-all text-main/40 hover:text-main group">
          <LogOut class="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          <span class="text-sm font-bold uppercase tracking-widest">Çıkış Yap</span>
        </button>
      </div>

      <!-- Stats Summary -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2rem] p-8 shadow-2xl">
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 mb-4">Bugünkü Randevular</p>
          <div class="flex items-end justify-between">
            <h4 class="text-4xl font-serif text-main">{{ todayAppointments.length }}</h4>
            <div class="w-10 h-10 bg-[#C5A059]/10 rounded-xl flex items-center justify-center border border-[#C5A059]/20">
              <Calendar class="w-5 h-5 text-[#C5A059]" />
            </div>
          </div>
        </div>
        <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2rem] p-8 shadow-2xl">
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 mb-4">Gelecek Randevular</p>
          <div class="flex items-end justify-between">
            <h4 class="text-4xl font-serif text-main">{{ upcomingAppointments.length }}</h4>
            <div class="w-10 h-10 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
              <Clock class="w-5 h-5 text-blue-400" />
            </div>
          </div>
        </div>
        <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2rem] p-8 shadow-2xl">
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-main/30 mb-4">Toplam Tamamlanan</p>
          <div class="flex items-end justify-between">
            <h4 class="text-4xl font-serif text-main">{{ appointments.filter(a => a.status === 'Tamamlandı').length }}</h4>
            <div class="w-10 h-10 bg-emerald-500/10 rounded-xl flex items-center justify-center border border-emerald-500/20">
              <CheckCircle2 class="w-5 h-5 text-emerald-400" />
            </div>
          </div>
        </div>
      </div>

      <!-- Appointments List -->
      <div class="space-y-6">
        <h3 class="text-xl font-serif text-main mb-8 ml-2 flex items-center gap-4">
          Randevu Listesi
          <span class="px-3 py-1 rounded-full bg-main/5 border border-main/10 text-[10px] font-black text-main/40">{{ appointments.length }}</span>
        </h3>

        <div v-if="isLoading" class="space-y-4">
          <div v-for="i in 3" :key="i" class="h-24 bg-main/5 rounded-[1.5rem] animate-pulse"></div>
        </div>

        <div v-else-if="appointments.length === 0" class="text-center py-20 bg-main/[0.02] border border-main/5 rounded-[2.5rem]">
          <div class="w-20 h-20 bg-main/5 rounded-full flex items-center justify-center mx-auto mb-6">
            <Calendar class="w-10 h-10 text-main/10" />
          </div>
          <p class="text-main/30 font-medium">Henüz randevunuz bulunmuyor.</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-4">
          <div v-for="appt in appointments" :key="appt.id" 
               class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[1.5rem] p-6 shadow-xl hover:bg-surface-elevated transition-all group flex flex-col md:flex-row md:items-center justify-between gap-6">
            
            <div class="flex items-center gap-6 flex-grow">
               <div class="w-14 h-14 bg-main/5 rounded-2xl flex items-center justify-center border border-main/10 group-hover:border-[#C5A059]/30 transition-all">
                  <User class="w-6 h-6 text-main/20" />
               </div>
               <div class="space-y-1">
                  <h4 class="text-lg font-serif text-main">{{ appt.user_name }}</h4>
                  <div class="flex items-center gap-3">
                     <span class="text-[10px] text-main/40 flex items-center gap-1.5 font-bold tracking-wider">
                        <Phone class="w-3 h-3" /> {{ appt.user_email }}
                     </span>
                     <span class="text-[10px] text-main/40 flex items-center gap-1.5 font-bold tracking-wider">
                        <Wallet class="w-3 h-3" /> {{ appt.amount }} TL
                     </span>
                  </div>
               </div>
            </div>

            <div class="flex flex-wrap items-center gap-4 md:gap-8 min-w-[300px]">
               <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-main/5 rounded-xl flex items-center justify-center border border-main/10">
                    <Briefcase class="w-4 h-4 text-main/30" />
                  </div>
                  <div>
                    <span class="text-[8px] font-black uppercase tracking-widest text-main/20 block">Hizmet</span>
                    <p class="text-sm font-bold text-main/90">{{ appt.service_name }}</p>
                  </div>
               </div>

               <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-main/5 rounded-xl flex items-center justify-center border border-main/10">
                    <Clock class="w-4 h-4 text-main/30" />
                  </div>
                  <div>
                    <span class="text-[8px] font-black uppercase tracking-widest text-main/20 block">Zaman</span>
                    <p class="text-sm font-bold text-main/90">{{ formatDate(appt.appointment_date) }} • {{ appt.appointment_time }}</p>
                  </div>
               </div>
            </div>

            <div class="flex items-center gap-3 shrink-0">
               <div :class="[
                  'px-4 py-2 rounded-xl text-[9px] font-black uppercase tracking-[0.2em] border transition-all',
                  appt.status === 'İptal Edildi' ? 'text-main/40 border-main/10 bg-main/5' : 
                  appt.status === 'Tamamlandı' ? 'text-emerald-400 border-emerald-400/20 bg-emerald-400/10' :
                  'text-[#C5A059] border-[#C5A059]/20 bg-[#C5A059]/10'
               ]">
                  {{ appt.status }}
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  UserCircle, Lock, ShieldCheck, AlertCircle, Loader2, 
  LogOut, Calendar, Clock, CheckCircle2, User, Phone, Wallet, Briefcase 
} from 'lucide-vue-next'

const staffCode = ref('')
const password = ref('')
const isLoading = ref(false)
const isAuthenticated = ref(!!localStorage.getItem('staffToken'))
const staffInfo = ref<any>(JSON.parse(localStorage.getItem('staffInfo') || 'null'))
const error = ref('')
const appointments = ref<any[]>([])

const handleLogin = async () => {
  if (!staffCode.value || !password.value) {
    error.value = 'Lütfen personel kodu ve şifrenizi girin.'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const res = await fetch('/api/staff/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ staff_code: staffCode.value, password: password.value })
    })

    const data = await res.json()
    if (res.ok) {
      localStorage.setItem('staffToken', data.token)
      localStorage.setItem('staffInfo', JSON.stringify(data.staff))
      staffInfo.value = data.staff
      isAuthenticated.value = true
      fetchAppointments()
    } else {
      error.value = data.detail || 'Giriş yapılamadı.'
    }
  } catch (e) {
    error.value = 'Bağlantı hatası.'
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('staffToken')
  localStorage.removeItem('staffInfo')
  isAuthenticated.value = false
  staffInfo.value = null
  appointments.value = []
}

const fetchAppointments = async () => {
  isLoading.value = true
  try {
    const res = await fetch('/api/staff/appointments', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('staffToken')}` }
    })
    if (res.ok) {
      appointments.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })
}

const todayAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return appointments.value.filter(a => a.appointment_date === today)
})

const upcomingAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return appointments.value.filter(a => a.appointment_date > today)
})

onMounted(() => {
  if (isAuthenticated.value) fetchAppointments()
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-fade-in-up {
  animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-shake {
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>
