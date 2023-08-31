# map_rz_npc.py
# Create a colored image map representing non-ponded-crop data
# Copyright (C) 2023 University of California
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------



def map_rz_npc(dataset, min_x, max_x, min_y, max_y, max_value, image_name):
    """map_rz() - Create a colored image map representing non-ponded-crop data.

    Parameters
    ----------
    dataset : list of tuples
        A list containing tuples of three values (x, y, value), representing the x and y coordinates of each
        data point along with their corresponding values.

    min_x : float
        The minimum x coordinate of the dataset.

    max_x : float
        The maximum x coordinate of the dataset.

    min_y : float
        The minimum y coordinate of the dataset.

    max_y : float
        The maximum y coordinate of the dataset.

    max_value : float
        The maximum value in the dataset, used for color mapping.

    image_name : str
        The desired name of the image file to be saved.

    Returns
    -------
    nothing
    """
    import iwfm.plot as iplot
    from PIL import Image, ImageDraw

    # Calculate the range of x and y values
    range_x = max_x - min_x
    range_y = max_y - min_y
   
    # Determine the size of the image (you can adjust this based on your data range)
    scaling_factor = 0.01  # You can adjust this value as needed

    # Create a new image with a white background for the main plot
    image_width = int(range_x * scaling_factor) + 200
    image_height = int(range_y * scaling_factor) + 200
    image = Image.new('RGB', (image_width, image_height), color='white')

    # Create a drawing context for the main plot
    draw = ImageDraw.Draw(image)

    # Scale the coordinates to fit within the image size
    scale_x = lambda x: int((x - min_x) * scaling_factor) + 100
    scale_y = lambda y: int((y - min_y) * scaling_factor) + 100


    # Draw polygons around each data point
    for x, y, value in dataset:
        norm_value = (value - min_value) / (max_value - min_value)
        color = iplot.data_to_color(norm_value * (max_value - min_value) + min_value, min_value, max_value)
        scaled_x = scale_x(x)
        scaled_y = scale_y(y)

        # Define the vertices of the polygon
        vertices = [
            (scaled_x - 50, scaled_y),
            (scaled_x, scaled_y - 50),
            (scaled_x + 50, scaled_y),
            (scaled_x, scaled_y + 50)
        ]

        # Draw the polygon
        draw.polygon(vertices, fill=color, outline=color)

    # Save the image
    image.save(image_name)

    print(f"Image of non-ponded crop data saved to {image_name}")



if __name__ == "__main__":
    import iwfm as iwfm
    import iwfm.plot as iplot

    #  Read IWFM nodes.dat file for node (x,y) values
    node_file = "C2VSimCG_Nodes.dat"
    dataset, _ = iwfm.iwfm_read_nodes(node_file, 0.0)
 

    rz_npc_file = "C2VSimCG_NonPondedCrop.dat"
    crops = ["gr", "co", "sb", "cn", "db", "sa", "fl", "al", "pa", "tp", "tf", "cu", "og", "po", "tr", "ap", "or", "cs", "vi", "id"]
    
    #  Choose parameter and layer to graph
    crop = 0

    #  Set image file name
    image_name = f"rz_map_npc_{crops[crop]}.png"
    
    #  Read all relevant values from NonPondedCrop.dat
    values = iwfm.iwfm_read_rz_npc(rz_npc_file)

    #  Add node's value to each coordinate pair
    dataset = dataset[:-1]

    i = 1
    for data in dataset:
        data.append(values[crop][i])
        i += 1

    #  Find min and max values
    min_x, min_y, min_value = iplot.get_mins(dataset)
    max_x, max_y, max_value = iplot.get_maxs(dataset)

    #  Produce map
    map_rz_npc(dataset, min_x, max_x, min_y, max_y, max_value, image_name)

    