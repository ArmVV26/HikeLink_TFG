import './assets/styles/main.css'
import 'leaflet/dist/leaflet.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import VueGoogleLogin from 'vue3-google-login'
import App from './App.vue'
import router from './router'

const app = createApp(App);
app.use(router)
app.use(createPinia())
// app.use(VueGoogleLogin, { clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID })
app.mount('#app')