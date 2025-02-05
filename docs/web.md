# Web Page

Molo Pipeline provides a Shiny-based online analysis platform that users can deploy locally to perform data analysis and visualize results through a web interface.

## Molo_web

You can use the **Molo_web** function to rapidly deploy this web interface locally for data analysis and result visualization. Below are parameter descriptions for Molo_web:

| Parameter Name |                     Function                      | Data Type |       Input Example/Optional Values       |
| :------------: | :-----------------------------------------------: | :-------: | :---------------------------------------: |
| molo_env_path  |     Specify the path to the Molo environment      | character | `molo_env_path = "/Anaconda3/envs/Molo/"` |
|   data_path    |           Specify the dataset directory           | character |          `data_path = "./data/"`          |
|   plot_path    | Specify the output path for visualization results | character |         `plot_path = "./plots/"`          |

> *Tip: All data must be stored in subfolders under data_path following <u>page instructions</u>. For example, 10X Visium data should be placed in data_path/visium. Data directly stored in data_path will NOT be recognized!*

## Web Page Installation

### **Install Shiny Server**:
   ```bash
sudo apt-get install shiny-server
   ```

### **Deploy Molo Pipeline Web App**:
   Copy the Web App folder to Shiny Server's application directory and restart the service:
   ```bash
sudo cp -r web_app /srv/shiny-server/
sudo systemctl restart shiny-server
   ```

## Running Pipeline via Web Page (10X Visium Example)

### **Access Local Webpage**:
   Open a browser and navigate to `http://localhost:3838/web_app`. The interface after loading will appear as follows:

   <img src="./web_1.png" width="100%"/>

   You can either (1) open the scRNA-seq Analyse menu and click 10X Visium (indicated by the blue arrow), or (1) directly click Analyse Directly to jump to 10X Visium analysis (indicated by the green arrow).

### **Configure Parameters**:
   After opening the analysis, follow the sidebar instructions to (1) place data files, (2) set parameters, then click (3) RUN to start analysis:

   <img src="./web_2.png" width="100%"/>

### **Execute Molo Pipeline**:
   After clicking RUN, confirm execution as prompted. Do not perform any operations or close the webpage during execution to avoid unexpected errors. The runtime depends on your server performance and dataset size. Upon completion, results will display on the right. You can (1) collapse the sidebar and (2) select analysis results from the menu:

   <img src="./web_3.png" width="100%"/>

   > *Tip: If a plot shows "Waiting for Analysis", it indicates no valid results were generated. Please verify your data for exploratory analysis or retry with adjusted parameters.*
