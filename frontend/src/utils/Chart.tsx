import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

interface PlayerStatsData {
  headers: string[];
  rows: (string | number)[][];
}

const DynamicPlayerStatsTable = ({ data }: { data: PlayerStatsData }) => {

  const { headers, rows } = data;
  
  const generatePurpleShades = (count:number) => {
    const shades = [];
    
    for (let i = 0; i < count; i++) {
      const shade = i % 4;
      if (shade === 0) shades.push('rgba(156, 39, 176, 0.8)');      // Deep purple
      else if (shade === 1) shades.push('rgba(186, 104, 200, 0.8)'); // Medium purple
      else if (shade === 2) shades.push('rgba(142, 36, 170, 0.8)');  // Rich purple
      else shades.push('rgba(103, 58, 183, 0.8)');                  // Purple-blue
    }
    
    return shades;
  };

  const formatLabels = headers.slice(1);
  const colorPalette = generatePurpleShades(formatLabels.length);

  // Parse data for charts
  const parseNumericValue = (value:any) => {
    if (value === '–' || value === '-' || value === undefined) return 0;
    if (typeof value === 'number') return value;
    return parseFloat(value.toString().replace(/,/g, ''));
  };

  // Find indices for specific row types if they exist
  const findRowIndex = (rowName:any) => {
    return rows.findIndex(row => row[0].toString().toLowerCase().includes(rowName.toLowerCase()));
  };

  const matchesIndex = findRowIndex('matches');
  const runsIndex = findRowIndex('runs');
  const wicketsIndex = findRowIndex('wickets');

  // Extract data for charts if rows exist
  const getRowData = (index:any) => {
    if (index !== -1) {
      return rows[index].slice(1).map(parseNumericValue);
    }
    return Array(formatLabels.length).fill(0);
  };

  const matches = getRowData(matchesIndex);
  const runsScored = getRowData(runsIndex);
  const wickets = getRowData(wicketsIndex);

  // Chart data configurations
  const createChartData = (dataArray:any, label:any) => {
    return {
      labels: formatLabels,
      datasets: [
        {
          label,
          data: dataArray,
          backgroundColor: colorPalette
        },
      ],
    };
  };

  const barChartData = createChartData(runsScored, 'Runs Scored');
  const bowlingBarChartData = createChartData(wickets, 'Wickets Taken');
  const pieChartData = createChartData(matches, 'Matches Played');

  const chartOptions = {
    plugins: {
      legend: {
        labels: {
          color: 'black'
        }
      }
    },
    responsive: true,
    maintainAspectRatio: true
  };

  return (
    <div className="p-8 max-w-full overflow-x-auto overflow-y-auto h-screen">
      <h2 className="text-2xl mb-4 text-center">
        Cricket Player Career Stats
      </h2>

      {/* Dynamic Table */}
      <div className="mb-10 overflow-x-auto">
        <table className="w-full border border-gray-300 text-black">
          <thead>
            <tr>
              {headers.map((header, idx) => (
                <th
                  key={idx}
                  className="border border-gray-300 p-2 bg-gray-100 font-bold"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIdx) => (
              <tr
                key={rowIdx}
                className={rowIdx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
              >
                {row.map((cell, cellIdx) => (
                  <td
                    key={cellIdx}
                    className="border border-gray-300 p-2 text-left"
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Dynamic Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="flex flex-col space-y-8">
          {runsIndex !== -1 && (
            <div>
              <h3 className="text-center text-lg font-semibold mb-2">Runs Scored</h3>
              <Bar data={barChartData} options={chartOptions} />
            </div>
          )}

          {wicketsIndex !== -1 && (
            <div>
              <h3 className="text-center text-lg font-semibold mb-2">Wickets Taken</h3>
              <Bar data={bowlingBarChartData} options={chartOptions} />
            </div>
          )}
        </div>

        {matchesIndex !== -1 && (
          <div className="flex items-center justify-center">
            <div className="w-full">
              <h3 className="text-center text-lg font-semibold mb-2">Matches Played</h3>
              <Pie data={pieChartData} options={chartOptions} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DynamicPlayerStatsTable;