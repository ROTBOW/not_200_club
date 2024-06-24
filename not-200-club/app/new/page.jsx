"use client"
import { useState } from 'react';
import Link from 'next/link';
import { Timestamp } from 'firebase/firestore';
import addHealthCheck from '@/firebase/addHealthCheck';

const UploadData = () => {

    const [json, setJson] = useState('{}');
    const [pass, setPass] = useState('');

    const handleFileUpload = (e) => {

        if (pass !== process.env.NEXT_PUBLIC_PASSWORD) {
            alert('Wrong password!\ndoing nothing...')
            return
        }

        let fr = new FileReader();

        fr.onload = (e) => {
            
            let data = JSON.parse(e.target.result)
            data.date = Timestamp.fromDate(new Date())
            setJson(JSON.stringify(data, null, 2))
            
            addHealthCheck(data)
            .then(res => {
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
                <p className='py-5'>Manual upload health json file in case the auto upload isn't working</p>
                <label className='p-5'>
                    Password&ensp;
                    <input type='password' className='text-black' onChange={(e)=>{setPass(e.target.value)}}/>
                </label>
                <input type="file" onChange={handleFileUpload}/>
            </div>
            <pre className='w-3/5 h-96 overflow-auto pl-2 mx-5 bg-gray-700 rounded font-mono'>
                <code>
                    {json}
                </code>
            </pre>
        </div>
    )
};

export default UploadData;