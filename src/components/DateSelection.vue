<template>
  <div 
    class="max-w-7xl mx-auto px-4 py-12 md:py-20 animate-fade-in-up font-sans"
    :style="{
      '--accent': currentTheme.accent,
      '--accent-rgb': currentTheme.accentRgb,
      '--accent-dark': currentTheme.accentDark,
      '--accent-light': currentTheme.accentLight,
    }"
  >
    <!-- Premium Step Indicator -->
    <div class="flex items-center justify-center mb-20">
      <div class="flex items-center gap-3 md:gap-4">
        <template v-for="step in 5" :key="step">
          <div class="flex items-center">
            <div 
              class="w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500 font-sans font-bold text-sm"
              :class="[
                currentBookingStep >= (step - 1) 
                  ? 'bg-[#C5A059] border-[#C5A059] text-[#0a0a0a] shadow-[0_0_20px_rgba(197,160,89,0.3)]' 
                  : 'bg-surface-elevated border-main/10 text-main/40'
              ]"
            >
              <Check v-if="currentBookingStep > (step - 1)" class="w-5 h-5" />
              <span v-else>{{ step }}</span>
            </div>
            <div 
              v-if="step < 5"
              class="w-8 md:w-16 h-0.5 mx-1 transition-all duration-700 rounded-full"
              :class="currentBookingStep >= step ? 'bg-[#C5A059]' : 'bg-main/10'"
            ></div>
          </div>
        </template>
      </div>
    </div>

    <!-- ══ STEP 0: Sector Selection ═══════════════════════════════ -->
    <div v-if="currentBookingStep === 0" class="animate-scale-in">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-serif text-main mb-4">Size Nasıl Yardımcı Olabiliriz?</h2>
        <p class="text-main/50 text-lg max-w-2xl mx-auto font-sans">Uzman ekibimiz ve modern tesislerimizle dilediğiniz hizmeti seçerek hemen randevunuzu oluşturun.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <button v-for="sector in sectors"
                :key="sector.id"
                @click="selectSector(sector.id)"
                class="group relative bg-surface/80 backdrop-blur-xl rounded-[2rem] p-10 shadow-2xl hover:bg-surface-elevated/90 transition-all duration-500 border border-main/5 overflow-hidden flex flex-col items-center text-center">
          
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"
               :style="`background: radial-gradient(circle at 50% 100%, ${sector.theme.accent}15 0%, transparent 70%)`"></div>

          <div class="w-20 h-20 bg-surface-elevated rounded-2xl flex items-center justify-center text-5xl mb-8 group-hover:scale-110 transition-transform duration-500 border border-main/5">
            {{ sector.emoji }}
          </div>

          <div class="relative z-10 space-y-3">
            <h3 class="text-2xl font-serif text-main">{{ sector.name }}</h3>
            <p class="text-main/50 text-sm leading-relaxed font-sans">{{ sector.tagline }}</p>
          </div>

          <div class="mt-8 flex items-center gap-2 px-4 py-2 bg-surface-elevated rounded-full group-hover:bg-[#C5A059] transition-colors duration-500 border border-main/5">
            <span class="text-[10px] font-black uppercase tracking-[0.2em] text-main/40 group-hover:text-[#0a0a0a]">İncele</span>
            <ChevronRight class="w-4 h-4 text-main/40 group-hover:text-[#0a0a0a]" />
          </div>
        </button>
      </div>
    </div>

    <!-- ══ STEP 1: Company Selection ═══════════════════════════════ -->
    <div v-if="currentBookingStep === 1" class="animate-scale-in">
      <div class="flex items-center gap-4 mb-12 group cursor-pointer w-fit" @click="currentBookingStep = 0">
        <div class="w-10 h-10 flex items-center justify-center border border-main/10 rounded-full group-hover:bg-[#C5A059] group-hover:border-[#C5A059] transition-all duration-300">
          <ChevronLeft class="w-5 h-5 text-main/40 group-hover:text-[#0a0a0a] transition-colors" />
        </div>
        <span class="text-main/40 font-black uppercase text-[10px] tracking-[0.2em] group-hover:text-main transition-colors">Sektör Seçimine Dön</span>
      </div>

      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-serif text-main mb-4">Şubelerimiz</h2>
        <p class="text-main/50 text-lg">Size en yakın veya tercih ettiğiniz şubemizi seçin.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16 max-w-5xl mx-auto">
        <button v-for="company in sectorCompanies" :key="company.id"
                @click="selectCompany(company.id)"
                class="group relative bg-surface/80 backdrop-blur-xl rounded-[2rem] border border-main/5 p-8 shadow-2xl hover:bg-surface-elevated/90 transition-all duration-500 flex items-center gap-8 text-left">
           
           <div class="w-20 h-20 bg-surface-elevated rounded-2xl flex items-center justify-center border border-main/5 group-hover:bg-[#C5A059] transition-colors duration-500">
             <MapPin class="w-8 h-8 text-main/40 group-hover:text-[#0a0a0a] transition-colors" />
           </div>

           <div class="flex-grow space-y-2">
             <h3 class="text-2xl font-serif text-main">{{ company.name }}</h3>
             <div class="flex items-center gap-3">
               <div class="flex items-center">
                 <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= Math.round(getCompanyRating(company.id)) ? 'text-[#C5A059] fill-[#C5A059]' : 'text-main/10'" />
               </div>
               <span class="text-xs font-black text-main/40">{{ getCompanyRating(company.id) }} / 5.0</span>
             </div>
           </div>

           <div class="w-12 h-12 rounded-full bg-surface-elevated flex items-center justify-center group-hover:translate-x-1 transition-transform duration-300 border border-main/5">
             <ChevronRight class="w-6 h-6 text-main/30 group-hover:text-main" />
           </div>
        </button>
      </div>
    </div>

    <!-- ══ STEP 2: Service Selection ═══════════════════════════════ -->
    <div v-if="currentBookingStep === 2" class="animate-scale-in">
      <div class="flex items-center gap-4 mb-12 group cursor-pointer w-fit" @click="currentBookingStep = 1">
        <div class="w-10 h-10 flex items-center justify-center border border-main/10 rounded-full group-hover:bg-[#C5A059] group-hover:border-[#C5A059] transition-all duration-300">
          <ChevronLeft class="w-5 h-5 text-main/40 group-hover:text-[#0a0a0a] transition-colors" />
        </div>
        <span class="text-main/40 font-black uppercase text-[10px] tracking-[0.2em] group-hover:text-main transition-colors">Şube Seçimine Dön</span>
      </div>

      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-serif text-main mb-4">Hizmetlerimiz</h2>
        <p class="text-main/50 text-lg">Size en uygun deneyimi menümüzden seçin.</p>
      </div>
      
      <div v-for="(groupServices, category) in categorizedServices" :key="category" class="mb-12 max-w-5xl mx-auto">
        <h3 class="text-xl font-serif text-[#C5A059] mb-8 uppercase tracking-[0.3em] flex items-center gap-4">
          <span class="w-12 h-px bg-[#C5A059]/30"></span>
          {{ category }}
          <span class="flex-grow h-px bg-[#C5A059]/30"></span>
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <button v-for="(service, index) in groupServices" 
                  :key="service.id"
                  @click="selectedServiceId = service.id"
                  class="group relative bg-surface/80 backdrop-blur-xl rounded-[2.5rem] border transition-all duration-500 p-8 flex flex-col text-left"
                  :class="selectedServiceId === service.id ? 'border-[#C5A059] shadow-[0_0_30px_rgba(197,160,89,0.15)] scale-[1.02] bg-surface-elevated/90' : 'border-main/5 shadow-2xl hover:border-main/20'"
          >
            <div class="flex justify-between items-start mb-6">
              <span class="text-[10px] font-black tracking-widest uppercase text-main/30">#{{ index + 1 }}</span>
              <div v-if="selectedServiceId === service.id" class="w-6 h-6 bg-[#C5A059] text-[#0a0a0a] rounded-full flex items-center justify-center">
                <Check class="w-4 h-4" />
              </div>
            </div>

            <div class="space-y-2 mb-8">
              <h4 class="text-2xl font-serif text-main">{{ service.name }}</h4>
              <p class="text-main/50 text-sm leading-relaxed">{{ service.description }}</p>
            </div>

            <div class="mt-auto pt-6 border-t border-main/10 flex items-center justify-between">
              <div class="flex items-baseline gap-1">
                <span class="text-3xl font-serif text-main">{{ getServicePrice(service) }}</span>
                <span class="text-[10px] font-black text-main/40 uppercase tracking-widest">TL</span>
              </div>
              <div class="flex items-center gap-2 text-main/40">
                <Clock class="w-4 h-4" />
                <span class="text-xs font-bold">{{ getServiceDuration(service) }}</span>
              </div>
            </div>
          </button>
        </div>
      </div>

      <div class="flex justify-center mt-12">
        <button v-if="selectedServiceId"
                @click="currentBookingStep = 3" 
                class="px-12 py-5 bg-[#C5A059] text-[#0a0a0a] rounded-full font-black uppercase tracking-widest text-xs hover:bg-[#d4b06a] hover:scale-105 active:scale-95 transition-all shadow-[0_0_25px_rgba(197,160,89,0.3)] flex items-center gap-3">
          Uzman Seçimine Devam Et
          <ChevronRight class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- ══ STEP 3: Staff Selection ═══════════════════════════════ -->
    <div v-if="currentBookingStep === 3" class="animate-scale-in">
       <div class="flex items-center gap-4 mb-12 group cursor-pointer w-fit" @click="currentBookingStep = 2">
         <div class="w-10 h-10 flex items-center justify-center border border-main/10 rounded-full group-hover:bg-[#C5A059] group-hover:border-[#C5A059] transition-all duration-300">
           <ChevronLeft class="w-5 h-5 text-main/40 group-hover:text-[#0a0a0a] transition-colors" />
         </div>
         <span class="text-main/40 font-black uppercase text-[10px] tracking-[0.2em] group-hover:text-main transition-colors">Hizmet Seçimine Dön</span>
       </div>
       
       <div class="text-center mb-16">
         <h2 class="text-4xl md:text-5xl font-serif text-main mb-4">Uzmanlarımız</h2>
         <p class="text-main/50 text-lg">İşleminizi gerçekleştirecek deneyimli ekibimizle tanışın.</p>
       </div>
       
       <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-16 max-w-6xl mx-auto">
          <button v-for="staff in staffList.filter((s:any) => s.company_id === selectedCompanyId && s.service_ids?.includes(selectedServiceId))" :key="staff.id"
                  @click="selectedStaffName = staff.name; currentBookingStep = 4"
                  class="group relative bg-surface/80 backdrop-blur-xl border border-main/5 rounded-[2rem] p-8 shadow-2xl hover:bg-surface-elevated transition-all duration-500 flex flex-col items-center text-center">
             
             <div class="w-24 h-24 bg-surface-elevated border border-main/5 rounded-3xl flex items-center justify-center text-5xl mb-6 group-hover:scale-110 transition-transform duration-500 shadow-inner">
               {{ staff.avatar }}
             </div>

             <div class="space-y-1">
               <h3 class="text-xl font-serif text-main group-hover:text-[#C5A059] transition-colors">{{ staff.name }}</h3>
               <p class="text-[9px] font-black text-main/40 uppercase tracking-widest">{{ staff.title }}</p>
             </div>

             <div class="mt-6 w-full py-2 bg-surface-elevated rounded-xl group-hover:bg-[#C5A059] transition-colors duration-500 border border-main/5">
               <span class="text-[10px] font-black uppercase tracking-[0.2em] text-main/40 group-hover:text-[#0a0a0a]">Seç</span>
             </div>
          </button>
       </div>
    </div>

    <!-- ══ STEP 4: Date & Time Selection ═══════════════════════════════ -->
    <div v-if="currentBookingStep === 4" class="animate-scale-in">
      <div class="flex items-center gap-4 mb-12 group cursor-pointer w-fit" @click="currentBookingStep = 3">
        <div class="w-10 h-10 flex items-center justify-center border border-main/10 rounded-full group-hover:bg-[#C5A059] group-hover:border-[#C5A059] transition-all duration-300">
          <ChevronLeft class="w-5 h-5 text-main/40 group-hover:text-[#0a0a0a] transition-colors" />
        </div>
        <span class="text-main/40 font-black uppercase text-[10px] tracking-[0.2em] group-hover:text-main transition-colors">Uzman Seçimine Dön</span>
      </div>

      <div class="flex flex-col lg:flex-row gap-12 items-start">
        <!-- Calendar -->
        <div class="w-full lg:w-2/3 space-y-6">
          <div class="bg-surface/80 backdrop-blur-xl rounded-[2.5rem] p-8 shadow-2xl border border-main/5">
            <div class="flex items-center justify-between mb-10">
              <h2 class="text-3xl font-serif text-main tracking-tight">Randevu Tarihi</h2>
              <div class="flex items-center gap-3 bg-surface-elevated p-2 rounded-full border border-main/5">
                <button @click="prevMonth" class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-main/5 hover:text-main transition-all text-main/40">
                  <ChevronLeft class="w-5 h-5" />
                </button>
                <span class="text-[11px] font-black text-main min-w-[120px] text-center uppercase tracking-widest">
                  {{ format(currentDisplayDate, 'MMMM yyyy', { locale: tr }) }}
                </span>
                <button @click="nextMonth" class="w-10 h-10 flex items-center justify-center rounded-full hover:bg-main/5 hover:text-main transition-all text-main/40">
                  <ChevronRight class="w-5 h-5" />
                </button>
              </div>
            </div>

            <div class="grid grid-cols-7 gap-2">
              <div v-for="day in weekDays" :key="day" class="text-center text-[10px] uppercase tracking-widest font-black mb-6 text-main/30">
                {{ day }}
              </div>
              
              <div v-for="{ date, isCurrentMonth, isSelected, isToday, isClosed } in calendarDays" :key="date.toISOString()" class="aspect-square flex items-center justify-center">
                <button 
                  v-if="isCurrentMonth"
                  @click="!isClosed && selectDate(date)"
                  :disabled="isClosed"
                  class="w-full h-full rounded-2xl flex flex-col items-center justify-center transition-all duration-300 relative group overflow-hidden border"
                  :class="[
                    isClosed ? 'opacity-20 cursor-not-allowed border-transparent text-main/20' : 
                    isSelected ? 'bg-[#C5A059] border-[#C5A059] text-[#0a0a0a] shadow-[0_0_15px_rgba(197,160,89,0.3)] scale-105' : 
                    'bg-surface-elevated border-main/5 text-main/70 hover:border-main/20 hover:bg-surface-active'
                  ]"
                >
                  <span class="text-base font-serif z-10">{{ date.getDate() }}</span>
                  <div v-if="isToday && !isSelected" class="absolute bottom-2 w-1 h-1 rounded-full bg-[#C5A059]"></div>
                </button>
                <div v-else class="w-full h-full"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Hours List -->
        <div class="w-full lg:w-1/3">
          <div class="bg-surface/80 backdrop-blur-xl rounded-[2.5rem] p-8 shadow-2xl border border-main/5 min-h-[500px] flex flex-col">
            <div class="flex items-center gap-3 mb-8">
              <div class="w-10 h-10 rounded-xl bg-surface-elevated border border-main/5 flex items-center justify-center text-[#C5A059]">
                <Clock class="w-5 h-5" />
              </div>
              <h3 class="text-xl font-serif text-main">Uygun Saatler</h3>
            </div>

            <div v-if="isLoadingSlots" class="space-y-3">
              <BaseSkeleton v-for="i in 6" :key="i" height="56px" radius="16px" className="bg-main/5" />
            </div>

            <div v-else class="grid grid-cols-1 gap-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              <button 
                v-for="slot in availableSlots" 
                :key="slot"
                @click="selectTime(slot)"
                :disabled="bookedSlots.includes(slot)"
                class="h-14 rounded-2xl flex items-center justify-between px-6 transition-all duration-300 border font-sans font-bold tracking-widest text-[11px]"
                :class="[
                  selectedTime === slot ? 'bg-[#C5A059] border-[#C5A059] text-[#0a0a0a] shadow-lg' :
                  bookedSlots.includes(slot) ? 'bg-surface-elevated border-transparent text-main/20 cursor-not-allowed' :
                  'bg-surface-elevated border-main/5 text-main/60 hover:border-main/20 hover:bg-surface-active hover:text-main'
                ]"
              >
                <span>{{ slot }}</span>
                <Check v-if="selectedTime === slot" class="w-4 h-4" />
              </button>
            </div>

            <div class="mt-auto pt-8" v-if="selectedTime">
              <button @click="confirmBooking" 
                      :disabled="isProcessing"
                      class="w-full py-5 bg-[#C5A059] text-[#0a0a0a] rounded-2xl font-black text-[11px] uppercase tracking-[0.2em] hover:bg-[#d4b06a] hover:shadow-[0_0_20px_rgba(197,160,89,0.3)] transition-all flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed">
                <template v-if="isProcessing">
                   <div class="w-5 h-5 border-2 border-[#0a0a0a]/30 border-t-[#0a0a0a] rounded-full animate-spin"></div>
                   <span>İşleniyor...</span>
                </template>
                <template v-else>
                   Randevuyu Tamamla
                   <ShieldCheck class="w-5 h-5" />
                </template>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <CustomerModal 
      :is-open="isModalOpen" 
      :is-loading="isProcessing"
      :is-success="isRedirecting"
      :error-message="apiError"
      @close="isModalOpen = false" 
      @confirm="handleConfirm"
    />

    <!-- REVIEWS SECTION -->
    <div v-if="currentBookingStep >= 1 && selectedCompanyId && companyReviews && companyReviews.length > 0" class="mt-32 max-w-7xl mx-auto border-t border-main/10 pt-20">
       <div class="text-center mb-16">
         <h2 class="text-4xl font-serif text-main mb-4">Müşteri Deneyimleri</h2>
         <p class="text-main/40 font-black uppercase tracking-[0.3em] text-[9px]">Şubemiz hakkında ne dediler?</p>
       </div>
       
       <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div v-for="review in companyReviews.slice(0, 3)" :key="'preview-'+review.id"
               class="bg-surface/80 border border-main/5 rounded-[2rem] p-8 shadow-2xl hover:bg-surface-elevated transition-all cursor-pointer backdrop-blur-xl"
               @click="isPreviewModalOpen = true">
             <div class="flex items-center gap-1 mb-6">
               <Star v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= review.rating ? 'text-[#C5A059] fill-[#C5A059]' : 'text-main/10'" />
             </div>
             <p class="text-main/60 text-sm font-serif italic leading-relaxed mb-8">"{{ review.comment || 'Mükemmel bir hizmet aldım.' }}"</p>
             <div class="flex items-center gap-4">
               <div class="w-10 h-10 bg-surface-elevated border border-main/10 rounded-full flex items-center justify-center text-[#C5A059] font-serif text-lg">
                 {{ review.user_name.charAt(0) }}
               </div>
               <div class="flex flex-col">
                 <span class="text-xs font-bold text-main">{{ review.user_name }}</span>
                 <span class="text-[8px] font-black text-main/30 uppercase tracking-[0.2em] mt-0.5">{{ review.service_name }}</span>
               </div>
             </div>
          </div>
       </div>

       <div v-if="companyReviews.length > 3" class="text-center">
         <button @click="isPreviewModalOpen = true" class="px-8 py-3 bg-surface-elevated border border-main/10 rounded-full text-main/60 text-[10px] font-black uppercase tracking-[0.2em] hover:bg-surface-active hover:text-main transition-all">
           Tüm Yorumları Gör ({{ companyReviews.length }})
         </button>
       </div>
    </div>
    
    <!-- ALL REVIEWS MODAL -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="isPreviewModalOpen" class="fixed inset-0 z-[400] flex items-center justify-center p-6">
          <div class="absolute inset-0 bg-app/95 backdrop-blur-xl" @click="isPreviewModalOpen = false"></div>
          
          <div class="relative z-10 bg-surface border border-main/10 rounded-[3rem] p-8 w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl animate-scale-in">
            <!-- Header -->
            <div class="flex justify-between items-center mb-10 px-4">
               <div>
                  <h2 class="text-3xl font-serif text-main mb-2">Tüm Değerlendirmeler</h2>
                  <p class="text-[10px] font-sans uppercase tracking-[0.2em] text-main/40 font-black">Toplam {{ companyReviews.length }} Yorum</p>
               </div>
               <button @click="isPreviewModalOpen = false" class="w-12 h-12 rounded-full border border-main/10 bg-surface-elevated flex items-center justify-center text-main/50 hover:bg-main/10 hover:text-main transition-all outline-none">
                  <X class="w-5 h-5" />
               </button>
            </div>
            
            <!-- Scrollable Content -->
            <div class="flex-1 overflow-y-auto pr-4 space-y-6 custom-scrollbar">
               <div v-for="review in companyReviews" :key="review.id" class="p-8 bg-surface-elevated border border-main/5 rounded-3xl relative">
                  <div class="flex items-center gap-2 mb-4">
                     <Star v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= review.rating ? 'text-[#C5A059] fill-[#C5A059]' : 'text-main/10'" />
                  </div>
                  <p class="text-main/70 text-sm font-serif italic leading-relaxed mb-6">"{{ review.comment || 'Puanlama yapıldı.' }}"</p>
                  <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                     <div class="flex flex-col">
                       <span class="text-main font-bold text-sm">{{ review.user_name }}</span>
                       <span class="text-[9px] uppercase tracking-[0.2em] text-main/40 font-black mt-1">{{ review.service_name }}</span>
                     </div>
                     <span class="text-main/30 text-[10px] font-sans font-medium">{{ new Date(review.created_at).toLocaleDateString('tr-TR') }}</span>
                  </div>
               </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- PAYMENT CHECKOUT MODAL -->
    <Teleport to="body">
      <transition name="fade">
        <CheckoutSimulation 
          v-if="showCheckout" 
          :id="paymentId" 
          :amount="checkoutAmount"
          @success="handlePaymentSuccess" 
          @back="showCheckout = false" 
        />
      </transition>
    </Teleport>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import { startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, format, isSameDay, isSameMonth, addMonths, subMonths } from 'date-fns'
