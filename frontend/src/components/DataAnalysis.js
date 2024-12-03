import React, { useEffect, useState } from 'react';
import {
  ScatterChart,
  Scatter,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { styles } from './styles';

const DataAnalysis = ({ googleMapsApiKey, laCoordinates }) => {
  const [realScatterData, setRealScatterData] = useState([]);
  const [predictedScatterData, setPredictedScatterData] = useState([]);

  const [combinedHistogramData, setCombinedHistogramData] = useState(null);

  const mergeHistogramData = (realData, predictedData) => {
    const mergedData = [];

    const realMap = new Map(realData.map((item) => [item.range, item.count]));
    const predictedMap = new Map(predictedData.map((item) => [item.range, item.count]));

    const allRanges = Array.from(new Set([...realMap.keys(), ...predictedMap.keys()]));

    allRanges.sort((a, b) => {
      const startA = parseInt(a.split(' to ')[0], 10);
      const startB = parseInt(b.split(' to ')[0], 10);
      return startA - startB;
    });

    allRanges.forEach((range) => {
      mergedData.push({
        range,
        realCount: realMap.get(range) || 0,
        predictedCount: predictedMap.get(range) || 0,
      });
    });

    return mergedData;
  };

  useEffect(() => {
    fetch('http://localhost:5000/api/collision-data?type=scatter')
      .then((response) => response.json())
      .then((data) => {
        setRealScatterData(data.scatter_real_data);
        setPredictedScatterData(data.scatter_predicted_data);
      })
      .catch((error) => console.error('Error fetching scatter data:', error));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/collision-data?type=histogram')
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        const realData = data['histogram_real_data'].map((item) => ({
          range: `${item.range} to ${item.range + 10}`,
          count: item.count,
        }));

        const predictedData = data['histogram_predicted_data'].map((item) => ({
          range: `${item.range} to ${item.range + 10}`,
          count: item.count,
        }));

        const mergedData = mergeHistogramData(realData, predictedData);
        setCombinedHistogramData(mergedData);

        console.log('Real Data:', realData);
        console.log('Predicted Data:', predictedData);
        console.log('Merged Data:', mergedData);
      })
      .catch((error) => console.error('Error fetching histogram data:', error));
  }, []);

  return (
    <div style={styles.grid}>
      <div style={{ ...styles.card, ...styles.fullWidth }}>
        <div style={styles.cardTitle}>사고 전후 평균 속도 비교</div>
        <div style={styles.chartContainer}>
          <ResponsiveContainer>
            <ScatterChart>
              <CartesianGrid />
              <XAxis
                type="number"
                dataKey="preSpeed"
                name="교통사고 이전 속도"
                unit="km/h"
                domain={[0, 80]}
              />
              <YAxis
                type="number"
                dataKey="postSpeed"
                name="교통사고 이후 속도"
                unit="km/h"
                domain={[0, 80]}
              />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Legend />
              <Scatter name="실제 데이터" data={realScatterData} fill="#8884d8" />
              <Scatter name="예측 데이터" data={predictedScatterData} fill="#82ca9d" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ ...styles.card, ...styles.fullWidth }}>
        <div style={styles.cardTitle}>속도 변화 분포</div>
        <div style={styles.chartContainer}>
          <ResponsiveContainer>
            <BarChart data={combinedHistogramData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" label={{ position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Count', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="realCount" fill="#8884d8" name="실제 데이터" />
              <Bar dataKey="predictedCount" fill="#82ca9d" name="예측 데이터" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default DataAnalysis;
