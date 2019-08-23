<template>
    <v-card outlined>
        <v-subheader inset>Now Playing</v-subheader>
        <v-list-item v-if="nowPlaying">
            <v-list-item-icon>
                <v-icon>mdi-play</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
                <v-list-item-title>
                    Song #{{ nowPlaying }}
                </v-list-item-title>
                <v-list-item-subtitle>
                    Artist Here
                </v-list-item-subtitle>
            </v-list-item-content>
            <!--<v-list-item-action>
                <v-btn icon>
                    <v-icon color="green accent-3">mdi-thumb-up</v-icon>
                </v-btn>
            </v-list-item-action>
            <v-list-item-action>
                <v-btn icon>
                    <v-icon color="red accent-3">mdi-thumb-down</v-icon>
                </v-btn>
            </v-list-item-action>-->
        </v-list-item>

        <v-divider inset></v-divider>

        <v-subheader inset>Next Up</v-subheader>
        <v-list-item v-for="song in nextUp" :key="song">
            <v-list-item-action></v-list-item-action>
            <v-list-item-content>
                <v-list-item-title>Song #{{ song }}</v-list-item-title>
                <v-list-item-subtitle>Artist Here</v-list-item-subtitle>
            </v-list-item-content>
            <!--<v-list-item-action>
                <v-btn icon>
                    <v-icon color="green accent-3">mdi-thumb-up</v-icon>
                </v-btn>
            </v-list-item-action>
            <v-list-item-action>
                <v-btn icon>
                    <v-icon color="red accent-3">mdi-thumb-down</v-icon>
                </v-btn>
            </v-list-item-action>-->
        </v-list-item>
        <v-card-text>
            Queue last updated
            <span v-if="lastUpdated == false">never</span>
            <span v-else>{{ lastUpdated | moment("h:mm:ss a") }}</span>.
        </v-card-text>
    </v-card>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Queue",
        data: () => ({
            queue: [],
            lastUpdated: false
        }),
        methods: {
            fetchQueue() {
                this.lastUpdated = new Date();
                axios({
                    method: "GET",
                    url: "/api/queue"
                }).then((result) => {
                    this.queue = result.data;
                })
            }
        },
        computed: {
            nowPlaying() {
                if (this.queue.length > 0) {
                    return this.queue[0];
                }
                return null;
            },
            nextUp() {
                if (this.queue.length > 1) {
                    return this.queue.slice(1);
                }
                return [];
            }
        },
        mounted() {
            this.fetchQueue();
            setInterval(() => {
                this.fetchQueue();
            }, 10000);
        }
    }
</script>

<style scoped>

</style>