import bpy
from compas.plugins import plugin


__all__ = [
    'boolean_union_mesh_mesh',
    'boolean_difference_mesh_mesh',
    'boolean_intersection_mesh_mesh',
]


@plugin(category='booleans', requires=['bpy'])
def boolean_union_mesh_mesh(A, B, remesh=False):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.
    """
    return _boolean_operation(A, B, 'UNION')


@plugin(category='booleans', requires=['bpy'])
def boolean_difference_mesh_mesh(A, B, remesh=False):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.
    """
    return _boolean_operation(A, B, 'DIFFERENCE')


@plugin(category='booleans', requires=['bpy'])
def boolean_intersection_mesh_mesh(A, B, remesh=False):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.
    """
    return _boolean_operation(A, B, 'INTERSECT')


def _boolean_operation(A, B, method):
    from compas_blender.utilities import draw_mesh
    from compas_blender.utilities import delete_object
    from compas_blender.utilities import delete_unused_data
    A = draw_mesh(* A)
    B = draw_mesh(* B)
    boolean = A.modifiers.new(type="BOOLEAN", name="A {} B".format(method))
    boolean.object = B
    boolean.operation = method
    bpy.ops.object.modifier_apply({"object": A}, modifier=boolean.name)
    graph = bpy.context.evaluated_depsgraph_get()
    C = A.evaluated_get(graph)
    D = bpy.data.meshes.new_from_object(C)
    vertices = [list(vertex.co)[:] for vertex in D.vertices]
    faces = [list(face.vertices)[:] for face in D.polygons]
    delete_object(A)
    delete_object(B)
    delete_unused_data()
    return vertices, faces
