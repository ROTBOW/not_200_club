import firebase_app from "./config";
import { getFirestore, getDocs, orderBy, query, collection, where } from "firebase/firestore";

const db = getFirestore(firebase_app)
const sixMothsAgo = new Date(new Date().setMonth(new Date().getMonth() - 6));

/**
 * this function hits the firestore database for the all documents.
 * @returns the all documents in firestore
 */
export default async function getLastSixMonths() {
    const q = query(collection(db, 'healthData'),  where('date', '>', sixMothsAgo), orderBy('date', 'desc'));
    const qsnap = await getDocs(q);
    
    let docs = [];
    qsnap.forEach(doc => {
        docs.push(doc.data())
    })
    
    return docs;
};