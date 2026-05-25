<template>
  <div class="max-w-5xl mx-auto px-4 py-12 md:py-20 animate-fade-in-up font-sans relative z-10">
    <div class="flex items-center justify-between mb-12">
      <div>
        <h2 class="text-4xl font-serif text-main mb-2">Randevularım</h2>
        <p class="text-main/50">Geçmiş ve gelecek randevularınızı buradan takip edebilirsiniz.</p>
      </div>
    </div>

    <!-- Empty State or Not Logged In -->
    <div v-if="!customerUser || myAppointments.length === 0" class="bg-surface/80 backdrop-blur-xl border border-main/5 rounded-[2.5rem] p-16 text-center shadow-2xl">
      <div class="w-20 h-20 rounded-2xl bg-surface-elevated flex items-center justify-center mx-auto mb-6 border border-main/5">
        <CalendarX class="w-10 h-10 text-main/20" />
      </div>
      <h3 class="text-2xl font-serif text-main mb-2">{{ !customerUser ? 'Giriş Yapmalısınız' : 'Henüz Randevunuz Yok' }}</h3>
      <p class="text-main/40 max-w-sm mx-auto mb-8 text-sm">
        {{ !customerUser ? 'Randevularınızı görmek için lütfen hesabınıza giriş yapın.' : 'Henüz bir randevu oluşturmamışsınız. Hemen yeni bir randevu alarak başlayabilirsiniz.' }}
      </p>
      <router-link :to="!customerUser ? '/auth' : '/'" class="inline-flex items-center gap-2 px-8 py-3 bg-[#C5A059] text-[#0a0a0a] rounded-full font-black uppercase tracking-widest text-[10px] hover:bg-[#d4b06a] transition-all shadow-[0_0_20px_rgba(197,160,89,0.3)]">
        {{ !customerUser ? 'Giriş Yap' : 'Randevu Al' }}
        <ChevronRight class="w-4 h-4" />
      </router-link>
    </div>

    <!-- Appointments List -->
    <div v-else class="space-y-6">
      <div v-for="appt in myAppointments" :key="appt.id" 
           class="bg-surface/80 backdrop-blur-xl border border-main/5 rounded-[1.5rem] p-5 shadow-2xl hover:bg-surface-elevated/90 transition-all duration-500 flex flex-col md:flex-row items-center justify-between gap-6 relative"
           :class="{ 'opacity-50 grayscale': appt.status === 'İptal Edildi' }">
        
        <!-- Status Indicator Bar -->
        <div class="absolute left-0 top-0 bottom-0 w-1.5 transition-all duration-500" 
             :class="appt.status === 'İptal Edildi' ? 'bg-main/10' : 'bg-[#C5A059]'"
             :style="appt.status !== 'İptal Edildi' ? { background: appt.theme_accent || '#C5A059' } : {}"></div>
        
        <div class="flex-grow flex flex-col sm:flex-row items-start sm:items-center gap-6 w-full pl-2">
          <!-- Service Info -->
          <div class="min-w-[180px]">
            <div class="flex items-center gap-2 mb-1">
               <span class="text-[8px] uppercase tracking-widest font-black text-[#C5A059] bg-[#C5A059]/10 px-2 py-0.5 rounded-full border border-[#C5A059]/20">{{ appt.sector_name }}</span>
               <span class="text-[8px] uppercase tracking-widest font-black text-main/30">{{ appt.company_name }}</span>
            </div>
            <h3 class="text-lg font-serif text-main">{{ appt.service_name }}</h3>
            <p class="text-[10px] text-main/40 mt-1 font-medium">Uzman: <span class="text-main/60">{{ appt.staff_name }}</span></p>
          </div>
          
          <!-- Appointment Details -->
          <div class="flex flex-wrap gap-4 md:gap-8">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 bg-surface-elevated rounded-lg flex items-center justify-center border border-main/5">
                <Calendar class="w-3.5 h-3.5 text-main/50" />
              </div>
              <div>
                <span class="text-[8px] uppercase tracking-widest font-black text-main/20 block mb-0">Tarih</span>
                <p class="text-[11px] font-bold text-main/90">{{ formatDate(appt.date) }}</p>
              </div>
            </div>
            
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 bg-surface-elevated rounded-lg flex items-center justify-center border border-main/5">
                <Clock class="w-3.5 h-3.5 text-main/50" />
              </div>
              <div>
                <span class="text-[8px] uppercase tracking-widest font-black text-main/20 block mb-0">Saat</span>
                <p class="text-[11px] font-bold text-main/90">{{ appt.time }}</p>
              </div>
            </div>
 
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 bg-surface-elevated rounded-lg flex items-center justify-center border border-main/5">
                <Wallet class="w-3.5 h-3.5 text-main/50" />
              </div>
              <div>
                <span class="text-[8px] uppercase tracking-widest font-black text-main/20 block mb-0">Tutar</span>
                <p class="text-[11px] font-bold text-main/90">{{ appt.amount }} TL</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-3 w-full md:w-auto mt-4 md:mt-0">
          <div :class="[
            'px-4 py-2 rounded-xl text-[9px] font-black uppercase tracking-[0.2em] border transition-all', 
            appt.status === 'İptal Edildi' ? 'text-main/40 border-main/10 bg-surface-elevated' : 
            appt.status === 'Tamamlandı' ? 'text-emerald-400 border-emerald-400/20 bg-emerald-400/10' :
            'text-[#34d399] border-[#34d399]/20 bg-[#34d399]/10'
          ]">
            {{ appt.status }}
          </div>
          
          <div class="flex gap-2">
            <button v-if="appt.status === 'Kesinleşti'"
                    @click="initiateCancel(appt)"
                    :disabled="!isCancellable(appt.date, appt.time)"
                    class="p-3 rounded-xl border border-main/5 bg-surface-elevated text-main/40 hover:text-rose-400 hover:border-rose-400/20 hover:bg-rose-400/10 transition-all disabled:opacity-30 disabled:cursor-not-allowed group relative"
                    title="İptal Et">
              <Trash2 class="w-4 h-4" />
              <!-- Tooltip -->
              <div v-if="!isCancellable(appt.date, appt.time)" class="absolute bottom-full right-0 mb-3 w-48 p-3 bg-app border border-main/10 text-main/70 text-[10px] rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-[100] shadow-2xl text-center leading-relaxed">
                24 saatten az kaldığı için iptal edilemez.
              </div>
            </button>

            <button @click="addToCalendar(appt)"
                    class="p-3 rounded-xl border border-main/5 bg-surface-elevated text-main/40 hover:text-emerald-400 hover:border-emerald-400/20 hover:bg-emerald-400/10 transition-all"
                    title="Takvime Ekle">
              <Calendar class="w-4 h-4" />
            </button>

            <button @click="openReview(appt)" v-if="appt.status === 'Tamamlandı'"
                    class="p-3 rounded-xl border border-main/5 bg-surface-elevated text-main/40 hover:text-[#C5A059] hover:border-[#C5A059]/20 hover:bg-[#C5A059]/10 transition-all"
                    title="Değerlendir">
              <Star class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Cancellation Dialog Modal -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="cancellingAppointment" class="fixed inset-0 z-[300] flex items-center justify-center p-6">
          <div class="absolute inset-0 bg-app/90 backdrop-blur-md" @click="!isCancelling && cancelDialog()"></div>
          
          <div class="relative z-10 bg-surface border border-main/10 rounded-[2.5rem] p-10 w-full max-w-md shadow-2xl animate-scale-in">
            <div class="flex flex-col items-center text-center">
              <div class="w-16 h-16 bg-surface-elevated rounded-2xl flex items-center justify-center mb-6 border border-main/5 text-rose-500">
                <AlertCircle class="w-8 h-8" />
              </div>
              <h3 class="text-3xl font-serif text-main mb-4">Randevuyu İptal Et</h3>
              <p class="text-main/50 text-sm leading-relaxed mb-8">
                <span class="text-main font-bold block mb-1">{{ cancellingAppointment.service_name }}</span>
                {{ formatDate(cancellingAppointment.date) }} - {{ cancellingAppointment.time }} tarihindeki randevunuzu iptal etmek istediğinize emin misiniz?<br/><br/>
                <span class="text-[9px] uppercase font-black tracking-[0.2em] text-[#34d399] bg-[#34d399]/10 px-3 py-1 rounded-full border border-[#34d399]/20">Ücret iadesi yapılacaktır.</span>
              </p>
              
              <div class="flex gap-4 w-full">
                <button @click="cancelDialog()" :disabled="isCancelling"
                        class="flex-1 py-4 rounded-2xl border border-main/10 text-main/50 font-bold text-xs uppercase tracking-widest hover:bg-surface-elevated hover:text-main transition-all disabled:opacity-50">
                  Vazgeç
                </button>
                <button @click="confirmCancellation" :disabled="isCancelling"
                        class="flex-1 py-4 rounded-2xl bg-rose-500/20 text-rose-400 font-bold text-xs uppercase tracking-widest hover:bg-rose-500 hover:text-main border border-rose-500/30 transition-all shadow-lg disabled:opacity-50 flex justify-center items-center gap-2">
                  <Loader2 v-if="isCancelling" class="w-4 h-4 animate-spin" />
                  <span v-else>İptal Et</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Review Dialog Modal -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="reviewingAppt" class="fixed inset-0 z-[300] flex items-center justify-center p-6">
          <div class="absolute inset-0 bg-app/90 backdrop-blur-md" @click="!isReviewSubmitting && (reviewingAppt = null)"></div>
          
          <div class="relative z-10 bg-surface border border-main/10 rounded-[2.5rem] p-10 w-full max-w-lg shadow-2xl animate-scale-in text-center">
            <h2 class="text-3xl font-serif text-main mb-2">Deneyiminizi Paylaşın</h2>
            <p class="text-xs font-bold text-main/50 mb-10">{{ reviewingAppt.service_name }} hizmetimizi değerlendirin.</p>
            
            <div class="flex items-center justify-center gap-3 mb-8">
               <button v-for="star in 5" :key="star" @click="reviewRating = star" class="hover:scale-110 transition-transform focus:outline-none">
                 <Star :class="['w-10 h-10 transition-colors', reviewRating >= star ? 'text-[#C5A059] fill-[#C5A059]' : 'text-main/10']" />
               </button>
            </div>
            
            <textarea v-model="reviewComment" placeholder="Deneyiminizi birkaç kelimeyle anlatın..."
                      class="w-full bg-surface-elevated border border-main/5 rounded-2xl p-6 text-sm text-main focus:outline-none focus:border-[#C5A059]/50 h-32 resize-none mb-8 transition-all placeholder:text-main/20"></textarea>
                       
            <button @click="submitReview" :disabled="!reviewRating || isReviewSubmitting"
                    class="w-full py-5 bg-[#C5A059] text-[#0a0a0a] rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-[#d4b06a] transition-all shadow-[0_0_20px_rgba(197,160,89,0.3)] flex items-center justify-center gap-3 disabled:opacity-50 disabled:shadow-none">
               <Loader2 v-if="isReviewSubmitting" class="w-4 h-4 animate-spin" />
               <span v-else>Değerlendirmeyi Gönder</span>
            </button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { CalendarX, AlertCircle, Loader2, Star, Calendar, Clock, Wallet, ChevronRight, Trash2 } from 'lucide-vue-next'
