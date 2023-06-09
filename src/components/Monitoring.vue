<script setup lang="ts">
import { ref, computed } from "vue";
const eventSource = new EventSource(
  "/api/sse/07be49d8109b6576fd8ad3e0ee2f74b2112fa77414986310556d61c98b873132/stats"
);
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const { cpu, memory, disk, network } = data;
  cpuData.value = cpu;
  memoryData.value = memory;
  networkData.value = network;
  diskData.value = disk;
};

const cpuData = ref<number>();
const memoryData = ref<number>();
const networkData = ref<{
  tx: number;
  rx: number;
}>();
const diskData = ref<{
  read: number;
  write: number;
}>();

const all = computed(() => {
  return {
    cpu: cpuData.value,
    memory: memoryData.value,
    network: networkData.value,
    disk: diskData.value,
  };
});
</script>
<template>
  <div>
    <Chart :value="all.memory!" title="Memory Usage" />
    <Chart :value="all.cpu!" title="CPU Usage" />
    <Chart :value="all.network!.tx" title="Bytes Sent" />
    <Chart :value="all.network!.rx" title="Bytes Received" />
    <Chart :value="all.disk!.read" title="Bytes Read from Disk" />
    <Chart :value="all.disk!.write" title="Bytes Written to Disk" />
  </div>
</template>
