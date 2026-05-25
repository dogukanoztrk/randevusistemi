<template>
  <div class="fixed inset-0 z-[100] w-full h-[100dvh] bg-black/50 backdrop-blur-sm overflow-y-auto font-sans">
    <div class="min-h-full w-full flex items-center justify-center p-4 py-12">
      <div class="flex flex-row flex-wrap justify-center items-start gap-6 w-full max-w-[950px] transition-all duration-500 my-auto">
        
        <!-- Main Payment Card (Credit Card) -->
        <div class="max-w-md w-full bg-main rounded-2xl shadow-xl overflow-hidden flex-shrink-0 transition-all duration-300 mx-auto z-10">
      <!-- Header -->
      <div class="bg-[#2D3135] p-6 text-main flex justify-between items-center">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-blue-500 rounded flex items-center justify-center font-bold">i</div>
          <span class="font-bold tracking-tight">iyzico <span class="font-light">checkout</span></span>
        </div>
        <div class="flex items-center gap-4">
          <button @click="$emit('back')" class="text-xs font-bold opacity-60 hover:opacity-100 transition-opacity flex items-center gap-1">
            <ArrowLeft class="w-3 h-3" /> GERİ DÖN
          </button>
          <div class="text-xs opacity-60 px-2 py-1 bg-main/10 rounded">TEST MODU</div>
        </div>
      </div>

      <!-- Price Section -->
      <div class="p-8 border-b border-gray-100 flex justify-between items-center bg-gray-50">
        <div>
          <p class="text-[10px] uppercase font-bold text-gray-400 tracking-wider mb-1">ÖDENECEK TUTAR</p>
          <p class="text-2xl font-bold text-gray-800">{{ amount }} TL</p>
        </div>
        <div class="text-right">
          <p class="text-[10px] uppercase font-bold text-gray-400 tracking-wider mb-1">İŞLEM NO</p>
          <p class="text-sm font-mono text-gray-600">ID: {{ id.slice(0, 8) }}</p>
        </div>
      </div>

      <!-- Mock Card Form -->
      <div class="p-8 space-y-6">
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="text-xs font-bold text-gray-500">Kart Üzerindeki İsim</label>
            <input v-model="cardHolder" type="text" class="w-full border border-gray-300 bg-main rounded-lg py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-gray-900 font-medium" placeholder="AD SOYAD" />
          </div>
          <div class="space-y-1">
            <label class="text-xs font-bold text-gray-500">Kart Numarası</label>
            <input 
              :value="cardNumber" 
              @input="handleCardInput"
              type="text" 
              class="w-full border border-gray-300 bg-main rounded-lg py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-gray-900 font-medium" 
              placeholder="0000 0000 0000 0000" 
              maxlength="19" 
            />
          </div>
          <div class="grid grid-cols-2 gap-4">
             <div class="space-y-1">
              <label class="text-xs font-bold text-gray-500">Son Kullanma</label>
              <input :value="expiryDate" @input="handleExpiryInput" type="text" class="w-full border border-gray-300 bg-main rounded-lg py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-gray-900 font-medium" placeholder="AA/YY" maxlength="5" />
            </div>
             <div class="space-y-1">
              <label class="text-xs font-bold text-gray-500">CVC</label>
              <input :value="cvv" @input="handleCvvInput" type="text" class="w-full border border-gray-300 bg-main rounded-lg py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none transition-all text-gray-900 font-medium" placeholder="000" maxlength="3" />
            </div>
          </div>
        </div>

        <div v-if="error" class="text-xs text-red-500 font-bold animate-shake bg-red-50 p-3 rounded-lg border border-red-100 flex items-center gap-2">
           <AlertTriangle class="w-3 h-3" /> {{ error }}
        </div>




        <button @click="simulatePayment" 
                :disabled="isProcessing"
                class="w-full bg-[#34A853] text-main py-4 rounded-lg font-bold hover:bg-[#2D9B48] transition-all flex items-center justify-center gap-3">
          <span v-if="!isProcessing">ŞİMDİ ÖDE (TEST)</span>
          <span v-else class="flex items-center gap-2">
            <svg class="animate-spin h-5 w-5 text-main" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            İŞLENİYOR...
          </span>
        </button>

        <div class="flex items-center justify-center gap-2 text-[10px] text-gray-400 font-medium">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path></svg>
          256-BIT SSL GÜVENLİ ÖDEME SİSTEMİ
        </div>

        <div class="mt-6 border-t border-gray-100 pt-4 hidden">
          <!-- Button removed based on user request -->
        </div>
      </div>
    </div>

    <!-- QR Payment Card -->
    <div class="w-full max-w-md bg-main rounded-2xl shadow-xl overflow-y-auto overflow-x-hidden flex flex-col items-center justify-start p-8 transition-all border border-gray-100 flex-grow-0 sm:min-w-[320px] sm:max-w-[380px] z-0 max-h-[90vh]">
      <div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
        <QrCode class="w-8 h-8 text-blue-500" />
      </div>
      <h3 class="font-bold text-gray-800 text-lg mb-2">QR ile Ödeme</h3>
      <p class="text-xs font-medium text-gray-500 text-center mb-6 leading-relaxed">Ödemeyi tamamlamak için banka uygulamanızdan okutulacak bir QR kod oluşturun.</p>
      
      <button @click="generateQR" class="w-full bg-[#1A73E8] text-main py-3.5 rounded-lg font-bold hover:bg-[#1557B0] transition-all flex items-center justify-center gap-2 text-sm shadow-sm mb-2 mt-auto">
        <QrCode class="w-4 h-4" /> QR İLE ÖDE / YENİ OLUŞTUR
      </button>

      <div v-if="showQR" class="w-full flex flex-col items-center animate-fade-in mt-6">
        <div class="bg-main p-4 rounded-xl shadow-sm border border-gray-200 mb-4 hover:shadow-md transition-shadow">
          <img :src="qrImageUrl" alt="Payment QR Code" class="w-48 h-48 object-contain mx-auto" />
        </div>
        
        <div class="w-full bg-gray-50 rounded-lg p-3 text-center border border-gray-100">
          <p class="text-[10px] uppercase font-bold text-gray-400 tracking-wider mb-1">REFERANS NO</p>
          <p class="text-sm font-mono text-gray-700 font-bold tracking-widest">{{ qrRef }}</p>
        </div>
      </div>
    </div>
    
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ArrowLeft, AlertTriangle, QrCode } from 'lucide-vue-next'

