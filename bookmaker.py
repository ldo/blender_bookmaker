#+
# Blender add-on script to generate a random row of books.
#-

import sys
import math
import random
import colorsys
import bpy
from mathutils import \
    Matrix, \
    Vector

bl_info = \
    {
        "name" : "Bookmaker",
        "author" : "Lawrence D'Oliveiro <ldo@geek-central.gen.nz>",
        "version" : (0, 6, 0),
        "blender" : (2, 7, 9),
        "location" : "Add > Mesh > Books",
        "description" :
            "generates a row of book objects with randomly-distributed parameters.",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Add Mesh",
    }

#+
# Useful stuff
#-

deg = math.pi / 180

class Failure(Exception) :

    def __init__(self, msg) :
        self.msg = msg
    #end __init__

#end Failure

#+
# Book mesh and materials
#-

book_mesh = \
    {
        "vertices" :
          [
            (0.06460488, 0.129904, 0.1982849),
            (0.06526268, 0, 0.198523),
            (0, 0, 0.198523),
            (-0.000395142, 0.1299042, 0.1982849),
            (0.06460488, 0.129904, 0.201535),
            (0.009671181, -0.001442945, 0.198523),
            (-0.000395142, 0.1299042, 0.201535),
            (0.06460488, 0.133154, 0.201535),
            (-0.000395142, 0.133154, 0.201535),
            (-0.0004412518, 0.006495208, 2.624452e-05),
            (0.0005205204, 0.004330136, 1.749635e-05),
            (0, 0.002165068, 8.748175e-06),
            (0.06460488, 0.133154, 0.1982849),
            (-0.000395142, 0.133154, 0.1982849),
            (0.06526268, 0.002165068, 8.748175e-06),
            (0.06439215, 0.004330136, 1.748861e-05),
            (0.06463331, 0.006495208, 2.623678e-05),
            (0.06135488, 0.129904, 0.201535),
            (0.06135482, 0.005415067, 0.201535),
            (0.06135488, 0.133154, 0.201535),
            (-6.585539e-05, 0.002165068, 0.003086619),
            (0.0005205204, 0.004330136, 0.00312629),
            (0.06135488, 0.133154, 0.1982849),
            (0.06526268, 0.002165068, 0.003086619),
            (0.002854846, 0.005415067, 0.201535),
            (0.002854858, 0.1299042, 0.201535),
            (0.002854858, 0.133154, 0.201535),
            (0.06439215, 0.004330132, 0.00312629),
            (0.06493378, 0.006495208, 0.003165964),
            (0.002854858, 0.133154, 0.1982849),
            (-0.0001975701, 0.006495208, 0.003165964),
            (0.04345435, -0.005715966, 0.003046945),
            (0.03289026, -0.006876484, 0.003046945),
            (0.02084944, -0.005181804, 0.003046945),
            (0.05393749, -0.002041858, 0.198523),
            (0.04345435, -0.005715966, 0.198523),
            (0.03289026, -0.006876484, 0.198523),
            (0.02084944, -0.005181804, 0.198523),
            (0.05393749, -0.002041858, 0.003046945),
            (0.002854858, 0.133154, 0.003284983),
            (0.002854858, 0.133154, 3.498496e-05),
            (0.002854858, 0.1299042, 3.498496e-05),
            (-0.0001975701, 0.006495208, 0.1984041),
            (0.002854846, 0.005415067, 3.498496e-05),
            (0.06493378, 0.006495208, 0.1984041),
            (0.06135488, 0.133154, 0.003284983),
            (0.06135488, 0.133154, 3.498496e-05),
            (0.06439215, 0.004330132, 0.1984437),
            (0.06526268, 0.002165068, 0.1984832),
            (0.06135482, 0.005415067, 3.498496e-05),
            (0.06135488, 0.129904, 3.498496e-05),
            (0.0005205204, 0.004330136, 0.1984437),
            (-6.585539e-05, 0.002165068, 0.1984832),
            (0.06463331, 0.006495208, 0.2015438),
            (0.06439215, 0.004330136, 0.2015524),
            (0.06526268, 0.002165068, 0.2015612),
            (0, 0.002165068, 0.2015612),
            (0.0005205204, 0.004330136, 0.2015524),
            (-0.0004412518, 0.006495208, 0.2015438),
            (0.009671181, -0.001442945, 0.20157),
            (0.02084944, -0.005181804, 0.20157),
            (0.03289026, -0.006876484, 0.20157),
            (0.06526268, 0, 0.20157),
            (0.04345435, -0.005715966, 0.20157),
            (0.05393749, -0.002041858, 0.20157),
            (0, 0, 0.20157),
            (0.009671181, 0.001807056, 0.20157),
            (0.02084944, -0.001931805, 0.20157),
            (0.03289026, -0.003626484, 0.20157),
            (0.04345435, -0.002465971, 0.20157),
            (0.05393749, 0.001208143, 0.20157),
            (-0.000395142, 0.133154, 0.003284983),
            (0.06460488, 0.133154, 0.003284983),
            (-0.000395142, 0.133154, 3.498496e-05),
            (0.06460488, 0.133154, 3.498496e-05),
            (-0.000395142, 0.1299042, 3.498496e-05),
            (0.009671181, -0.001442945, 0.003046945),
            (0.06460488, 0.129904, 3.498496e-05),
            (-0.000395142, 0.1299042, 0.003284983),
            (0, 0, 0.003046945),
            (0.06526268, 0, 0.003046945),
            (0.06460488, 0.129904, 0.003284983),
            (0.009671181, 0.001807056, 0.1984634),
            (0.02084944, -0.001931805, 0.1984634),
            (0.03289026, -0.003626484, 0.1984634),
            (0.04345435, -0.002465971, 0.1984634),
            (0.05393749, 0.001208143, 0.1984634),
            (0.06165636, 0.0042588, 0.201349),
            (0.003217638, 0.0042588, 0.201349),
            (0.06135488, 0.129904, 0.1984634),
            (0.06135482, 0.005415067, 0.1984634),
            (0.002854846, 0.005415067, 0.1984634),
            (0.002854858, 0.1299042, 0.1984634),
            (0.06165636, 0.0042588, 0.1984634),
            (0.003217638, 0.0042588, 0.1984634),
            (0.002869524, 0.00198606, 0.2015655),
            (0.06156611, 0.001686607, 0.2015655),
            (0.002869524, 0.00198606, 0.1984634),
            (0.06156611, 0.001686607, 0.1984634),
            (0.05160481, 0.00417291, 0.1984634),
            (0.04185486, 0.001240239, 0.1984634),
            (0.03210485, 0.001240239, 0.1984634),
            (0.02235484, 0.001240239, 0.1984634),
            (0.01260485, 0.00417291, 0.1984634),
            (0.009671181, -0.001442945, 0),
            (0.02084944, -0.005181804, 0),
            (0.03289026, -0.006876484, 0),
            (0.06526268, 0, 0),
            (0.04345435, -0.005715966, 0),
            (0.05393749, -0.002041858, 0),
            (0, 0, 0),
            (0.009671181, 0.001807056, 0),
            (0.02084944, -0.001931805, 0),
            (0.03289026, -0.003626484, 0),
            (0.04345435, -0.002465971, 0),
            (0.05393749, 0.001208143, 0),
            (0.009671181, 0.001807056, 0.003106453),
            (0.02084944, -0.001931805, 0.003106453),
            (0.03289026, -0.003626484, 0.003106453),
            (0.04345435, -0.002465971, 0.003106453),
            (0.05393749, 0.001208143, 0.003106453),
            (0.06165636, 0.0042588, 0.0002210443),
            (0.003217638, 0.0042588, 0.0002210522),
            (0.06135488, 0.129904, 0.003106453),
            (0.06135482, 0.005415067, 0.003106453),
            (0.002854846, 0.005415067, 0.003106453),
            (0.002854858, 0.1299042, 0.003106453),
            (0.06165636, 0.0042588, 0.003106453),
            (0.003217638, 0.0042588, 0.003106453),
            (0.002869524, 0.00198606, 4.377958e-06),
            (0.06156611, 0.001686607, 4.377958e-06),
            (0.002869524, 0.00198606, 0.003106453),
            (0.06156611, 0.001686607, 0.003106453),
            (0.05160481, 0.00417291, 0.003106453),
            (0.04185486, 0.001240239, 0.003106453),
            (0.03210485, 0.001240239, 0.003106453),
            (0.02235484, 0.001240239, 0.003106453),
            (0.01260485, 0.00417291, 0.003106453),
          ],

        # "bounds" : ((min_x, max_x), (min_y, max_y), (min_z, max_z)) computed below

        "faces" :
          [
            [59, 60, 67, 66],
            [92, 91, 103, 102, 101, 100, 99, 90, 89],
            [42, 58, 6, 3],
            [51, 57, 58, 42],
            [112, 117, 118, 113],
            [4, 0, 12, 7],
            [114, 119, 120, 115],
            [74, 46, 45, 72],
            [104, 111, 112, 105],
            [111, 116, 117, 112],
            [105, 112, 113, 106],
            [3, 6, 8, 13],
            [104, 110, 11, 129, 111],
            [7, 12, 22, 19],
            [14, 23, 80, 107],
            [106, 113, 114, 108],
            [104, 76, 79, 110],
            [4, 7, 19, 17],
            [13, 8, 26, 29],
            [108, 114, 115, 109],
            [8, 6, 25, 26],
            [20, 11, 110, 79],
            [37, 60, 59, 5],
            [38, 31, 108, 109],
            [14, 15, 27, 23],
            [28, 16, 77, 81],
            [52, 56, 57, 51],
            [44, 0, 4, 53],
            [54, 47, 44, 53],
            [55, 48, 47, 54],
            [36, 61, 60, 37],
            [33, 37, 5, 76],
            [34, 64, 63, 35],
            [35, 63, 61, 36],
            [34, 1, 62, 64],
            [61, 63, 69, 68],
            [59, 65, 2, 5],
            [55, 62, 1, 48],
            [52, 2, 65, 56],
            [15, 16, 28, 27],
            [113, 118, 119, 114],
            [126, 123, 124, 133, 134, 135, 136, 137, 125],
            [30, 21, 51, 42],
            [41, 43, 9, 75],
            [109, 115, 130, 14, 107],
            [77, 74, 72, 81],
            [77, 50, 46, 74],
            [73, 40, 41, 75],
            [10, 9, 43, 122],
            [32, 33, 105, 106],
            [31, 32, 106, 108],
            [79, 76, 5, 2],
            [30, 78, 75, 9],
            [20, 79, 2, 52],
            [21, 20, 52, 51],
            [1, 80, 23, 48],
            [23, 27, 47, 48],
            [27, 28, 44, 47],
            [63, 64, 70, 69],
            [60, 61, 68, 67],
            [33, 76, 104, 105],
            [59, 66, 95, 56, 65],
            [64, 62, 55, 96, 70],
            [78, 71, 73, 75],
            [71, 39, 40, 73],
            [21, 30, 9, 10],
            [50, 77, 16, 49],
            [38, 109, 107, 80],
            [20, 21, 10, 11],
            [25, 6, 58, 24],
            [17, 18, 53, 4],
            [67, 68, 84, 83],
            [68, 69, 85, 84],
            [66, 67, 83, 82],
            [69, 70, 86, 85],
            [57, 88, 24, 58],
            [87, 54, 53, 18],
            [25, 24, 91, 92],
            [56, 95, 88, 57],
            [55, 54, 87, 96],
            [97, 95, 66, 82],
            [98, 86, 70, 96],
            [94, 88, 95, 97],
            [88, 94, 91, 24],
            [103, 91, 94, 97, 82],
            [85, 86, 99, 100],
            [84, 85, 100, 101],
            [83, 84, 101, 102],
            [82, 83, 102, 103],
            [22, 89, 17, 19],
            [26, 25, 92, 29],
            [121, 49, 16, 15],
            [41, 126, 125, 43],
            [49, 124, 123, 50],
            [11, 10, 122, 129],
            [14, 130, 121, 15],
            [131, 116, 111, 129],
            [132, 130, 115, 120],
            [49, 121, 127, 124],
            [128, 131, 129, 122],
            [122, 43, 125, 128],
            [137, 116, 131, 128, 125],
            [120, 133, 124, 127, 132],
            [119, 134, 133, 120],
            [118, 135, 134, 119],
            [117, 136, 135, 118],
            [116, 137, 136, 117],
            [45, 46, 50, 123],
            [40, 39, 126, 41],
            [92, 89, 123, 126],
            [3, 78, 30, 42],
            [3, 13, 71, 78],
            [13, 29, 39, 71],
            [92, 126, 39, 29],
            [22, 12, 72, 45],
            [12, 0, 81, 72],
            [127, 121, 130, 132],
            [93, 98, 96, 87],
            [87, 18, 90, 93],
            [98, 93, 90, 99, 86],
            [89, 22, 45, 123],
            [18, 17, 89, 90],
            [44, 28, 81, 0],
            [32, 36, 37, 33],
            [35, 36, 32, 31],
            [34, 35, 31, 38],
            [1, 34, 38, 80],
          ],

        "left_vertices" :
            {
                2,
                3,
                6,
                8,
                9,
                10,
                11,
                13,
                20,
                21,
                24,
                25,
                26,
                29,
                30,
                39,
                40,
                41,
                42,
                43,
                51,
                52,
                56,
                57,
                58,
                65,
                71,
                73,
                75,
                78,
                79,
                88,
                91,
                92,
                94,
                95,
                97,
                110,
                122,
                125,
                126,
                128,
                129,
                131,
            },

        "right_vertices" :
            {
                0,
                1,
                4,
                7,
                12,
                14,
                15,
                16,
                17,
                18,
                19,
                22,
                23,
                27,
                28,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                53,
                54,
                55,
                62,
                72,
                74,
                77,
                80,
                81,
                87,
                89,
                90,
                93,
                96,
                98,
                121,
                123,
                124,
                127,
                130,
                132,
            },

        # "front_vertices" : done below

        "back_vertices" :
            {
                0,
                3,
                4,
                6,
                7,
                8,
                12,
                13,
                17,
                19,
                22,
                25,
                26,
                29,
                39,
                40,
                41,
                45,
                46,
                50,
                71,
                72,
                73,
                74,
                75,
                77,
                78,
                81,
                89,
                92,
                123,
                126,
            },

        "top_vertices" :
            {
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                12,
                13,
                17,
                18,
                19,
                22,
                24,
                25,
                26,
                29,
                34,
                35,
                36,
                37,
                42,
                44,
                47,
                48,
                51,
                52,
                53,
                54,
                55,
                56,
                57,
                58,
                59,
                60,
                61,
                62,
                63,
                64,
                65,
                66,
                67,
                68,
                69,
                70,
                82,
                83,
                84,
                85,
                86,
                87,
                88,
                89,
                90,
                91,
                92,
                93,
                94,
                95,
                96,
                97,
                98,
                99,
                100,
                101,
                102,
                103,
            },

        # "bottom_vertices" : done below

        "paper_faces" :
            {
                1,
                41,
                84,
                85,
                86,
                87,
                88,
                101,
                102,
                103,
                104,
                105,
                106,
                109,
                119,
            },

    }
