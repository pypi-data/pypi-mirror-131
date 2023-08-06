from typing import Optional
from typing import Any
from typing import List
from typing import Union

import bpy

import compas_blender
from compas_blender.utilities import RGBColor
from compas.geometry import Torus
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class TorusArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        A COMPAS torus.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 torus: Torus,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):

        super().__init__(shape=torus, collection=collection or torus.name, **kwargs)

    def draw(self, color: Optional[RGBColor] = None, u: Optional[int] = None, v: Optional[int] = None) -> List[bpy.types.Object]:
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the torus.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~TorusArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~TorusArtist.v``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        v = v or self.v
        color = color or self.color
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=color, collection=self.collection)
        return [obj]
