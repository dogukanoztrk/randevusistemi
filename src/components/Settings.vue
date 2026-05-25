<template>
  <div class="min-h-screen bg-transparent pb-20">
    <div class="w-full max-w-[95%] xl:max-w-[1400px] mx-auto animate-fade-in py-10 px-4 md:px-6"
         :style="companyContext?.theme ? { '--accent': companyContext.theme.accent, '--accent-rgb': companyContext.theme.accentRgb, '--accent-dark': companyContext.theme.accentDark, '--accent-light': companyContext.theme.accentLight } : { '--accent': '#0F172A', '--accent-rgb': '15, 23, 42', '--accent-dark': '#000000', '--accent-light': '#334155' }"
    >
      
      <!-- ══ COMPANY LOGIN SCREEN ════════════════════════════════════ -->
      <div v-if="!isAuthenticated" class="max-w-md mx-auto mt-20 md:mt-32 animate-scale-in relative z-10">
        <div class="bg-surface/80 backdrop-blur-2xl border border-main/10 rounded-[2.5rem] p-8 md:p-12 shadow-2xl text-center relative overflow-hidden">
          
          <!-- Subtle Glow Behind -->
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-[#C5A059]/5 blur-[100px] pointer-events-none rounded-full"></div>

          <div class="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-8 bg-surface-elevated border border-main/5 relative z-10">
            <Lock class="w-10 h-10 text-[#C5A059]" />
          </div>
          <h2 class="text-3xl font-serif text-main mb-2 relative z-10">İşletme Paneli</h2>
          <p class="text-[10px] text-main/40 font-black uppercase tracking-[0.2em] mb-10 relative z-10">Güvenli yönetim paneline erişin</p>
          
          <div class="space-y-5 mb-10 relative z-10">
            <div class="space-y-2 text-left">
              <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Şirket Kodu</label>
              <input type="text" v-model="dashboardCode" placeholder="Örn: INK001" 
                     class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 text-center font-sans font-bold tracking-widest transition-all uppercase placeholder:text-main/20 shadow-inner" />
            </div>
            <div class="space-y-2 text-left">
              <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Giriş Şifresi</label>
              <input type="password" v-model="password" @keyup.enter="login" placeholder="••••••••"
                     class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main focus:outline-none focus:border-[#C5A059] focus:ring-1 focus:ring-[#C5A059]/50 text-center font-sans text-xl transition-all placeholder:text-main/20 shadow-inner" />
            </div>
          </div>

          <div v-if="loginError" class="p-4 bg-rose-500/100/10 border border-rose-500/20 rounded-2xl mb-8 flex items-center gap-3 animate-shake relative z-10">
            <AlertCircle class="w-5 h-5 text-rose-400 shrink-0" />
            <p class="text-rose-400 text-[11px] font-bold text-left leading-tight">{{ loginError }}</p>
          </div>
                 
          <button @click="login" :disabled="isLoggingIn"
                  class="relative z-10 w-full py-5 bg-[#C5A059] text-[#0a0a0a] rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-[#d4b06a] transition-all flex items-center justify-center gap-3 shadow-[0_0_20px_rgba(197,160,89,0.3)] disabled:opacity-50">
            <Loader2 v-if="isLoggingIn" class="w-5 h-5 animate-spin" />
            <template v-else>
              Sistemi Aç
              <LockOpen class="w-5 h-5" />
            </template>
          </button>
        </div>
      </div>

      <!-- ══ ADMIN DASHBOARD ═════════════════════════════════════════ -->
      <div v-else class="space-y-8">
        
        <!-- Dashboard Header & Top Navigation -->
        <div class="bg-surface/80 backdrop-blur-xl rounded-[2.5rem] border border-main/10 p-6 md:p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)] mb-8">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
            <div class="flex items-center gap-6">
              <div class="w-16 h-16 bg-[#C5A059] rounded-2xl flex items-center justify-center shadow-lg shrink-0">
                <ShieldCheck class="w-8 h-8 text-main" />
              </div>
              <div>
                <div class="flex items-center gap-3 mb-1">
                  <h2 class="text-3xl font-heading font-bold text-main tracking-tight">{{ companyContext?.company_name || 'Panel' }}</h2>
                  <span class="px-3 py-1 bg-main/5 text-main/60 text-[9px] font-black uppercase tracking-widest rounded-lg border border-main/10">
                    {{ companyContext?.sector_name || 'Business' }}
                  </span>
                </div>
                <p class="text-main/40 text-[10px] font-bold uppercase tracking-widest flex items-center gap-2">
                  ID: <span class="text-main font-mono">{{ companyContext?.dashboard_code || '—' }}</span>
                </p>
              </div>
            </div>
            
            <div class="flex items-center gap-2 bg-surface-elevated p-1.5 rounded-[1.25rem] border border-main/10 overflow-x-auto no-scrollbar">
              <button v-for="tab in [
                { id: 'appointments', label: 'Randevular', icon: Clock },
                { id: 'analytics', label: 'İstatistikler', icon: BarChart3 },
                { id: 'crm', label: 'Müşteriler', icon: Users },
                { id: 'services', label: 'Hizmetler', icon: LayoutGrid },
                { id: 'staff', label: 'Ekip', icon: UserCircle },
                { id: 'reviews', label: 'Yorumlar', icon: Star },
                { id: 'logs', label: 'İşlem Kayıtları', icon: ShieldCheck },
                { id: 'settings', label: 'Ayarlar', icon: SettingsIcon }
              ]" 
              :key="tab.id"
              @click="activeTab = tab.id" 
              :class="[
                'px-5 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center gap-2 whitespace-nowrap',
                activeTab === tab.id ? 'bg-surface/80 backdrop-blur-xl text-main shadow-sm border border-main/10' : 'text-main/40 hover:text-main/60 hover:bg-main/5/50'
              ]">
                <component :is="tab.icon" class="w-4 h-4" />
                {{ tab.label }}
              </button>
            </div>

            <button @click="logout" class="px-6 py-4 bg-surface/80 backdrop-blur-xl text-rose-500 rounded-xl text-[10px] font-black uppercase tracking-widest border border-main/10 hover:bg-rose-500/10 hover:text-rose-400 hover:border-rose-500/20 transition-all shadow-sm">
              Sistemi Kilitle
            </button>
          </div>
        </div>


        <!-- TAB 1: Appointments -->
        <div v-if="activeTab === 'appointments'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-6 md:p-8 shadow-2xl overflow-hidden">
             <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
               <div>
                  <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Randevu Kayıtları</h3>
                  <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Tüm rezervasyonları buradan yönetin</p>
               </div>
               <div class="flex items-center gap-3">
                   <button @click="exportCSV" class="px-6 py-3 bg-surface/80 backdrop-blur-xl border border-main/10 text-main/60 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-surface-elevated transition-all flex items-center gap-2">
                      <Download class="w-3.5 h-3.5" />
                      Dışa Aktar
                   </button>
                   <button @click="clearAllAppts" class="px-6 py-3 bg-rose-500/10 border border-rose-500/20 text-rose-500 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-rose-500/20 transition-all">
                      Logları Temizle
                   </button>
               </div>
             </div>
             
             <div class="overflow-x-auto no-scrollbar -mx-6 md:mx-0">
                <table class="w-full text-left font-sans min-w-[1000px]">
                   <thead>
                     <tr class="text-[10px] text-main/40 uppercase tracking-widest border-b border-main/5 bg-surface-elevated/50">
                       <th class="py-5 px-6 font-black first:rounded-l-2xl">Müşteri</th>
                       <th class="py-5 px-6 font-black">Hizmet & Tutar</th>
                       <th class="py-5 px-6 font-black">Zaman</th>
                       <th class="py-5 px-6 font-black">Durum</th>
                       <th class="py-5 px-6 font-black">Notlar</th>
                       <th class="py-5 px-6 font-black text-right last:rounded-r-2xl">Aksiyon</th>
                     </tr>
                   </thead>
                   <tbody class="text-sm">
                     <tr v-for="app in adminAppointments" :key="app.id" class="border-b border-main/5 hover:bg-surface-elevated/50 transition-colors group">
                       <td class="py-5 px-6">
                         <div class="flex items-center gap-4">
                           <div class="w-10 h-10 rounded-full bg-main/5 flex items-center justify-center text-main/40 font-bold border border-main/10">
                             {{ app.user_name?.charAt(0) || '?' }}
                           </div>
                           <div>
                             <p class="font-bold text-main text-base leading-none mb-1.5">{{ app.user_name }}</p>
                             <p class="text-[10px] font-medium text-main/40">{{ app.user_email }}</p>
                           </div>
                         </div>
                       </td>
                       <td class="py-5 px-6">
                         <p class="font-bold text-main mb-1">{{ app.service_name }}</p>
                         <p class="text-xs font-black text-main/40 uppercase tracking-widest">{{ app.amount }} TL</p>
                       </td>
                       <td class="py-5 px-6">
                         <div class="flex flex-col">
                           <span class="font-bold text-main">{{ new Date(app.appointment_date).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' }) }}</span>
                           <span class="text-xs font-medium text-main/40">{{ app.appointment_time }}</span>
                         </div>
                       </td>
                       <td class="py-5 px-6">
                         <span :class="[
                           'px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border',
                           app.status === 'Tamamlandı' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                           app.status === 'Kesinleşti' ? 'bg-[#34d399]/10 text-[#34d399] border-[#34d399]/20' :
                           app.status === 'Beklemede' ? 'bg-[#C5A059]/10 text-[#C5A059] border-[#C5A059]/20' :
                           'bg-rose-500/10 text-rose-400 border-rose-500/20'
                         ]">
                           {{ app.status }}
                         </span>
                       </td>
                       <td class="py-5 px-6 max-w-[200px]">
                         <input type="text" v-model="app.admin_notes" @blur="saveNote(app)" placeholder="Not ekle..." 
                                class="w-full bg-transparent border-none focus:ring-0 text-xs text-main/50 italic placeholder:opacity-30" />
                       </td>
                       <td class="py-5 px-6 text-right flex justify-end gap-2">
                          <a v-if="app.status === 'Kesinleşti' || app.status === 'Beklemede'" 
                             :href="`https://wa.me/90${app.user_email?.replace(/\\D/g, '')}?text=Merhaba ${app.user_name}, ${new Date(app.appointment_date).toLocaleDateString('tr-TR')} ${app.appointment_time} tarihindeki randevunuzu hatırlatmak isteriz.`"
                             target="_blank"
                             class="p-2 text-main/20 hover:text-green-400 hover:bg-green-500/10 rounded-lg transition-all" title="WhatsApp'tan Hatırlat">
                            <MessageCircle class="w-4 h-4" />
                          </a>
                          <button v-if="app.status === 'Kesinleşti'" @click="completeAppt(app)" :disabled="app.isCompleting"
                                  class="p-2 text-main/20 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all disabled:opacity-30" title="Tamamlandı İşaretle">
                            <CheckCircle2 v-if="!app.isCompleting" class="w-4 h-4" />
                            <Loader2 v-else class="w-4 h-4 animate-spin" />
                          </button>
                          <button v-if="app.status !== 'İptal Edildi' && app.status !== 'Kesinleşti' && app.status !== 'Tamamlandı'" @click="forceCancel(app)" :disabled="app.isCancelling"
                                  class="p-2 text-main/20 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-all disabled:opacity-30" title="İptal Et">
                            <Ban v-if="!app.isCancelling" class="w-4 h-4" />
                            <Loader2 v-else class="w-4 h-4 animate-spin" />
                          </button>
                          <button v-if="isPast(app.appointment_date) || app.status === 'İptal Edildi' || app.status === 'Tamamlandı'" @click="deleteAppt(app)" :disabled="app.isDeleting"
                                  class="p-2 text-main/20 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-all disabled:opacity-30" title="Kaydı Sil">
                            <Trash2 v-if="!app.isDeleting" class="w-4 h-4" />
                            <Loader2 v-else class="w-4 h-4 animate-spin" />
                          </button>
                        </td>
                     </tr>
                   </tbody>
                </table>
             </div>
           </div>
        </div>


        <!-- TAB: Analytics -->
        <div v-if="activeTab === 'analytics'" class="animate-fade-in space-y-8">
           <!-- Analytics Summary Overview -->
           <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2rem] shadow-2xl relative overflow-hidden group hover:border-[#C5A059]/50 transition-colors">
                <div class="absolute -right-4 -bottom-4 opacity-5 rotate-12 transition-transform group-hover:scale-110">
                  <DollarSign class="w-32 h-32 text-main" />
                </div>
                <h3 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-4">Net Ciro</h3>
                <p class="text-4xl font-heading font-bold tracking-tight text-main">
                  {{ analyticsData?.revenue || 0 }} TL
                </p>
                <div class="mt-4 flex items-center gap-2">
                  <span class="text-[10px] font-bold text-[#34d399] bg-[#34d399]/10 px-2 py-0.5 rounded-full"><TrendingUp class="w-3 h-3 inline" /> Aktif</span>
                  <span class="text-[9px] text-main/40 font-bold uppercase tracking-widest">Bu Dönem</span>
                </div>
              </div>

              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2rem] shadow-2xl relative overflow-hidden group hover:border-[#C5A059]/50 transition-colors">
                <div class="absolute -right-4 -bottom-4 opacity-5 rotate-12 transition-transform group-hover:scale-110">
                  <Calendar class="w-32 h-32 text-main" />
                </div>
                <h3 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-4">Toplam Randevu</h3>
                <p class="text-4xl font-heading font-bold tracking-tight text-main">
                  {{ analyticsData?.total || 0 }}
                </p>
                <div class="mt-4 flex items-center gap-2">
                  <span class="text-[9px] text-main/40 font-bold uppercase tracking-widest">Tamamlanan</span>
                </div>
              </div>

              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2rem] shadow-2xl relative overflow-hidden group hover:border-[#C5A059]/50 transition-colors">
                <div class="absolute -right-4 -bottom-4 opacity-5 rotate-12 transition-transform group-hover:scale-110">
                  <ClockAlert class="w-32 h-32 text-main" />
                </div>
                <h3 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-4">Bekleyen</h3>
                <p class="text-4xl font-heading font-bold tracking-tight text-main">
                  {{ analyticsData?.pending || 0 }}
                </p>
                <div class="mt-4 flex items-center gap-2">
                  <span class="text-[9px] text-main/40 font-bold uppercase tracking-widest">İşlem Bekliyor</span>
                </div>
              </div>

              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2rem] shadow-2xl relative overflow-hidden group hover:border-[#C5A059]/50 transition-colors">
                <div class="absolute -right-4 -bottom-4 opacity-5 rotate-12 transition-transform group-hover:scale-110">
                  <Ban class="w-32 h-32 text-main" />
                </div>
                <h3 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-4">İptaller</h3>
                <p class="text-4xl font-heading font-bold tracking-tight text-main">
                  {{ analyticsData?.cancelled || 0 }}
                </p>
                <div class="mt-4 flex items-center gap-2">
                  <span class="text-[9px] text-main/40 font-bold uppercase tracking-widest">Gelmeyen</span>
                </div>
              </div>
           </div>

           <!-- Analytics Charts Section -->
           <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <!-- Revenue Trend Chart -->
              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2.5rem] shadow-2xl">
                 <div class="flex items-center justify-between mb-8">
                   <h3 class="text-xs font-black uppercase tracking-widest text-main/40 flex items-center gap-2">
                      <DollarSign class="w-4 h-4" />
                      Ciro Trendi (Son 14 Gün)
                   </h3>
                 </div>
                 <div v-if="chartData.dailyRevenue.length">
                    <apexchart type="area" height="300" :options="revenueChartOptions" :series="revenueChartSeries" />
                 </div>
                 <div v-else class="py-20 text-center">
                    <p class="text-main/30 text-xs font-bold uppercase tracking-widest">Henüz veri bulunmuyor</p>
                 </div>
              </div>

              <!-- Service Popularity Pie -->
              <div class="bg-surface/80 backdrop-blur-xl border border-main/10 p-8 rounded-[2.5rem] shadow-2xl">
                 <div class="flex items-center justify-between mb-8">
                   <h3 class="text-xs font-black uppercase tracking-widest text-main/40 flex items-center gap-2">
                      <LayoutGrid class="w-4 h-4" />
                      Hizmet Dağılımı
                   </h3>
                 </div>
                 <div v-if="chartData.servicePopularity.length">
                    <apexchart type="donut" height="300" :options="serviceChartOptions" :series="serviceChartSeries" />
                 </div>
                 <div v-else class="py-20 text-center">
                    <p class="text-main/30 text-xs font-bold uppercase tracking-widest">Henüz veri bulunmuyor</p>
                 </div>
              </div>
           </div>
        </div>


        <!-- TAB 2: CRM (Customers) -->
        <div v-if="activeTab === 'crm'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
              <div class="flex items-center justify-between mb-12">
                 <div>
                    <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Müşteri Portföyü</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Sadık müşterilerinizi ve harcamalarını takip edin</p>
                 </div>
                 <div class="bg-surface-elevated p-2 rounded-2xl border border-main/10 flex items-center gap-4">
                    <span class="text-[10px] font-black uppercase tracking-widest text-main/40 ml-2">Filtrele:</span>
                    <select v-model="selectedCrmSectorId" class="bg-transparent border-none text-[10px] font-black uppercase tracking-widest text-main focus:ring-0 cursor-pointer">
                       <option v-for="s in adminSectors" :key="s.id" :value="s.id">{{ s.name }}</option>
                    </select>
                 </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                 <div v-for="customer in crmCustomers" :key="customer.contact" 
                      class="bg-surface/80 backdrop-blur-xl border border-main/5 p-8 rounded-[2rem] shadow-sm hover:shadow-[0_0_40px_rgba(0,0,0,0.5)] hover:border-[#C5A059]/50 transition-all group">
                    <div class="flex items-start justify-between mb-8">
                       <div class="w-14 h-14 bg-surface-elevated rounded-2xl flex items-center justify-center text-main/40 text-xl font-bold border border-main/5 group-hover:bg-[#C5A059] group-hover:text-main transition-all">
                          {{ customer.name?.charAt(0) }}
                       </div>
                       <div class="text-right">
                          <p class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-1">Toplam Harcama</p>
                          <p class="text-2xl font-heading font-bold text-main">{{ customer.totalSpent }} TL</p>
                       </div>
                    </div>
                    <div class="space-y-1 mb-8">
                       <h4 class="text-lg font-heading font-bold text-main">{{ customer.name }}</h4>
                       <p class="text-[10px] font-bold text-main/40 uppercase tracking-widest">{{ customer.contact }}</p>
                    </div>
                    <div class="pt-6 border-t border-slate-50 grid grid-cols-2 gap-4">
                       <div>
                          <p class="text-[8px] text-main/40 uppercase tracking-widest font-black mb-1">Randevu</p>
                          <p class="text-sm font-bold text-main">{{ customer.totalAppointments }} İşlem</p>
                       </div>
                       <div>
                          <p class="text-[8px] text-main/40 uppercase tracking-widest font-black mb-1">Son Ziyaret</p>
                          <p class="text-sm font-bold text-main">{{ new Date(customer.lastVisit).toLocaleDateString('tr-TR') }}</p>
                       </div>
                    </div>
                 </div>
              </div>
               <div v-if="!crmCustomers.length" class="py-20 text-center">
                  <p class="text-main/40 text-xs font-bold uppercase tracking-widest">Bu kriterlerde müşteri bulunamadı</p>
               </div>
            </div>
         </div>
        <!-- TAB 3: Services -->
        <div v-if="activeTab === 'services'" class="animate-fade-in space-y-8">
          <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
             <div class="flex items-center justify-between mb-12">
                <div>
                   <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Hizmet Kataloğu</h3>
                   <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Fiyat ve süre tanımlamalarını yönetin</p>
                </div>
                <div class="flex items-center gap-3">
                   <button @click="addNewService" class="px-6 py-3 bg-surface/80 backdrop-blur-xl border border-main/10 text-main/60 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-surface-elevated transition-all">
                      + Yeni Hizmet
                   </button>
                   <button @click="saveCompanyServices" class="px-8 py-3 bg-[#C5A059] text-[#0a0a0a] rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#d4b06a] transition-all shadow-lg">
                      Kataloğu Kaydet
                   </button>
                </div>
             </div>

             <div v-if="currentCompany" class="space-y-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                   <div v-for="service in currentCompany.services" :key="service.id" 
                        class="bg-surface-elevated border border-main/10 rounded-[2rem] p-8 hover:bg-surface/80 backdrop-blur-xl hover:border-[#C5A059]/50 transition-all shadow-sm">
                      <div class="flex items-center justify-between mb-6 gap-4">
                          <input type="text" v-model="service.name" placeholder="Hizmet Adı" 
                                 class="w-full bg-transparent border-none p-0 text-lg font-heading font-bold text-main focus:ring-0 placeholder:text-main/30" />
                          <button @click="removeService(service.id)" class="text-[9px] font-black uppercase tracking-widest text-rose-400 hover:text-rose-500 transition-colors shrink-0 bg-rose-500/10 hover:bg-rose-500/20 px-3 py-1.5 rounded-lg border border-rose-500/20">
                             Kaldır
                          </button>
                      </div>
                      <div class="grid grid-cols-2 gap-6">
                         <div class="space-y-2">
                            <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Fiyat (TL)</label>
                            <input type="number" v-model="service.price" 
                                   class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-bold focus:outline-none focus:border-[#C5A059] transition-all" />
                         </div>
                         <div class="space-y-2">
                            <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Süre</label>
                            <input type="text" v-model="service.duration" 
                                   class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-bold focus:outline-none focus:border-[#C5A059] transition-all" />
                         </div>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </div>

        <!-- TAB 4: Staff (Ekip) -->
        <div v-if="activeTab === 'staff'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
              <div class="flex items-center justify-between mb-12">
                 <div>
                    <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Ekip Yönetimi</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Uzmanları ve yetkinliklerini belirleyin</p>
                 </div>
                 <div class="flex items-center gap-3">
                    <button @click="addNewStaff" class="px-6 py-3 bg-surface/80 backdrop-blur-xl border border-main/10 text-main/60 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-surface-elevated transition-all">
                       + Yeni Üye
                    </button>
                    <button @click="saveStaff" class="px-8 py-3 bg-[#C5A059] text-[#0a0a0a] rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#d4b06a] transition-all shadow-lg">
                       Ekibi Güncelle
                    </button>
                 </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                 <div v-for="staff in adminStaff.filter(s => s.company_id === companyContext.company_id)" :key="staff.id" 
                      class="bg-surface-elevated border border-main/10 rounded-[2rem] p-8 hover:bg-surface/80 backdrop-blur-xl hover:border-[#C5A059]/50 transition-all shadow-sm">
                    <div class="flex items-center gap-6 mb-8">
                       <input type="text" v-model="staff.avatar" class="w-16 h-16 bg-surface/80 backdrop-blur-xl rounded-2xl text-3xl flex items-center justify-center border border-main/10 text-center focus:outline-none focus:border-[#C5A059]" />
                       <div class="flex-grow space-y-1">
                          <input type="text" v-model="staff.name" class="w-full bg-transparent border-none p-0 text-lg font-heading font-bold text-main focus:ring-0 placeholder:text-main/30" placeholder="İsim Soyisim" />
                          <input type="text" v-model="staff.title" class="w-full bg-transparent border-none p-0 text-[10px] font-bold text-main/40 uppercase tracking-widest focus:ring-0 placeholder:text-main/20" placeholder="Uzmanlık Alanı" />
                       </div>
                    </div>
                    <div class="space-y-6">
                       <div class="space-y-2">
                          <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Verilen Hizmet ID'leri (Virgül ile ayırın)</label>
                          <input type="text" :value="staff.service_ids?.join(', ')" @input="(e) => updateServiceIds(staff, e)"
                                 class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-mono text-xs focus:outline-none focus:border-[#C5A059] transition-all" />
                       </div>

                       <div v-if="staff.working_hours" class="grid grid-cols-2 gap-4">
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mesai Başlangıç</label>
                             <input type="time" v-model="staff.working_hours.startTime"
                                    class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-2 px-3 text-main text-xs focus:border-[#C5A059]" />
                          </div>
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mesai Bitiş</label>
                             <input type="time" v-model="staff.working_hours.endTime"
                                    class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-2 px-3 text-main text-xs focus:border-[#C5A059]" />
                          </div>
                       </div>

                       <div v-if="staff.breaks" class="grid grid-cols-2 gap-4">
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mola Başlangıç</label>
                             <input type="time" v-model="staff.breaks.startTime"
                                    class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-2 px-3 text-main text-xs focus:border-[#C5A059]" />
                          </div>
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mola Bitiş</label>
                             <input type="time" v-model="staff.breaks.endTime"
                                    class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-2 px-3 text-main text-xs focus:border-[#C5A059]" />
                          </div>
                       </div>

                       <button @click="removeStaff(staff.id)" class="text-[9px] font-black uppercase tracking-widest text-rose-300 hover:text-rose-500 transition-colors ml-1">
                          Personeli Kaldır
                       </button>
                    </div>
                 </div>
              </div>
           </div>
        </div>

        <!-- TAB 5: Reviews (Yorumlar) -->
        <div v-if="activeTab === 'reviews'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
              <div class="flex items-center justify-between mb-12">
                 <div>
                    <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Müşteri Değerlendirmeleri</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Hizmet kalitenizi ölçümleyin</p>
                 </div>
                 <div class="flex items-center gap-6">
                    <div class="text-right">
                       <p class="text-[9px] text-main/40 uppercase tracking-widest font-black mb-1">Ortalama Puan</p>
                       <div class="flex items-center gap-2">
                          <Star class="w-5 h-5 text-amber-400 fill-amber-400" />
                          <span class="text-2xl font-heading font-bold text-main">{{ companyRating }}</span>
                       </div>
                    </div>
                 </div>
              </div>

              <div class="space-y-4">
                 <div v-for="review in adminReviews" :key="review.id" 
                      class="bg-surface-elevated border border-main/5 rounded-[2rem] p-8 hover:bg-surface/80 backdrop-blur-xl hover:border-main/10 transition-all flex flex-col md:flex-row gap-8">
                    <div class="shrink-0">
                       <div class="flex items-center gap-1 mb-4">
                          <Star v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= review.rating ? 'text-amber-400 fill-amber-400' : 'text-main/20'" />
                       </div>
                       <p class="text-[10px] font-black uppercase tracking-widest text-main/40">{{ new Date(review.created_at).toLocaleDateString('tr-TR') }}</p>
                    </div>
                    <div class="flex-grow">
                       <p class="text-main text-sm font-medium leading-relaxed mb-4 italic">"{{ review.comment || 'Puanlama yapıldı, yorum bırakılmadı.' }}"</p>
                       <p class="text-xs font-bold text-main/50 uppercase tracking-widest">— {{ review.user_name }}</p>
                    </div>
                 </div>
                 <div v-if="!adminReviews.length" class="py-20 text-center">
                    <p class="text-main/40 text-xs font-bold uppercase tracking-widest">Henüz değerlendirme yapılmamış</p>
                 </div>
              </div>
           </div>
        </div>

        <!-- TAB 6: Settings (Ayarlar) -->
        <div v-if="activeTab === 'settings'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
              <div class="flex items-center justify-between mb-12">
                 <div>
                    <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">Sistem Ayarları</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Çalışma saatleri ve randevu algoritması</p>
                 </div>
                 <button @click="save" class="px-10 py-4 bg-[#C5A059] text-[#0a0a0a] rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#d4b06a] transition-all shadow-lg">
                    Ayarları Kaydet
                 </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                 <div class="space-y-10">
                    <div>
                       <h4 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-6 flex items-center gap-2">
                          <Clock class="w-3.5 h-3.5" /> Mesai Saatleri
                       </h4>
                       <div class="grid grid-cols-2 gap-6">
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Açılış</label>
                             <input type="time" v-model="form.startTime" class="w-full bg-surface-elevated border border-main/10 rounded-xl py-4 px-6 text-main font-bold focus:outline-none focus:border-[#C5A059] transition-all" />
                          </div>
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Kapanış</label>
                             <input type="time" v-model="form.endTime" class="w-full bg-surface-elevated border border-main/10 rounded-xl py-4 px-6 text-main font-bold focus:outline-none focus:border-[#C5A059] transition-all" />
                          </div>
                       </div>
                    </div>

                    <div>
                       <h4 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-6 flex items-center gap-2">
                          <Calendar class="w-3.5 h-3.5" /> Kapalı Günler
                       </h4>
                       <div class="flex flex-wrap gap-2">
                          <button v-for="day in weekDays" :key="day.value" 
                                  @click="toggleDay(day.value)"
                                  :class="['px-5 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest border transition-all', form.closedDays.includes(day.value) ? 'bg-rose-500/10 border-rose-500/20 text-rose-500' : 'bg-surface-elevated border-main/10 text-main/40 hover:border-slate-400']">
                             {{ day.label }}
                          </button>
                       </div>
                    </div>
                 </div>

                 <div class="space-y-10">
                    <!-- Kurumsal Kimlik -->
                    <div>
                       <h4 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-6 flex items-center gap-2">
                          <LayoutGrid class="w-3.5 h-3.5" /> Kurumsal Kimlik
                       </h4>
                       <div class="bg-surface-elevated rounded-[2rem] p-8 space-y-6 border border-main/5">
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Logo URL</label>
                             <input type="text" v-model="form.logo_url" placeholder="https://..." class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main text-xs focus:border-[#C5A059]" />
                          </div>
                          <div class="space-y-2">
                             <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Marka Rengi</label>
                             <div class="flex items-center gap-4">
                                <input type="color" v-model="form.brand_color" class="w-12 h-12 bg-transparent border-none cursor-pointer" />
                                <span class="text-xs font-mono text-main/40">{{ form.brand_color }}</span>
                             </div>
                          </div>
                       </div>
                    </div>

                    <div>
                       <h4 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-6 flex items-center gap-2">
                          <Coffee class="w-3.5 h-3.5" /> Mola Ayarları
                       </h4>
                       <div class="bg-surface-elevated rounded-[2rem] p-8 space-y-6 border border-main/5">
                          <div class="flex items-center justify-between">
                             <span class="text-xs font-bold text-main/60">Öğle Molası Uygula</span>
                             <button @click="form.hasBreak = !form.hasBreak" :class="['w-14 h-8 rounded-full relative transition-all duration-300', form.hasBreak ? 'bg-[#C5A059]' : 'bg-slate-200']">
                                <div :class="['absolute top-1 w-6 h-6 bg-surface/80 backdrop-blur-xl rounded-full transition-all duration-300', form.hasBreak ? 'left-7' : 'left-1']"></div>
                             </button>
                          </div>
                          <div v-if="form.hasBreak" class="grid grid-cols-2 gap-4 animate-fade-in">
                             <div class="space-y-2">
                                <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mola Başlangıç</label>
                                <input type="time" v-model="form.breakStartTime" class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-bold focus:outline-none focus:border-[#C5A059]" />
                             </div>
                             <div class="space-y-2">
                                <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Mola Bitiş</label>
                                <input type="time" v-model="form.breakEndTime" class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-bold focus:outline-none focus:border-[#C5A059]" />
                             </div>
                          </div>
                       </div>
                    </div>

                    <div>
                       <h4 class="text-[10px] text-main/40 uppercase tracking-widest font-black mb-4 flex items-center gap-2">
                          <Hourglass class="w-3.5 h-3.5" /> Randevu Sıklığı
                       </h4>
                       <div class="relative">
                          <select v-model="form.intervalMinutes" class="w-full bg-surface-elevated border border-main/10 rounded-xl py-4 px-6 text-main font-bold focus:outline-none focus:border-[#C5A059] appearance-none cursor-pointer">
                             <option :value="15">Her 15 Dakikada Bir</option>
                             <option :value="30">Her 30 Dakikada Bir</option>
                             <option :value="45">Her 45 Dakikada Bir</option>
                             <option :value="60">Her 60 Dakikada Bir</option>
                             <option :value="90">Her 90 Dakikada Bir</option>
                             <option :value="120">Her 2 Saatte Bir</option>
                          </select>
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>

        <!-- TAB: İşlem Kayıtları (Audit Logs) -->
        <div v-if="activeTab === 'logs'" class="animate-fade-in space-y-8">
           <div class="bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[2.5rem] p-8 shadow-[0_0_40px_rgba(0,0,0,0.5)]">
              <div class="flex items-center justify-between mb-12">
                 <div>
                    <h3 class="text-2xl font-heading font-bold text-main tracking-tight mb-1">İşlem Kayıtları</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Panelde yapılan tüm değişikliklerin günlüğü</p>
                 </div>
                 <div class="flex items-center gap-2">
                    <span class="text-[10px] font-black uppercase tracking-widest text-main/30">{{ auditLogs.length }} kayıt</span>
                 </div>
              </div>

              <div v-if="auditLogs.length" class="space-y-3">
                 <div v-for="log in auditLogs" :key="log.id" 
                      class="bg-surface-elevated border border-main/5 rounded-2xl p-6 hover:border-main/10 transition-all group">
                    <div class="flex items-start justify-between gap-4">
                       <div class="flex items-start gap-4 min-w-0">
                          <div class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 mt-0.5"
                               :class="[
                                  log.action?.includes('DELETE') || log.action?.includes('CANCEL') ? 'bg-rose-500/10 border border-rose-500/20' :
                                  log.action?.includes('CREATE') || log.action?.includes('COMPLETE') ? 'bg-emerald-500/10 border border-emerald-500/20' :
                                  'bg-[#C5A059]/10 border border-[#C5A059]/20'
                               ]">
                             <ShieldCheck class="w-4 h-4" 
                                  :class="[
                                     log.action?.includes('DELETE') || log.action?.includes('CANCEL') ? 'text-rose-400' :
                                     log.action?.includes('CREATE') || log.action?.includes('COMPLETE') ? 'text-emerald-400' :
                                     'text-[#C5A059]'
                                  ]" />
                          </div>
                          <div class="min-w-0">
                             <div class="flex items-center gap-2 mb-1.5">
                                <span class="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md"
                                      :class="[
                                         log.action?.includes('DELETE') || log.action?.includes('CANCEL') ? 'bg-rose-500/10 text-rose-400' :
                                         log.action?.includes('CREATE') || log.action?.includes('COMPLETE') ? 'bg-emerald-500/10 text-emerald-400' :
                                         'bg-[#C5A059]/10 text-[#C5A059]'
                                      ]">
                                   {{ log.action }}
                                </span>
                                <span class="text-[9px] font-bold text-main/20">•</span>
                                <span class="text-[9px] font-bold text-main/30">{{ log.admin_name }}</span>
                             </div>
                             <p class="text-sm text-main/60 leading-relaxed truncate">{{ log.detail }}</p>
                          </div>
                       </div>
                       <span class="text-[9px] font-bold text-main/20 whitespace-nowrap shrink-0">
                          {{ log.created_at ? new Date(log.created_at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '' }}
                       </span>
                    </div>
                 </div>
              </div>

              <div v-else class="py-20 text-center">
                 <div class="w-16 h-16 bg-surface-elevated border border-main/10 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <ShieldCheck class="w-8 h-8 text-main/20" />
                 </div>
                 <p class="text-main/40 text-xs font-bold uppercase tracking-widest mb-2">Henüz işlem kaydı bulunmuyor</p>
                 <p class="text-main/20 text-[10px]">Paneldeki değişiklikler otomatik olarak burada listelenecektir</p>
              </div>
           </div>
        </div>


        <!-- TAB: Manual Booking (Overlay UI) -->
        <div v-if="activeTab === 'manual_booking'" class="animate-fade-in">
           <div class="max-w-2xl mx-auto bg-surface/80 backdrop-blur-xl border border-main/10 rounded-[3rem] p-12 shadow-2xl">
              <div class="flex justify-between items-start mb-12">
                 <div>
                    <h3 class="text-3xl font-heading font-bold text-main mb-2">Manuel Kayıt</h3>
                    <p class="text-[10px] text-main/40 font-black uppercase tracking-widest">Telefonla gelen randevuları sisteme işleyin</p>
                 </div>
                 <button @click="activeTab = 'appointments'" class="p-3 bg-surface-elevated text-main/40 rounded-full hover:bg-[#C5A059] hover:text-main transition-all">
                    <X class="w-6 h-6" />
                 </button>
              </div>

              <div class="space-y-6">
                 <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Müşteri Adı</label>
                       <input type="text" v-model="manualForm.customer_name" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Telefon</label>
                       <input type="text" v-model="manualForm.customer_phone" placeholder="05XX" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                 </div>

                 <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Hizmet Tutarı (TL)</label>
                       <input type="number" v-model="manualForm.service_price" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Alınan Ön Ödeme (TL)</label>
                       <input type="number" v-model="manualForm.deposit_amount" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                 </div>

                 <div class="space-y-2">
                    <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Hizmet</label>
                    <input type="text" v-model="manualForm.service_name" placeholder="Örn: Saç Kesimi" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                 </div>

                 <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Tarih</label>
                       <input type="date" v-model="manualForm.appointment_date" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                    <div class="space-y-2">
                       <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Saat</label>
                       <input type="time" v-model="manualForm.appointment_time" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold focus:bg-surface/80 backdrop-blur-xl transition-all" />
                    </div>
                 </div>

                 <div class="pt-10">
                    <button @click="submitManualBooking" 
                            class="w-full py-5 bg-[#C5A059] text-[#0a0a0a] rounded-2xl font-heading font-bold text-lg hover:bg-[#d4b06a] transition-all shadow-xl">
                       Randevuyu Kesinleştir
                    </button>
                 </div>
              </div>
           </div>
        </div>

      </div>
    </div>

    <!-- Company Custom Prices Modal (RESTORED) -->
    <div v-if="editingCompanyPrices" class="fixed inset-0 bg-[#C5A059]/60 backdrop-blur-md z-[200] flex items-center justify-center p-4">
      <div class="bg-surface/80 backdrop-blur-xl rounded-[3rem] p-10 lg:p-14 max-w-2xl w-full shadow-2xl relative overflow-hidden animate-scale-in">
         <div class="relative z-10">
           <div class="flex items-center gap-4 mb-8">
              <div class="w-14 h-14 bg-surface-elevated border border-main/10 rounded-2xl flex items-center justify-center">
                 <Coffee class="w-7 h-7 text-main" />
              </div>
              <div>
                 <h3 class="text-3xl font-heading font-bold text-main tracking-tight">{{ editingCompanyPrices.name }}</h3>
                 <p class="text-xs text-main/40 font-bold uppercase tracking-widest">Özel Fiyatlandırma Paneli</p>
              </div>
           </div>

           <p class="text-main/50 text-sm mb-10 leading-relaxed italic">Bu şubeye özel fiyat ve süre tanımlaması yapabilirsiniz. Boş bırakılan alanlarda sektörün genel ayarları geçerli olacaktır.</p>
           
           <div class="space-y-4 max-h-[50vh] overflow-y-auto pr-4 no-scrollbar">
              <div v-for="svc in getSectorServices(editingCompanyPrices.sector_id)" :key="svc.id" class="bg-surface-elevated border border-main/10 p-6 rounded-[2rem] group hover:bg-surface/80 backdrop-blur-xl hover:shadow-[0_0_40px_rgba(0,0,0,0.5)] transition-all">
                 <div class="mb-6">
                    <p class="text-lg font-heading font-bold text-main">{{ svc.name }}</p>
                    <p class="text-[9px] uppercase tracking-widest text-main/40 font-black mt-1">Standart: {{ svc.price }} TL | {{ svc.duration }}</p>
                 </div>
                 
                 <div class="grid grid-cols-2 gap-6">
                    <div class="space-y-1">
                       <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Özel Fiyat (TL)</label>
                       <input type="number" v-model="editingCompanyPrices.custom_prices[svc.id]" placeholder="Standart" class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-heading font-bold focus:border-[#C5A059] transition-all text-right" />
                    </div>
                    <div class="space-y-1">
                       <label class="text-[9px] uppercase tracking-widest font-black text-main/40 ml-1">Özel Süre</label>
                       <input type="text" v-model="editingCompanyPrices.custom_durations[svc.id]" placeholder="Örn: 45 dk" class="w-full bg-surface/80 backdrop-blur-xl border border-main/10 rounded-xl py-3 px-4 text-main font-heading font-bold focus:border-[#C5A059] transition-all" />
                    </div>
                 </div>
              </div>
           </div>
           
           <div class="mt-12 flex justify-end gap-4">
              <button @click="editingCompanyPrices = null" class="px-8 py-4 text-main/40 hover:text-main text-[10px] font-black uppercase tracking-widest transition-all">Kapat</button>
              <button @click="saveCompanyPrices" class="px-10 py-4 bg-[#C5A059] text-[#0a0a0a] rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-[#d4b06a] transition-all shadow-lg active:scale-95">Değişiklikleri Uygula</button>
           </div>
         </div>
      </div>
    </div>

    <!-- Complete Appointment Confirmation Modal -->
    <Teleport to="body">
      <div v-if="completingAppt" class="fixed inset-0 bg-app/90 backdrop-blur-md z-[300] flex items-center justify-center p-6">
        <div class="bg-surface border border-main/10 rounded-[2.5rem] p-10 w-full max-w-md shadow-2xl animate-scale-in">
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-emerald-500/20">
              <CheckCircle2 class="w-8 h-8 text-emerald-400" />
            </div>
            <h3 class="text-2xl font-heading font-bold text-main mb-2">Hizmeti Tamamla</h3>
            <p class="text-main/40 text-xs font-bold uppercase tracking-widest">{{ completingAppt.user_name }} - {{ completingAppt.service_name }}</p>
          </div>

          <div class="space-y-6 mb-10">
            <div class="space-y-2">
              <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Alınan Toplam Tutar (TL)</label>
              <input type="number" v-model="completeForm.finalPrice" class="w-full bg-surface-elevated border border-main/10 rounded-2xl py-4 px-6 text-main font-bold text-xl text-center focus:border-emerald-500 transition-all" />
            </div>
            
            <div class="space-y-2">
              <label class="text-[10px] uppercase tracking-widest font-black text-main/40 ml-2">Ödeme Yöntemi</label>
              <div class="grid grid-cols-2 gap-4">
                <button v-for="m in ['Nakit', 'Kart']" :key="m" @click="completeForm.paymentMethod = m"
                        :class="[
                          'py-3 rounded-xl text-[10px] font-black uppercase tracking-widest border transition-all',
                          completeForm.paymentMethod === m ? 'bg-main text-black border-main' : 'bg-surface-elevated text-main/40 border-main/5 hover:border-main/20'
                        ]">
                  {{ m }}
                </button>
              </div>
            </div>
          </div>

          <div class="flex gap-4">
            <button @click="completingAppt = null" class="flex-1 py-4 text-main/40 font-bold text-[10px] uppercase tracking-widest hover:text-main transition-all">Vazgeç</button>
            <button @click="submitComplete" :disabled="completingAppt.isCompleting" class="flex-1 py-4 bg-emerald-500 text-[#0a0a0a] rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-emerald-400 transition-all shadow-lg flex justify-center items-center gap-2">
               <Loader2 v-if="completingAppt.isCompleting" class="w-4 h-4 animate-spin" />
               <span v-else>Kaydet ve Kapat</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAppointmentStore } from '../stores/appointment'
import { 
  Lock, LockOpen, Loader2, ShieldCheck, Calendar, UserPlus, Users, Briefcase, 
  Settings as SettingsIcon, LogOut, CheckCircle2, Clock, MapPin, Phone, 
  CreditCard, ChevronRight, Download, Filter, Search, AlertCircle, 
  Trash2, Mail, ExternalLink, ArrowUpRight, BarChart3, TrendingUp, DollarSign, 
  Coffee, UserCircle, Star, LayoutGrid, Hourglass, ClockAlert, Ban, MessageCircle
} from 'lucide-vue-next'
import BaseSkeleton from './BaseSkeleton.vue'
import ApexCharts from 'vue3-apexcharts'

const store = useAppointmentStore()
const emit = defineEmits(['toast'])

// Authentication State
const authToken = ref(localStorage.getItem('companyToken') || '')
const isAuthenticated = ref(!!authToken.value)
const isLoggingIn = ref(false)
const password = ref('')
const dashboardCode = ref('')
const loginError = ref('')
const activeTab = ref('appointments')
const companyContext = ref<any>(JSON.parse(localStorage.getItem('companyContext') || 'null'))

const selectedCrmSectorId = ref<string | null>(null)
const editingCompanyPrices = ref<any>(null)

const currentCompany = computed(() => {
  return adminCompanies.value.find(c => c.id === companyContext.value?.company_id) || null
})

const initCompanyServices = () => {
  if (currentCompany.value && !currentCompany.value.services) {
    const sector = adminSectors.value.find(s => s.id === currentCompany.value.sector_id)
    if (sector) {
      currentCompany.value.services = JSON.parse(JSON.stringify(sector.services))
    } else {
      currentCompany.value.services = []
    }
  }
}

// Data State
const adminAppointments = ref<any[]>([])
const adminSectors = ref<any[]>([])
const adminStaff = ref<any[]>([])
const adminReviews = ref<any[]>([])
const adminCompanies = ref<any[]>([])
const auditLogs = ref<any[]>([])

// Complete Appointment Modal State
const completingAppt = ref<any>(null)
const completeForm = ref({ finalPrice: 0, paymentMethod: 'Nakit' })

// Manual Booking State
const manualForm = ref({
  customer_name: '',
  customer_phone: '',
  service_name: '',
  service_price: 0,
  deposit_amount: 0,
  staff_name: 'Panel (Admin)',
  company_id: '',
  appointment_date: '',
  appointment_time: ''
})

const analyticsData = ref<any>(null)
const fetchAnalytics = async () => {
    try {
        const res = await apiFetch('/api/admin/analytics')
        analyticsData.value = await res.json()
    } catch(e) {
        console.error(e)
    }
}

watch(activeTab, (newTab) => {
    if (newTab === 'analytics') fetchAnalytics()
})

const submitManualBooking = async () => {
  manualForm.value.company_id = companyContext.value.company_id
  
  if (!manualForm.value.customer_name || !manualForm.value.service_name || !manualForm.value.appointment_date || !manualForm.value.appointment_time) {
    emit('toast', { msg: 'Lütfen tüm zorunlu alanları (İsim, Hizmet, Tarih, Saat) doldurun.', type: 'error' })
    return
  }
  
  try {
    const res = await apiFetch('/api/admin/appointments/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(manualForm.value)
    })
    
    if (res.ok) {
      emit('toast', { msg: 'Manuel randevu başarıyla eklendi.', type: 'success' })
      activeTab.value = 'appointments'
      // Reset form
      manualForm.value = {
        customer_name: '',
        customer_phone: '',
        service_name: '',
        service_price: 0,
        deposit_amount: 0,
        staff_name: 'Panel (Admin)',
        company_id: '',
        appointment_date: '',
        appointment_time: ''
      }
      bootAdminData()
    } else {
      const data = await res.json()
      console.error('Manual booking error:', data)
      emit('toast', { msg: 'Kayıt eklenemedi: Veri doğrulama hatası.', type: 'error' })
    }
  } catch (e) {
    console.error('Network error:', e)
    emit('toast', { msg: 'Bağlantı hatası.', type: 'error' })
  }
}

const apiFetch = async (url: string, options: any = {}) => {
  const headers = { ...options.headers, 'Authorization': `Bearer ${authToken.value}` }
  const res = await fetch(url, { ...options, headers })
  if (res.status === 401 || res.status === 403) {
    logout()
    emit('toast', { msg: 'Oturum süresi doldu.', type: 'error' })
    throw new Error('Unauthorized')
  }
  return res
}

const login = async () => {
  loginError.value = ''
  if (!dashboardCode.value || !password.value) {
    loginError.value = 'Şirket kodu ve şifre gereklidir.'
    return
  }
  
  isLoggingIn.value = true
  try {
    const res = await fetch('/api/company/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dashboard_code: dashboardCode.value.toUpperCase(), password: password.value })
    })
    const data = await res.json()
    if (res.ok) {
      authToken.value = data.token
      const sectorTheme = data.sector?.theme || { accent: '#0F172A', accentRgb: '15, 23, 42', accentDark: '#000000', accentLight: '#334155' }
      companyContext.value = {
        company_id: data.company.id,
        company_name: data.company.name,
        sector_id: data.company.sector_id,
        sector_name: data.sector?.name || '',
        dashboard_code: data.company.dashboard_code,
        brand_color: data.company.brand_color,
        logo_url: data.company.logo_url,
        theme: sectorTheme
      }
      localStorage.setItem('companyToken', data.token)
      localStorage.setItem('companyContext', JSON.stringify(companyContext.value))
      isAuthenticated.value = true
      emit('toast', { msg: `${data.company.name} paneline giriş yapıldı.`, type: 'success' })
      bootAdminData()
    } else {
      loginError.value = data.detail || 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.'
    }
  } catch (e) {
    loginError.value = 'Bağlantı hatası. Lütfen internetinizi kontrol edin.'
  } finally {
    isLoggingIn.value = false
  }
}

const logout = () => {
  isAuthenticated.value = false
  password.value = ''
  dashboardCode.value = ''
  authToken.value = ''
  companyContext.value = null
  localStorage.removeItem('companyToken')
  localStorage.removeItem('companyContext')
  adminAppointments.value = []
}

const bootAdminData = async () => {
  fetchAdminAppointments()
  fetchAnalytics()
  fetchChartData()
  fetchSectorsData()
  fetchAdminStaff()
  fetchAdminReviews()
  fetchAdminCompanies()
  fetchAuditLogs()
}

// Fetch Functions
const fetchAdminAppointments = async () => {
  try {
     const res = await apiFetch('/api/admin/appointments')
     if (res.ok) adminAppointments.value = await res.json()
  } catch (e) {}
}

// consolidated fetchAnalytics is defined earlier

const chartData = ref<any>({ dailyRevenue: [], servicePopularity: [], hourlyHeatmap: [], companyBreakdown: [] })

const fetchChartData = async () => {
  try {
     const res = await apiFetch('/api/admin/analytics/charts')
     if (res.ok) {
        const data = await res.json()
        chartData.value = { dailyRevenue: data.daily_revenue || [], servicePopularity: data.service_popularity || [], hourlyHeatmap: data.hourly_heatmap || [], companyBreakdown: data.company_breakdown || [] }
     }
  } catch (e) {}
}

// Chart Options (Optimized for Dark Theme)
const revenueChartOptions = computed(() => ({
  chart: { type: 'area' as const, toolbar: { show: false }, background: 'transparent', fontFamily: 'Inter, sans-serif' },
  theme: { mode: 'dark' as const },
  colors: ['#C5A059'],
  fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.3, opacityTo: 0.05, stops: [0, 100] } },
  stroke: { curve: 'smooth' as const, width: 3 },
  xaxis: { categories: chartData.value.dailyRevenue.map((d: any) => { const p = d.date.split('-'); return p[2] + '/' + p[1] }), labels: { style: { colors: '#94A3B8', fontSize: '10px', fontWeight: 600 } }, axisBorder: { show: false }, axisTicks: { show: false } },
  yaxis: { labels: { style: { colors: '#94A3B8', fontSize: '10px', fontWeight: 600 } } },
  grid: { borderColor: 'rgba(255,255,255,0.05)', strokeDashArray: 4 },
  tooltip: { theme: 'dark' },
  dataLabels: { enabled: false }
}))
const revenueChartSeries = computed(() => [{ name: 'Ciro', data: chartData.value.dailyRevenue.map((d: any) => d.revenue) }])

const serviceChartOptions = computed(() => ({
  chart: { type: 'donut' as const, background: 'transparent', fontFamily: 'Inter, sans-serif' },
  theme: { mode: 'dark' as const },
  colors: ['#C5A059', '#D4B06A', '#9A7A40', '#634E28', '#3F3118', '#E8D5A3'],
  labels: chartData.value.servicePopularity.map((s: any) => s.name),
  legend: { position: 'bottom' as const, labels: { colors: '#94A3B8' }, fontSize: '11px', fontWeight: 600 },
  stroke: { colors: ['#111111'], width: 3 },
  plotOptions: { pie: { donut: { size: '75%', labels: { show: true, total: { show: true, label: 'Toplam', color: '#94A3B8' } } } } },
  dataLabels: { enabled: false }
}))
const serviceChartSeries = computed(() => chartData.value.servicePopularity.map((s: any) => s.count))

const companyRating = computed(() => {
  if (!adminReviews.value.length) return '0.0'
  const sum = adminReviews.value.reduce((acc, r) => acc + r.rating, 0)
  return (sum / adminReviews.value.length).toFixed(1)
})

const fetchSectorsData = async () => {
  try {
     const res = await fetch('/api/sectors')
     if (res.ok) adminSectors.value = await res.json()
  } catch (e) {}
}

const fetchAdminStaff = async () => {
  try {
     const res = await apiFetch('/api/staff')
     if (res.ok) adminStaff.value = await res.json()
  } catch (e) {}
}

const fetchAdminReviews = async () => {
  try {
     const res = await apiFetch('/api/admin/reviews')
     if (res.ok) adminReviews.value = await res.json()
  } catch (e) {}
}

const fetchAdminCompanies = async () => {
  try {
     const res = await fetch('/api/companies')
     if (res.ok) {
         adminCompanies.value = await res.json()
         initCompanyServices()
     }
  } catch (e) {}
}

// Logic Actions
const addNewStaff = () => {
  const newId = `s${Date.now()}_temp`
  adminStaff.value.push({
    id: newId,
    name: '',
    title: '',
    avatar: '👤',
    company_id: companyContext.value.company_id,
    service_ids: [],
    working_hours: { startTime: '09:00', endTime: '18:00' },
    breaks: { startTime: '12:00', endTime: '13:00' }
  })
}

const removeStaff = (id: string) => {
  adminStaff.value = adminStaff.value.filter(s => s.id !== id)
}

const addNewService = () => {
  if (currentCompany.value) {
    if (!currentCompany.value.services) currentCompany.value.services = []
    const nextId = currentCompany.value.services.length > 0 ? Math.max(...currentCompany.value.services.map((s: any) => s.id)) + 1 : 1
    currentCompany.value.services.push({
      id: nextId,
      name: '',
      price: 0,
      duration: '60 dk',
      description: '',
      features: []
    })
  }
}

const removeService = (serviceId: number) => {
  if (currentCompany.value) {
    currentCompany.value.services = currentCompany.value.services.filter((s: any) => s.id !== serviceId)
  }
}

const updateServiceIds = (staff: any, event: Event) => {
  const target = event.target as HTMLInputElement | null;
  if (target) {
    staff.service_ids = target.value.split(',').map(n => Number(n.trim())).filter(n => n);
  }
}

const saveStaff = async () => {
   try {
      const res = await apiFetch(`/api/staff`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(adminStaff.value)
      })
      if (res.ok) {
        emit('toast', { msg: 'Personel listesi güncellendi.', type: 'success' })
        store.fetchInitialData()
      }
   } catch (e) {}
}

const saveNote = async (app: any) => {
   try {
      const res = await apiFetch(`/api/admin/appointments/${app.id}/notes`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ note: app.admin_notes })
      })
      if (res.ok) emit('toast', { msg: 'CRM notu güncellendi.', type: 'success' })
   } catch(e) {}
}

