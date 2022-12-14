import tkinter as tk
from tkinter import ttk
import sys, os
import xml.dom.minidom as xr
import pandas as pd
import numpy as np
import geopandas as gpd
import rasterio as rio
from rasterio.plot import show
import shapely
from pyproj import _datadir, datadir
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
from PIL import Image



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('GS Topographic X-Section Tool v2.0')
        self.geometry('1000x800')

# Frame 1: Data Upload
        self.frame1 = tk.LabelFrame(self, text="Data Upload", width=450, height=400)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.frame1.grid_propagate(False)

        # Button: Select DEM
        self.upload_dem_button = ttk.Button(self.frame1, text='Select DEM', command=self.load_dem_path)
        self.upload_dem_button.grid(row = 0, column = 0, padx=10, pady=10,sticky="ew")

        # Entry: DEM path
        self.dem_path = ttk.Entry(self.frame1, width=45)
        self.dem_path.insert(0, "DEM Path")
        self.dem_path.grid(row = 0, column = 1, sticky="ew")

        # Scrollbar: DEM path
        self.scroll_dem_path = ttk.Scrollbar(self.frame1, orient='horizontal', command=self.dem_path.xview, )
        self.dem_path.config(xscrollcommand=self.scroll_dem_path.set)
        self.scroll_dem_path.grid(row = 1, column = 1, sticky='ew')

        # Button: Select X Section Lines
        self.upload_lines_button = ttk.Button(self.frame1, text='Select X-section Lines', command=self.load_line_path)
        self.upload_lines_button.grid(row = 2, column = 0, padx=10, pady=10,sticky="ew")

        # Entry: X Section Lines path
        self.lines_path = ttk.Entry(self.frame1, width=45)
        self.lines_path.insert(0, "X-section Lines Path")
        self.lines_path.grid(row = 2, column = 1, sticky="ew")

        # Scrollbar: X Section Lines path
        self.scroll_lines_path = ttk.Scrollbar(self.frame1, orient='horizontal', command=self.lines_path.xview, )
        self.lines_path.config(xscrollcommand=self.scroll_lines_path.set)
        self.scroll_lines_path.grid(row = 3, column = 1, sticky='ew')

        # Label: X Section Lines width
        self.line_width_label = ttk.Label(self.frame1, text="Line width (Map Units)")
        self.line_width_label.grid(row = 4, column = 0, padx=10, pady=10, sticky="ew")

        # Entry: X Section Lines width
        self.line_width_entry = ttk.Entry(self.frame1, width=10)
        self.line_width_entry.grid(row = 4, column = 1, sticky="w")

        # Button: Select Vertical MPs
        self.upload_vmps_button = ttk.Button(self.frame1, text='Select Vertical MPs', command=self.load_vmps_path)
        self.upload_vmps_button.grid(row = 5, column = 0, padx=10, pady=10,sticky="ew")

        # Entry: Vertical MPs path
        self.vmps_path = ttk.Entry(self.frame1, width=45)
        self.vmps_path.insert(0, "Vertical MPs Path")
        self.vmps_path.grid(row = 5, column = 1, sticky="ew")

        # Scrollbar: Vertical MPs path
        self.scroll_vmps_path = ttk.Scrollbar(self.frame1, orient='horizontal', command=self.vmps_path.xview, )
        self.vmps_path.config(xscrollcommand=self.scroll_vmps_path.set)
        self.scroll_vmps_path.grid(row = 6, column = 1, sticky='ew')

        # Button: Select Horizontal MPs
        self.upload_hmps_button = ttk.Button(self.frame1, text='Select East-West MPs', command=self.load_hmps_path)
        self.upload_hmps_button.grid(row = 7, column = 0, padx=10, pady=10,sticky="ew")

        # Entry: Horizontal MPs path
        self.hmps_path = ttk.Entry(self.frame1, width=45)
        self.hmps_path.insert(0, "Horizontal MPs Path")
        self.hmps_path.grid(row = 7, column = 1, sticky="ew")

        # Scrollbar: Horizontal MPs path
        self.scroll_hmps_path = ttk.Scrollbar(self.frame1, orient='horizontal', command=self.hmps_path.xview, )
        self.hmps_path.config(xscrollcommand=self.scroll_hmps_path.set)
        self.scroll_hmps_path.grid(row = 8, column = 1, sticky='ew')        

        # Button: Load Data 
        self.load_data_button = ttk.Button(self.frame1, text='Load Data', command=self.upload_data)
        self.load_data_button.grid(row = 9, column = 0, padx=10, pady=10,sticky="ew")

        # Button: Load Data 
        self.map_button = ttk.Button(self.frame1, text='Map Preview', command=self.plot_map)
        self.map_button.grid(row = 9, column = 1, padx=10, pady=10,sticky="ew")

        # # Progress bar: Upload
        # self.data_upload_pb = ttk.Progressbar(self.frame1, orient="horizontal", mode="indeterminate")
        # self.data_upload_pb.grid(row = 10, column = 0, columnspan=2, padx=10, pady=10,sticky="ew")

        # Label: Upload progress bar
        self.label_pb = ttk.Label(self.frame1)
        self.label_pb.grid(row = 10, column = 0, columnspan=2, padx=10)

        
    # Frame 3: Configure project
        self.frame2 = tk.LabelFrame(self, text="Configure Cross Section", width=450, height=300)
        self.frame2.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")
        self.frame2.grid_propagate(False)

        # Label: Vector Scale
        self.label_vec_scale = ttk.Label(self.frame2, text='Vector Scale')
        self.label_vec_scale.grid(row = 0, column = 0, padx=10, pady=10, sticky="w")

        # Entry: Vector Scale
        self.vec_scale_entry = ttk.Entry(self.frame2, width=10)
        self.vec_scale_entry.insert(0, "1.0")
        self.vec_scale_entry.grid(row = 0, column = 1,sticky="w")

        # Label: Vertical exaggeration
        self.label_vert_scale = ttk.Label(self.frame2, text='Vertical Exaggeration')
        self.label_vert_scale.grid(row = 1, column = 0, padx=10, pady=10, sticky="w")

        # Entry: Vertical exaggeration
        self.vert_scale_entry = ttk.Entry(self.frame2, width=10)
        self.vert_scale_entry.insert(0, "1.0")
        self.vert_scale_entry.grid(row = 1, column = 1,sticky="w")

        # Label: Arrow length
        self.label_arrow_length = ttk.Label(self.frame2, text='Arrow Length (mm)')
        self.label_arrow_length.grid(row = 2, column = 0, padx=10, pady=10, sticky="w")

        # Entry: Arrow length
        self.arrow_length_entry = ttk.Entry(self.frame2, width=10)
        self.arrow_length_entry.insert(0, "10.0")
        self.arrow_length_entry.grid(row = 2, column = 1,sticky="w")

        # Label: Y Limits
        self.label_y_lims = ttk.Label(self.frame2, text='Y min, Y max (m)')
        self.label_y_lims.grid(row = 3, column = 0, padx=10, pady=10, sticky="ew")

        # Entry: Y Limits Min
        self.y_min = ttk.Entry(self.frame2, )
        self.y_min.insert(0, "-100")
        self.y_min.grid(row = 3, column = 1,sticky="ew")     

        # Entry: Y Limits Max
        self.y_max = ttk.Entry(self.frame2,)
        self.y_max.insert(0, "100")
        self.y_max.grid(row = 3, column = 2,padx=10, pady=10,sticky="w")

        # Label: Select Start and End date
        self.label_date = ttk.Label(self.frame2, text="Cumulative displacement is calculated between two dates:")
        self.label_date.grid(row = 4, column = 0, columnspan=3, padx=10, pady=10, sticky="w")

        # Label: Select Start and End date
        self.label_date = ttk.Label(self.frame2, text="Start Date, End Date")
        self.label_date.grid(row = 5, column = 0, padx=10, pady=10, sticky="w")

        # Combobox: Select Start Date
        self.start_date_combo_text = tk.StringVar()
        self.start_date_combo = ttk.Combobox(self.frame2, textvariable=self.start_date_combo_text, state="readonly")
        self.start_date_combo.grid(row = 5, column = 1, sticky="ew")

        # Combobox: Select End Date
        self.end_date_combo_text = tk.StringVar()
        self.end_date_combo = ttk.Combobox(self.frame2, textvariable=self.end_date_combo_text, state="readonly")
        self.end_date_combo.grid(row = 5, column = 2, padx=10, pady=10, sticky="ew")

        # Label: Select x-section
        self.label_xsect = ttk.Label(self.frame2, text="X-section to plot")
        self.label_xsect.grid(row = 6, column = 0, padx=10, pady=10, sticky="w")

        # Combobox: Select Start Date
        self.xsect_combo_text = tk.StringVar()
        self.xsect_combo = ttk.Combobox(self.frame2, textvariable=self.xsect_combo_text, state="readonly")
        self.xsect_combo.grid(row = 6, column = 1, columnspan=2,padx=10, pady=10, sticky="ew")

        # Button: Plot x-section 
        self.plot_xsect_button = ttk.Button(self.frame2, text='Plot x-section', command=lambda: [self.create_xsection(), self.xsection()])
        self.plot_xsect_button.grid(row = 7, column = 0, columnspan=3, padx=10, pady=10,sticky="ew")

    # Frame 3: Cross Section Preview
        self.frame3 = tk.LabelFrame(self, text="Cross Section Preview", width=450, height=350)
        self.frame3.grid(row=1, column=0, columnspan=3, padx=20, sticky="nsew")
        self.frame3.grid_propagate(False)

        self.canvas_frame3 = tk.Canvas(self.frame3, width=450, height=350, highlightthickness=0)
        self.scrollbar_frame3 = ttk.Scrollbar(self, orient="vertical", command=self.canvas_frame3.yview)
        self.sub_frame3 = ttk.Frame(self.canvas_frame3, width=450, height=350)

        self.sub_frame3.bind(
            "<Configure>",
            lambda e: self.canvas_frame3.configure(
                scrollregion=self.canvas_frame3.bbox("all")
            )
        )

        self.canvas_frame3.create_window((0, 0), window=self.sub_frame3, anchor="n")

        self.canvas_frame3.configure(yscrollcommand=self.scrollbar_frame3.set)

        self.canvas_frame3.pack(side="right", fill="both", expand=True)
        self.scrollbar_frame3.grid(column=4, row=1, sticky="ns")


        # # Frame: Preview
        self.frame_preview = tk.Frame(self.sub_frame3, width=400, height=400)
        self.frame_preview.grid(row=0, column=0, padx=10, pady=10)

        

