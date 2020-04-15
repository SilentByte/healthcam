<!--
    HealthCam: Protective Equipment Detection
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container v-if="activitiesPending"
                 fill-height>
        <v-flex class="text-center display-1 align-self-center text--disabled">
            <v-progress-circular indeterminate
                                 color="primary" />
        </v-flex>
    </v-container>
    <v-container v-else-if="activities.length===0"
                 fill-height>
        <v-flex class="text-center display-1 align-self-center text--disabled">
            There are no current activities
        </v-flex>
    </v-container>
    <v-container v-else pa-5 style="max-width: 720px">
        <v-layout wrap>
            <v-flex v-for="activity in activities"
                    :key="activity.id"
                    class="align-center justify-center"
                    xs12 mb-2 mb-sm-4>
                <v-card class="align-center justify-center align-self-center">
                    <div class="d-flex flex-no-wrap">
                        <v-avatar tile
                                  :size="calculatePreviewSize"
                                  class="ma-2 ma-sm-4">
                            <v-img :src="activity.photoUrl">
                                <template v-slot:placeholder>
                                    <v-row class="fill-height ma-0"
                                           align="center"
                                           justify="center">
                                        <v-progress-circular indeterminate
                                                             color="primary" />
                                    </v-row>
                                </template>
                            </v-img>
                        </v-avatar>

                        <v-layout row>
                            <v-flex xs12 sm8>
                                <v-card-title class="headline">
                                    {{ activity.camera }}
                                </v-card-title>
                                <v-card-subtitle class="pb-1 caption">
                                    <div>
                                        <v-icon small class="mr-1">mdi-calendar-clock</v-icon>
                                        <span>{{ activity.timestamp.toLocaleString() }}</span>
                                    </div>
                                    <v-flex>
                                        <v-icon small class="mr-1">mdi-account-arrow-left</v-icon>
                                        <span>{{ activity.peopleInFrame }}</span>

                                        <v-icon small class="ml-1">mdi-alpha</v-icon>
                                        <span>{{ activity.minConfidence.toFixed(2) }}</span>
                                    </v-flex>
                                </v-card-subtitle>
                            </v-flex>
                            <v-flex ma-5>
                                <v-layout column align-end>
                                    <v-chip class="mr-2 text-uppercase"
                                            :color="formatActivityType(activity).color">
                                        <v-avatar left>
                                            <v-icon>{{formatActivityType(activity).icon}}</v-icon>
                                        </v-avatar>
                                        {{ formatActivityType(activity).text }}
                                    </v-chip>
                                    <v-flex my-5 pt-5 mr-4>
                                        <v-layout column align-center>
                                            <v-layout row>
                                                <v-btn icon color="primary"
                                                       :loading="(pendingRatings[activity.id] || 0) > 0"
                                                       :disabled="(pendingRatings[activity.id] || 0) < 0"
                                                       @click="onRateActivity(activity, +1)">
                                                    <v-icon>mdi-thumb-up</v-icon>
                                                </v-btn>
                                                <v-btn icon color="primary"
                                                       :loading="(pendingRatings[activity.id] || 0) < 0"
                                                       :disabled="(pendingRatings[activity.id] || 0) > 0"
                                                       @click="onRateActivity(activity, -1)">
                                                    <v-icon>mdi-thumb-down</v-icon>
                                                </v-btn>
                                            </v-layout>
                                            <small class="text--disabled">
                                                Rate Detection
                                            </small>
                                        </v-layout>
                                    </v-flex>
                                </v-layout>
                            </v-flex>
                        </v-layout>
                    </div>
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
    } from "vue-property-decorator";

    import { getModule } from "vuex-module-decorators";

    import { IActivity } from "@/store/models";

    import { AppModule } from "@/store/app";

    const app = getModule(AppModule);

    @Component
    export default class ActivityLogView extends Vue {
        pendingRatings: { [key: string]: boolean } = {};

        get activities() {
            return app.activities;
        }

        get activitiesPending() {
            return app.activitiesPending
        }

        get calculatePreviewSize() {
            return this.$vuetify.breakpoint.xs ? 80
                : this.$vuetify.breakpoint.sm ? 100
                    : 140;
        }

        formatActivityType(activity: IActivity) {
            return {
                "compliant": {
                    text: "Compliant",
                    color: "success",
                    icon: "mdi-checkbox-marked-circle",
                },
                "violation": {
                    text: "Violation",
                    color: "error",
                    icon: "mdi-alert-octagon",
                },
                "override": {
                    text: "Override",
                    color: "warning",
                    icon: "mdi-alert-circle",
                },
            }[activity.type];
        }

        async onRateActivity(activity: IActivity, rating: number) {
            try {
                this.$set(this.pendingRatings, activity.id, rating);
                await app.doRateActivity({
                    activityId: activity.id,
                    rating,
                });
            } finally {
                this.$delete(this.pendingRatings, activity.id);
            }
        }
    }
</script>
