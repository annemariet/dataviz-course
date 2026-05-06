<!--
  Two-column layout with a spanning header and two optional spanning bottom areas:
  - ::tagline:: sits right below the columns, same/larger font size
  - ::footer::  is pinned to the slide bottom, smaller footnote size

  Usage:
  ---
  layout: two-cols-footer
  ---
  # Title spanning both columns

  ::left::
  Left content

  ::right::
  Right content

  ::tagline::
  > Emphasis quote right below the columns

  ::footer::
  ¹ Small footnote pinned to the bottom
-->

<script setup lang="ts">
defineProps({
  layoutClass: { type: String },
})
</script>

<template>
  <div class="slidev-layout two-cols-footer w-full h-full" :class="layoutClass">
    <div class="main">
      <div class="col-header">
        <slot />
      </div>
      <div class="columns-area">
        <div class="col-left">
          <slot name="left" />
        </div>
        <div class="col-right">
          <slot name="right" />
        </div>
      </div>
      <div v-if="$slots.tagline" class="col-tagline">
        <slot name="tagline" />
      </div>
    </div>
    <div v-if="$slots.footer" class="col-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.two-cols-footer {
  display: flex;
  flex-direction: column;
}

/* header + columns + tagline are vertically centered as a group */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.columns-area {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 2rem;
  margin-top: 0.5rem;
}

.col-left,
.col-right {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
  overflow: hidden;
}

.col-tagline {
  margin-top: 1.25rem;
  font-size: 1.1em;
}

/* pinned to slide bottom, footnote style */
.col-footer {
  font-size: 0.7em;
  opacity: 0.6;
  padding-bottom: 0.25rem;
}
</style>
