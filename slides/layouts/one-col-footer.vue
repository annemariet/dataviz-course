<!--
  One-column layout with two optional spanning bottom areas:
  - ::tagline:: sits below main content
  - ::footer::  is pinned to the slide bottom, footnote size

  Usage:
  ---
  layout: one-col-footer
  ---
  # Title
  Main content

  ::tagline::
  > Optional emphasis line

  ::footer::
  Small source note
-->

<script setup lang="ts">
defineProps({
  layoutClass: { type: String },
})
</script>

<template>
  <div class="slidev-layout one-col-footer w-full h-full" :class="layoutClass">
    <div class="main">
      <slot />
      <div v-if="$slots.tagline" class="tagline">
        <slot name="tagline" />
      </div>
    </div>
    <div v-if="$slots.footer" class="footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.one-col-footer {
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tagline {
  margin-top: 1.25rem;
  font-size: 1.1em;
}

.footer {
  font-size: 0.7em;
  opacity: 0.6;
  padding-bottom: 0.25rem;
}
</style>
