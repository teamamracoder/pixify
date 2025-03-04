importScripts("https://www.gstatic.com/firebasejs/11.2.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/11.2.0/firebase-messaging-compat.js");

// Your Firebase configuration
const firebaseConfig = {

    apiKey: "AIzaSyAGoApbXczwcRy8eRbQP7qTeJ907YRa5NA",
    authDomain: "pixify-d9536.firebaseapp.com",
    projectId: "pixify-d9536",
    storageBucket: "pixify-d9536.firebasestorage.app",
    messagingSenderId: "210451275321",
    appId: "1:210451275321:web:b15d869d8a6b89056c37e8",
    measurementId: "G-5RQY8K6R4Q"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Retrieve Firebase Messaging
const messaging = firebase.messaging();

// Background message handler
messaging.onBackgroundMessage((payload) => {
    //console.log("Received background message ", payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: payload.notification.icon
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
