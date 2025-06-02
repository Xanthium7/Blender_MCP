import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure:
1. The server is running before running this script.
2. The server is configured to use SSE transport.
3. The server is listening on port 8050.

To run the server:
uv run server.py
"""


async def main():
    # Connect to the server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            blender_code = """
import bpy
import bmesh
from mathutils import Vector
import math

# Clear existing mesh
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a new mesh and object
mesh = bpy.data.meshes.new("Hexagonoid")
obj = bpy.data.objects.new("Hexagonoid", mesh)

# Link object to scene
bpy.context.collection.objects.link(obj)

# Create bmesh instance
bm = bmesh.new()

# Create hexagonal prism (3D hexagonoid)
# Create bottom hexagon vertices
radius = 2.0
height = 2.0
bottom_verts = []
top_verts = []

# Create hexagon vertices (6 sides)
for i in range(6):
    angle = i * math.pi / 3  # 60 degrees in radians
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    
    # Bottom vertices
    bottom_vert = bm.verts.new((x, y, -height/2))
    bottom_verts.append(bottom_vert)
    
    # Top vertices
    top_vert = bm.verts.new((x, y, height/2))
    top_verts.append(top_vert)

# Create bottom face
bm.faces.new(bottom_verts)

# Create top face (reverse order for correct normal)
bm.faces.new(reversed(top_verts))

# Create side faces
for i in range(6):
    next_i = (i + 1) % 6
    # Create quad face for each side
    face_verts = [
        bottom_verts[i],
        bottom_verts[next_i],
        top_verts[next_i],
        top_verts[i]
    ]
    bm.faces.new(face_verts)

# Update mesh
bm.to_mesh(mesh)
bm.free()

# Set object as active and select it
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Add smooth shading
bpy.ops.object.shade_smooth()

print("3D Hexagonoid created successfully!")
print(f"Object name: {obj.name}")
print(f"Vertices: {len(mesh.vertices)}")
print(f"Faces: {len(mesh.polygons)}")
            """
            result = await session.call_tool("execute_blender_code", arguments={"code": blender_code})
            print(f"Blender execution result:\n{result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
