import './assets/styles/main.css'
import 'leaflet/dist/leaflet.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App);
app.use(router)
app.use(createPinia())
app.mount('#app')

router.beforeEach((to, from, next) => {
  const defaultTitle = 'HikeLink'
  document.title = to.meta.title || defaultTitle
  next()
})