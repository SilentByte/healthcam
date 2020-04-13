<!--
    HealthCam: Protective Equipment Detection
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container fill-height style="max-width: 1000px">
        <v-flex v-show="pending" class="text-center align-self-center">
            <v-progress-circular indeterminate
                                 color="primary" />
        </v-flex>
        <v-layout v-show="!pending" wrap>
            <v-flex xs12 sm6>
                <v-card class="mx-2 pa-8 text-center fill-height">
                    <div class="pt-4 title text-center">
                        Activity Log
                    </div>
                    <v-card-text>
                        <v-chip x-large label
                                color="success"
                                class="ma-1 pa-5 display-2">
                            {{ stats.compliantCount }}
                        </v-chip>

                        <v-chip x-large label
                                color="error"
                                class="ma-1 pa-5 display-2">
                            {{ stats.violationCount }}
                        </v-chip>

                        <v-chip x-large label
                                color="warning"
                                class="ma-1 pa-5 display-2">
                            {{ stats.overrideCount }}
                        </v-chip>
                    </v-card-text>
                </v-card>
            </v-flex>

            <v-flex xs12 sm6>
                <v-card class="mx-2 pa-8 fill-height">
                    <v-card-title class="pb-0">
                        Cameras
                    </v-card-title>
                    <v-list dense>
                        <v-list-item v-for="cam in cameras"
                                     :key="cam.id">
                            <v-list-item-icon>
                                <v-icon :color="cam.state === 'online' ? 'success' : 'error'">
                                    mdi-cctv
                                </v-icon>
                            </v-list-item-icon>

                            <v-list-item-content>
                                <v-list-item-title>{{ cam.name }}</v-list-item-title>
                            </v-list-item-content>

                            <v-list-item-content>
                                <div>
                                    <v-chip x-small label color="success" class="px-1 mx-1">
                                        {{ cam.compliantCount }}
                                    </v-chip>
                                    <v-chip x-small label color="error" class="px-1 mx-1">
                                        {{ cam.violationCount }}
                                    </v-chip>
                                    <v-chip x-small label color="warning" class="px-1 mx-1">
                                        {{ cam.overrideCount }}
                                    </v-chip>

                                    <v-chip v-if="cam.state === 'online'"
                                            x-small label color="success" class="px-1 mx-1">
                                        Online
                                    </v-chip>
                                    <v-chip v-else
                                            x-small label color="error" class="px-1 mx-1">
                                        Offline
                                    </v-chip>
                                </div>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-flex>

            <v-flex xs12 sm12 class="mt-4">
                <v-card class="mx-2">
                    <div class="pt-4 title text-center">
                        This Week
                    </div>
                    <v-card-text>
                        <canvas ref="chart" />
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import {
        Component,
        Vue,
        Watch,
    } from "vue-property-decorator";

    import { Chart } from "chart.js";

    import { getModule } from "vuex-module-decorators";
    import { AppModule } from "@/store/app";

    const app = getModule(AppModule);

    @Component
    export default class DashboardView extends Vue {
        pending = false;
        chart: Chart | null = null;

        get stats() {
            return {
                compliantCount: this.cameras.reduce((acc, cam) => acc + cam.compliantCount, 0),
                violationCount: this.cameras.reduce((acc, cam) => acc + cam.violationCount, 0),
                overrideCount: this.cameras.reduce((acc, cam) => acc + cam.overrideCount, 0),
            };
        }

        get cameras() {
            return app.cameras;
        }

        get weekDayNames() {
            const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            const today = new Date().getDay();
            const days = [];

            for(let i = 0; i < 7; i++) {
                let day = today - i;
                if(day < 0) {
                    day = 7 + day;
                }
                days.push(weekdays[day]);
            }

            return days.reverse();
        }

        initChart() {
            const context = (this.$refs.chart as HTMLCanvasElement).getContext("2d") as CanvasRenderingContext2D;
            this.chart = new Chart(context, {
                type: "bar",
                data: {
                    labels: this.weekDayNames,
                    datasets: [
                        {
                            label: "Compliant",
                            data: app.activityHistory.compliant,
                            backgroundColor: "#4caf50",
                        },
                        {
                            label: "Violation",
                            data: app.activityHistory.violation,
                            backgroundColor: "#ff5252",
                        },
                        {
                            label: "Override",
                            data: app.activityHistory.override,
                            backgroundColor: "#f57c00",
                        },
                    ],
                },
                options: {
                    responsive: true,
                    tooltips: {
                        mode: "index",
                        intersect: true,
                    },
                    scales: {
                        xAxes: [{
                            stacked: true,
                        }],
                        yAxes: [{
                            stacked: true,
                        }],
                    },
                },
            });
        }

        @Watch("stats")
        onStatsChanged() {
            if(this?.chart?.data?.datasets) {
                this.chart.data.datasets[0].data = app.activityHistory.compliant;
                this.chart.data.datasets[1].data = app.activityHistory.violation;
                this.chart.data.datasets[2].data = app.activityHistory.override;
                this.chart.update();
            }
        }

        async mounted() {
            this.initChart();

            try {
                this.pending = true;
                await app.doFetchStats();
            } finally {
                this.pending = false;
            }
        }

        destroyed() {
            if(this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        }
    }
</script>

<style lang="scss">

</style>
