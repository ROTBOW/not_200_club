
import { assignDangerLevel } from '@/utils/seekerListUtils';
import { parseIssues, filterSeekersByProject } from "@/utils/utils"
import { useSeeker } from '@/context/seekerContext';

const SeekerList = ({coachData, seenSeekers}) => {
    const { showSolo, setShowSolo, showCapstone, setShowCapstone, showGroup, setShowGroup } = useSeeker();

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

    const seekers = () => {
        let s = [];
        
        let data = filterSeekersByProject(
            coachData,
            {solo: showSolo, capstone: showCapstone, group: showGroup}
        );
        
        for (let seeker in data) {

            let solo = Object.values(coachData[seeker]['solo']);
            let cap = Object.values(coachData[seeker]['capstone']);
            let group = Object.values(coachData[seeker]['group']);

            const rowStyle = 'p-2 border max-w-44 h-1 overflow-auto whitespace-nowrap';
            
            s.push(
                <tr key={seeker}>
                    <td className={`p-2 border ${(seenSeekers.has(seeker.toLowerCase())) ? 'seeker-bad' : ''}`}>{seeker}</td>
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
            <h2 className="text-3xl underline">Seeker Site Issues</h2>
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
            </div>

            <table className="mt-2 p-5 border rounded">
                <tbody>
                    <tr>
                        <th className="p-2 border w-80">Seeker Name</th>
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