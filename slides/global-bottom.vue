<template>
  <div class="slide-page-number">
    <SlideCurrentNo /> / <SlidesTotal />
  </div>
</template>

<style scoped>
.slide-page-number {
  position: fixed;
  right: 1rem;
  bottom: 0.75rem;
  font-size: 0.75rem;
  color: rgb(107 114 128);
  opacity: 0.8;
  z-index: 1000;
}
</style>
