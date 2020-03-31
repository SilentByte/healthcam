<!--
    SmartCam
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<template>
    <v-app>
        <v-app-bar app dark
                   clipped-left
                   color="primary">

            <v-app-bar-nav-icon @click="drawer = !drawer" />

            <span v-if="!$vuetify.breakpoint.xs"
                  class="title ml-3 mr-5 text-uppercase">
                Smart<span class="font-weight-light">Cam</span>
            </span>

            <v-spacer />

            <v-btn large rounded text :to="{ name: 'CameraView' }">
                <template v-if="perimeterStatus === 'clear'">
                    <v-icon class="pl-4 pr-2" left large>mdi-check</v-icon>
                    <div class="ml-2">Clear</div>
                </template>
                <template v-else-if="perimeterStatus === 'suspicious'">
                    <v-icon class="pl-5 pr-2" left large>mdi-alert</v-icon>
                    <div class="ml-2">Suspicious</div>
                </template>
                <template v-else>
                    <v-icon class="pl-5 pr-2" left large>mdi-alert-octagon</v-icon>
                    <div class="ml-2">Alert!</div>
                </template>
            </v-btn>
        </v-app-bar>

        <v-navigation-drawer app clipped
                             v-model="drawer">
            <v-layout column fill-height>
                <v-list nav dense>
                    <v-list-item link exact :to="{ name: 'HomeView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-map-marker</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Overview</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item link exact :to="{ name: 'CameraView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-cctv</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Cameras</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item link :to="{ name: 'AboutView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-information</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>What's This?</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

                <v-spacer />

                <v-list nav dense>
                    <v-list-item>
                        <v-layout row justify-center>
                            <v-btn small text
                                   href="https://twitter.com/RicoBeti"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @RicoBeti
                            </v-btn>
                            <v-btn small text
                                   href="https://twitter.com/Phtevem"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @Phtevem
                            </v-btn>
                        </v-layout>
                    </v-list-item>
                </v-list>
            </v-layout>
        </v-navigation-drawer>

        <v-content>
            <router-view />
        </v-content>
    </v-app>
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
    export default class App extends Vue {
        drawer = null;

        get perimeterStatus() {
            return app.perimeterStatus;
        }
    }
</script>
