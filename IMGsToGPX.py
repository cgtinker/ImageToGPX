#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import gpxpy
import gpxpy.gpx as g
import exifread
import os
import time

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Based on https://gist.github.com/erans/983821
def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon

# Adding a Waypoint to the GPXFile
def AddWaypoint(label, lat, long, desc):
    # Creating WP
    wp = g.GPXWaypoint()
    # WP Data
    wp.name = label
    wp.latitude = lat
    wp.longitude = long
    wp.description = desc
    # Append WP
    gpx.waypoints.append(wp)

# Saving GPX
def Export_File():
    # Printing generated GPX_XML contents
    contents = gpx.to_xml()
    print('Created GPX:', contents)
    messagebox.showinfo("Information", "Successfully created a GPX File! Choose an output directory.")

    # asks user to choose a directory
    dir_name = filedialog.askdirectory(title="Please select an output folder.")

    if(dir_name):
        os.chdir(dir_name) # changes your current directory
        #generating new text file
        name = time.strftime("%Y-%m-%d_%H-%M-%S") + ".gpx"
        text_file = open(name, "w")
        n = text_file.write(contents)
        text_file.close()
    else:
        messagebox.showinfo("Session Cancelled","Cancelled Saving Process")


#open multiple files
root = tk.Tk()
root.withdraw()
f_paths = filedialog.askopenfilenames(title='Select Image Files with Location Information')

# Creating new GPXFile
gpx = g.GPX()
gpx.name = 'NewGPX'

if(f_paths):
    for path in f_paths:
        # Current File
        fileName = os.path.basename(path)
        print(fileName)

        # Open image file for reading (binary mode)
        file = open(path, 'rb')
        exif_data = exifread.process_file(file)

        # getting the latitude and longitude of the current file
        lat, long = get_exif_location(exif_data)
        print('lat: ' , lat, 'long ', long)

        # Adding Waypon to GPX
        if lat is not None:
            AddWaypoint(fileName, lat, long, "description")

    # Exporting the GPX
    Export_File()


else:
    messagebox.showinfo("Session Cancelled","No image files selected.")
