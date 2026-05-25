<template>
  <div class="max-w-4xl mx-auto py-16 px-6">
    <div class="bg-surface-elevated border border-main/10 rounded-3xl p-8 md:p-12 shadow-[0_0_40px_rgba(197,160,89,0.05)] relative overflow-hidden">
      <!-- Decorative Elements -->
      <div class="absolute top-0 left-0 w-64 h-64 bg-[#C5A059]/10 blur-[80px] rounded-full pointer-events-none"></div>
      <div class="absolute bottom-0 right-0 w-64 h-64 bg-main/5 blur-[80px] rounded-full pointer-events-none"></div>
      
      <div class="relative z-10">
        <h1 class="text-4xl md:text-5xl font-heading font-black text-main mb-8 tracking-tight">Gizlilik <span class="text-[#C5A059]">Politikası</span></h1>
        
        <div class="space-y-8 text-main/70 text-sm md:text-base leading-relaxed">
          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              1. Verilerin Toplanması
            </h2>
            <p>Platformumuzu ziyaret ettiğinizde, ad, soyad, telefon numarası gibi kişisel verileriniz, size daha iyi hizmet sunabilmek ve randevularınızı yönetmek amacıyla toplanabilir.</p>
          </section>

          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              2. Verilerin Kullanımı
            </h2>
            <p>Toplanan bilgileriniz, yalnızca randevu işlemlerinin gerçekleştirilmesi, bilgilendirme amaçlı iletişim kurulması ve kullanıcı deneyiminin iyileştirilmesi için kullanılır. Verileriniz asla üçüncü şahıslara satılmaz.</p>
          </section>

          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              3. Veri Güvenliği
            </h2>
            <p>Kişisel bilgilerinizin güvenliğini sağlamak amacıyla en son güvenlik teknolojileri (SSL sertifikaları, veri şifreleme yöntemleri) kullanılmaktadır. Bilgilerinize yalnızca yetkili personel erişebilir.</p>
          </section>
          
          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              4. Çerezler (Cookies)
            </h2>
            <p>Platformumuz, site içi gezinme verilerinizi analiz etmek ve size özelleştirilmiş bir deneyim sunmak için çerezler kullanabilir. Tarayıcı ayarlarınızdan çerezleri yönetebilirsiniz.</p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>
