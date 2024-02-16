'use client'
import Link from 'next/link';
import { useState, useEffect } from 'react';
import getLastSixReports from '@/firebase/getLastSixReports';
import StatAllIssues from '@/components/charts/statAllIssues';
import PieIssues from '@/components/charts/pieIssues';
import ProjectSummary from '@/components/projectSummary';

const Stats = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        getLastSixReports()
        .then(res => {
            setData(res);
        })
    }, [])

    const getIssueCount = (proj) => {
        let res = [];

        for (let doc of data) {
            let count = 0;
            for (let coach in doc) {
                if (coach === 'date') continue;
                for (let seeker in doc[coach]) {
                    if (Object.values(doc[coach][seeker][proj]).length !== 0) {
                        count++;
                    }
                }
            }
            res.push(count)
        }

        return res;
    };

    const getProjectIssues = (data, proj) => {
        let sw = 0;
        let swo = 0;

        for (let coach in data) {
            if (coach === 'date') continue;
            for (let seeker in data[coach]) {
                if (Object.values(data[coach][seeker][proj]).length === 0) {
                    swo++;
                } else {
                    sw++;
                }
            }
        }

        return [sw, swo];
    }

    if (data === null) {
        return <div>Loading...</div>
    }
    return (
        <div className='flex flex-col items-center my-10'>
            <Link href="/" className='fixed top-5 right-6 rounded p-1 bg-gray-800 hover:bg-slate-600 transition-all'>Home</Link>
            <h2 className="text-2xl">Here are those numbers for you Anna :)<br/>Hope your day is going well</h2>

            <StatAllIssues solo={getIssueCount('solo')} capstone={getIssueCount('capstone')} group={getIssueCount('group')}/>
            <div className='flex mb-2'>
                <ProjectSummary project={'solo'} currData={getProjectIssues(data[0], 'solo')} lastData={getProjectIssues(data[1], 'solo')}/>
                <ProjectSummary project={'capstone'} currData={getProjectIssues(data[0], 'capstone')} lastData={getProjectIssues(data[1], 'capstone')}/>
                <ProjectSummary project={'group'} currData={getProjectIssues(data[0], 'group')} lastData={getProjectIssues(data[1], 'group')}/>
            </div>
            <div className='flex mb-2'>
                <PieIssues eleId='pie1' title="Current Report - Solo" data={getProjectIssues(data[0], 'solo')}/>
                <PieIssues eleId='pie2' title="Current Report - Capstone" data={getProjectIssues(data[0], 'capstone')}/>
                <PieIssues eleId='pie3' title="Current Report - Group" data={getProjectIssues(data[0], 'group')}/>
            </div>
            <div className='flex'>
                <PieIssues eleId='pie4' title="Last Report - Solo" data={getProjectIssues(data[1], 'solo')}/>
                <PieIssues eleId='pie5' title="Last Report - Capstone" data={getProjectIssues(data[1], 'capstone')}/>
                <PieIssues eleId='pie6' title="Last Report - Group" data={getProjectIssues(data[1], 'group')}/>
            </div>
        </div>
    )
}

export default Stats;