const isPast = (dateStr: string) => {
  const appDate = new Date(dateStr)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return appDate < today
}

const deleteAppt = async (app: any) => {
   if (!confirm('Bu randevu kaydını kalıcı olarak silmek istediğinize emin misiniz?')) return
   app.isDeleting = true
   try {
      const res = await apiFetch(`/api/admin/appointments/${app.id}`, { method: 'DELETE' })
      if (res.ok) {
        adminAppointments.value = adminAppointments.value.filter(a => a.id !== app.id)
        emit('toast', { msg: `Randevu kaydı silindi.`, type: 'success' })
        fetchAnalytics()
      }
   } catch(e) {} finally { app.isDeleting = false }
}

const clearAllAppts = async () => {
   if (!confirm('TÜM randevu kayıtlarını (geçmiş ve gelecek) kalıcı olarak temizlemek istediğinize emin misiniz? Bu işlem geri alınamaz!')) return
   try {
      const res = await apiFetch(`/api/admin/appointments/clear-all`, { method: 'DELETE' })
      if (res.ok) {
        adminAppointments.value = []
        emit('toast', { msg: `Tüm randevu kayıtları temizlendi.`, type: 'success' })
        fetchAnalytics()
      }
   } catch(e) {}
}

const forceCancel = async (app: any) => {
   if (app.status === 'Kesinleşti' || app.status === 'Tamamlandı') {
      emit('toast', { msg: 'Kesinleşmiş veya tamamlanmış randevular iptal edilemez.', type: 'error' })
      return
   }
   if (!confirm('Bu randevuyu iptal etmek istediğinize emin misiniz?')) return
   app.isCancelling = true
   try {
      const res = await apiFetch(`/api/admin/appointments/${app.id}/cancel`, { method: 'POST' })
      if (res.ok) {
        app.status = 'İptal Edildi'
        emit('toast', { msg: `Randevu iptal edildi.`, type: 'success' })
        fetchAnalytics()
      }
   } catch(e) {} finally { app.isCancelling = false }
}

