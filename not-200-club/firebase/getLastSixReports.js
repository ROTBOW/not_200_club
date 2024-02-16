import firebase_app from "./config";
import { getFirestore, getDocs, orderBy, query, collection, where, limit } from "firebase/firestore";

const db = getFirestore(firebase_app)

/**
 * this function hits the firestore database for the all documents.
 * @returns the all documents in firestore
 */
export default async function getLastSixReports() {
    const q = query(collection(db, 'healthData'), orderBy('date', 'desc'), limit(6));
    const qsnap = await getDocs(q);
    
    let docs = [];
    qsnap.forEach(doc => {
        docs.push(doc.data())
    })
    
    return docs;
};