import { tr } from 'date-fns/locale'
import { useAppointmentStore } from '../stores/appointment'
import { storeToRefs } from 'pinia'
import { ChevronLeft, ChevronRight, CheckCircle, ShieldCheck, Check, Star, X, MapPin, Clock } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import CustomerModal from './CustomerModal.vue'
import BaseSkeleton from './BaseSkeleton.vue'
import CheckoutSimulation from './CheckoutSimulation.vue'

const router = useRouter()
const store = useAppointmentStore()

const { 
  services, 
  selectedServiceId,
  selectedSectorId,
  sectors,
  companies,
  selectedCompanyId,
  staffList,
  selectedStaffName,
  currentTheme,
  selectedDate, 
  selectedTime,
  availableSlots,
  currentBookingStep,
  businessSettings,
  reviews,
  categorizedServices
} = storeToRefs(store)

const sectorCompanies = computed(() => companies.value.filter((c:any) => c.sector_id === selectedSectorId.value))
const companyReviews = computed(() => reviews.value.filter((r: any) => r.company_id === selectedCompanyId.value))

const getCompanyRating = (cid: string) => {
  const compReviews = reviews.value.filter((r:any) => r.company_id === cid && r.rating);
  if(!compReviews.length) return companies.value.find((c:any) => c.id === cid)?.rating || 0;
  return Number((compReviews.reduce((sum:number, r:any) => sum + r.rating, 0) / compReviews.length).toFixed(1));
}

