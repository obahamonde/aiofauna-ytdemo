<template>
  <button class="icon-btn tr fixed m-8" @click="toggleDark()">
    <Icon
      :icon="isDark ? 'mdi-weather-night' : 'mdi-weather-sunny'"
      class="x2"
    />
  </button>
</template>
