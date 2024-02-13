'use client'
import { useEffect } from 'react';
import Chart from "chart.js";

const StatAllIssues = ({solo, capstone, group}) => {

  useEffect(() => {
    let config = {
      type: "line",
      data: {
        labels: [
          'Current Report',
          '1 Report ago',
          '2 Report ago',
          '3 Report ago',
          '4 Report ago',
          '5 Report ago',
        ],
        datasets: [
          {
            label: 'Solo',
            fill: false,
            backgroundColor: "#860B35",
            borderColor: "#860B35",
            data: solo,
          },
          {
            label: 'Capstone',
            fill: false,
            backgroundColor: "#09B852",
            borderColor: "#09B852",
            data: capstone,
          },
          {
            label: 'Group',
            fill: false,
            backgroundColor: "#98709C",
            borderColor: "#98709C",
            data: group,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
          display: false,
          text: "Sales Charts",
          fontColor: "white",
        },
        legend: {
          labels: {
            fontColor: "white",
          },
          align: "end",
          position: "bottom",
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        hover: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          xAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Month",
                fontColor: "white",
              },
              gridLines: {
                display: true,
                borderDash: [2],
                borderDashOffset: [2],
                color: "rgba(33, 37, 41, 0.3)",
                zeroLineColor: "rgba(0, 0, 0, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
          yAxes: [
            {
              ticks: {
                fontColor: "rgba(255,255,255,.7)",
              },
              display: true,
              scaleLabel: {
                display: false,
                labelString: "Value",
                fontColor: "white",
              },
              gridLines: {
                borderDash: [3],
                borderDashOffset: [3],
                drawBorder: false,
                color: "rgba(255, 255, 255, 0.15)",
                zeroLineColor: "rgba(33, 37, 41, 0)",
                zeroLineBorderDash: [2],
                zeroLineBorderDashOffset: [2],
              },
            },
          ],
        },
      },
    };
    var ctx = document.getElementById("line-chart").getContext("2d");
    window.myLine = new Chart(ctx, config);
  }, []);

    return (
      <div className="relative flex flex-col min-w-0 w-1/2 my-6 shadow-lg rounded bg-gray-700 break-words">
          <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
            <div className="flex flex-wrap items-center">
              <div className="relative w-full max-w-full flex-grow flex-1">
                <h2 className="text-white text-xl font-semibold">Projects with Issues</h2>
              </div>
            </div>
          </div>
          <div className="p-4 flex-auto">
            {/* Chart */}
            <div className="relative h-450-px">
              <canvas id="line-chart" className='!h-64'></canvas>
            </div>
          </div>
      </div>
    );
}

export default StatAllIssues;