const completeAppt = (app: any) => {
   completingAppt.value = app
   completeForm.value.finalPrice = app.amount
}

const submitComplete = async () => {
   if (!completingAppt.value) return
   const app = completingAppt.value
   app.isCompleting = true
   try {
      const res = await apiFetch(`/api/admin/appointments/${app.id}/complete`, { 
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ 
            final_price: completeForm.value.finalPrice,
            payment_method: completeForm.value.paymentMethod
         })
      })
      if (res.ok) {
        app.status = 'Tamamlandı'
        emit('toast', { msg: `Randevu tamamlandı. Ödeme: ${completeForm.value.finalPrice} TL (${completeForm.value.paymentMethod})`, type: 'success' })
        completingAppt.value = null
        fetchAnalytics()
      }
   } catch(e) {} finally { app.isCompleting = false }
}

const saveCompanyServices = async () => {
   await saveCompanies()
   emit('toast', { msg: 'Hizmet kataloğu güncellendi.', type: 'success' })
}

const saveSectors = async () => {
   try {
      const res = await apiFetch(`/api/sectors`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(adminSectors.value)
      })
      if (res.ok) {
        emit('toast', { msg: 'Hizmet kataloğu senkronize edildi.', type: 'success' })
        store.fetchInitialData()
      }
   } catch(e) {}
}

