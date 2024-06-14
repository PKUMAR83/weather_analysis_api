from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3

app = Flask(__name__)
api = Api(app)

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Weather Crop API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Database connection function
def query_db(query, args=(), one=False):
    try:
        conn = sqlite3.connect('../db/weather_crop.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500


# Helper function to convert SQLite row objects to dictionaries
def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


# Helper function for pagination
def paginate(query_result, page, per_page):
    total_items = len(query_result)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'total_items': total_items,
        'page': page,
        'per_page': per_page,
        'items': query_result[start:end]
    }


class Weather(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('station_id', type=int, required=False, location='args')
            parser.add_argument('start_date', type=str, required=False, location='args')
            parser.add_argument('end_date', type=str, required=False, location='args')
            parser.add_argument('page', type=int, default=1, location='args')
            parser.add_argument('per_page', type=int, default=10, location='args')
            args = parser.parse_args()

            query = 'SELECT * FROM weather_data WHERE 1=1'
            query_params = []
            if args['station_id']:
                query += ' AND station_id = ?'
                query_params.append(args['station_id'])
            if args['start_date']:
                query += ' AND date >= ?'
                query_params.append(args['start_date'])
            if args['end_date']:
                query += ' AND date <= ?'
                query_params.append(args['end_date'])

            weather_data = query_db(query, query_params)
            weather_data = [row_to_dict(row) for row in weather_data]  # Convert rows to dicts
            paginated_data = paginate(weather_data, args['page'], args['per_page'])

            return jsonify(paginated_data)
        except Exception as e:
            return internal_error(e)


class WeatherStats(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('station_id', type=int, required=False, location='args')
            parser.add_argument('year', type=int, required=False, location='args')
            parser.add_argument('page', type=int, default=1, location='args')
            parser.add_argument('per_page', type=int, default=10, location='args')
            args = parser.parse_args()

            query = ('SELECT station_id,year,avg_max_temp,avg_min_temp, '
                     'total_precipitation FROM weather_statistics WHERE 1=1')
            query_params = []
            if args['station_id']:
                query += ' AND station_id = ?'
                query_params.append(args['station_id'])
            if args['year']:
                query += ' AND year = ?'
                query_params.append(args['year'])

            weather_stats = query_db(query, query_params)
            weather_stats = [row_to_dict(row) for row in weather_stats]  # Convert rows to dicts
            paginated_data = paginate(weather_stats, args['page'], args['per_page'])

            return jsonify(paginated_data)
        except sqlite3.Error as e:
            return internal_error(e)


api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

if __name__ == '__main__':
    app.run(debug=True)
