import { parseIssues } from "@/utils/utils";
import { useState, useEffect } from 'react';
import { useSeeker } from '@/context/seekerContext';
import { filterSeekersByProject } from "@/utils/utils";



const LargeOut = ({coachData}) => {

    const [message, setMessage] = useState('')
    const { showSolo, showCapstone, showGroup } = useSeeker();

    useEffect(() => {
        setMessage(genMessage())
    }, [coachData, showSolo, showCapstone, showGroup])

    const genMessage = () => {

        let data = filterSeekersByProject(
            coachData,
            {solo: showSolo, capstone: showCapstone, group: showGroup}
        )

        let message = [
            'Hey Everyone, I know you know how important it is keep your projects up and running.',
            'with that in mind, I\'ve checked your sites and a few of them are having some issues.',
        ];

        for (let seeker in data) {

            message.push(`### ${seeker}:`)

            for (let proj in coachData[seeker]) {
                if (Object.values(coachData[seeker][proj]).length === 0 || proj === 'email') continue;
                message.push(`* ${proj}: ${parseIssues(Object.values(coachData[seeker][proj]))}`)
            }

        }

        return message.join('\n')
    }

    const handleCopy = () => {
        navigator.clipboard.writeText(message);
        alert('Copied Discord Message');
    }

    return (
        <div className="pl-3 my-5">
            <h2 className="text-3xl">
                Discord Message -&ensp;
                <button className="px-2 py-1 rounded bg-gray-800 hover:bg-slate-600 transition-all" onClick={handleCopy}>Copy All</button>
            </h2>
            <textarea className="w-full h-full mt-2 p-2 bg-gray-700 rounded" readOnly value={message}/>
        </div>
    )
}


export default LargeOut;