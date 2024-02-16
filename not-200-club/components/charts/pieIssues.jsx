'use client'
import { useEffect } from 'react';
import Chart from "chart.js";


const PieIssues = ({eleId, title, data}) => {

    useEffect(() => {
        const config = {
            type: 'pie',
            data: {
                labels: ['Seekers With issues', 'Seekers Without'],
                datasets: [
                    {
                        label: 'issues_pie',
                        data: data,
                        backgroundColor: ['rgb(255, 99, 132)', 'rgb(102, 204, 0)']
                    }
                ],
                hoverOffset: 4
            },
            options: {
                responsive: true,
                legend: {
                    labels: {
                        fontColor: "white",
                    },
                    align: "center",
                    position: "bottom",
                },
                plugins: {
                title: {
                    display: true,
                    text: 'Chart.js Pie Chart'
                }
                }
            },
        };

        var ctx = document.getElementById(eleId).getContext("2d");
        window[eleId+'ID'] = new Chart(ctx, config);
    }, [])

    return (
        <div className='bg-gray-700 rounded mx-2' style={{width: '26rem'}}>
            <h2 className='p-2 text-xl font-semibold'>{title}</h2>
            <div className="relative h-450-px">
              <canvas id={eleId} className='h-64'></canvas>
            </div>
        </div>
    )

}

export default PieIssues;