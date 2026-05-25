<script setup lang="ts">
import { useAppointmentStore } from '@/stores/appointment'
import { CheckCircle2, AlertCircle, X, Info } from 'lucide-vue-next'

const store = useAppointmentStore()
</script>

<template>
  <div class="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none max-w-sm w-full">
    <TransitionGroup 
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="transform translate-x-full opacity-0"
      enter-to-class="transform translate-x-0 opacity-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="transform translate-x-0 opacity-100"
      leave-to-class="transform translate-x-full opacity-0"
    >
      <div 
        v-for="toast in store.toasts" 
        :key="toast.id"
        class="pointer-events-auto w-full glass-dark text-main rounded-2xl shadow-2xl p-4 flex items-start gap-3 overflow-hidden group relative"
      >
        <!-- Icon logic -->
        <div class="flex-shrink-0 mt-0.5">
          <CheckCircle2 v-if="toast.type === 'success'" class="w-5 h-5 text-emerald-400" />
          <AlertCircle v-else-if="toast.type === 'error'" class="w-5 h-5 text-rose-400" />
          <Info v-else class="w-5 h-5 text-sky-400" />
        </div>

        <div class="flex-grow">
          <p class="text-sm font-medium leading-tight">{{ toast.message }}</p>
        </div>

        <button 
          @click="store.removeToast(toast.id)"
          class="flex-shrink-0 text-main/40 hover:text-main transition-colors"
        >
          <X class="w-4 h-4" />
        </button>

        <!-- Progress bar (Auto-hide indicator) -->
        <div class="absolute bottom-0 left-0 h-0.5 bg-main/10 w-full">
          <div class="h-full bg-main/30 animate-[shrink_3s_linear_forwards]"></div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
@keyframes shrink {
  from { width: 100%; }
  to { width: 0%; }
}
</style>
