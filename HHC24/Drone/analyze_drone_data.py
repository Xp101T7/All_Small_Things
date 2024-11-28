import pandas as pd

def create_enhanced_kml(data, output_filename='drone_flight.kml'):
    try:
        # Extract valid GPS coordinates and relevant data
        required_columns = ['OSD.latitude', 'OSD.longitude', 'OSD.height [ft]', 
                          'BATTERY.chargeLevel [%]', 'OSD.hSpeedMax [MPH]', 'OSD.flyTime [s]']
        coordinates = data[required_columns].dropna()
        
        if coordinates.empty:
            print("No valid GPS data available to create KML.")
            return
        
        # Create KML content
        kml_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<kml xmlns="http://www.opengis.net/kml/2.2">',
            '<Document>',
            '  <name>Enhanced Drone Flight Data</name>',
            
            # First create the flight path
            '  <Placemark>',
            '    <name>Flight Path</name>',
            '    <LineString>',
            '      <extrude>1</extrude>',
            '      <altitudeMode>relativeToGround</altitudeMode>',
            '      <coordinates>'
        ]
        
        # Add path coordinates
        coord_lines = []
        for _, row in coordinates.iterrows():
            altitude_meters = row['OSD.height [ft]'] * 0.3048
            coord_lines.append(f'{row["OSD.longitude"]},{row["OSD.latitude"]},{altitude_meters}')
        
        kml_content.append('        ' + ' '.join(coord_lines))
        
        # Close flight path placemark
        kml_content.extend([
            '      </coordinates>',
            '    </LineString>',
            '  </Placemark>'
        ])
        
        # Add enhanced data points (every 10th point to avoid overcrowding)
        point_interval = 10
        for i, row in coordinates.iterrows():
            if i % point_interval == 0:
                altitude_meters = row['OSD.height [ft]'] * 0.3048
                battery_level = row['BATTERY.chargeLevel [%]']
                speed = row['OSD.hSpeedMax [MPH]']
                flight_time = row['OSD.flyTime [s]']
                
                # Create enhanced placemark for this point
                kml_content.extend([
                    '  <Placemark>',
                    f'    <name>Data Point {i}</name>',
                    '    <description><![CDATA[',
                    '      <div style="font-family: Arial, sans-serif;">',
                    '        <h3>Flight Data</h3>',
                    '        <table style="width:300px; border-collapse: collapse;">',
                    '          <tr style="background-color: #f2f2f2;">',
                    '            <td style="padding: 8px;"><b>Altitude:</b></td>',
                    f'            <td style="padding: 8px;">{row["OSD.height [ft]"]:.1f} ft</td>',
                    '          </tr>',
                    '          <tr>',
                    '            <td style="padding: 8px;"><b>Battery Level:</b></td>',
                    f'            <td style="padding: 8px;">{battery_level:.1f}%</td>',
                    '          </tr>',
                    '          <tr style="background-color: #f2f2f2;">',
                    '            <td style="padding: 8px;"><b>Speed:</b></td>',
                    f'            <td style="padding: 8px;">{speed:.1f} MPH</td>',
                    '          </tr>',
                    '          <tr>',
                    '            <td style="padding: 8px;"><b>Flight Time:</b></td>',
                    f'            <td style="padding: 8px;">{flight_time:.1f} s</td>',
                    '          </tr>',
                    '        </table>',
                    '      </div>',
                    '    ]]></description>',
                    '    <LookAt>',
                    f'      <longitude>{row["OSD.longitude"]}</longitude>',
                    f'      <latitude>{row["OSD.latitude"]}</latitude>',
                    f'      <altitude>{altitude_meters}</altitude>',
                    '      <heading>0</heading>',
                    '      <tilt>45</tilt>',
                    '      <range>100</range>',
                    '    </LookAt>',
                    '    <Point>',
                    f'      <coordinates>{row["OSD.longitude"]},{row["OSD.latitude"]},{altitude_meters}</coordinates>',
                    '    </Point>',
                    '  </Placemark>'
                ])
        
        # Close main KML tags
        kml_content.extend([
            '</Document>',
            '</kml>'
        ])
        
        # Write to file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(kml_content))
            
        print(f"Enhanced flight path KML saved as '{output_filename}'")
        
    except Exception as e:
        print(f"Error creating KML file: {str(e)}")

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
    
    # Create enhanced KML
    create_enhanced_kml(df)
    
except Exception as e:
    print(f"Error in main execution: {str(e)}")