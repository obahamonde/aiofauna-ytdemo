<template>
  <LineChart v-bind="lineChartProps" style="width: 800px; display: flex;" />
</template>

<script setup lang="ts">
import { computed, ref, Ref, reactive, watch } from "vue";
import { LineChart, useLineChart } from "vue-chart-3";
import { Chart, ChartData, ChartOptions, registerables } from "chart.js";

Chart.register(...registerables);

const dataValues = ref([]) as Ref<number[]>;
const dataLabels = ref([new Date().toLocaleTimeString()]);

const chartData = computed<ChartData<"line">>(() => ({
  labels: dataLabels.value,
  datasets: [
    {
      label: props.title,
      data: dataValues.value,
      backgroundColor: ["#008080"],
    },
  ],
}));

const options = computed<ChartOptions<"line">>(() => ({
  scales: {
    myScale: {
      type: "linear",
      position: "right",
    },
  },
  plugins: {
    legend: {
      position: "bottom",
    },
    title: {
      display: true,
      text: props.title,
    },
  },
}));

const { lineChartProps } = useLineChart({
  chartData,
  options,
});

const addData = (value: number) => {
  dataValues.value.push(value);
  dataLabels.value.push(new Date().toLocaleTimeString());
};

const props = defineProps({
  value: {
    type: Number,
    required: true,
  },
  title: {
    type: String,
    default: "Metrics",
  },
});

const rxProps = reactive(props);

watch(
  () => rxProps.value,
  (value) => {
    addData(value);
  }
);
</script>
