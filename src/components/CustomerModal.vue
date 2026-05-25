<template>
  <Teleport to="body">
    <transition name="fade">
      <div v-if="isOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-6">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="!isLoading && $emit('close')"></div>
        
        <!-- Modal Content -->
        <div class="relative z-10 bg-main rounded-[2.5rem] p-10 w-full max-w-md shadow-2xl border border-slate-100 animate-scale-in">
          <button @click="$emit('close')" 
                  :disabled="isLoading || isSuccess"
                  class="absolute top-8 right-8 p-2 text-slate-400 hover:text-slate-900 transition-colors disabled:opacity-0">
            <X class="w-6 h-6" />
          </button>

          <div class="flex flex-col items-center text-center mb-10">
            <div class="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center mb-6 border border-slate-100">
              <User class="w-8 h-8 text-slate-900" />
            </div>
            <h3 class="text-3xl font-heading font-bold text-slate-900 mb-2">Müşteri Bilgileri</h3>
            <p class="text-slate-500 text-sm">Randevunuzu tamamlamak için lütfen bilgilerinizi doğrulayın.</p>
          </div>

          <div class="space-y-6">
            <!-- Error Message -->
            <div v-if="errorMessage" class="p-4 bg-rose-50 border border-rose-100 rounded-2xl flex items-center gap-3 animate-pulse">
              <AlertCircle class="w-5 h-5 text-rose-500" />
              <p class="text-rose-600 text-xs font-bold">{{ errorMessage }}</p>
            </div>

            <!-- Name Input -->
            <div class="space-y-2">
              <label class="text-[10px] uppercase tracking-widest font-black text-slate-400 ml-2">Ad Soyad</label>
              <div class="relative group">
                <input 
                  v-model="name"
                  type="text" 
                  placeholder="Örn: Selin Yılmaz"
                  :disabled="isLoading || isSuccess"
                  class="w-full bg-slate-50 border border-slate-100 rounded-2xl py-4 px-6 text-slate-900 font-medium focus:outline-none focus:border-slate-900 focus:bg-main transition-all placeholder:text-slate-300"
                  :class="{ 'border-rose-300 bg-rose-50': errors.name }"
                />
                <p v-if="errors.name" class="text-[10px] text-rose-500 font-bold mt-1.5 ml-2">{{ errors.name }}</p>
              </div>
            </div>

            <!-- Phone Input -->
            <div class="space-y-2">
              <label class="text-[10px] uppercase tracking-widest font-black text-slate-400 ml-2">Telefon Numarası</label>
              <div class="relative">
                 <div class="absolute inset-y-0 left-6 flex items-center pointer-events-none text-slate-400 font-bold text-sm">
                  +90
                </div>
                <input 
                  :value="phoneNumber"
                  @input="handlePhoneInput"
                  type="tel" 
                  placeholder="5XX XXX XX XX"
                  maxlength="15"
                  :disabled="isLoading || isSuccess"
                  class="w-full bg-slate-50 border border-slate-100 rounded-2xl py-4 pl-16 pr-6 text-slate-900 font-medium focus:outline-none focus:border-slate-900 focus:bg-main transition-all placeholder:text-slate-300"
                  :class="{ 'border-rose-300 bg-rose-50': errors.phone }"
                />
                <p v-if="errors.phone" class="text-[10px] text-rose-500 font-bold mt-1.5 ml-2">{{ errors.phone }}</p>
              </div>
            </div>

            <!-- Action Button -->
            <div class="pt-4">
              <button @click="handleConfirm"
                      :disabled="isLoading || isSuccess"
                      class="relative w-full bg-slate-900 text-main py-5 rounded-2xl font-heading font-bold text-lg hover:bg-slate-800 hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden flex items-center justify-center gap-3">
                
                <template v-if="isSuccess">
                   <div class="w-5 h-5 border-2 border-main/30 border-t-white rounded-full animate-spin"></div>
                   <span class="text-sm">Yönlendiriliyorsunuz...</span>
                </template>
                <template v-else-if="isLoading">
                   <div class="flex gap-1.5">
                     <div class="w-1.5 h-1.5 bg-main rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                     <div class="w-1.5 h-1.5 bg-main rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                     <div class="w-1.5 h-1.5 bg-main rounded-full animate-bounce"></div>
                   </div>
                </template>
                <template v-else>
                   <span>Onayla ve Devam Et</span>
                   <ChevronRight class="w-5 h-5" />
                </template>
              </button>
            </div>
            
            <div class="flex items-center justify-center gap-2 mt-8 py-3 bg-slate-50 rounded-xl border border-slate-100">
               <ShieldCheck class="w-4 h-4 text-emerald-500" />
               <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">SSL Güvenli Ödeme Altyapısı</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { X, User, ChevronRight, ShieldCheck, AlertCircle } from 'lucide-vue-next'
import { useAppointmentStore } from '../stores/appointment'
import { storeToRefs } from 'pinia'

const store = useAppointmentStore()
const { currentTheme } = storeToRefs(store)

const props = defineProps<{
  isOpen: boolean
  isLoading?: boolean
  isSuccess?: boolean
  errorMessage?: string
}>()

const emit = defineEmits(['close', 'confirm'])

const name = ref('')
const phoneNumber = ref('')
const errors = ref({ name: '', phone: '' })

// Form Validation
const validateForm = () => {
  let isValid = true
  errors.value = { name: '', phone: '' }

  if (!name.value.trim()) {
    errors.value.name = 'Ad Soyad zorunludur.'
    isValid = false
  }

  const cleanPhone = phoneNumber.value.replace(/\D/g, '')
  if (cleanPhone.length !== 10 || !cleanPhone.startsWith('5')) {
    errors.value.phone = 'Geçerli bir numara giriniz.'
    isValid = false
  }

  return isValid
}

const handlePhoneInput = (e: Event) => {
  const input = e.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  
  // Eğer kullanıcı 0 ile başlarsa (örn: 0532), 0'ı temizle
  if (value.startsWith('0')) {
    value = value.substring(1)
  }
  
  // Sadece 5 ile başlamasına izin ver (Opsiyonel: Daha esnek olabilir ama TR standartı 5)
  if (value.length > 0 && value[0] !== '5') {
    // Eğer yanlış bir rakamla başlarsa temizle
    value = ''
  }
  
  if (value.length > 10) value = value.slice(0, 10)
  
  let formatted = ''
  if (value.length > 0) {
    formatted = '(' + value.substring(0, 3)
    if (value.length > 3) formatted += ') ' + value.substring(3, 6)
    if (value.length > 6) formatted += ' ' + value.substring(6, 8)
    if (value.length > 8) formatted += ' ' + value.substring(8, 10)
  }
  
  phoneNumber.value = formatted
}

const handleConfirm = () => {
  if (validateForm()) {
    emit('confirm', { name: name.value, phone: phoneNumber.value })
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
