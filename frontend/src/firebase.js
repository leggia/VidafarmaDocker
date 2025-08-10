// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBupIonvAdOKxgLZdoOUZMMgAp3dC52RyA",
  authDomain: "vidafarmaia.firebaseapp.com",
  projectId: "vidafarmaia",
  storageBucket: "vidafarmaia.firebasestorage.app",
  messagingSenderId: "148928896872",
  appId: "1:148928896872:web:74195f589af38eb18f00dd",
  measurementId: "G-C3ENLSJQ7L"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export auth and provider
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
