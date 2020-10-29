import firebase from "firebase";
import { Observable } from "rxjs";

export const config = {
  apiKey: "AIzaSyCN_bf8UfnUuuY5u0id2Vx0vFuTCiCXMD0",
  authDomain: "image-classifier-bfcf5.firebaseapp.com",
  databaseURL: "https://image-classifier-bfcf5.firebaseio.com",
  projectId: "image-classifier-bfcf5",
  storageBucket: "image-classifier-bfcf5.appspot.com",
  messagingSenderId: "905120757353",
  appId: "1:905120757353:web:ccee55b2f2c99c343314f8",
  measurementId: "G-8BE6Q5B42D",
};

export const getImages = async (collectionName: string) => {
  firebase.initializeApp(config);
  const db = firebase.firestore();
  const citiesRef = db.collection(collectionName);
  const snapshot = await citiesRef.get();
  const arr: string[] = [];
  snapshot.forEach((doc) => {
    const link = doc.data();
    arr.push(link.frame_url);
    console.log(link.frame_url);
  });
  console.log(arr);
  return arr;
};
