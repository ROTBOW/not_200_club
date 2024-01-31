
import { parseIssues } from "@/utils"

const SeekerList = ({coachData}) => {

    const assignDangerLevel = (issues) => {

        for (let issue of issues) {
            const re = /^\d{0,4}\.\d+$/;
            if (re.test(issue.toString())) {
                return 'seeker-mid'
            }
        }

        if (issues.length === 0) {
            return 'seeker-good'
        }

        return 'seeker-bad'
    }


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

        for (let seeker in coachData) {

            let solo = Object.values(coachData[seeker]['solo']);
            let cap = Object.values(coachData[seeker]['capstone']);
            let group = Object.values(coachData[seeker]['group']);

            const rowStyle = 'p-2 border max-w-44 h-1 overflow-auto whitespace-nowrap';

            s.push(
                <tr key={seeker}>
                    <td className="p-2 border">{seeker}</td>
                    <td className={`${rowStyle} ${assignDangerLevel(solo)}`}>{parseIssues(solo)}</td>
                    <td className={`${rowStyle} ${assignDangerLevel(cap)}`}>{parseIssues(cap)}</td>
                    <td className={`${rowStyle} ${assignDangerLevel(group)}`}>{parseIssues(group)}</td>
                    <td className="p-2 border flex justify-center h-full">
                        <button className="w-full h-full rounded bg-gray-800 hover:bg-slate-600 transition-all" onClick={createSingleDiscordMessage(coachData[seeker], seeker)}>Copy</button>
                    </td>
                </tr>
            )
        }

        return s;
    }

    return (
        <div className="my-5">
            <h2 className="text-3xl underline">Seeker Site Issues</h2>

            <table className="mt-2 p-5 border rounded">
                <tbody>
                    <tr>
                        <th className="p-2 border w-80">Seeker Name</th>
                        <th className="p-2 border">Solo Issues</th>
                        <th className="p-2 border">Capstone Issues</th>
                        <th className="p-2 border">Group Issues</th>
                        <th className="p-2 border">Discord Message</th>
                    </tr>
                    { seekers() }
                </tbody>
            </table>
        </div>
    )
}


export default SeekerList;