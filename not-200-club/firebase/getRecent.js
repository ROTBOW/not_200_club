import firebase_app from "./config";
import { getFirestore, getDocs, orderBy, query, collection, limit } from "firebase/firestore";

const db = getFirestore(firebase_app)

/**
 * this function hits the firestore database for the two most recent documents.
 * @returns the two most recent documents in firestore
 */
export default async function getRecent() {
    const q = query(collection(db, 'healthData'), orderBy('date', 'desc'), limit(2));
    const qsnap = await getDocs(q);
    
    let docs = [];
    qsnap.forEach(doc => {
        docs.push(doc.data())
    })
    
    return docs;
};