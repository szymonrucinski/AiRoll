import firebase from "firebase";
import { expect } from "chai";

const config = {
  apiKey: "AIzaSyCN_bf8UfnUuuY5u0id2Vx0vFuTCiCXMD0",
  authDomain: "image-classifier-bfcf5.firebaseapp.com",
  databaseURL: "https://image-classifier-bfcf5.firebaseio.com",
  projectId: "image-classifier-bfcf5",
  storageBucket: "image-classifier-bfcf5.appspot.com",
  messagingSenderId: "905120757353",
  appId: "1:905120757353:web:ccee55b2f2c99c343314f8",
  measurementId: "G-8BE6Q5B42D",
};

describe("Test Firebase connection", () => {
  it("should return list of all movies from DB", async () => {
    firebase.initializeApp(config);
    const db = firebase.firestore();
    const citiesRef = db.collection("0A_LIST_OF_MOVIES");
    const snapshot = await citiesRef.get();
    snapshot.forEach((doc) => {
      console.log(doc.id, "=>", doc.data());
    });
    expect("HelloWorld").to.equal("Hello World!");
  });
});
