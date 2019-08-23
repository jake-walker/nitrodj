<template>
  <v-app>
    <v-app-bar app dark color="primary">
      <v-toolbar-title>NitroDJ</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <v-container>
        <v-row>
          <v-col cols="12" md="6" order="2" order-md="1">
            <Search/>
          </v-col>
          <v-col cols="12" md="6" order="1" order-md="2">
            <Queue/>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Queue from './components/Queue';
import Search from './components/Search';

export default {
  name: 'App',
  components: {
    Queue,
    Search
  }
};
</script>
