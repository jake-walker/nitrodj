import Vue from 'vue';
import Vuetify from 'vuetify/lib';

import colors from 'vuetify/lib/util/colors';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      dark: {
        primary: colors.cyan.darken1
      }
    },
    dark: true
  },
  icons: {
    iconfont: "mdiSvg"
  }
});