book_mesh["bounds"] = \
    (
        (min(v[0] for v in book_mesh["vertices"]), max(v[0] for v in book_mesh["vertices"])),
        (min(v[1] for v in book_mesh["vertices"]), max(v[1] for v in book_mesh["vertices"])),
        (min(v[2] for v in book_mesh["vertices"]), max(v[2] for v in book_mesh["vertices"])),
    )
print("book_mesh[\"bounds\"] = %s" % repr(book_mesh["bounds"])) # debug
book_mesh["front_vertices"] = \
    set(range(len(book_mesh["vertices"]))) - book_mesh["back_vertices"]
  # everything that isn’t a back vertex
book_mesh["bottom_vertices"] = \
    set(range(len(book_mesh["vertices"]))) - book_mesh["top_vertices"]
  # everything that isn’t a top vertex

def define_book_materials() :
    materials = {}
    for name, hsv_colour, gloss in \
        (
            ("cover", (0.96, 0.68, 0.5), 0.5),
            ("paper", (0, 0, 0.906), 0),
        ) \
    :
        rgb_colour = colorsys.hsv_to_rgb(*hsv_colour)
        material = bpy.data.materials.new(name)
        material.diffuse_color = rgb_colour
        material.use_nodes = True
        material_tree = material.node_tree
        for node in material_tree.nodes :
          # clear out default nodes
            material_tree.nodes.remove(node)
        #end for
        colour_shader = material_tree.nodes.new("ShaderNodeBsdfDiffuse")
        colour_shader.location = (0, 0)
        colour_shader.inputs[0].default_value = rgb_colour + (1,)
        material_output = material_tree.nodes.new("ShaderNodeOutputMaterial")
        if gloss != 0 :
            material_output.location = (400, 0)
            gloss_shader = material_tree.nodes.new("ShaderNodeBsdfGlossy")
            gloss_shader.location = (0, -150)
            mix_shader = material_tree.nodes.new("ShaderNodeMixShader")
            mix_shader.location = (200, 0)
            material_tree.links.new(colour_shader.outputs[0], mix_shader.inputs[1])
            material_tree.links.new(gloss_shader.outputs[0], mix_shader.inputs[2])
            mix_shader.inputs[0].default_value = gloss
            material_tree.links.new(mix_shader.outputs[0], material_output.inputs[0])
        else :
            material_output.location = (200, 0)
            material_tree.links.new(colour_shader.outputs[0], material_output.inputs[0])
        #end if
        for node in material_tree.nodes :
            node.select = False
        #end for
        materials[name] = material
    #end for
    return \
        materials
