<template>
  <div class="min-h-screen bg-app flex items-center justify-center p-4 sm:p-8 relative overflow-hidden font-sans">
    
    <!-- Subtle Background Accents -->
    <div class="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-br from-accent/10 to-transparent rounded-full blur-[120px] -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
    <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-accent/5 to-transparent rounded-full blur-[100px] translate-y-1/3 -translate-x-1/3 pointer-events-none"></div>

    <!-- Main Container -->
    <div class="w-full max-w-5xl bg-surface/90 backdrop-blur-3xl border border-main/10 rounded-[2.5rem] shadow-2xl flex flex-col md:flex-row overflow-hidden relative z-10 animate-fade-in mt-16 md:mt-0">
      
      <!-- Left: Branding Side -->
      <div class="w-full md:w-5/12 bg-gradient-to-br from-surface-elevated to-app p-10 lg:p-14 flex flex-col justify-between relative overflow-hidden border-b md:border-b-0 md:border-r border-main/5">
        <!-- Abstract Pattern overlay -->
        <div class="absolute inset-0 opacity-[0.03] bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+PHBhdGggZD0iTTAgMGg0MHY0MEgwek0wIDBoNDB2NDBIMHptMjAgMjBjMTEuMDQ2IDAgMjAtOC45NTQgMjAtMjBTMzEuMDQ2IDAgMjAgMCAwIDguOTU0IDAgMjBzOC45NTQgMjAgMjAgMjB6IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjEiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjwvc3ZnPg==')] pointer-events-none"></div>
        
        <div class="relative z-10">
          <h1 class="text-4xl md:text-5xl font-black tracking-[0.3em] uppercase text-main mb-4 drop-shadow-lg">Di<span class="text-accent">TA</span></h1>
          <p class="text-[10px] text-main/50 uppercase tracking-[0.3em] font-bold">Premium Appointment Suite</p>
        </div>

        <div class="relative z-10 mt-12 md:mt-0">
          <h2 class="text-3xl font-serif text-main mb-5 leading-tight tracking-wide">Zamanınızı<br>değerli kılın.</h2>
          <p class="text-sm text-main/40 leading-relaxed max-w-[250px]">Modern bakım ve stil deneyiminizin dijital adresi. En seçkin uzmanlara anında erişin.</p>
        </div>
      </div>

      <!-- Right: Form Side -->
      <div class="w-full md:w-7/12 p-8 sm:p-12 lg:p-16 relative bg-surface">
        <div class="max-w-sm mx-auto">
          
          <!-- Modern Tab Switcher (Segmented Control) -->
          <div class="flex p-1.5 bg-surface-elevated rounded-2xl border border-main/5 mb-10 relative shadow-inner">
            <!-- Active indicator pill -->
            <div class="absolute inset-y-1.5 w-[calc(50%-6px)] bg-surface-active rounded-xl shadow-md transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] z-0 border border-main/5"
                 :class="mode === 'login' ? 'left-1.5' : 'left-[calc(50%+4px)]'"></div>
            
            <button @click="mode = 'login'" 
                    class="flex-1 py-3.5 text-[11px] font-bold uppercase tracking-widest rounded-xl transition-colors duration-300 relative z-10"
                    :class="mode === 'login' ? 'text-main' : 'text-main/40 hover:text-main/70'">
              Giriş Yap
            </button>
            <button @click="mode = 'register'" 
                    class="flex-1 py-3.5 text-[11px] font-bold uppercase tracking-widest rounded-xl transition-colors duration-300 relative z-10"
                    :class="mode === 'register' ? 'text-main' : 'text-main/40 hover:text-main/70'">
              Kayıt Ol
            </button>
          </div>

          <!-- Forms Container with height transition support -->
          <div class="relative min-h-[380px]">
            <!-- Login Form -->
            <transition name="slide-fade">
              <div v-if="mode === 'login'" class="absolute inset-0 w-full">
                <div class="space-y-6">
                  <div class="space-y-2.5">
                    <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Telefon Numarası</label>
                    <input type="tel" v-model="form.phone" placeholder="05XX XXX XX XX"
                           class="w-full bg-surface-elevated border border-main/10 rounded-xl py-4 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                  </div>
                  <div class="space-y-2.5">
                    <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Şifre</label>
                    <input type="password" v-model="form.password" placeholder="Şifreniz" @keyup.enter="handleLogin"
                           class="w-full bg-surface-elevated border border-main/10 rounded-xl py-4 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                  </div>

                  <div v-if="error" class="text-xs text-red-400 bg-red-500/10 border border-red-500/20 p-3.5 rounded-xl text-center font-medium mt-2 animate-shake">
                    {{ error }}
                  </div>

                  <button @click="handleLogin" :disabled="isLoading"
                          class="w-full mt-8 py-4.5 rounded-xl font-black text-[11px] uppercase tracking-widest text-[#0a0a0a] bg-[#C5A059] hover:bg-[#d4b06a] hover:shadow-[0_0_25px_rgba(197,160,89,0.4)] transition-all flex justify-center items-center gap-3 active:scale-[0.98]">
                    <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
                    <span v-else>Oturum Aç</span>
                  </button>
                </div>
              </div>
            </transition>

            <!-- Register Form -->
            <transition name="slide-fade">
              <div v-if="mode === 'register'" class="absolute inset-0 w-full">
                <div class="space-y-5">
                  <div class="space-y-2.5">
                    <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Ad Soyad</label>
                    <input type="text" v-model="form.name" placeholder="Adınız Soyadınız"
                           class="w-full bg-surface-elevated border border-main/10 rounded-xl py-3.5 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                  </div>
                  <div class="space-y-2.5">
                    <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Telefon Numarası</label>
                    <input type="tel" v-model="form.phone" placeholder="05XX XXX XX XX"
                           class="w-full bg-surface-elevated border border-main/10 rounded-xl py-3.5 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2.5">
                      <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Şifre</label>
                      <input type="password" v-model="form.password" placeholder="En az 6 karakter"
                             class="w-full bg-surface-elevated border border-main/10 rounded-xl py-3.5 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                    </div>
                    <div class="space-y-2.5">
                      <label class="text-[10px] uppercase tracking-wider font-bold text-main/60 ml-1">Tekrar</label>
                      <input type="password" v-model="form.confirmPassword" placeholder="Şifre tekrarı"
                             class="w-full bg-surface-elevated border border-main/10 rounded-xl py-3.5 px-5 text-main text-sm focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 transition-all placeholder:text-main/20 shadow-inner" />
                    </div>
                  </div>

                  <div v-if="error" class="text-xs text-red-400 bg-red-500/10 border border-red-500/20 p-3.5 rounded-xl text-center font-medium mt-2 animate-shake">
                    {{ error }}
                  </div>

                  <button @click="handleRegister" :disabled="isLoading"
                          class="w-full mt-6 py-4.5 rounded-xl font-black text-[11px] uppercase tracking-widest text-main bg-surface-active border border-main/10 hover:bg-[#333] hover:border-main/20 transition-all flex justify-center items-center gap-3 active:scale-[0.98] shadow-lg">
                    <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
                    <span v-else>Hesap Oluştur</span>
                  </button>
                </div>
              </div>
            </transition>
          </div>

        </div>
      </div>
    </div>

    <!-- Remember Me Modal -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="showRememberModal" class="fixed inset-0 z-[500] flex items-center justify-center p-6">
          <div class="absolute inset-0 bg-app/95 backdrop-blur-xl"></div>
          <div class="relative z-10 bg-[#111] border border-main/10 rounded-[2.5rem] p-10 max-w-sm w-full shadow-2xl text-center animate-scale-in">
            <div class="w-16 h-16 rounded-full bg-[#C5A059]/10 border border-[#C5A059]/20 flex items-center justify-center mx-auto mb-6">
              <ShieldCheck class="w-8 h-8 text-[#C5A059]" />
            </div>
            <h3 class="text-2xl font-serif text-main mb-3">Hoş Geldiniz!</h3>
            <p class="text-sm text-main/50 font-sans mb-8 leading-relaxed">Kayıt işleminiz tamamlandı. Bilgilerinizi hatırlayalım mı? Bir sonraki girişinizde otomatik olarak oturum açılacak.</p>

            <div class="space-y-3">
              <button @click="completeRegister(true)"
                      class="w-full py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] text-[#0a0a0a] bg-[#C5A059] hover:bg-[#d4b06a] hover:scale-[1.02] active:scale-95 transition-all shadow-xl">
                Evet, Hatırla
              </button>
              <button @click="completeRegister(false)"
                      class="w-full py-4 rounded-2xl font-black text-xs uppercase tracking-[0.2em] text-main/50 border border-main/10 bg-surface-elevated hover:bg-surface-active hover:text-main transition-all">
                Hayır, Bu Seferlik
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Loader2, ShieldCheck } from 'lucide-vue-next'
import { useAppointmentStore } from '../stores/appointment'

