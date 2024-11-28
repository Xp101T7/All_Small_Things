import pandas as pd
import folium
from folium import plugins

def create_enhanced_map(data, output_filename='drone_flight.html'):
    try:
        # Extract valid GPS coordinates and relevant data
        required_columns = ['OSD.latitude', 'OSD.longitude', 'OSD.height [ft]', 
                          'BATTERY.chargeLevel [%]', 'OSD.hSpeedMax [MPH]', 'OSD.flyTime [s]']
        coordinates = data[required_columns].dropna()
        
        if coordinates.empty:
            print("No valid GPS data available to create map.")
            return

        # Get center point for map
        center_lat = coordinates['OSD.latitude'].mean()
        center_lon = coordinates['OSD.longitude'].mean()

        # Create the map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

        # Create the flight path line
        path_coordinates = coordinates[['OSD.latitude', 'OSD.longitude']].values.tolist()
        folium.PolyLine(
            path_coordinates,
            weight=3,
            color='blue',
            opacity=0.8
        ).add_to(m)

        # Add markers with enhanced data points (every 10th point to avoid overcrowding)
        point_interval = 10
        for i, row in coordinates.iterrows():
            if i % point_interval == 0:
                # Create formatted popup content
                popup_html = f"""
                <div style="font-family: Arial, sans-serif; min-width: 180px;">
                    <h4 style="margin-bottom: 10px;">Flight Data Point {i}</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #f2f2f2;">
                            <td style="padding: 5px;"><b>Altitude:</b></td>
                            <td style="padding: 5px;">{row['OSD.height [ft]']:.1f} ft</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px;"><b>Battery:</b></td>
                            <td style="padding: 5px;">{row['BATTERY.chargeLevel [%]']:.1f}%</td>
                        </tr>
                        <tr style="background-color: #f2f2f2;">
                            <td style="padding: 5px;"><b>Speed:</b></td>
                            <td style="padding: 5px;">{row['OSD.hSpeedMax [MPH]']:.1f} MPH</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px;"><b>Flight Time:</b></td>
                            <td style="padding: 5px;">{row['OSD.flyTime [s]']:.1f} s</td>
                        </tr>
                    </table>
                </div>
                """

                # Create marker with popup
                folium.CircleMarker(
                    location=[row['OSD.latitude'], row['OSD.longitude']],
                    radius=6,
                    color='red',
                    fill=True,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"Data Point {i}"
                ).add_to(m)

        # Add start and end markers
        # Start point (green)
        first_row = coordinates.iloc[0]
        folium.Marker(
            [first_row['OSD.latitude'], first_row['OSD.longitude']],
            popup='Start',
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

        # End point (red)
        last_row = coordinates.iloc[-1]
        folium.Marker(
            [last_row['OSD.latitude'], last_row['OSD.longitude']],
            popup='End',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Add a minimap
        minimap = plugins.MiniMap()
        m.add_child(minimap)

        # Add fullscreen option
        plugins.Fullscreen().add_to(m)

        # Add mouse position
        plugins.MousePosition().add_to(m)

        # Add a measure control
        plugins.MeasureControl(position='topleft').add_to(m)

        # Save the map
        m.save(output_filename)
        print(f"Enhanced flight map saved as '{output_filename}'")
        
    except Exception as e:
        print(f"Error creating map: {str(e)}")

# Main execution
try:
    # Load data
    file_path = r"C:\Users\hecki\Prog\All_Small_Things\HHC24\Drone\filtered_data.csv"
    df = pd.read_csv(file_path)
    
    # Clean data
    df = df.replace(['NULL', 'N/A', '', ' '], None)
    
    # Convert numeric columns
    numeric_cols = ['OSD.height [ft]', 'OSD.hSpeedMax [MPH]', 'OSD.flyTime [s]', 
                   'BATTERY.chargeLevel [%]', 'OSD.latitude', 'OSD.longitude']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Create enhanced map
    create_enhanced_map(df)
    
except Exception as e:
    print(f"Error in main execution: {str(e)}")