const crmCustomers = computed(() => {
  const map = new Map<string, any>()
  adminAppointments.value.forEach(app => {
    const key = app.user_email || app.user_name
    if (!key) return;
    if (!map.has(key)) {
      map.set(key, {
         name: app.user_name,
         contact: app.user_email,
         totalSpent: 0,
         totalAppointments: 0,
         cancelled: 0,
         lastVisit: app.appointment_date,
         services: new Set<string>()
      })
    }
    const c = map.get(key)
    c.totalAppointments++
    if (app.service_name) c.services.add(app.service_name)
    if (app.status === 'Kesinleşti') c.totalSpent += app.amount
    else if (app.status === 'İptal Edildi') c.cancelled++
    if (new Date(app.appointment_date) > new Date(c.lastVisit)) c.lastVisit = app.appointment_date
  })
  return Array.from(map.values()).sort((a,b) => b.totalSpent - a.totalSpent)
})


const addNewCompany = () => {
  adminCompanies.value.push({ id: `c${Date.now()}`, name: '', sector_id: adminSectors.value[0]?.id, custom_prices: {}, custom_durations: {} })
}

const removeCompany = (id: string) => {
  adminCompanies.value = adminCompanies.value.filter(c => c.id !== id)
}

const saveCompanies = async () => {
   try {
      const res = await apiFetch(`/api/companies`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(adminCompanies.value)
      })
      if (res.ok) {
        emit('toast', { msg: 'Şube listesi güncellendi.', type: 'success' })
        store.fetchInitialData()
      }
   } catch (e) {}
}

