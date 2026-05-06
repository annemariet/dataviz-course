<!--
  Centered quote layout (no title).
  - Main content centered both vertically and horizontally
  - Optional ::author:: slot rendered below the quote

  Usage:
  ---
  layout: quote
  ---
  "Your quote text"

  ::author::
  Author, *Source*
-->

<script setup lang="ts">
defineProps({
  layoutClass: { type: String },
})
</script>

<template>
  <div class="slidev-layout quote w-full h-full" :class="layoutClass">
    <div class="quote-wrap">
      <div class="quote-text">
        <slot />
      </div>
      <div v-if="$slots.author" class="quote-author">
        <slot name="author" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.quote {
  display: grid;
  place-items: center;
}

.quote-wrap {
  max-width: 900px;
  text-align: center;
}

.quote-text {
  font-family: Inter, "Avenir Next", Avenir, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 4.1rem;
  line-height: 1.8;
  font-weight: 500;
}

.quote-text :deep(*) {
  margin: 0;
  font-size: inherit;
  line-height: inherit;
  font-weight: inherit;
}

.quote-author {
  font-family: Inter, "Avenir Next", Avenir, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin-top: 1.25rem;
  font-size: 1.4rem;
  opacity: 0.75;
}

.quote-author :deep(*) {
  margin: 0;
  font-size: inherit;
  line-height: 1.35;
}
</style>
