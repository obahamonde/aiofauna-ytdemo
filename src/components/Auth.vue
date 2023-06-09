<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const {
  isAuthenticated,
  loginWithRedirect,
  getAccessTokenSilently,
  user,
  logout,
} = useAuth0();

watch(user, async () => {
  user.value ? (state.user = await authorize()) : null;
});

const authorize = async () => {
  const token = await getAccessTokenSilently();
  const res = await fetch("/api/auth?token=" + token);
  const data = await res.json();
  state.notifications.push({
    message: "Welcome " + user.value.name,
    status: "success",
  });
  return data;
};

const modal = ref(false);
</script>
<template>
  <Notifier />
  <div v-if="state.user && isAuthenticated">
    <div class="tl fixed mx-16 my-6 z-50">
      <img
        class="img-cover x4 cp rf scale sh"
        :src="state.user.picture"
        :alt="state.user.name"
        @click="modal = !modal"
      />
      <Modal v-if="modal" @close="modal = false">
        <p class="text-center text-lg font-sans">{{ state.user.name }}</p>
        <p class="text-center text-sm font-sans">{{ state.user.email }}</p>
        <template #footer>
          <button class="btn-del" @click.prevent="logout()">Logout</button>
        </template>
      </Modal>
    </div>

    <slot />
  </div>
  <div v-else class="col center my-12">
    <h1 class="text-lg font-sans text-center">Not Authenticated</h1>
    <button class="btn-get" @click.prevent="loginWithRedirect()">Login</button>
  </div>
</template>