const selectSector = (id: string) => {
  selectedSectorId.value = id
  selectedCompanyId.value = null
  selectedServiceId.value = null
  currentBookingStep.value = 1
}

const getRomanNumeral = (idx: string | number) => {
  const numericIdx = Number(idx);
  const numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];
  return numerals[numericIdx] || String(numericIdx + 1);
}

const getServicePrice = (service: any) => {
  const comp = companies.value.find((c:any) => c.id === selectedCompanyId.value)
  if (comp && comp.custom_prices && comp.custom_prices[service.id]) {
     return comp.custom_prices[service.id]
  }
  return service.price
}

const getServiceDuration = (service: any) => {
  const comp = companies.value.find((c:any) => c.id === selectedCompanyId.value)
  if (comp && comp.custom_durations && comp.custom_durations[service.id]) {
     return comp.custom_durations[service.id]
  }
  return service.duration
}

const selectCompany = (id: string) => {
  selectedCompanyId.value = id
  selectedServiceId.value = null
  currentBookingStep.value = 2
}


const isModalOpen = ref(false)
const currentDisplayDate = ref(new Date())
const isLoadingSlots = ref(false)
const isPreviewModalOpen = ref(false)



const weekDays = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']

const calendarDays = computed(() => {
  const start = startOfWeek(startOfMonth(currentDisplayDate.value), { weekStartsOn: 1 })
  const end = endOfWeek(endOfMonth(currentDisplayDate.value), { weekStartsOn: 1 })
  
  const company = companies.value.find((c:any) => c.id === selectedCompanyId.value)
  const companySettings = company?.settings || businessSettings.value
  const closedDays = companySettings.closedDays || []

  return eachDayOfInterval({ start, end }).map(date => ({
    date,
    isCurrentMonth: isSameMonth(date, currentDisplayDate.value),
    isSelected: selectedDate.value ? isSameDay(date, selectedDate.value) : false,
    isToday: isSameDay(date, new Date()),
    isClosed: closedDays.includes(date.getDay())
  }))
})

