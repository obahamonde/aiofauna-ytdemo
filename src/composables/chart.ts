import { ref, watch, reactive } from 'vue'
import {
  Chart,
  registerables,
  ChartData,
  ChartOptions,
  ChartType,
} from "chart.js";
import 'chartjs-adapter-date-fns';

export const useChart = () => {
  Chart.register(...registerables);

  const chartRef = ref<HTMLCanvasElement | null>(null);
  const chart: Ref<Chart | null> = ref(null);

  const chartOptions = reactive<ChartOptions>({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales:{
      x:{
        type:'time',
        time:{
          unit:'second'
        }
      }
    }
  });

  const chartData = ref<ChartData>({
    labels: [],
    datasets: [
      {
        label: "Data",
        data: [],
        backgroundColor: [],
        borderColor: [],
        borderWidth: 1,
      }
    ],
  });

  const chartType: Ref<ChartType> = ref("line");


  return {
    chartRef,
    chart,
    chartData,
    chartOptions,
    chartType
  };
};