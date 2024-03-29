import { assignDangerLevel } from '@/utils/seekerListUtils';
import { parseIssues, filterSeekersByProject } from "@/utils/utils"
import { useSeeker } from '@/context/seekerContext';
import Image from 'next/image';
import copy from '@/public/content_copy.svg';

const SeekerList = ({coachData, seenSeekers}) => {
    // using context to control what projects we're showing, along with the issue type
    const { showSolo, setShowSolo, showCapstone, setShowCapstone, showGroup, setShowGroup, issueType, setIssueType } = useSeeker();

    const createSingleDiscordMessage = (projs, seeker) => {
        return (e) => {
            let message = [
                `Hey ${seeker.split(' ')[0]} some of your projects have issues:`
            ];
    
            for (let proj in projs) {
                if (Object.values(projs[proj]).length === 0) continue;
                message.push(`### ${proj}:`)
                for (let issue in projs[proj]) {
                    message.push(`  * ${(projs[proj][issue] === true) ? 'No Link in salesforce' : issue+' '+projs[proj][issue]}`)
                }
            }
    
            navigator.clipboard.writeText(message.join('\n'));
        }
    }

    /**
     * The function `handleCopyEmails` copies all non-empty email values from elements with the class
     * name 'email-container' and joins them into a single string, which is then copied to the
     * clipboard.
     */
    const handleCopyEmails = (e) => {
        let emailsEles = document.getElementsByClassName('email-container');
        let emails = [];

        for (let ele of emailsEles) {
            if (ele.tagName.toLowerCase() === 'input' && ele.value !== 'n/a') {
                emails.push(ele.value);
            }
        }

        navigator.clipboard.writeText(emails.join(' '));
        alert('Copied all emails');
    }

    const seekers = () => { // this function creates each seeker's row for the table
        let s = [];
        
        let data = filterSeekersByProject( // this filters the data based on the project and or type
            coachData,
            {solo: showSolo, capstone: showCapstone, group: showGroup},
            issueType
        );
        
        for (let seeker in data) {
            
            let solo = Object.values(coachData[seeker]['solo']);
            let cap = Object.values(coachData[seeker]['capstone']);
            let group = Object.values(coachData[seeker]['group']);
            let email = data[seeker].email ? data[seeker].email : 'n/a'

            const rowStyle = 'p-2 border max-w-44 h-1 overflow-auto whitespace-nowrap';
            
            s.push(
                <tr key={seeker}>
                    <td className={`p-2 border ${(seenSeekers.has(seeker.toLowerCase())) ? 'seeker-bad' : ''}`}>{seeker}</td>
                    <td className={rowStyle}>
                        <input 
                            className='bg-black w-full email-container'
                            onClick={e => e.target.select()}
                            value={email}
                        />
                    </td>
                    {showSolo && <td className={`${rowStyle} ${assignDangerLevel(solo)}`}>{parseIssues(solo)}</td>}
                    {showCapstone && <td className={`${rowStyle} ${assignDangerLevel(cap)}`}>{parseIssues(cap)}</td>}
                    {showGroup && <td className={`${rowStyle} ${assignDangerLevel(group)}`}>{parseIssues(group)}</td>}
                    <td className="p-2 border flex justify-center h-full">
                        <button className="w-full h-full rounded bg-gray-800 hover:bg-slate-600 transition-all" onClick={createSingleDiscordMessage(coachData[seeker], seeker)}>Copy</button>
                    </td>
                </tr>
            )
        }

        return s;
    }

    const checkboxStyle = 'flex items-center pr-2 text-lg';
    return (
        <div className="my-5">
            <h2 className="text-3xl">
                Seeker Site Issues
                <label className='text-sm'>
                    <select className='mx-2 text-black rounded' onChange={e => (setIssueType(e.target.value))}>
                        <option defaultValue value="all">All</option>
                        {
                            ['status', 'time', 'no-link', 'timeout', 'bad_url'].map(issue => (
                                <option value={issue}>{issue}</option>
                            ))
                        }
                    </select>
                    : Issue Type
                </label>
            </h2>
            <div className="flex">
                <label className={checkboxStyle}>
                    <input type='checkbox' checked={showSolo} onChange={(e) => (setShowSolo(e.target.checked))}/>
                    Solo
                </label>
                <label className={checkboxStyle}>
                    <input type='checkbox' checked={showCapstone} onChange={(e) => (setShowCapstone(e.target.checked))}/>
                    Capstone
                </label>
                <label className={checkboxStyle}>
                    <input type='checkbox' checked={showGroup} onChange={(e) => (setShowGroup(e.target.checked))}/>
                    Group
                </label>
                <div className='flex items-center underline ml-4'>Total Seekers With Issues: {Object.keys(coachData).length}</div>
            </div>

            <table className="mt-2 p-5 border rounded">
                <tbody>
                    <tr>
                        <th className="p-2 border w-64">Seeker Name</th>
                        <th className="p-2 border w-52 h-full">
                            Email
                            <button onClick={handleCopyEmails}><Image src={copy} className='ml-2'/></button>
                        </th>
                        {showSolo && <th className="p-2 border">Solo Issues</th>}
                        {showCapstone && <th className="p-2 border">Capstone Issues</th>}
                        {showGroup && <th className="p-2 border">Group Issues</th>}
                        <th className="p-2 border">Discord Message</th>
                    </tr>
                    { seekers() }
                </tbody>
            </table>
        </div>
    )
}


export default SeekerList;