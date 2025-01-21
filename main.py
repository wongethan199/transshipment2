import streamlit as st
import pandas
import csv
pandas.set_option('display.max_rows', None)
x=pandas.read_csv("https://raw.githubusercontent.com/wongethan199/carbon_emission_1/refs/heads/main/ESG%20-%20Data%20sheet%20air%20freight%20shipping%20hubs.xlsx%20-%20Main%20-%20Air%20shipping.csv")#distance
ef=pandas.read_csv("https://raw.githubusercontent.com/wongethan199/carbon_emission_1/refs/heads/main/ESG%20-%20Data%20sheet%20air%20freight%20shipping%20hubs.xlsx%20-%20Sheet1.csv")
w=pandas.read_csv("https://raw.githubusercontent.com/wongethan199/carbon_emission_1/refs/heads/main/aircraft%20weight.csv")
import searoute as sr
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
def coord(airport_code):
  geolocator=Nominatim(user_agent="airport_distance_calculator")
  try:
    loc=geolocator.geocode(f"{airport_code} airport")
    if loc:
      return(loc.latitude,loc.longitude)
    else:
      return None
  except:
    return None
def ctry(airport_code):
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
  coords1=coord(airport_code1)
  coords2=coord(airport_code2)
  if coords1 and coords2:
    distance=geodesic(coords1, coords2).kilometers
    st.write("Distance:",round(distance),'km')
    return distance
def check_same_country(airport_code1, airport_code2):
  country1=ctry(airport_code1)
  country2=ctry(airport_code2)
  return (country1 and country2) and country1==country2
st.header("Carbon Emission Transshipment")
"Carbon emission calculator for 3 ports, all air or all sea for now"
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
    st.write("The distance of the first part of the journey is",round(dist1),"km")
    route2=sr.searoute(intr,dest)
    dist2=route2.properties['length']
    st.write("The distance of the second part of the journey is",round(dist2),"km")
    distance=dist1+dist2
    st.write("The total distance is",round(distance),"km")
    try:
      teu=float(st.text_input("Enter TEU capacity:"))
    except:
      teu=24000
    try:
      percent=float(st.text_input("Enter % of teu capacity: Default 70:"))
    except:
      percent=70
    percent=min(100,percent)
    if teu<1000:
      ef2=0.0363
    elif teu<2000:
      ef2=0.0321
    elif teu<3000:
      ef2=0.0200
    elif teu<8000:
      ef2=0.0167
    else:
      ef2=0.0125
    try:
      ref_teu=int(st.text_input("Enter refrigerated plug capacity, default 800:"))
    except:
      ref_teu=800
    ref_teu=min(ref_teu,teu)
    weight=teu*24000*percent/100 
    st.write("weight of cargo ship is",int(weight),"kg")
    st.markdown(":red[Warning: Only fill one of the below 2]")
    speed=st.text_input("Enter speed in knots")
    days=st.text_input("enter expected number of days")
    if speed and days:
      st.write("You entered both speed and days")
    elif speed:
      speed=float(speed)
      days=distance/(speed*1.852)/24
      st.write('Days',days)
      ref_consum=ref_teu*0.75*days*24
      st.write("Refrigerator fuel consumption",round(ref_consum*0.9,2),'kg')
      co2=weight*distance*ef2*(speed/21)**2/1000+ref_consum*3.15
      st.write("CO2 Emission:",round(co2,1),"kg")
      st.write("CO2 Emission to load ratio:",co2/weight)
      st.write("CO2 Emission to load ratio per km:",co2/weight/distance)
      co2/=1000
      st.write("This is equivalent to:",round(co2*370.37,1),"kg of rice,",round(co2*16.67,2),"kg of beef,",round(co2*833.33,1),"liters of milk, or",round(co2*0.8,4),"hectares of cropland of fertilizer")
      st.write("Also equivalent to:",round(co2/4.6,3),"years of carbon footprint for an average car,",round(co2/1.5,3),"flights of 10000km, or the average carbon footprint of",round(co2/4.8),"people in a year")
      dry_intensity=ef2/126.85*(speed/21)**2/teu/(percent/100)*1000000
      st.write("Dry Container Emission Intensity:",dry_intensity)
      ref_intensity=dry_intensity+ef2*ref_consum/distance/(percent/100)/ref_teu/1.9
      st.write("Refrigerated Container Emission Intensity",ref_intensity)
    elif days:
      days=float(days)
      speed=distance/(days*24)/1.852
      st.write("Speed",speed,"knots")
      ref_consum=ref_teu*0.75*days*24
      st.write("Refrigerator fuel consumption",round(ref_consum*0.9,2),'kg')
      co2=weight*distance*ef2*(speed/21)**2/1000+ref_consum*3.15
      st.write("CO2 Emission:",round(co2,1),"kg")
      st.write("CO2 Emission to load ratio:",co2/weight)
      st.write("CO2 Emission to load ratio per km:",co2/weight/distance)
      co2/=1000
      st.write("This is equivalent to:",round(co2*370.37,1),"kg of rice,",round(co2*16.67,2),"kg of beef,",round(co2*833.33,1),"liters of milk, or",round(co2*0.8,4),"hectares of cropland of fertilizer")
      st.write("Also equivalent to:",round(co2/4.6,3),"years of carbon footprint for an average car,",round(co2/1.5,3),"flights of 10000km, or the average carbon footprint of",round(co2/4.8),"people in a year")
      dry_intensity=ef2/126.85*(speed/21)**2/teu/(percent/100)*1000000
      st.write("Dry Container Emission Intensity:",dry_intensity)
      ref_intensity=dry_intensity+ef2*ref_consum/distance/(percent/100)/ref_teu/1.9
      st.write("Refrigerated Container Emission Intensity",ref_intensity)