# Functions
    # Load DEM file
    def load_dem_path(self):
        fp = tk.filedialog.askopenfilename(
            title='Select DEM GeoTIFF',
            initialdir='/',
            filetypes=(('GeoTIFF Files', '*.tif'),))
        self.dem_path.delete(0, 'end')
        self.dem_path.insert(0, fp)
        return

    # Load X-section lines file
    def load_line_path(self):
        fp = tk.filedialog.askopenfilename(
            title='Select x-section line SHP',
            initialdir='/',
            filetypes=(('Shapefiles', '*.shp'),))
        self.lines_path.delete(0, 'end')
        self.lines_path.insert(0, fp)
        return

    # Load vertical MPs file
    def load_vmps_path(self):
        fp = tk.filedialog.askopenfilename(
            title='Select vertical MPs SHP',
            initialdir='/',
            filetypes=(('Shapefiles', '*.shp'),))
        self.vmps_path.delete(0, 'end')
        self.vmps_path.insert(0, fp)
        return

    # Load horizontal MPs file
    def load_hmps_path(self):
        fp = tk.filedialog.askopenfilename(
            title='Select east-west MPs SHP',
            initialdir='/',
            filetypes=(('Shapefiles', '*.shp'),))
        self.hmps_path.delete(0, 'end')
        self.hmps_path.insert(0, fp)
        return

    # Upload Data
    def upload_data(self):
        # Load the data sequentially
        # Load DEM
        self.label_pb["text"] = "Loading DEM ..."
        self.frame1.update_idletasks()
        self.dem = rio.open(self.dem_path.get()) # DEM object containing the data, CRS, and other useful attributes
        
        # Load x-section lines
        self.label_pb["text"] = "Loading x-section lines..."
        self.frame1.update_idletasks()
        self.xlines = gpd.read_file(self.lines_path.get())
        distance = float(self.line_width_entry.get())
        self.buffer_lines = self.xlines.buffer(distance=distance, cap_style=3)
        self.xsect_combo["values"] = self.xlines["Name"].to_list()

        # Load vertical MPs
        self.label_pb["text"] = "Loading vertical MPs ..."
        self.frame1.update_idletasks()
        self.vert = gpd.read_file(self.vmps_path.get()) # vertical MPs geopandas dataframe
        self.vert_transformed = self.vert.to_crs(self.xlines.crs)

        # Load horizontal MPs
        self.label_pb["text"] = "Loading horizontal MPs ..."
        self.frame1.update_idletasks()
        self.hori = gpd.read_file(self.hmps_path.get()) # horizontal MPs geopandas dataframe
        self.hori_transformed = self.hori.to_crs(self.xlines.crs)
        self.start_date_combo["values"] = [col for col in self.hori_transformed if col.startswith('D')] # populate start and end date dropdowns
        self.end_date_combo["values"] = self.start_date_combo["values"]
        
        self.label_pb["text"] = "Data loaded."
        
    
    def plot_map(self):
        self.mapWindow = tk.Toplevel(app)
        self.mapWindow.title("Map Preview")
        self.mapWindow.geometry("600x600")
        frame_map = tk.LabelFrame(self.mapWindow)
        frame_map.grid(row=0, column=0)
        distance = float(self.line_width_entry.get())
        self.buffer_lines = self.xlines.buffer(distance=distance, cap_style=3)
        fig_map, ax = plt.subplots(1,1)
        dem_ax = show(self.dem, ax=ax)
        self.vert_transformed.plot("VEL_V", vmin=-100, vmax=100, cmap="jet_r", markersize=4, ax=ax)
        self.buffer_lines.plot(ax=ax, color="blue", alpha=0.5)
        canvas_map = FigureCanvasTkAgg(fig_map, master = self.mapWindow)
        canvas_map.draw()
        canvas_map.get_tk_widget().grid(row = 0, column = 0, padx=10)
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas_map, self.mapWindow, pack_toolbar=False)
        toolbar.grid(row=1, column=0)


    def add_watermark(self, ax, fig):
        img = Image.open(resource_path("img\TREA-logo1_rgb_hi.png"))
        width, height = ax.figure.get_size_inches()*fig.dpi
        wm_width = int(width/25) # make the watermark 1/4 of the figure size
        scaling = (wm_width / float(img.size[0]))
        wm_height = int(float(img.size[1])*float(scaling))
        img = img.resize((wm_width, wm_height))

        imagebox = OffsetImage(img, zoom=1, alpha=0.4)
        imagebox.image.axes = ax

        ao = AnchoredOffsetbox(2, pad=0.5, borderpad=0, child=imagebox)
        ao.patch.set_alpha(0)
        ax.add_artist(ao)

    def create_xsection(self):
        res = np.min(self.dem.res) # DEM resolution

        mp_hd = []
        mp_vd = []
        mp_dist_along_profile = []
        mp_height_along_profile = []
        profile_distances = []
        profile_heights = []
        start_date = self.start_date_combo_text.get()
        end_date = self.end_date_combo_text.get()

        for prf, buff in zip(self.xlines["geometry"], self.buffer_lines): # for all x-section lines
            # Get angle coefficient of the line
            p0 = prf.boundary.geoms[0]
            p1 = prf.boundary.geoms[1]
            angle_coef = np.abs(np.sin(np.arctan2(p1.x - p0.x, p1.y - p0.y))) # Used to account for offset in angle from E-W

            # Get MPs within the buffer
            within = self.vert_transformed.within(buff) # Mask for MPs within buffer
            mp_h = self.hori_transformed[within==True] # Horizontal MPs within buffer
            mp_v = self.vert_transformed[within==True] # Vertical MPs within buffer

            # Get MP displacements
            d_h = (mp_h[end_date] - mp_h[start_date]) * angle_coef # Account for the angle of the profile when calculating displacement vector
            d_v = mp_v[end_date] - mp_v[start_date]
            mp_hd.append(d_h)
            mp_vd.append(d_v)

            # Project MPs onto the profile
            mp_coords = []
            mp_coords += [list(p.coords)[0] for p in mp_h["geometry"]]
            mp_dists = [prf.project(shapely.geometry.Point(p)) for p in mp_coords]
            mp_dist_along_profile.append(mp_dists)

            # Get height of projected MPs
            mp_projected_coords = [prf.interpolate(prf.project(shapely.geometry.Point(p))).coords[0] for p in mp_coords] # Coordinates of the projected MPs along the line
            mp_heights = np.array([x for x in self.dem.sample(mp_projected_coords)]).ravel()
            mp_height_along_profile.append(mp_heights)

            # Get height of the DEM surface
            s_dists = np.arange(0, prf.length, res/2) # Distances along the line with a sampling frequency adequate for the DEM resolution
            s_coords = [prf.interpolate(distance).coords[0] for distance in s_dists] # Coordinates for the DEM samples [prf.boundary.geoms[1].coords[0]]
            s_heights = np.array([x for x in self.dem.sample(s_coords)]).ravel()
            profile_distances.append(s_dists)
            profile_heights.append(s_heights)
        
        self.xlines["mp_hd"] = mp_hd
        self.xlines["mp_vd"] = mp_vd
        self.xlines["mp_dist_along_profile"] = mp_dist_along_profile
        self.xlines["mp_height_along_profile"] = mp_height_along_profile
        self.xlines["profile_distances"] = profile_distances
        self.xlines["profile_heights"] = profile_heights

    def xsection(self):
        self.xlines_select = self.xlines[self.xlines["Name"] == self.xsect_combo_text.get()]
        print(self.xlines_select)
        print(self.xlines_select["mp_dist_along_profile"].iloc[0])
        V = self.xlines_select["mp_vd"].iloc[0]
        U = self.xlines_select["mp_hd"].iloc[0]
        X = self.xlines_select["mp_dist_along_profile"].iloc[0]
        Y = self.xlines_select["mp_height_along_profile"].iloc[0]
        label = self.xlines_select["Name"]

        ymin = float(self.y_min.get())
        ymax = float(self.y_max.get())
        vert_scale = float(self.vert_scale_entry.get())
        vec_scale = float(self.vec_scale_entry.get())
        mm_scale = 1 / vec_scale # scale of the arrows in mm

        key_scale = float(self.arrow_length_entry.get()) # m, y units of DEM


        fig, ax = plt.subplots(figsize=(8,6))
        ax.plot(self.xlines_select["profile_distances"].iloc[0], self.xlines_select["profile_heights"].iloc[0])
        ax.set_title(self.xsect_combo_text.get())
        q = ax.quiver(X, Y, U, V, scale=mm_scale, scale_units="xy", angles="xy", width=0.002)
        ax.quiverkey(q, X=0.87, Y=1.05, U=key_scale,
                    label=str(key_scale)+' mm', labelpos='E')
        ax.set_aspect(vert_scale)
        ax.set_ylim([ymin, ymax])        

        self.add_watermark(ax, fig)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = self.frame_preview)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row = 6, column = 1, columnspan=2, padx = 5, pady = 5)

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    self.frame_preview, pack_toolbar=False)
        # toolbar.update()
        toolbar.grid(row = 7, column = 1, padx = 5, pady = 5)

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().grid(row = 6, column = 1, padx = 5, pady = 5)

if __name__ == "__main__":
  app = App()
  app.protocol("WM_DELETE_WINDOW", sys.exit)
  app.mainloop()
