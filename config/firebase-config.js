// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDit1eq6R3YZX9eFsOBV2AI9u-9K4xgIJI",
  authDomain: "cardscan-1750b.firebaseapp.com",
  projectId: "cardscan-1750b",
  storageBucket: "cardscan-1750b.firebasestorage.app",
  messagingSenderId: "590237265131",
  appId: "1:590237265131:web:5676e3aae5608812f8a2ae",
  measurementId: "G-60HP322XY3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);