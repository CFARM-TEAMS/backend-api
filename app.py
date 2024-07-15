from flask import Flask, request, jsonify
from scraper import loop_month_day
import bps_scraper
from scrapper import get_web

app = Flask(__name__)

@app.route('/')
def index():
    return "Weather and Price Scraper API"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    start_year = data.get('start_year')
    start_month = data.get('start_month')
    end_year = data.get('end_year')
    end_month = data.get('end_month')

    if not all([start_year, start_month, end_year, end_month]):
        return jsonify({"error": "Missing required parameters"}), 400

    df, responses = loop_month_day(start_month, start_year, end_month, end_year)
    result = df.to_dict(orient='records')

    return jsonify({
        "data": result,
        "responses": responses
    })


@app.route('/scrape_bps', methods=['GET'])
def scrape_data():
    try:
        start_year = int(request.args.get('start_year'))
        end_year = int(request.args.get('end_year'))
        
        if start_year < bps_scraper.set_year or end_year > bps_scraper.current_year or start_year > end_year:
            return jsonify({'error': 'Invalid year range. Please ensure the range is within 2010 to current year.'}), 400
        
        data = bps_scraper.scrape_bps_prices(start_year, end_year)
        return data.to_json(orient='records'), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/download_csv', methods=['POST'])
def download_csv_endpoint():
    data = request.get_json()
    file_name = data.get('file_name')

    if not file_name:
        return jsonify({"error": "Missing 'file_name' parameter"}), 400

    csv_content = get_web(file_name)

    if csv_content:
        return jsonify({"csv_content": csv_content}), 200
    else:
        return jsonify({"error": "Failed to download file"}), 500

if __name__ == '__main__':
    app.run(debug=True)
