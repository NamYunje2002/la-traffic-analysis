from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from geopy.distance import geodesic
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

collision_file_path = "./dataset/collision.csv"

app.config.from_object(Config)

@app.route('/api/google-maps-key', methods=['GET'])
def get_google_maps_key():
    print(app.config['GOOGLE_MAPS_API_KEY'])
    return jsonify({'apiKey': app.config['GOOGLE_MAPS_API_KEY']})

speed_data = pd.read_csv('./dataset/speed.csv')
collision_data = pd.read_csv('./dataset/collision.csv')
sensor_locations = pd.read_csv('./dataset/graph_sensor_locations.csv')

speed_data['Date Occurred'] = pd.to_datetime(speed_data['Date Occurred'], errors='coerce')
collision_data['Date Occurred'] = pd.to_datetime(collision_data['Date Occurred'], errors='coerce')

def find_nearby_sensors(latitude, longitude, sensors, radius_km=5):
    location_point = (latitude, longitude)
    nearby_sensors = []
    for _, sensor_row in sensors.iterrows():
        sensor_point = (sensor_row['latitude'], sensor_row['longitude'])
        distance = geodesic(location_point, sensor_point).km
        if distance <= radius_km:
            nearby_sensors.append(sensor_row['sensor_id'])
    return nearby_sensors

def get_speed_trends(lat, lon, datetime_str):
    collision_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    start_time = collision_time - timedelta(minutes=5)
    end_time = collision_time + timedelta(minutes=30)

    def find_nearby_sensors(latitude, longitude, sensors, radius_km=5):
        location_point = (latitude, longitude)
        nearby_sensors = []
        for _, sensor_row in sensors.iterrows():
            sensor_point = (sensor_row['latitude'], sensor_row['longitude'])
            distance = geodesic(location_point, sensor_point).km
            if distance <= radius_km:
                nearby_sensors.append(sensor_row)
        return nearby_sensors

    nearby_sensors = find_nearby_sensors(lat, lon, sensor_locations, radius_km=5)

    sensor_mapping = {
        str(int(sensor_row['sensor_id'])): f"({sensor_row['latitude']}, {sensor_row['longitude']})"
        for _, sensor_row in pd.DataFrame(nearby_sensors).iterrows()
    }

    relevant_columns = ['Date Occurred'] + list(sensor_mapping.keys())
    speed_data['Date Occurred'] = pd.to_datetime(speed_data['Date Occurred'], format="%a, %d %b %Y %H:%M:%S %Z", errors='coerce')
    filtered_speed_data = speed_data[
        (speed_data['Date Occurred'] >= start_time) & (speed_data['Date Occurred'] <= end_time)
    ][relevant_columns]

    filtered_speed_data = filtered_speed_data.rename(columns=sensor_mapping)

    filtered_speed_data['Date Occurred'] = filtered_speed_data['Date Occurred'].dt.strftime("%Y-%m-%d %H:%M")

    return filtered_speed_data.to_dict(orient='records')

@app.route('/api/get_speed_data', methods=['GET'])
def get_speed_data():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    datetime_str = request.args.get('datetime')

    try:
        speed_trends = get_speed_trends(latitude, longitude, datetime_str)
        return jsonify({'success': True, 'speed_trends': speed_trends})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def convert_month_to_number(month_abbr):
    month_to_number = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12"
    }
    return month_to_number.get(month_abbr.upper(), None)
    
@app.route('/api/collisions', methods=['GET'])
def get_collisions():
    start_datetime = request.args.get('start_datetime')
    end_datetime = request.args.get('end_datetime')
    
    try:
        collision_df = pd.read_csv(collision_file_path)
        filtered_df = collision_df[['latitude', 'longitude', 'Date Occurred', 'Time Occurred']].copy()

        if (start_datetime and end_datetime):
            filtered_df['Datetime'] = pd.to_datetime(filtered_df['Date Occurred'] + ' ' + filtered_df['Time Occurred'])

            start_date = f'{start_datetime[11:15]}-{convert_month_to_number(start_datetime[4:7])}-{start_datetime[8:10]}'
            start_time = f'{start_datetime[16:21]}'
            start_datetime = start_date + ' ' + start_time

            end_date = f'{end_datetime[11:15]}-{convert_month_to_number(end_datetime[4:7])}-{end_datetime[8:10]}'
            end_time = f'{end_datetime[16:21]}'
            end_datetime = end_date + ' ' + end_time

            filtered_df = filtered_df[(filtered_df['Datetime'] >= start_datetime) & (filtered_df['Datetime'] <= end_datetime)]

        result = filtered_df.to_dict(orient='records')
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/collision-data', methods=['GET'])
def get_collision_data():
    collision_data = pd.read_csv("./dataset/collision_speed_data.csv")
    
    data_type = request.args.get('type', 'scatter')

    if data_type == 'scatter':
        scatter_data = collision_data[['pre_speed_mean', 'post_speed_mean']].dropna().rename(
            columns={
                'pre_speed_mean': 'preSpeed',
                'post_speed_mean': 'postSpeed'
            }
        ).to_dict(orient='records')
        return jsonify(scatter_data)

    elif data_type == 'histogram':
        if 'speed_change' not in collision_data.columns or collision_data['speed_change'].dropna().empty:
            return jsonify({"error": "No data for histogram"}), 400

        collision_data['speed_change_bins'] = collision_data['speed_change'].dropna().apply(
            lambda x: int(x // 10) * 10
        )
        histogram_data = collision_data['speed_change_bins'].value_counts().reset_index()

        if len(histogram_data.columns) == 2:
            histogram_data = histogram_data.rename(columns={histogram_data.columns[0]: 'range', histogram_data.columns[1]: 'count'})
        else:
            print("Unexpected histogram structure:", histogram_data.columns)
            return jsonify({"error": "Unexpected histogram data structure"}), 500

        histogram_data['range'] = pd.to_numeric(histogram_data['range'], errors='coerce')
        histogram_data = histogram_data.sort_values('range')

        return jsonify(histogram_data.to_dict(orient='records'))
    
    else:
        return jsonify({"error": "Invalid type parameter"}), 400

if __name__ == "__main__":
    app.run(debug = True)