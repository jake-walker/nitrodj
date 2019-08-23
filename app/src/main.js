import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueMoment from 'vue-moment';

Vue.config.productionTip = false

Vue.use(VueMoment);

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