import { useAppointmentStore } from '../stores/appointment'

const store = useAppointmentStore()
const { myAppointments } = storeToRefs(store)

const customerUser = computed(() => store.currentUser)

onMounted(() => {
  const phone = customerUser.value?.phone || store.customerPhone || localStorage.getItem('dita_user_phone')
  if (phone) {
    store.loadMyAppointments(phone)
  }
})

const emit = defineEmits(['toast'])

const cancellingAppointment = ref<any>(null)
const isCancelling = ref(false)

const formatDate = (isoString: string) => {
  if (!isoString) return ''
  return new Date(isoString).toLocaleDateString('tr-TR', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

const addToCalendar = (appt: any) => {
  const dateParts = appt.date.split('T')[0].split('-')
  const timeParts = appt.time.split(':')
  
  const yyyy = dateParts[0]
  const mm = dateParts[1]
  const dd = dateParts[2]
  const hh = timeParts[0]
  const min = timeParts[1]
  
  const startDt = `${yyyy}${mm}${dd}T${hh}${min}00`
  const endHh = (parseInt(hh) + 1).toString().padStart(2, '0')
  const endDt = `${yyyy}${mm}${dd}T${endHh}${min}00`
  
  const icsContent = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//DiTA//Appointment//TR
BEGIN:VEVENT
UID:${appt.id || Date.now()}@dita.com
DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'}
DTSTART;TZID=Europe/Istanbul:${startDt}
DTEND;TZID=Europe/Istanbul:${endDt}
SUMMARY:${appt.service_name} - ${appt.company_name || 'Randevu'}
DESCRIPTION:Hizmet: ${appt.service_name}\\nSektör: ${appt.sector_name}\\nDurum: ${appt.status}\\nUzman: ${appt.staff_name}
END:VEVENT
END:VCALENDAR`;

  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `randevu_${startDt}.ics`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Check if appointment is more than 24 hours away
const isCancellable = (dateStr: string, timeStr: string) => {
  if (!dateStr || !timeStr) return false
  
  try {
    const dtString = dateStr.split('T')[0] // handle if it's full ISO string
    const targetDt = new Date(`${dtString}T${timeStr}:00`)
    const diffMs = targetDt.getTime() - new Date().getTime()
    const diffHours = diffMs / (1000 * 60 * 60)
    return diffHours > 24
  } catch(e) {
    return false
  }
}

const initiateCancel = (appt: any) => {
  if (!isCancellable(appt.date, appt.time)) return
  cancellingAppointment.value = appt
}

const cancelDialog = () => {
  if (isCancelling.value) return
  cancellingAppointment.value = null
}

const confirmCancellation = async () => {
  if (!cancellingAppointment.value || !cancellingAppointment.value.cancel_token) {
    store.addToast('İptal tokeni bulunamadı.', 'error')
    cancelDialog()
    return
  }

  isCancelling.value = true
  const token = cancellingAppointment.value.cancel_token
  
  try {
    const response = await fetch(`/api/cancel-appointment/${token}`)
    const data = await response.json()
    
    if (response.ok && data.status === 'cancelled') {
        store.cancelAppointmentLocally(cancellingAppointment.value.id)
        store.addToast('Randevunuz iptal edildi ve iade başlatıldı.', 'success')
    } else {
        store.addToast(data.detail || data.message || 'İptal hatası.', 'error')
    }
  } catch (error) {
    store.addToast('Sunucu bağlantı hatası.', 'error')
  } finally {
    isCancelling.value = false
    cancelDialog()
  }
}

const reviewingAppt = ref<any>(null)
const reviewRating = ref(0)
const reviewComment = ref('')
const isReviewSubmitting = ref(false)

const openReview = (appt: any) => {
   reviewingAppt.value = appt
   reviewRating.value = 0
   reviewComment.value = ''
}

const submitReview = async () => {
    isReviewSubmitting.value = true
    try {
        const res = await fetch('/api/reviews', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                appointment_id: Number(reviewingAppt.value.db_id) || 0,
                rating: reviewRating.value,
                comment: reviewComment.value
            })
        })
        if (res.ok) {
           store.addToast('Değerlendirmeniz için teşekkürler!', 'success')
           reviewingAppt.value = null
           store.fetchInitialData() // refresh public reviews
        }
    } catch(e) {
      console.error(e)
    } finally {
      isReviewSubmitting.value = false
    }
}
</script>

<style scoped>
.animate-fade-in-up {
  animation: fade-in-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes fade-in-up {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
