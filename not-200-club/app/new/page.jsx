"use client"
import { useState } from 'react';
import Link from 'next/link';
import { Timestamp } from 'firebase/firestore';
import addHealthCheck from '@/firebase/addHealthCheck';

const UploadData = () => {

    const [json, setJson] = useState('{}')

    const handleFileUpload = (e) => {
        let fr = new FileReader();

        fr.onload = (e) => {
            
            let data = JSON.parse(e.target.result)
            data.date = Timestamp.fromDate(new Date())
            setJson(JSON.stringify(data, null, 2))
            
            addHealthCheck(data)
            .then(res => {
                console.log(res);
                if (res.result) {
                    alert('Upload Success')
                }
            })
        }
        
        fr.readAsText(e.target.files[0])
    }

    return (
        <div className="flex justify-around mt-5">
            <div className='w-2/5 pl-5'>
                <Link href='/' className="rounded p-1 bg-gray-800 hover:bg-slate-600 transition-all">Home</Link>
                <p className='py-5'>Upload health json file</p>
                <input type="file" onChange={handleFileUpload}/>
            </div>
            <pre className='w-3/5 h-96 overflow-auto pl-2 mx-5 bg-red-400 rounded font-mono'>
                <code>
                    {json}
                </code>
            </pre>
        </div>
    )
};

export default UploadData;