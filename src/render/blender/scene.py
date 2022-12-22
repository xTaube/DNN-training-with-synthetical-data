import bpy
import os
import shutil
import numpy as np
from typing import Dict, List

from src.render.blender.exceptions import (
    ObjectAlreadyAddedToScene,
    ObjectNotInScene,
    LayerNotSupported,
)
from src.render.blender.consts import LAYER_MAP


class Scene:
    def __init__(
        self,
        scene,
        render_engine: str,
        file_format: str,
        temp_render_dir: str = os.path.join(os.getcwd(), "temp"),
    ):
        self.background = None
        self.camera = None
        self.objects = []
        self._scene = scene
        self._configure_render(
            render_engine=render_engine,
            temp_render_dir=temp_render_dir,
            file_format=file_format,
        )

    def _configure_render(
        self, render_engine: str, temp_render_dir: str, file_format: str
    ) -> None:
        self._scene.render.engine = render_engine
        self._scene.render.filepath = temp_render_dir
        self._scene.render.image_settings.file_format = file_format
        self._scene.cycles.samples = 1

        self._scene.view_layers["ViewLayer"].use_pass_object_index = True
        self._scene.view_layers["ViewLayer"].use_pass_z = True
        self._scene.use_nodes = True

        tree = self._scene.node_tree
        links = tree.links

        for node in tree.nodes:
            tree.nodes.remove(node)

        image_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
        image_output_node.label = "RGB_output"
        image_output_node.base_path = os.path.join(temp_render_dir, "RGB")
        image_output_node.set_location = 400, 0

        index_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
        index_output_node.label = "segmentation_output"
        index_output_node.base_path = os.path.join(temp_render_dir, "segmentation")
        index_output_node.set_location = 400, -200

        render_layers_node = tree.nodes.new(type="CompositorNodeRLayers")
        render_layers_node.set_location = 0, 0

        links.new(
            render_layers_node.outputs["Image"], image_output_node.inputs["Image"]
        )
        links.new(
            render_layers_node.outputs["IndexOB"], index_output_node.inputs["Image"]
        )

    def set_background(self, background_path) -> None:
        node_tree = self._scene.world.node_tree
        tree_nodes = node_tree.nodes
        tree_nodes.clear()
        node_background = tree_nodes.new(type="ShaderNodeBackground")
        node_environment = tree_nodes.new("ShaderNodeTexEnvironment")
        node_environment.image = bpy.data.images.load(background_path)
        node_environment.set_location = -300, 0
        node_output = tree_nodes.new(type="ShaderNodeOutputWorld")
        node_output.set_location = 200, 0
        links = node_tree.links
        links.new(node_environment.outputs["Color"], node_background.inputs["Color"])
        links.new(node_background.outputs["Background"], node_output.inputs["Surface"])

    def set_camera(self, camera):
        self.camera = camera

    def add_object(self, obj) -> None:
        if obj in self.objects:
            raise ObjectAlreadyAddedToScene
        obj.reference.pass_index = len(self.objects) + 1
        self.objects.append(obj)

    def remove_object(self, obj) -> None:
        if obj not in self.objects:
            raise ObjectNotInScene
        self.objects.remove(obj)

    def render_image(self, layers: List[str]) -> Dict[str, np.ndarray]:
        if any([layer not in LAYER_MAP.keys() for layer in layers]):
            raise LayerNotSupported(f"Supported layers: {LAYER_MAP.keys()}")

        bpy.ops.render.render(layer="CompositorNodeRLayers")
        frame = {
            layer: LAYER_MAP[layer](
                os.path.join(self._scene.render.filepath, layer, "Image0001.exr")
            )
            for layer in layers
        }
        shutil.rmtree(self._scene.render.filepath)
        return frame
