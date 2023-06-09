<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const { isAuthenticated } = useAuth0();
const show = ref(false);
</script>
<template>
  <Request
    v-if="state.user && isAuthenticated && state.user.ref"
    :url="'/api/pipeline?user=' + state.user.ref"
  >
    <template #default="{ json }">
      <div class="row center gap-24">
        <a
          :href="json.codeserver.url"
          class="cp hover:brightness-125 col center"
          target="_blank"
        >
          <img src="/dev.png" class="x20" />
          <p class="m-4 text-caption text-lg text-primary">
            Access your Development Environment
          </p>
        </a>

        <a
          :href="json.python.url"
          class="cp hover:brightness-125 col center"
          target="_blank"
        >
          <img src="/python.webp" class="x20" />
          <p class="m-4 text-caption text-lg text-primary">
            Access your Python Sandbox
          </p>
        </a>
      </div>

      <h1
        class="font-mono text-lg text-amber bg-primary sh px-4 py-2 text-center rounded-lg cp hover:underline m-16"
        title="How does this work?"
        @click="show = !show"
      >
        Everything runs on the browser no installations needed!
      </h1>
      <details class="m-16" v-if="show">
        <summary
          class="font-mono text-lg text-amber bg-primary sh px-4 py-2 text-center rounded-lg cp hover:underline m-16"
          title="How does this work?"
        >
          How does this work?
        </summary>
        <section class="text-center text-lg text-primary">
          This is a demo of a Cloud Development Platform built on top of open
          source technologies

          <footer class="row center m-4 gap-12">
            <figure class="col center">
              <img
                src="https://camo.githubusercontent.com/8033966333c822969128a390a28c46a8dfa2cf87928d43abd71ab8ba836bc26d/68747470733a2f2f692e696d6775722e636f6d2f5543714f7746432e706e67"
                class="w-24"
                alt="code-server"
              />
              <caption>
                Code Server
              </caption>
            </figure>

            <figure class="col center">
              <img
                src="https://cdn.worldvectorlogo.com/logos/docker.svg"
                class="w-24"
                alt="docker"
              />
              <caption>
                Docker
              </caption>
            </figure>

            <figure class="col center">
              <img src="/favicon.svg" class="w-24" alt="aiofauna" />
              <caption>
                AioFauna
              </caption>
            </figure>
          </footer>
        </section>
      </details>
    </template>
  </Request>
</template>
