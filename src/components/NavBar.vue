<script setup lang="ts">
const routes = ref([
  {
    name: "Home",
    icon: "mdi-home",
    to: "/",
  },
  {
    name: "About",
    icon: "mdi-information",
    to: "/about",
  },
  {
    name: "Docs",
    icon: "mdi-book-open",
    to: "/docs",
  },
  {
    name: "Tutorial",
    icon: "mdi-school",
    to: "/tutorial",
  },
  {
    name: "DashBoard",
    icon: "mdi-desktop-mac-dashboard",
    to: "/dashboard",
  },
]);
</script>

<template>
  <nav
    class="flex tl fixed col center bg-gray-200 dark:bg-gray-900 h-screen p-4 rounded-lg sh"
  >
    <img
      src="/favicon.svg"
      class="x4 hover:brightness-150 cursor-none hover:animate-pulse"
    />
    <h1
      class="text-2xl text-primary font-italic mx-4 my-4 hover:text-white cursor-none"
    >
      AioFauna
    </h1>
    <iframe
      src="https://ghbtns.com/github-btn.html?user=obahamonde&repo=aiofauna&type=star&count=true&size=large"
      frameborder="0"
      scrolling="0"
      width="170"
      height="30"
      title="GitHub"
      class="px-6"
    ></iframe>

    <RouterLink
      class="@apply flex items-center text-primary dark: text-gray-300 no-underline hover:bg-gray-300 dark:hover:bg-gray-800 p-2 mr-4 my-4 rounded-md transition-colors duration-300"
      :to="route.to"
      v-for="route in routes"
    >
      <Icon :icon="route.icon" class="text-xl mr-2" />
      <span class="text-sm">{{ route.name }}</span>
    </RouterLink>
    <a href="https://github.com/obahamonde/aiofauna" target="_blank">
      <Icon icon="logos:github-icon" class="x2 m-4 mt-8 dark:invert cp scale" />
    </a>
    <a href="https://pypi.org/project/aiofauna/" target="_blank">
      <Icon icon="logos:python" class="x2 m-4 mt-4 dark:invert cp scale" />
    </a>
    <a href="https://ob-be-fwuw7gz7oq-uc.a.run.app/" target="_blank">
      <img src="/logo.png" class="x2 m-4 mt-4 dark:invert cp scale" />
    </a>
  </nav>
</template>

<style global>
.router-link-active {
  background-color: #9ca3af;
  color: #fff;
}
</style>
