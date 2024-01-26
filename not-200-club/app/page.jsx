"use client"
import { useState, useEffect } from 'react';
import Link from 'next/link';
import getRecent from '@/firebase/getRecent';
import SeekerList from '@/components/seekerList';
import LargeOut from '@/components/largeOut';


const Home = () => {
  const [coachData, setCoachData] = useState({});
  const [currCoach, setCurrCoach] = useState('none');

  useEffect(() => {
    getRecent()
    .then(res => {
      setCoachData(res);
    })
  }, [])

  const createCoaches = () => {
    let coaches = [];
    for (let coach in coachData) {
      if (coach === 'date') continue
      coaches.push(
        <option value={coach} key={coach}>{coach}</option>
      );
    };
    return coaches;
  };

  const coachOutput = () => {
      if (currCoach === 'none') return <div className='p-5'>Select coach</div>;
      let coach = coachData[currCoach];

      return (
        <>
          <SeekerList coachData={coach}/>
          <LargeOut coachData={coach}/>
        </>
      )
  };

  return (
    <main className='px-5'>
      <h1 className="pt-5 text-2xl text-red-500 font-mono ">Not 200 Club</h1>
      <h2 className="text-xl text-red-500 font-mono">a/A site health check</h2>
      <label>
        Coach: &ensp;
        <select className='text-black' onChange={(e) => (setCurrCoach(e.target.value))}>
          <option defaultValue>None</option>
          {createCoaches()}
        </select>
      </label>

      <Link href="new" className='fixed top-5 right-6 rounded p-1 bg-gray-800 hover:bg-slate-600 transition-all'>Upload(Josiah Only)</Link>

      <div className='flex'>
        {coachOutput()}
      </div>
    </main>
  );
};


export default Home;