const router = useRouter()
const store = useAppointmentStore()
const emit = defineEmits(['authenticated'])

const mode = ref<'login' | 'register'>('login')
const isLoading = ref(false)
const error = ref('')
const showRememberModal = ref(false)
const pendingToken = ref('')
const pendingUser = ref<any>(null)

const form = ref({
  name: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  error.value = ''
  if (!form.value.name || !form.value.phone || !form.value.password) {
    error.value = 'Tüm alanları doldurunuz.'
    return
  }
  if (form.value.password.length < 6) {
    error.value = 'Şifre en az 6 karakter olmalıdır.'
    return
  }
  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Şifreler eşleşmiyor.'
    return
  }

  isLoading.value = true
  try {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: form.value.name, phone: form.value.phone, password: form.value.password })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.detail || 'Kayıt başarısız.'
      return
    }
    pendingToken.value = data.token
    pendingUser.value = data.user
    showRememberModal.value = true
  } catch {
    error.value = 'Bağlantı hatası.'
  } finally {
    isLoading.value = false
  }
}

const completeRegister = (remember: boolean) => {
  store.triggerAuthOverlay('Hesap oluşturuluyor...', 'loading')
  
  setTimeout(() => {
    if (remember) {
      localStorage.setItem('dita_customer_token', pendingToken.value)
      localStorage.setItem('dita_customer_user', JSON.stringify(pendingUser.value))
    } else {
      sessionStorage.setItem('dita_customer_token', pendingToken.value)
      sessionStorage.setItem('dita_customer_user', JSON.stringify(pendingUser.value))
    }
    showRememberModal.value = false
    store.setCurrentUser(pendingUser.value)
    store.triggerAuthOverlay('Kayıt başarılı!', 'success')
    
    setTimeout(() => {
        emit('authenticated', { token: pendingToken.value, user: pendingUser.value })
        router.push('/')
    }, 1000)
  }, 1000)
}

