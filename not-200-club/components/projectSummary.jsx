import { useState } from 'react';

const ProjectSummary = ({project, currData, lastData}) => {
    const [num, setNum] = useState(currData[0])
    const [num2, setNum2] = useState(lastData[0])
    let percentChange = num2 !== 0 ? ((num - num2) / num2) * 100 : 0; // Calculate percent change
    let absoluteChange = num - num2; // Calculate absolute change

    const colorMe = (num) => {
        if (num > 0) {
            return 'text-red-500'
        } else {
            return 'text-green-500'
        }
    }

    return (
        <div className="bg-gray-700 rounded w-62 p-3 mx-2" style={{width: '26rem'}}>
            <h3 className="p-3 font-semibold capitalize text-center text-3xl">{project}</h3>
            From {num2} to {num} from last report to this one <br/>
            <div>
                Percent Change: <div className={`inline ${colorMe(percentChange)}`}>{percentChange.toFixed(2)}%</div>
            </div>
            <div>
                Absolute Change: <div className={`inline ${colorMe(absoluteChange)}`}>{absoluteChange}</div>
            </div>
        </div>
    )
}

export default ProjectSummary;