#end define_book_materials

#+
# Mainline
#-

dimensions_min = \
    (
            max
              (
                v[0] - book_mesh["bounds"][0][0]
                for i in range(len(book_mesh["vertices"]))
                for v in (book_mesh["vertices"][i],)
                if i in book_mesh["left_vertices"]
              )
        +
            max
              (
                book_mesh["bounds"][0][1] - v[0]
                for i in range(len(book_mesh["vertices"]))
                for v in (book_mesh["vertices"][i],)
                if i in book_mesh["right_vertices"]
              ),
        max
          (
            v[1] - book_mesh["bounds"][1][0]
            for i in range(len(book_mesh["vertices"]))
            for v in (book_mesh["vertices"][i],)
            if i in book_mesh["front_vertices"]
          ),
        0.001
    )
dimension_defaults = tuple(v[1] - v[0] for v in book_mesh["bounds"])

class Bookmaker(bpy.types.Operator) :
    bl_idname = "add_mesh.bookmaker"
    bl_label = "Bookmaker"
    bl_context = "objectmode"
    bl_options = {"REGISTER", "UNDO"}

    count = bpy.props.IntProperty \
      (
        name = "count",
        description = "How many books to generate",
        min = 1,
        default = 1,
      )
    width = bpy.props.FloatProperty \
      (
        name = "width",
        description = "base width of one book",
        min = dimensions_min[0],
        default = dimension_defaults[0],
      )
    width_var = bpy.props.FloatProperty \
      (
        name = "width_var",
        description = "variation in width (logarithmic)",
        min = 0,
        max = 10,
        default = 0,
      )
    depth = bpy.props.FloatProperty \
      (
        name = "depth",
        description = "base depth of one book",
        min = dimensions_min[1],
        default = dimension_defaults[1],
      )
    depth_var = bpy.props.FloatProperty \
      (
        name = "depth_var",
        description = "variation in depth (logarithmic)",
        min = 0,
        max = 10,
        default = 0,
      )
    height = bpy.props.FloatProperty \
      (
        name = "height",
        description = "base height of one book",
        min = dimensions_min[2],
        default = dimension_defaults[2],
      )
    height_var = bpy.props.FloatProperty \
      (
        name = "height_var",
        description = "variation in height (logarithmic)",
        min = 0,
        max = 10,
        default = 0,
      )
    rotate_var = bpy.props.FloatProperty \
      (
        name = "rotate_var",
        description = "variation in rotation angle",
        min = 0,
        max = 45 * deg,
        default = 0,
        subtype = "ANGLE"
      )
    ranseed = bpy.props.IntProperty \
      (
        name = "ranseed",
        description = "Pseudorandom seed",
        min = 0,
        default = 0,
      )

    def draw(self, context) :
        the_col = self.layout.column(align = True)
        the_col.prop(self, "count")
        the_col.prop(self, "width")
        the_col.prop(self, "width_var")
        the_col.prop(self, "depth")
        the_col.prop(self, "depth_var")
        the_col.prop(self, "height")
        the_col.prop(self, "height_var")
        the_col.prop(self, "rotate_var")
        the_col.prop(self, "ranseed")
    #end draw

    def action_common(self, context, redoing) :
        try :
            if context.scene.render.engine != "CYCLES" :
                raise Failure("Only Cycles renderer is supported")
            #end if
            pos = context.scene.cursor_location.copy()
            random.seed(self.ranseed)
            prev_rotation_displacement = 0
            bpy.ops.object.select_all(action = "DESELECT")
            materials = None
            for j in range(self.count) :
                if materials == None :
                    materials = define_book_materials()
                #end if
                width = max(self.width * 10 ** ((2 * random.random() - 1) * self.width_var / 10), dimensions_min[0])
                depth = max(self.depth * 10 ** ((2 * random.random() - 1) * self.depth_var / 10), dimensions_min[1])
                height = max(self.height * 10 ** ((2 * random.random() - 1) * self.height_var / 10), dimensions_min[2])
                rotate = (2 * random.random() - 1) * self.rotate_var
                rotation_displacement = height * math.sin(rotate)
                x_disp_delta = rotation_displacement - prev_rotation_displacement
                z_disp_delta = max(width * math.sin(rotate), 0)
                vertices = []
                bounds = book_mesh["bounds"]
                for i in range(len(book_mesh["vertices"])) :
                    coords = list(book_mesh["vertices"][i])
                    coords[0] -= bounds[0][0]
                    coords[1] -= bounds[1][0]
                    coords[2] -= bounds[2][0]
                    if i in book_mesh["right_vertices"] :
                        coords[0] += width - (bounds[0][1] - bounds[0][0])
                    elif i not in book_mesh["left_vertices"] :
                        coords[0] *= width / (bounds[0][1] - bounds[0][0])
                    #end if
                    if i in book_mesh["back_vertices"] :
                        coords[1] += depth - (bounds[1][1] - bounds[1][0])
                    #end if
                    if i in book_mesh["top_vertices"] :
                        coords[2] += height - (bounds[2][1] - bounds[2][0])
                    #end if
                    vertices.append(coords)
                #end for
                new_mesh_name = new_obj_name = "Book.%03d" % (j + 1)
                new_mesh = bpy.data.meshes.new(new_mesh_name)
                new_mesh.materials.append(materials["cover"])
                new_mesh.materials.append(materials["paper"])
                new_mesh.from_pydata(vertices, [], book_mesh["faces"])
                for i in range(len(book_mesh["faces"])) :
                    p = new_mesh.polygons[i]
                    if i in book_mesh["paper_faces"] :
                        p.material_index = 1
                    else :
                        p.material_index = 0
                    #end if
                #end for
                new_obj = bpy.data.objects.new(new_mesh_name, new_mesh)
                new_obj.matrix_basis = \
                    (
                        Matrix.Translation
                          (
                            Vector(((0, - x_disp_delta)[x_disp_delta < 0], 0, z_disp_delta))
                          )
                    *
                        Matrix.Translation(pos)
                    *
                        Matrix.Rotation(rotate, 4, Vector((0, 1, 0)))
                    )
                context.scene.objects.link(new_obj)
                bpy.data.objects[new_obj_name].select = True
                context.scene.objects.active = new_obj
                for this_vertex in new_mesh.vertices :
                    this_vertex.select = True # usual Blender default for newly-created object
                #end for
                pos += Vector((width + (0, - x_disp_delta)[x_disp_delta < 0], 0, 0))
                prev_rotation_displacement = rotation_displacement
            #end for
            # all done
            status = {"FINISHED"}
        except Failure as why :
            sys.stderr.write("Failure: %s\n" % why.msg) # debug
            self.report({"ERROR"}, why.msg)
            status = {"CANCELLED"}
        #end try
        return \
            status
    #end action_common

    def execute(self, context) :
        return \
            self.action_common(context, True)
    #end execute

    def invoke(self, context, event) :
        return \
            self.action_common(context, False)
    #end invoke

#end Bookmaker

def add_invoke_item(self, context) :
    self.layout.operator(Bookmaker.bl_idname, text = "Books")
#end add_invoke_item

def register() :
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(add_invoke_item)
#end register

def unregister() :
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(add_invoke_item)
#end unregister

if __name__ == "__main__" :
    register()
#end if
