import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
def get_airport_coordinates(airport_code):
  geolocator=Nominatim(user_agent="airport_distance_calculator")
  try:
    loc=geolocator.geocode(f"{airport_code} airport")
    if loc:
      return(loc.latitude,loc.longitude)
    else:
      return None
  except:
    return None
def get_airport_country(airport_code):
  geolocator=Nominatim(user_agent="airport_country_checker")
  try:
    location=geolocator.geocode(f"{airport_code} airport")
    if location:
      address=location.raw.get('display_name','')
      return address.split(",")[-1].strip()
    else:
      return None
  except:
    return None
def calculate_distance(airport_code1, airport_code2):
  coords1=get_airport_coordinates(airport_code1)
  coords2=get_airport_coordinates(airport_code2)
  if coords1 and coords2:
    distance=geodesic(coords1, coords2).kilometers
    st.write("Distance:",round(distance),'km')
    return distance
def check_same_country(airport_code1, airport_code2):
  country1=get_airport_country(airport_code1)
  country2=get_airport_country(airport_code2)
  return (country1 and country2) and country1==country2
st.header("Carbon Emission Transshipment")
"Carbon emission calculator for 3 ports"
choice=st.text_input("Enter mode 1 for sea and 0 for air(Default)")
if choice=='1':
  st.write("Current mode: sea")
  lst=[st.text_input("Latitude 1 (-90 to 90): "),st.text_input("Longitude 1 (-180 to 180):"),st.text_input("Latitude 2 (-90 to 90) (Intermediate):"),st.text_input("Longitude 2 (-180 to 180) (Intermediate): "),st.text_input("Latitude 3 (-90 to 90): "),st.text_input("Longitude 3 (-180 to 180):")]
  if all(lst):
    lst=[float(i)for i in lst]
    orig=lst[:2][::-1]
    intr=lst[2:4][::-1]
    dest=lst[4:][::-1]
    route1=sr.searoute(orig,intr)
    dist1=route1.properties['length']
    st.write("The distance of the first part of the journey is",round(dist1),"km"
    route2=sr.searoute(intr,end)
    dist2=route2.properties['length']
    st.write("The distance of the second part of the journey is",round(dist1),"km"
    dist=dist1+dist2
    st.write("The total distance is",dist,"km")
    
    
