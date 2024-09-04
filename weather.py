from flask import Flask, render_template, request
import json
import urllib.parse
import urllib.request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def weather():
    lat = ''
    lon = ''
    if request.method == 'POST':
        lat = request.form['lat']
        lon = request.form['lon']
        
        if not lat or not lon:
            return render_template("windex.html", data={"error": "Please enter both latitude and longitude."})

        try:
            api_key = '2c5dd26bb1829a93ca364cbb2c6d3ffa'
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            url = f"{base_url}?lat={lat}&lon={lon}&appid={api_key}"
            print(f"Requesting URL: {url}")
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            data = {
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp']}k",
                "temp_cel": f"{list_of_data['main']['temp'] - 273.15:.2f}°C",
                "country": f"{list_of_data['sys']['country']}",
                "weather": f"{list_of_data['weather'][0]['main']}"
            }

            return render_template('windex.html', data=data)
        
        except urllib.error.HTTPError as e:
            print("Error occured due to the urlLib error")
            return render_template("windex.html", data={"error": f"HTTP Error: {e.code}. Please check your input or try again later."})
        except Exception as e:
            print("Error occured")
            return render_template("windex.html", data={"error": f"An error occurred: {str(e)}"}) 


    else:
        return render_template("windex.html", data={})

if __name__ == '__main__':
    app.run(debug=True)
