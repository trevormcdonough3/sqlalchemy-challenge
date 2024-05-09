## Flask and our App setup
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

# Creating the session
session = Session(engine)
app = Flask(__name__)

# Defining routes with some descriptions of the routes 
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App! By Trevor McDonough<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Precipitation Data for the Last 12 months<br/>"
        f"/api/v1.0/stations - List of Stations<br/>"
        f"/api/v1.0/tobs -Most Active station Temp in the last 12 Months<br/>"
        f"/api/v1.0/<start> - Min, Avg, and Max Temp for the Start Date<br/>"
        f"/api/v1.0/<start>/<end> - Min, Avg, and Max Tempe for the End Date"
    )

# Looking at the previous 12 month precipitation data 
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= '2016-08-23').all()
    prcp_dict = {date: prcp for date, prcp in prcp_data}
    return jsonify(prcp_dict)

# Listing all the stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(station.station, station.name).all()
    stations_list = [{"Station": station, "Name": name} for station, name in stations_data]
    return jsonify(stations_list)

# Getting the temperature for the most active station we found in the other file
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= '2016-08-23').all()
    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)

# Getting the summary statistics for a certain start date
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    session = Session(engine)
    start_date = datetime.strptime(start, '%Y-%m-%d')
    temperature_stats = session.query(func.min(measurement.tobs).label('min_temperature'),func.avg(measurement.tobs).label('avg_temperature'),func.max(measurement.tobs).label('max_temperature')).filter(measurement.date >= start_date).all()
    session.close()
    min_temp, avg_temp, max_temp = temperature_stats[0]
    return jsonify({"min_temperature": min_temp, "avg_temperature": avg_temp, "max_temperature": max_temp})

# Doing the same as above with a start and end date
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_start_end(start, end):
    session = Session(engine)
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    temperature_stats = session.query(func.min(measurement.tobs).label('min_temperature'),func.avg(measurement.tobs).label('avg_temperature'),func.max(measurement.tobs).label('max_temperature')).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()
    min_temp, avg_temp, max_temp = temperature_stats[0]
    return jsonify({"min_temperature": min_temp, "avg_temperature": avg_temp, "max_temperature": max_temp})

# Now we run the app
if __name__ == "__main__":
    app.run(debug=True)