const prevMonth = () => currentDisplayDate.value = subMonths(currentDisplayDate.value, 1)
const nextMonth = () => currentDisplayDate.value = addMonths(currentDisplayDate.value, 1)

const selectDate = async (date: Date) => {
  store.setSelectedDate(date)
  await fetchBookedHours(format(date, 'yyyy-MM-dd'))
}

const bookedSlots = ref<string[]>([])

const fetchBookedHours = async (dateStr: string) => {
  isLoadingSlots.value = true
  await new Promise(resolve => setTimeout(resolve, 800))
  
  try {
    let url = `/api/available-hours?date=${dateStr}`
    if (selectedStaffName.value) {
      url += `&staff_name=${encodeURIComponent(selectedStaffName.value)}`
    }
    const response = await fetch(url)
    if (response.ok) {
      bookedSlots.value = await response.json()
    }
  } catch (e) {
    console.error('Failed to fetch booked hours', e)
  } finally {
    isLoadingSlots.value = false
  }
}

const selectTime = (time: string) => {
  if (bookedSlots.value.includes(time)) return
  store.setSelectedTime(time)
}

const confirmBooking = () => {
  const userJson = localStorage.getItem('dita_customer_user') || sessionStorage.getItem('dita_customer_user')
  const user = userJson ? JSON.parse(userJson) : null
  
  if (user && user.name && user.phone) {
    handleConfirm({ name: user.name, phone: user.phone })
  } else {
    isModalOpen.value = true
  }
}

