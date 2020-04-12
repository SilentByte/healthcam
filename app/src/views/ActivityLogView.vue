<!--
    HealthCam: Protective Equipment Detection
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container v-if="activities.length===0"
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
                            <v-img :src="activity.photoUrl" />
                        </v-avatar>

                        <v-layout row>
                            <v-flex xs12 sm8>
                                <v-card-title class="headline">
                                    {{ activity.camera }}
                                </v-card-title>
                                <v-card-subtitle class="pb-1 caption">
                                    <div>
                                        <v-icon x-small>mdi-calendar-clock</v-icon>
                                        {{ activity.timestamp.toLocaleString() }}
                                    </div>
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
                                        <v-btn small color="primary"
                                               :loading="!!pendingConfirmations[activity.id]"
                                               @click="onConfirmActivity(activity)">
                                            Confirm
                                        </v-btn>
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
        pendingConfirmations: { [key: string]: boolean } = {};

        get activities() {
            return app.activities;
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

        async onConfirmActivity(activity: IActivity) {
            try {
                this.$set(this.pendingConfirmations, activity.id, true);
                await app.doConfirmActivity({activityId: activity.id});
            } finally {
                this.$delete(this.pendingConfirmations, activity.id);
            }
        }
    }
</script>
