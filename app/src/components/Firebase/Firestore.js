import { initializeApp } from "firebase/app";
import "firebase/firestore"
import { getFirestore, collection, doc, getDoc, setDoc } from "firebase/firestore";
import { getDatabase } from "firebase/database";
import { getStorage, ref, getDownloadURL } from "firebase/storage";

const firebaseConfig = {
    apiKey: "AIzaSyB13Rzp7Ey2IFI3RTY9cD1VHFq9p8_uF4U",
    authDomain: "wolvercoin-hw.firebaseapp.com",
    projectId: "wolvercoin-hw",
    storageBucket: "wolvercoin-hw.appspot.com",
    messagingSenderId: "101117958130",
    appId: "1:101117958130:web:49ad8f0613ef4eb66d3d6b",
    measurementId: "G-PC4QR208EF"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const firestore = getFirestore(app);
const prodDb = getDatabase(app);
const storage = getStorage(app);

class Firestore {
    constructor(app, firestore, prodDb, storage) {
        this.app = app;
        this.firestore = firestore;
        this.prodDb = prodDb;
        this.storage = storage;
    }

    // Grab collection data
    async getDocument(collectionId, docId) {
        const docRef = doc(this.firestore, collectionId, decodeURI(docId));
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            return docSnap.data();
        } else {
            // doc.data() will be undefined in this case
            console.log("No such document!");
            return {};
        }
    }

    // Grab images by folder/url
    async getStorageImage(folder, docId) {
        let imgRef = folder + '/' + decodeURI(docId);
        let storageUrl = await getDownloadURL(ref(this.storage, imgRef)).then(function(url) 
        {
            return url;
        }).catch(function(error) 
        {
            switch (error.code) 
            {
                case 'storage/object_not_found':
                    break;

                case 'storage/unauthorized':
                    break;

                case 'storage/canceled':
                    break;

                case 'storage/unknown':
                    break;
            }
        });
        return storageUrl;
    }

}

export default new Firestore(app, firestore, prodDb, storage);