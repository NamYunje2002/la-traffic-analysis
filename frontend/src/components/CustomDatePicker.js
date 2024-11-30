import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { ko } from 'date-fns/locale';
import { useState } from 'react';

const CustomDatePicker = ({ minDate, maxDate, handleSearch }) => {
  const [startDateTime, setStartDateTime] = useState(minDate);
  const [endDateTime, setEndDateTime] = useState(maxDate);

  return (
    <div style={{ margin: '32px 0px' }}>
      <LocalizationProvider dateAdapter={AdapterDateFns} locale={ko}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <DateTimePicker
            label="시작 날짜"
            value={startDateTime}
            onChange={(newValue) => setStartDateTime(newValue)}
            minDateTime={minDate}
            maxDateTime={maxDate}
            ampm={false}
            format="yyyy-MM-dd HH:mm"
          />
          <span>-</span>
          <DateTimePicker
            label="종료 날짜"
            value={endDateTime}
            onChange={(newValue) => setEndDateTime(newValue)}
            minDateTime={startDateTime}
            maxDateTime={maxDate}
            ampm={false}
            format="yyyy-MM-dd HH:mm"
          />
          <button
            style={{
              padding: '8px 16px',
              backgroundColor: '#1976d2',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
            onClick={() => handleSearch(startDateTime, endDateTime)}
          >
            검색
          </button>
        </div>
      </LocalizationProvider>
    </div>
  );
};

export default CustomDatePicker;