const openPriceEditor = (comp: any) => {
  if (!comp.custom_prices) comp.custom_prices = {}
  if (!comp.custom_durations) comp.custom_durations = {}
  editingCompanyPrices.value = comp
}

const getSectorServices = (sectorId: string) => {
  const sector = adminSectors.value.find(s => s.id === sectorId)
  return sector ? sector.services : []
}

const saveCompanyPrices = async () => {
  await saveCompanies()
  editingCompanyPrices.value = null
}

// Business Settings Form
const form = ref({ 
  startTime: '09:00', 
  endTime: '19:00', 
  intervalMinutes: 60, 
  closedDays: [] as number[], 
  breakStartTime: '12:00', 
  breakEndTime: '13:00', 
  hasBreak: true,
  brand_color: '#C5A059',
  logo_url: ''
})
const weekDays = [ { label: 'Pzt', value: 1 }, { label: 'Sal', value: 2 }, { label: 'Çar', value: 3 }, { label: 'Per', value: 4 }, { label: 'Cum', value: 5 }, { label: 'Cmt', value: 6 }, { label: 'Paz', value: 0 } ]

onMounted(() => {
  if (isAuthenticated.value) bootAdminData()
  form.value = {
    startTime: store.businessSettings.startTime,
    endTime: store.businessSettings.endTime,
    intervalMinutes: store.businessSettings.intervalMinutes,
    closedDays: [...store.businessSettings.closedDays],
    breakStartTime: store.businessSettings.breakStartTime,
    breakEndTime: store.businessSettings.breakEndTime,
    hasBreak: store.businessSettings.hasBreak,
    brand_color: companyContext.value?.brand_color || '#C5A059',
    logo_url: companyContext.value?.logo_url || ''
  }
})

