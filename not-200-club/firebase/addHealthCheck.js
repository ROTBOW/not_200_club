import firebase_app from "./config";
import { getFirestore, collection, addDoc } from 'firebase/firestore';

const db = getFirestore(firebase_app)

/**
 * 
 * @param {*} data - a json string, that will be uploaded to firestore
 * @returns the result and or error from trying to upload seeker data
 */
export default async function addHealthCheck(data) {
    let result = null;
    let error = null;

    try {
        result = await addDoc(collection(db, 'healthData'), data);
    } catch (e) {
        error = e;
    }

    return { result, error }
};