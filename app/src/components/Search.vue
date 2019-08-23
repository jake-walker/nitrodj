<template>
    <v-card outlined>
        <v-card-text ref="form">
            <v-text-field ref="search" label="Search YouTube" outlined clearable v-model="query">
                <template v-slot:append>
                    <v-fade-transition leave-absolute>
                        <v-progress-circular size="24" indeterminate v-if="loading"></v-progress-circular>
                        <v-icon v-else>mdi-magnify</v-icon>
                    </v-fade-transition>
                </template>
            </v-text-field>
        </v-card-text>

        <v-list-item v-for="item in results" :key="item.id" @click="addToQueue(item.id)">
            <v-list-item-content>
                <v-list-item-title v-html="item.title"></v-list-item-title>
                <v-list-item-subtitle v-html="item.artist"></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-icon>
                <v-icon>mdi-plus</v-icon>
            </v-list-item-icon>
        </v-list-item>
    </v-card>
</template>

<script>
    import axios from 'axios';
    import _ from 'lodash';

    export default {
        name: "Search",
        data: () => ({
            loading: false,
            results: [],
            query: ""
        }),
        methods: {
            addToQueue(id) {
                this.loading = true;
                axios({
                    method: "GET",
                    url: `/api/queue/add/${id}`
                }).then(() => {
                    this.loading = false;
                    this.query = "";
                });
            }
        },
        watch: {
            query: _.debounce(function() {
                if (this.query.trim() === "" || this.query == null) {
                    this.results = [];
                    return;
                }
                this.loading = true;
                axios({
                    method: "GET",
                    url: `/api/search/${this.query}`
                }).then((result) => {
                    this.loading = false;
                    this.results = result.data;
                });
            }, 2000)
        }
    }
</script>

<style scoped>

</style>