const toggleDay = (val: number) => {
  const index = form.value.closedDays.indexOf(val)
  if (index === -1) form.value.closedDays.push(val)
  else form.value.closedDays.splice(index, 1)
}

const save = async () => {
  try {
     // Company Branding & Business Settings Combined
     const resBrand = await apiFetch('/api/company/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          brand_color: form.value.brand_color,
          logo_url: form.value.logo_url,
          settings: {
            startTime: form.value.startTime,
            endTime: form.value.endTime,
            intervalMinutes: form.value.intervalMinutes,
            closedDays: form.value.closedDays,
            breakStartTime: form.value.breakStartTime,
            breakEndTime: form.value.breakEndTime,
            hasBreak: form.value.hasBreak
          }
        })
     })

     if (resBrand.ok) {
       store.fetchInitialData()
       // Update local context
       if (companyContext.value) {
         companyContext.value.brand_color = form.value.brand_color
         companyContext.value.logo_url = form.value.logo_url
         
         // Also update settings in local context
         companyContext.value.settings = {
            startTime: form.value.startTime,
            endTime: form.value.endTime,
            intervalMinutes: form.value.intervalMinutes,
            closedDays: form.value.closedDays,
            breakStartTime: form.value.breakStartTime,
            breakEndTime: form.value.breakEndTime,
            hasBreak: form.value.hasBreak
         }

         localStorage.setItem('companyContext', JSON.stringify(companyContext.value))
       }
       emit('toast', { msg: 'Sistem ve kurumsal ayarlar güncellendi.', type: 'success' })
     }
  } catch(e) {}
}
const fetchAuditLogs = async () => {
  try {
    const res = await apiFetch('/api/admin/audit-logs')
    if (res.ok) auditLogs.value = await res.json()
  } catch (e) {}
}

const exportCSV = () => {
  if (!adminAppointments.value.length) return
  
  const headers = ["ID", "Müşteri", "Telefon", "Hizmet", "Tutar", "Tarih", "Saat", "Durum"]
  const rows = adminAppointments.value.map(app => [
    app.id,
    app.user_name,
    app.user_email,
    app.service_name,
    app.amount,
    app.appointment_date,
    app.appointment_time,
    app.status
  ])
  
  let csvContent = "\uFEFF" + headers.join(",") + "\n"
  rows.forEach(row => {
    csvContent += row.map(v => `"${v}"`).join(",") + "\n"
  })
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", `randevular_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
.animate-scale-in { animation: scaleIn 0.3s ease-out forwards; }
.animate-shake { animation: shake 0.3s ease-in-out; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

</style>