else:
  st.write("Current mode: Air")
  airports0=x[x.columns[2]].values.tolist()
  airports0=[str(i[-4:-1]) for i in airports0]
  airports1=x[x.columns[4]].values.tolist()
  airports1=[str(i[-4:-1]) for i in airports1]
  x["Codes_Starting"]=airports0
  x["Codes_Ending"]=airports1
  code1=st.text_input("Enter port code 1:").strip().upper()
  code2=st.text_input("Enter port code 2: (Intermediate)").strip().upper()
  code3=st.text_input("Enter port code 3:").strip().upper()
  aircraft=st.text_input("Enter the aircraft, please enter the company name e.g. Airbus A340-500, Antonov An-225, Boeing 747-400")
  if aircraft:
    aircraft1=w[w["Type"].str.lower()==aircraft.lower().strip()]
    if aircraft1.empty:
      st.write("No aircraft found")
    else:
      percent=st.text_input("enter % of maximum takeoff weight (Minimum 40)")
      if percent:
        speed=st.text_input("enter % of max speed")
        if speed:
          speed=min(100,float(speed))
          percent=max(min(float(percent),100),40)
          weight=aircraft1.iloc[0][1]*percent/100
          st.write("the weight of the aircraft is",round(weight,1),"kg")
  if code1 and code2 and code3:
    try:
      st.write("First part of journey:")
      target=x[((x["Codes_Starting"]==code1)&(x["Codes_Ending"]==code2))|((x["Codes_Ending"]==code1)&(x["Codes_Starting"]==code2))]
      if target.empty:
        distance=calculate_distance(code1,code2)
        if check_same_country(code1,code2):
          ef1=ef.iloc[0][5]#domestic
        elif distance<3700:
          ef1=ef.iloc[1][5]#short haul
        else:ef1=ef.iloc[2][5]#long haul
      else:
        distance=target.iloc[0][5]
        st.write("Distance:",distance,"km")
        if target.iloc[0][1]==target.iloc[0][3]:
          ef1=ef.iloc[0][5]#domestic
        elif distance<3700:
          ef1=ef.iloc[1][5]#short haul
        else:ef1=ef.iloc[2][5]#long haul
      co2=weight*distance*ef1*(speed/100)**2/1000
      st.write("Emission:",round(co2,1),"kg")
    except:
      st.write("Timed out for part 1, please try again")
    try:
      st.write("Second part of journey:")
      target=x[((x["Codes_Starting"]==code3)&(x["Codes_Ending"]==code2))|((x["Codes_Ending"]==code3)&(x["Codes_Starting"]==code2))]
      if target.empty:
        distance1=calculate_distance(code3,code2)
        if check_same_country(code3,code2):
          ef2=ef.iloc[0][5]#domestic
        elif distance1<3700:
          ef2=ef.iloc[1][5]#short haul
        else:ef2=ef.iloc[2][5]#long haul
      else:
        distance1=target.iloc[0][5]
        st.write("Distance:",distance1,"km")
        if target.iloc[0][1]==target.iloc[0][3]:
          ef2=ef.iloc[0][5]#domestic
        elif distance1<3700:
          ef2=ef.iloc[1][5]#short haul
        else:ef2=ef.iloc[2][5]#long haul
      Co2=weight*distance1*ef2*(speed/100)**2/1000
      st.write("Emission:",round(Co2,1),"kg")
    except:
      st.write("Timed out for part 2, please try again")
    try:
      st.write("Entire journey:")
      st.write("Distance:",round(distance1+distance),"km")
      tot=Co2+co2
      st.write("CO2 Emission:",round(tot,1),"kg")
      st.write("CO2 Emission to load ratio:",tot/weight)
      st.write("CO2 Emission to load ratio per km:",tot/weight/(distance+distance1))
      tot/=1000
      st.write("This is equivalent to:",round(tot*370.37,1),"kg of rice,",round(tot*16.67,2),"kg of beef,",round(tot*833.33,1),"liters of milk, or",round(tot*0.8,4),"hectares of cropland of fertilizer")
      st.write("Also equivalent to:",round(tot/4.6,3),"years of carbon footprint for an average car,",round(tot/1.5,3),"flights of 10000km, or the average carbon footprint of",round(tot/4.8),"people in a year")
    except:
      st.write("Unable to calculate because of timeout")
