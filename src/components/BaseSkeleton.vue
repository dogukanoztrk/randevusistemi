<script setup lang="ts">
defineProps<{
  width?: string
  height?: string
  radius?: string
  className?: string
}>()
</script>

<template>
  <div 
    :class="['shimmer relative overflow-hidden bg-slate-200/50', className]"
    :style="{
      width: width || '100%',
      height: height || '20px',
      borderRadius: radius || '8px'
    }"
  ></div>
</template>

<style scoped>
.shimmer {
  background: linear-gradient(
    90deg,
    rgba(226, 232, 240, 0) 0%,
    rgba(226, 232, 240, 0.5) 50%,
    rgba(226, 232, 240, 0) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>
