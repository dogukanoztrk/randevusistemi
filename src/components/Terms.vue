<template>
  <div class="max-w-4xl mx-auto py-16 px-6">
    <div class="bg-surface-elevated border border-main/10 rounded-3xl p-8 md:p-12 shadow-[0_0_40px_rgba(197,160,89,0.05)] relative overflow-hidden">
      <!-- Decorative Elements -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-[#C5A059]/10 blur-[80px] rounded-full pointer-events-none"></div>
      <div class="absolute bottom-0 left-0 w-64 h-64 bg-main/5 blur-[80px] rounded-full pointer-events-none"></div>
      
      <div class="relative z-10">
        <h1 class="text-4xl md:text-5xl font-heading font-black text-main mb-8 tracking-tight">Kullanım <span class="text-[#C5A059]">Koşulları</span></h1>
        
        <div class="space-y-8 text-main/70 text-sm md:text-base leading-relaxed">
          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              1. Kabul Edilme
            </h2>
            <p>Bu platformu kullanarak, aşağıda belirtilen şartları ve koşulları kabul etmiş sayılırsınız. Hizmetlerimizi kullanmadan önce bu metni dikkatlice okumanızı tavsiye ederiz.</p>
          </section>

          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              2. Hizmet Kullanımı
            </h2>
            <p>Platformumuz üzerinden aldığınız randevular tamamen kişisel kullanım içindir. Platformu hukuka aykırı veya başkalarının haklarını ihlal edecek şekilde kullanmamayı taahhüt edersiniz.</p>
          </section>

          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              3. İptal ve Değişiklik
            </h2>
            <p>Randevu iptal veya değişiklik işlemlerinizi, randevu saatinden en az 24 saat önce sistem üzerinden gerçekleştirmeniz gerekmektedir. Aksi takdirde, belirli bir hizmet bedeli yansıtılabilir.</p>
          </section>
          
          <section>
            <h2 class="text-xl font-bold text-main mb-3 flex items-center gap-2">
              <span class="w-8 h-px bg-[#C5A059]"></span>
              4. Değişiklik Hakları
            </h2>
            <p>DiTA, herhangi bir zamanda Kullanım Koşulları'nda önceden haber vermeksizin değişiklik yapma hakkını saklı tutar. Değişiklikler sitede yayımlandığı andan itibaren geçerli olacaktır.</p>
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
