<!--
    SmartCam
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container style="max-width: 1000px">
        <v-layout wrap>
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
                        <v-list-item v-for="cam in stats.cameras"
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
                <v-card class="mx-2 pa-8 text-center fill-height">
                    <div class="pt-4 title text-center">
                        Chart
                    </div>
                    <v-card-text>
                        TODO
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    import { getModule } from "vuex-module-decorators";
    import { AppModule } from "@/store/app";

    const app = getModule(AppModule);

    @Component
    export default class DashboardView extends Vue {
        get stats() {
            return app.stats;
        }
    }
</script>

<style lang="scss">

</style>