const isProcessing = ref(false)
const isRedirecting = ref(false)
const apiError = ref('')

const showCheckout = ref(false)
const paymentId = ref('')
const checkoutAmount = computed(() => {
  const srv = services.value.find((s:any) => s.id === selectedServiceId.value)
  return srv ? getServicePrice(srv) : 0
})

const handleConfirm = async (data: { name: string, phone: string }) => {
  if (isProcessing.value) return
  isProcessing.value = true
  apiError.value = ''
  store.setCustomerInfo(data.name, data.phone)
  const payload = store.prepareCheckoutPayload()
  
  try {
    const response = await fetch('/api/create-payment-intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) throw new Error('API Error')
    
    const result = await response.json()
    if (result.status === 'success') {
      isProcessing.value = false
      isRedirecting.value = true
      
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      paymentId.value = result.id || result.token?.split('_').pop() || `TRX-${Date.now()}`
      isModalOpen.value = false
      isRedirecting.value = false
      showCheckout.value = true
    } else {
       apiError.value = 'Sunucu hatası: ' + result.message
    }
  } catch (e) {
    apiError.value = 'Bağlantı hatası. Lütfen internetinizi kontrol edip tekrar deneyin.'
  } finally {
    isProcessing.value = false
  }
}

const handlePaymentSuccess = async () => {
  showCheckout.value = false
  isProcessing.value = true
  
  try {
    // Backend'e ödemenin başarılı olduğunu bildiriyoruz
    const response = await fetch(`/api/payment-callback?id=${paymentId.value}&status=SUCCESS`, {
      method: 'POST'
    })
    
    if (response.ok) {
      const data = await response.json()
      console.log('Payment success callback result:', data)
    } else {
      console.error('Payment callback failed', await response.text())
    }
  } catch (error) {
    console.error('Network error calling payment-callback', error)
  } finally {
    isProcessing.value = false
    // Başarılı ödeme sonrası randevularım sayfasına yönlendir veya formu sıfırla
    store.resetBooking()
    router.push('/my-appointments')
  }
}

const emit = defineEmits(['checkout'])





</script>

<style scoped>
.tracking-tightest {
  letter-spacing: -0.05em;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scale-in-center {
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes shimmer {
  100% { transform: translateX(100%); }
}


.slide-up-enter-active,

.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