const handleLogin = async () => {
  error.value = ''
  if (!form.value.phone || !form.value.password) {
    error.value = 'Telefon ve şifre gereklidir.'
    return
  }

  isLoading.value = true
  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: form.value.phone, password: form.value.password })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.detail || 'Giriş başarısız.'
      return
    }
    
    store.triggerAuthOverlay('Giriş yapılıyor...', 'loading')
    
    setTimeout(() => {
        localStorage.setItem('dita_customer_token', data.token)
        localStorage.setItem('dita_customer_user', JSON.stringify(data.user))
        store.setCurrentUser(data.user)
        store.triggerAuthOverlay('Giriş başarılı!', 'success')
        
        setTimeout(() => {
            emit('authenticated', { token: data.token, user: data.user })
            router.push('/')
        }, 1000)
    }, 1000)
    
  } catch {
    error.value = 'Bağlantı hatası.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.animate-scale-in {
  animation: scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
.animate-shake {
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes shake {
  10%, 90% { transform: translate3d(-2px, 0, 0); }
  20%, 80% { transform: translate3d(3px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-5px, 0, 0); }
  40%, 60% { transform: translate3d(5px, 0, 0); }
}

/* Tab transitions */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease-out;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(15px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}

.fade-enter-active, .fade-leave-active { 
  transition: opacity 0.3s ease; 
}
.fade-enter-from, .fade-leave-to { 
  opacity: 0; 
}

/* Custom utility for padding-bottom in buttons */
.py-4\.5 {
  padding-top: 1.125rem;
  padding-bottom: 1.125rem;
}
</style>