const props = defineProps<{
  id: string
  amount: number
}>()

const emit = defineEmits(['success', 'back'])
const isProcessing = ref(false)
const error = ref('')

const cardHolder = ref('')
const cardNumber = ref('')
const expiryDate = ref('')
const cvv = ref('')

const showQR = ref(false)
const qrImageUrl = ref('')
const qrRef = ref('')

const generateQR = () => {
  const randomString = Math.random().toString(36).substring(2, 12).toUpperCase()
  qrRef.value = randomString
  qrImageUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=IYZICO-PAYMENT-${randomString}`
  showQR.value = true
}

const handleCardInput = (e: Event) => {
  error.value = ''
  const input = e.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  if (value.length > 16) value = value.slice(0, 16)
  
  // Format 4-4-4-4
  const parts = value.match(/.{1,4}/g)
  cardNumber.value = parts ? parts.join(' ') : value
  input.value = cardNumber.value
}

const handleExpiryInput = (e: Event) => {
  error.value = ''
  const input = e.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  if (value.length > 4) value = value.slice(0, 4)
  
  if (value.length > 2) {
    expiryDate.value = value.slice(0, 2) + '/' + value.slice(2)
  } else {
    expiryDate.value = value
  }
  input.value = expiryDate.value
}

const handleCvvInput = (e: Event) => {
  error.value = ''
  const input = e.target as HTMLInputElement
  let value = input.value.replace(/\D/g, '')
  if (value.length > 3) value = value.slice(0, 3)
  cvv.value = value
  input.value = value
}

const simulatePayment = () => {
  if (!cardHolder.value || cardNumber.value.length < 19 || expiryDate.value.length < 5 || cvv.value.length < 3) {
    error.value = 'Lütfen tüm kart bilgilerini eksiksiz ve doğru formatta giriniz.'
    return
  }

  isProcessing.value = true
  setTimeout(() => {
    isProcessing.value = false
    emit('success')
  }, 2000)
}
</script>

<style scoped>
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-shake {
  animation: shake 0.2s ease-in-out 0s 2;
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>
